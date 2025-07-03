import os
import random
import string
import psutil
import time
from datetime import datetime

# Setup log directory and file
LOG_DIR = os.path.join(os.getcwd(), "log")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "system_fake_keylog.txt")

# Simulate a realistic background logger
def random_key():
    return random.choice(string.ascii_letters + string.digits)

def log_system_activity():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_io_counters().write_bytes
    net = psutil.net_io_counters()
    net_sent = net.bytes_sent
    net_recv = net.bytes_recv
    process_count = len(psutil.pids())

    return cpu, ram, disk, net_sent, net_recv, process_count

def write_fake_log(file_path):
    with open(file_path, 'a') as f:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            key = random_key()
            cpu, ram, disk, net_sent, net_recv, procs = log_system_activity()

            log_line = f"[{timestamp}] Key: {key} | CPU: {cpu}% | RAM: {ram}% | Disk: {disk} | Net: ({net_sent}, {net_recv}) | Procs: {procs}\n"
            f.write(log_line)
            f.flush()
            time.sleep(0.3)

if __name__ == "__main__":
    print("[FAKE LOGGER] Running advanced keylogger simulation. Ctrl+C to stop.")
    try:
        write_fake_log(LOG_FILE)
    except KeyboardInterrupt:
        print("\n[FAKE LOGGER] Stopped.")
