# ban_ip.py - Bans IPs after multiple failed login attempts

import os
import subprocess
import logging

# Import configuration settings
from config import BAN_THRESHOLD, BANLIST_FILE, LOG_FILE

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def load_banned_ips():
    """Load existing banned IPs from file."""
    if not os.path.exists(BANLIST_FILE):
        return set()
    with open(BANLIST_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_banned_ip(ip):
    """Save a newly banned IP to the banlist file."""
    with open(BANLIST_FILE, "a") as f:
        f.write(ip + "\n")

def ban_ip(ip):
    """Ban an IP using iptables (Linux firewall)."""
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        logging.info(f"IP BANNED: {ip}")
        save_banned_ip(ip)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to ban IP {ip}: {e}")
        return False

def check_and_ban(ip, failed_attempts):
    """Check if an IP should be banned based on failed attempts."""
    banned_ips = load_banned_ips()
    
    if ip in banned_ips:
        return False  # IP is already banned

    if failed_attempts >= BAN_THRESHOLD:
        return ban_ip(ip)

    return False