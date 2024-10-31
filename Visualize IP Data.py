# visualize_ip_data.py with automatic updates every 30 seconds and conditional annotation positioning

import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.animation import FuncAnimation

# Path to the CSV file
CSV_FILE = 'data/csv/ip_traffic_data.csv'


def load_ip_data():
    ip_data = defaultdict(int)
    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                # Update to match your CSV structure
                src_address = row[0]  # Source address with port
                total_bytes = int(row[5])  # Total bytes

                # Aggregate data usage by source IP address
                ip = src_address.split(':')[0]  # Remove port
                ip_data[ip] += total_bytes
            except IndexError:
                print("Skipping malformed row:", row)
            except ValueError:
                print("Skipping row with invalid byte data:", row)
    return ip_data


def plot_ip_data(frame):
    plt.clf()  # Clear the current figure to redraw

    ip_data = load_ip_data()

    # Sort IP data by usage and get the top 10 IPs
    sorted_ip_data = sorted(ip_data.items(), key=lambda x: x[1], reverse=True)[:10]
    ips = [ip for ip, _ in sorted_ip_data]
    usage = [bytes_used / (1024 ** 3) for _, bytes_used in sorted_ip_data]  # Convert to GB

    # Plotting
    bars = plt.barh(ips, usage, color='skyblue')
    plt.xlabel('Data Used (GB)')
    plt.title('Top 10 IP Addresses by Data Consumption')
    plt.gca().invert_yaxis()

    # Add data labels conditionally inside or outside each bar
    for bar, gb in zip(bars, usage):
        if bar.get_width() < 20:  # Adjust threshold as needed
            plt.text(
                bar.get_width() + 0.1,  # Position outside the bar
                bar.get_y() + bar.get_height() / 2,
                f"{gb:.2f} GB",
                va='center',
                ha='left',
                color='black',
                fontweight='bold'
            )
        else:
            plt.text(
                bar.get_width() - 0.2,  # Position slightly inside the bar
                bar.get_y() + bar.get_height() / 2,
                f"{gb:.2f} GB",
                va='center',
                ha='right',
                color='black',
                fontweight='bold'
            )

    plt.tight_layout()


def main():
    plt.figure(figsize=(10, 6))
    ani = FuncAnimation(plt.gcf(), plot_ip_data, interval=3600000)  # Refresh 1 hour
    plt.show()


if __name__ == '__main__':
    main()
