#!/bin/bash

# 🛡️ Honeypot Security Tool Installation Script
echo "🚀 Starting Honeypot Installation..."

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "❌ This script must be run as root! Use sudo ./install.sh"
    exit 1
fi

# Update system packages
echo "🔄 Updating system packages..."
apt update && apt upgrade -y

# Install required dependencies
echo "📦 Installing dependencies..."
apt install -y python3 python3-pip python3-venv ufw logrotate

# Create a dedicated user for the honeypot
echo "👤 Creating honeypot user..."
useradd -r -s /usr/sbin/nologin honeypot || echo "User already exists."

# Set up the honeypot directory
echo "📂 Setting up directories..."
mkdir -p /honeypot/logs /honeypot/config
chown -R honeypot:honeypot /honeypot
chmod -R 750 /honeypot

# Ensure honeypot.py exists
if [[ ! -f "honeypot.py" ]]; then
    echo "❌ Error: honeypot.py not found! Make sure it's in the correct directory."
    exit 1
fi

# Copy honeypot files to the system
echo "📥 Copying honeypot files..."
cp honeypot.py /honeypot/
cp -r config/ /honeypot/

# Ensure honeypot.service exists
if [[ ! -f "config/honeypot.service" ]]; then
    echo "❌ Error: honeypot.service not found!"
    exit 1
fi
cp config/honeypot.service /etc/systemd/system/

# Set correct permissions
echo "🔒 Setting permissions..."
chown -R honeypot:honeypot /honeypot
chmod -R 750 /honeypot

# Check if requirements.txt exists
if [[ ! -f "/honeypot/config/requirements.txt" ]]; then
    echo "❌ Error: requirements.txt not found!"
    exit 1
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
python3 -m venv /honeypot/venv
/honeypot/venv/bin/pip install -r /honeypot/config/requirements.txt

# Enable and start honeypot service
echo "🛠️ Enabling and starting honeypot service..."
systemctl daemon-reload
systemctl enable honeypot.service
systemctl start honeypot.service

# Ask user before enabling UFW
read -p "Do you want to enable UFW firewall? (y/n) " answer
if [[ "$answer" == "y" ]]; then
    echo "🔥 Configuring UFW Firewall..."
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw enable
fi

# Configure log rotation
echo "🔄 Configuring log rotation..."
if [[ -f "config/logrotate.conf" ]]; then
    cp config/logrotate.conf /etc/logrotate.d/honeypot
else
    echo "⚠️ Warning: logrotate.conf not found. Log rotation will not be configured."
fi

echo "✅ Installation complete! Check service status:"
systemctl status honeypot.service
