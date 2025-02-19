# config.py - Honeypot Configuration File

# Server Settings
HONEYPOT_IP = "0.0.0.0"  # Listen on all interfaces
HONEYPOT_PORT = 2222      # Port for SSH honeypot

# Logging Settings
LOG_FILE = "../logs/honeypot.log"

# Attack Detection
BAN_THRESHOLD = 5  # Number of failed attempts before banning IP
BANLIST_FILE = "../config/banlist.txt"

# Email Alerts (Optional - Set up SMTP)
EMAIL_ALERTS = True
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@example.com"
EMAIL_RECEIVER = "admin@example.com"
EMAIL_PASSWORD = "your_password"

# Web Dashboard Settings
DASHBOARD_HOST = "0.0.0.0"
DASHBOARD_PORT = 5000