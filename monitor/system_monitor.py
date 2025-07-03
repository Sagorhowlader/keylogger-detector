import signal
import sys
import time

from monitor.keyboard_monitor import KeyboardMonitor
from monitor.mouse_monitor import MouseMonitor
from monitor.performance_monitor import PerformanceMonitor
from utils.file_manager import FileManager


class SystemMonitor:
    def __init__(self, interval=0, file_path='monitor_log.csv', label=0, file_format='csv', mode='monitor'):
        self.interval = interval
        self.file_path = file_path
        self.label = label
        self.file_format = file_format
        self.mode = mode
        self.keyboard_monitor = KeyboardMonitor()
        self.mouse_monitor = MouseMonitor()
        self.system_monitor = PerformanceMonitor()
        self.header = [
            "cpu_usage", "ram_usage", "disk_write_bytes",
            "net_sent", "net_recv", "process_count", "keystrokes",
            "mouse_clicks", "mouse_moves", "label"
        ]
        self.file_manager = FileManager(self.file_path, self.file_format, self.header)
        self.running = True
        self.file_manager.open()
        signal.signal(signal.SIGTERM, self.handle_exit)
        signal.signal(signal.SIGINT, self.handle_exit)

    def collect_all_metrics(self):
        system_metrics = self.system_monitor.performance_collect()
        keystrokes = self.keyboard_monitor.get_count()
        mouse_clicks, mouse_moves = self.mouse_monitor.get_counts()
        return system_metrics + [keystrokes, mouse_clicks, mouse_moves, self.label]

    def handle_exit(self, signum, frame):
        print("\n[!] Signal received. Shutting down...")
        self.stop()
        sys.exit(0)

    def start(self):
        print("[+] Monitoring started... Press Ctrl+C to stop.")
        print(f"[+] Monitoring data saved ... {self.file_path}")
        self.keyboard_monitor.start()
        self.mouse_monitor.start()
        self.system_monitor.start()
        while self.running:
            data = self.collect_all_metrics()
            if self.file_format == 'csv':
                self.file_manager.write(data)
            time.sleep(self.interval)

    def stop(self):
        """Safely stop all monitors and close file if in monitor mode."""
        self.keyboard_monitor.stop()
        self.mouse_monitor.stop()
        self.system_monitor.stop()
        if self.mode == "monitor":
            self.file_manager.close()
        self.running = False
        print("[!] Monitoring stopped and file closed.")

    def get_realtime_metrics(self):
        data = self.collect_all_metrics()
        return data[:-1]  # exclude label for prediction
