#!/bin/bash

# Honeypot Security Tool Installation Script
echo "🚀 Starting Honeypot Installation..."

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "❌ This script must be run as root! Use: sudo ./install.sh"
    exit 1
fi

# Update system packages
echo "🔄 Updating system packages..."
apt update && apt upgrade -y

# Install required dependencies
echo "📦 Installing dependencies..."
apt install -y python3 python3-pip python3-venv ufw logrotate iptables fail2ban

# Create a dedicated user for the honeypot
if id "honeypot" &>/dev/null; then
    echo "👤 Honeypot user already exists."
else
    echo "👤 Creating honeypot user..."
    useradd -r -s /usr/sbin/nologin honeypot
fi

# Set up the honeypot directory
echo "📂 Setting up directories..."
mkdir -p /honeypot/logs /honeypot/config /honeypot/analytics
chown -R honeypot:honeypot /honeypot
chmod -R 750 /honeypot

# Check if honeypot.py exists before copying
if [ ! -f honeypot/src/honeypot.py ]; then
    echo "❌ Error: honeypot.py not found! Make sure it's in the correct directory."
    exit 1
fi

# Copy honeypot files to the system
echo "📥 Copying honeypot files..."
cp -r honeypot/src/*.py /honeypot/
cp -r config/ /honeypot/
cp config/honeypot.service /etc/systemd/system/

# Set correct permissions
echo "🔒 Setting permissions..."
chown -R honeypot:honeypot /honeypot
chmod -R 750 /honeypot

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
python3 -m venv /honeypot/venv
source /honeypot/venv/bin/activate

if [ -f /honeypot/config/requirements.txt ]; then
    pip install -r /honeypot/config/requirements.txt
else
    echo "❌ Error: requirements.txt not found!"
    deactivate
    exit 1
fi

deactivate

# Enable and start honeypot service
echo "🛠️ Enabling and starting honeypot service..."
systemctl daemon-reload

if [ -f /etc/systemd/system/honeypot.service ]; then
    systemctl enable honeypot.service
    systemctl start honeypot.service
else
    echo "❌ Error: honeypot.service file not found!"
    exit 1
fi

# Configure firewall (optional)
echo "🔥 Configuring UFW Firewall..."
ufw allow 22/tcp  # SSH
ufw allow 80/tcp  # Web dashboard (if applicable)
ufw allow 443/tcp # HTTPS (if applicable)
ufw enable

# Set up log rotation
if [ -f config/logrotate.conf ]; then
    echo "🔄 Configuring log rotation..."
    cp config/logrotate.conf /etc/logrotate.d/honeypot
else
    echo "⚠️ Warning: logrotate.conf file not found! Skipping log rotation setup."
fi

echo "✅ Installation complete! Check service status:"
systemctl status honeypot.service
