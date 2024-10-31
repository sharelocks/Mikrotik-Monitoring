# visualize_traffic_data.py

import json
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation

# Path to the JSON file
JSON_FILE = 'data/json/traffic_summary.json'


def load_traffic_data():
    try:
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
            timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
            interval_tx = data['interval_tx_gb']
            interval_rx = data['interval_rx_gb']
            cumulative_tx = data['cumulative_tx_gb']
            cumulative_rx = data['cumulative_rx_gb']
        return timestamp, interval_tx, interval_rx, cumulative_tx, cumulative_rx
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return None, None, None, None, None


def plot_traffic_data(frame):
    # Load the latest data from JSON
    timestamp, interval_tx, interval_rx, cumulative_tx, cumulative_rx = load_traffic_data()

    if timestamp is not None:
        plt.clf()  # Clear the previous plot

        # Interval Plot
        plt.subplot(2, 1, 1)
        bars = plt.bar(['Transmitted', 'Received'], [interval_tx, interval_rx], color=['blue', 'red'])
        plt.title(f"Data Transmitted and Received in Last Interval ({timestamp})")
        plt.ylabel('Data (GB)')

        # Add labels inside the bars
        for bar, gb in zip(bars, [interval_tx, interval_rx]):
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # Center text horizontally
                bar.get_height() / 2,  # Position text in the middle of the bar
                f"{gb:.2f} GB",  # Format label as GB
                ha='center', va='center', color='white', fontweight='bold'
            )

        # Cumulative Plot
        plt.subplot(2, 1, 2)
        cumulative_bars = plt.bar(
            ['Cumulative Transmitted', 'Cumulative Received'],
            [cumulative_tx, cumulative_rx],
            color=['skyblue', 'salmon']
        )
        plt.title("Cumulative Data Transmitted and Received")
        plt.ylabel('Total Data (GB)')

        # Add labels inside the cumulative bars
        for bar, gb in zip(cumulative_bars, [cumulative_tx, cumulative_rx]):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() / 2,
                f"{gb:.2f} GB",
                ha='center', va='center', color='black', fontweight='bold'
            )

        plt.tight_layout()  # Adjust layout to fit titles and labels


def main():
    # Set up the figure and use FuncAnimation for live updating
    plt.figure(figsize=(8, 8)).canvas.manager.set_window_title('Traffic Data Visualization')
    ani = FuncAnimation(plt.gcf(), plot_traffic_data, interval=3600000)  # Update every 1 hour
    plt.show()


if __name__ == "__main__":
    main()
