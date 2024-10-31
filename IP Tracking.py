from librouteros import connect
import csv
import json
import time
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()  # This line loads variables from .env into os.environ

# Mikrotik API connection details from .env
API_HOST = os.getenv('API_HOST')
API_PORT = int(os.getenv('API_PORT'))
API_USERNAME = os.getenv('API_USERNAME')
API_PASSWORD = os.getenv('API_PASSWORD')

# Output file names
IP_LOG_CSV_FILE = 'data/csv/ip_traffic_data.csv'
IP_LOG_JSON_FILE = 'data/json/ip_traffic_data.json'


# Connect to the Mikrotik router
def connect_to_router():
    return connect(username=API_USERNAME, password=API_PASSWORD, host=API_HOST, port=API_PORT)


# Fetch IP-based traffic data with original and reply bytes
def fetch_ip_traffic_data(api):
    connections = api(cmd='/ip/firewall/connection/print')
    data = []

    for conn in connections:
        orig_bytes = int(conn.get('orig-bytes', 0))
        repl_bytes = int(conn.get('repl-bytes', 0))

        # Total bytes for this connection (sum of original and reply bytes)
        total_bytes = orig_bytes + repl_bytes

        data.append({
            'src_address': conn.get('src-address'),
            'dst_address': conn.get('dst-address'),
            'protocol': conn.get('protocol'),
            'orig_bytes': orig_bytes,
            'repl_bytes': repl_bytes,
            'total_bytes': total_bytes,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return data


# Save IP traffic data to CSV
def save_ip_traffic_to_csv(data):
    # Check if the CSV file needs headers
    try:
        with open(IP_LOG_CSV_FILE, 'x') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
    except FileExistsError:
        pass  # File exists, continue to append

    # Append data to CSV file
    with open(IP_LOG_CSV_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        for row in data:
            writer.writerow(row)


# Save IP traffic data to JSON
def save_ip_traffic_to_json(data):
    # Read existing data if the file exists
    try:
        with open(IP_LOG_JSON_FILE, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # Append new data and save
    existing_data.extend(data)
    with open(IP_LOG_JSON_FILE, 'w') as f:
        json.dump(existing_data, f, indent=4)


# Print data summary by IP
def print_ip_data_summary(data):
    # Aggregate bytes by IP address
    ip_data = defaultdict(int)
    for entry in data:
        ip_data[entry['src_address']] += entry['total_bytes']

    # Sort and print top IPs by data consumption
    sorted_ip_data = sorted(ip_data.items(), key=lambda x: x[1], reverse=True)
    print("\nData Usage by IP (Top Consumers):")
    for ip, bytes_used in sorted_ip_data[:10]:  # Print top 10 IPs by usage
        print(f"IP: {ip}, Data Used: {bytes_used / (1024 ** 3):.2f} GB")


def main():
    # Connect to Mikrotik router
    api = connect_to_router()

    while True:
        # Fetch IP-based traffic data
        ip_data = fetch_ip_traffic_data(api)

        # Save IP data to CSV and JSON
        save_ip_traffic_to_csv(ip_data)
        save_ip_traffic_to_json(ip_data)

        # Print IP data summary for the current interval
        print_ip_data_summary(ip_data)

        print(f"\nIP traffic data collected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Wait for 1 hour before the next fetch
        time.sleep(3600)  # 1 hour


if __name__ == '__main__':
    main()
