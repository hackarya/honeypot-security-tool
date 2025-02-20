#!/usr/bin/env python3
ASCII_ART = r"""
--  ░▒▓█▓▒░░▒▓█▓▒░░░▒▓██████▓▒░░░▒▓███████▓▒░░░▒▓████████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓███████▓▒░ ░░▒▓██████▓▒░░▒▓████████▓▒░ 
--  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░░▒▓█▓▒░     
--  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░░▒▓█▓▒░     
--  ░▒▓████████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░   ░▒▓██████▓▒░░░▒▓███████▓▒░░░▒▓█▓▒░░▒▓█▓▒░ ░░▒▓█▓▒░     
--  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░          ░▒▓█▓▒░   ░░▒▓█▓▒░      ░░▒▓█▓▒░░▒▓█▓▒░ ░░▒▓█▓▒░     
--  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░          ░▒▓█▓▒░   ░░▒▓█▓▒░      ░░▒▓█▓▒░░▒▓█▓▒░ ░░▒▓█▓▒░     
--  ░▒▓█▓▒░░▒▓█▓▒░░░▒▓██████▓▒░░░▒▓█▓▒░░▒▓█▓▒░░▒▓████████▓▒░   ░▒▓█▓▒░   ░░▒▓█▓▒░       ░░▒▓██████▓▒░  ░░▒▓█▓▒░     
--  Author @hackarya                                                                                                         
--                                                                                                                                                                                                                                                                             
"""
print(ASCII_ART)
print("🔥 Welcome to the Honeypot CLI - Secure & Monitor Your System 🔥\n")
import os
import sys
import subprocess

HONEYPOT_SERVICE = "honeypot.service"
LOG_FILE = "/honeypot/logs/honeypot.log"
WHITELIST_FILE = "/honeypot/config/whitelist.txt"

def start_honeypot():
    os.system(f"sudo systemctl start {HONEYPOT_SERVICE}")
    print("✅ Honeypot started.")

def stop_honeypot():
    os.system(f"sudo systemctl stop {HONEYPOT_SERVICE}")
    print("❌ Honeypot stopped.")

def restart_honeypot():
    os.system(f"sudo systemctl restart {HONEYPOT_SERVICE}")
    print("🔄 Honeypot restarted.")

def status_honeypot():
    os.system(f"sudo systemctl status {HONEYPOT_SERVICE}")

def live_logs():
    os.system(f"tail -f {LOG_FILE}")

def block_ip(ip):
    os.system(f"sudo ufw deny from {ip}")
    print(f"🚫 Blocked IP: {ip}")

def unblock_ip(ip):
    os.system(f"sudo ufw delete deny from {ip}")
    print(f"✅ Unblocked IP: {ip}")

def whitelist_ip(ip):
    with open(WHITELIST_FILE, "a") as file:
        file.write(ip + "\n")
    print(f"✅ Whitelisted IP: {ip}")

def remove_whitelist_ip(ip):
    with open(WHITELIST_FILE, "r") as file:
        lines = file.readlines()
    with open(WHITELIST_FILE, "w") as file:
        for line in lines:
            if line.strip() != ip:
                file.write(line)
    print(f"🚫 Removed IP from whitelist: {ip}")

def show_whitelist():
    with open(WHITELIST_FILE, "r") as file:
        whitelist = file.readlines()
    print("📜 Whitelisted IPs:")
    for ip in whitelist:
        print(f" - {ip.strip()}")

def change_port(port):
    with open("honeypot/src/config.py", "r") as file:
        lines = file.readlines()
    with open("honeypot/src/config.py", "w") as file:
        for line in lines:
            if "PORT =" in line:
                file.write(f"PORT = {port}\n")
            else:
                file.write(line)
    print(f"🔄 Changed honeypot port to {port}. Restart required.")

def cleanup_logs():
    os.system("sudo rm -rf /honeypot/logs/*.log")
    print("🧹 Logs cleaned up!")

def show_help():
    print("""
Honeypot CLI - Command List:
  start                  Start the honeypot service
  stop                   Stop the honeypot service
  restart                Restart the honeypot service
  status                 Show honeypot service status
  logs --live            View real-time logs
  block <IP>             Block an IP manually
  unblock <IP>           Unblock an IP
  whitelist add <IP>     Whitelist an IP
  whitelist remove <IP>  Remove an IP from whitelist
  whitelist show         Show whitelisted IPs
  port set <PORT>        Change honeypot port
  logs clean             Cleanup old logs
""")

if len(sys.argv) < 2:
    show_help()
    sys.exit(1)

command = sys.argv[1]

if command == "start":
    start_honeypot()
elif command == "stop":
    stop_honeypot()
elif command == "restart":
    restart_honeypot()
elif command == "status":
    status_honeypot()
elif command == "logs" and len(sys.argv) > 2 and sys.argv[2] == "--live":
    live_logs()
elif command == "block" and len(sys.argv) > 2:
    block_ip(sys.argv[2])
elif command == "unblock" and len(sys.argv) > 2:
    unblock_ip(sys.argv[2])
elif command == "whitelist" and len(sys.argv) > 3:
    if sys.argv[2] == "add":
        whitelist_ip(sys.argv[3])
    elif sys.argv[2] == "remove":
        remove_whitelist_ip(sys.argv[3])
elif command == "whitelist" and len(sys.argv) > 2 and sys.argv[2] == "show":
    show_whitelist()
elif command == "port" and len(sys.argv) > 3 and sys.argv[2] == "set":
    change_port(sys.argv[3])
elif command == "logs" and len(sys.argv) > 2 and sys.argv[2] == "clean":
    cleanup_logs()
else:
    show_help()
