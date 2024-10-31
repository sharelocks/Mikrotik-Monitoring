
# MikroTik Network Traffic Monitoring and Visualization

This project connects to a MikroTik router using the MikroTik API to track network traffic. It gathers IP-based data consumption information and visualizes it, providing both current and cumulative data views. Data is saved in CSV and JSON formats for persistent logging and uses Python scripts for live, animated visualizations.

## Features
- **Data Collection**: Retrieves data consumption metrics (original and reply bytes) for IP connections and interfaces on the MikroTik router.
- **Data Logging**: Logs data in `CSV` and `JSON` formats, organizing it for future use.
- **Visualizations**:
  - **Top IP Addresses** by Data Consumption.
  - **Transmitted and Received Data** (Interval and Cumulative).
- **Live Updates**: Uses `matplotlib` to provide live-updating visualizations.

## Project Structure
```plaintext
project-root/
│
├── data/
│   ├── csv/
│   │   └── ip_traffic_data.csv     # Stores IP data in CSV format
│   ├── json/
│   │   └── traffic_summary.json    # Stores cumulative and interval data in JSON format
│
├── .env                            # Contains sensitive MikroTik API details (see Setup)
├── IP Tracking.py                  # Fetches and logs IP-based traffic data
├── mikrotik_monitor.py             # Fetches and logs overall traffic per interface
├── Visualize IP Data.py            # Visualizes top IP addresses by data consumption
├── visualize_traffic_data.py       # Visualizes cumulative and interval-based traffic stats
└── requirements.txt                # Python package dependencies
```

## Setup and Installation

### Prerequisites
- **Python 3.x**
- **MikroTik Router** with API enabled and accessible credentials.

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Python Dependencies
Install required packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Configure the `.env` File
Create a `.env` file in the project root with your MikroTik API credentials:
```plaintext
API_HOST=192.168.88.1
API_PORT=8838
API_USERNAME=admin
API_PASSWORD=Amsf@226
```

> **Note**: Ensure `.env` is included in `.gitignore` to keep credentials secure.

### 4. Running the Scripts

#### 4.1 Collecting IP Traffic Data
`IP Tracking.py` connects to the router, collects IP traffic data, and saves it in both CSV and JSON formats:
```bash
python IP\ Tracking.py
```

#### 4.2 Collecting Interface Traffic Data
`mikrotik_monitor.py` collects traffic data for router interfaces, calculates transmission and reception metrics, and saves results in JSON format:
```bash
python mikrotik_monitor.py
```

#### 4.3 Visualizing IP Traffic Data
To view the top IP addresses by data consumption, use:
```bash
python Visualize\ IP\ Data.py
```

#### 4.4 Visualizing Cumulative Traffic Data
For interval and cumulative transmission and reception data:
```bash
python visualize_traffic_data.py
```

### 5. Notes on Customization
- The logging intervals can be modified in the `time.sleep()` statements of each script (currently set to 1 hour).
- The `CSV` and `JSON` file paths can be adjusted as needed in the relevant scripts.

## Dependencies
- `librouteros`: For connecting to the MikroTik API.
- `python-dotenv`: For managing sensitive environment variables.
- `matplotlib`: For creating live-updating visualizations.

Install these via `pip` using `requirements.txt`.

## Troubleshooting
- Ensure the MikroTik API service is enabled and accessible at the specified host and port.
- Verify `.env` credentials are correct; incorrect credentials will prevent API connections.

## License
This project is open-source and available under the [MIT License](LICENSE).
