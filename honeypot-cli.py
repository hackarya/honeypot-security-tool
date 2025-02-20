#!/usr/bin/env python3

import argparse
import os
import sys
import subprocess

HONEYPOT_SERVICE = "honeypot.service"
LOG_FILE = "/honeypot/logs/honeypot.log"

def start_honeypot():
    print("🚀 Starting Honeypot...")
    os.system(f"sudo systemctl start {HONEYPOT_SERVICE}")
    print("✅ Honeypot started successfully!")

def stop_honeypot():
    print("⏹️ Stopping Honeypot...")
    os.system(f"sudo systemctl stop {HONEYPOT_SERVICE}")
    print("✅ Honeypot stopped successfully!")

def restart_honeypot():
    print("🔄 Restarting Honeypot...")
    os.system(f"sudo systemctl restart {HONEYPOT_SERVICE}")
    print("✅ Honeypot restarted successfully!")

def status_honeypot():
    print("📊 Checking Honeypot status...")
    os.system(f"sudo systemctl status {HONEYPOT_SERVICE}")

def show_logs():
    print("📜 Displaying Honeypot logs...")
    os.system(f"sudo tail -f {LOG_FILE}")

def list_attackers():
    print("🔍 Listing blocked IPs...")
    os.system("sudo cat /var/log/fail2ban.log | grep 'Ban'")

def update_honeypot():
    print("📦 Updating Honeypot...")
    os.system("git pull origin main && sudo ./install.sh")
    print("✅ Update complete!")

def main():
    parser = argparse.ArgumentParser(description="Honeypot Security Tool CLI")
    
    parser.add_argument("command", choices=[
        "start", "stop", "restart", "status", "logs", "attackers", "update"
    ], help="Command to execute")

    args = parser.parse_args()

    if args.command == "start":
        start_honeypot()
    elif args.command == "stop":
        stop_honeypot()
    elif args.command == "restart":
        restart_honeypot()
    elif args.command == "status":
        status_honeypot()
    elif args.command == "logs":
        show_logs()
    elif args.command == "attackers":
        list_attackers()
    elif args.command == "update":
        update_honeypot()

if __name__ == "__main__":
    main()
