# generate_chart.py - Generates attack trends graph

import matplotlib.pyplot as plt
import datetime
import os

# Path to the honeypot log file
LOG_FILE = "../honeypot/logs/honeypot.log"
OUTPUT_IMAGE = "static/attack_trends.png"

def parse_logs():
    """Reads the honeypot logs and extracts timestamps of attacks."""
    if not os.path.exists(LOG_FILE):
        return []

    timestamps = []
    with open(LOG_FILE, "r") as f:
        for line in f.readlines():
            try:
                date_str = line.split(" - ")[0]
                timestamp = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                timestamps.append(timestamp)
            except Exception:
                continue  # Skip malformed lines
    return timestamps

def generate_attack_chart():
    """Generates and saves a graph of attack trends."""
    timestamps = parse_logs()
    if not timestamps:
        return

    # Count attacks per hour
    hourly_counts = {}
    for ts in timestamps:
        hour = ts.replace(minute=0, second=0)
        hourly_counts[hour] = hourly_counts.get(hour, 0) + 1

    # Sort data for plotting
    sorted_hours = sorted(hourly_counts.keys())
    counts = [hourly_counts[hour] for hour in sorted_hours]

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(sorted_hours, counts, marker="o", linestyle="-", color="red")
    plt.xlabel("Time")
    plt.ylabel("Number of Attacks")
    plt.title("Honeypot Attack Trends")
    plt.grid(True)
    plt.xticks(rotation=45)

    # Save the image
    plt.savefig(os.path.join("web_dashboard", OUTPUT_IMAGE), bbox_inches="tight")
    plt.close()

# Run the function
generate_attack_chart()