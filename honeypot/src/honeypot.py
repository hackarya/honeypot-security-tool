import os
import paramiko
import socket
import threading
import logging

LOG_DIR = "honeypot/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "honeypot.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format="%(asctime)s - %(message)s")
