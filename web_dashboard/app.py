# app.py - Web Dashboard for Honeypot Monitoring

from flask import Flask, render_template, jsonify
import os
import datetime
from generate_chart import generate_attack_chart

# Configuration
LOG_FILE = "../honeypot/logs/honeypot.log"

app = Flask(__name__)

def read_logs():
    """Reads the latest honeypot logs."""
    if not os.path.exists(LOG_FILE):
        return ["No logs found."]
    
    with open(LOG_FILE, "r") as f:
        logs = f.readlines()[-20:]  # Show last 20 logs
    return logs

def get_attack_stats():
    """Calculates attack statistics (total attacks, unique IPs)."""
    if not os.path.exists(LOG_FILE):
        return {"total_attacks": 0, "unique_ips": 0}

    unique_ips = set()
    total_attacks = 0

    with open(LOG_FILE, "r") as f:
        for line in f.readlines():
            total_attacks += 1
            ip_match = line.split()[-1]  # Assuming IP is last word in the log
            unique_ips.add(ip_match)

    return {"total_attacks": total_attacks, "unique_ips": len(unique_ips)}

@app.route("/")
def dashboard():
    """Render the dashboard with the attack trends graph."""
    generate_attack_chart()  # Generate latest attack trends graph
    logs = read_logs()
    stats = get_attack_stats()
    return render_template("index.html", logs=logs, stats=stats)

@app.route("/api/logs")
def api_logs():
    """API endpoint to fetch logs as JSON."""
    logs = read_logs()
    return jsonify({"logs": logs})

@app.route("/api/stats")
def api_stats():
    """API endpoint for attack statistics."""
    stats = get_attack_stats()
    return jsonify(stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)