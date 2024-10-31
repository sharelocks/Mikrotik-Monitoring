# mikrotik_monitor.py

from librouteros import connect
import csv
import json
import time
from datetime import datetime
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
CSV_FILE = 'data/csv/traffic_data.csv'
FINAL_TOTALS_FILE = 'data/json/traffic_summary.json'  # Updated file name for clarity


# Connect to the Mikrotik router
def connect_to_router():
    return connect(username=API_USERNAME, password=API_PASSWORD, host=API_HOST, port=API_PORT)


# Fetch traffic data
def fetch_traffic_data(api):
    interfaces = api(cmd='/interface/print')
    data = []
    for interface in interfaces:
        data.append({
            'interface': interface.get('name'),
            'type': interface.get('type'),
            'bytes_tx': int(interface.get('tx-byte', 0)),
            'bytes_rx': int(interface.get('rx-byte', 0))
        })
    return data


# Save summary data to JSON for visualization
def save_summary_to_json(timestamp, interval_tx, interval_rx, cumulative_tx, cumulative_rx):
    data = {
        "timestamp": timestamp,
        "interval_tx_gb": interval_tx / (1024 ** 3),
        "interval_rx_gb": interval_rx / (1024 ** 3),
        "cumulative_tx_gb": cumulative_tx / (1024 ** 3),
        "cumulative_rx_gb": cumulative_rx / (1024 ** 3)
    }
    with open(FINAL_TOTALS_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    api = connect_to_router()

    cumulative_tx = 0
    cumulative_rx = 0
    previous_tx = None
    previous_rx = None

    try:
        while True:
            data = fetch_traffic_data(api)
            total_tx = sum(interface['bytes_tx'] for interface in data)
            total_rx = sum(interface['bytes_rx'] for interface in data)

            if previous_tx is None or previous_rx is None:
                previous_tx = total_tx
                previous_rx = total_rx

            interval_tx = total_tx - previous_tx
            interval_rx = total_rx - previous_rx

            # Debug print statements for checking values
            print(f"Interval TX: {interval_tx} bytes, Interval RX: {interval_rx} bytes")

            # Update previous values for the next iteration
            previous_tx = total_tx
            previous_rx = total_rx

            # Update cumulative totals
            cumulative_tx += interval_tx
            cumulative_rx += interval_rx

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            print(f"Data collected at {timestamp}")
            print(f"Data transmitted in the last 5 min: {interval_tx / (1024 ** 3):.2f} GB")
            print(f"Data received in the last 5 min: {interval_rx / (1024 ** 3):.2f} GB")
            print(f"Cumulative data transmitted: {cumulative_tx / (1024 ** 3):.2f} GB")
            print(f"Cumulative data received: {cumulative_rx / (1024 ** 3):.2f} GB\n")

            # Save summary data to JSON for visualization
            save_summary_to_json(timestamp, interval_tx, interval_rx, cumulative_tx, cumulative_rx)

            time.sleep(3600)  # 1 hour interval

    except KeyboardInterrupt:
        print("Program stopped by user.")


if __name__ == '__main__':
    main()
