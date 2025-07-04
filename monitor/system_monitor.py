import logging
import signal
import sys
from threading import Timer

import pandas as pd

from monitor.keyboard_monitor import KeyboardMonitor
from monitor.mouse_monitor import MouseMonitor
from monitor.performance_monitor import PerformanceMonitor
from utils.file_manager import FileManager, project_path

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class SystemMonitor:
    def __init__(self, interval, label=0, file_name=None, mode=None):
        self.interval = interval
        self.label = label
        self.running = True
        self.keyboard_monitor = KeyboardMonitor(interval=interval)
        self.mouse_monitor = MouseMonitor(interval=interval)
        self.system_monitor = PerformanceMonitor(interval=interval)
        self.mode = mode
        self.header = [
            "cpu_usage", "ram_usage", "disk_write_bytes",
            "net_sent", "net_recv", "process_count", "keystrokes",
            "mouse_clicks", "mouse_moves", "label"
        ]
        file_path = f"data/{file_name}" if file_name else 'data/monitor_log_anomaly.csv'
        self.file_path = project_path(file_path)
        self.file_manager = FileManager(self.file_path, 'csv', self.header)
        self.lastValues = {}
        signal.signal(signal.SIGTERM, self.handle_exit)
        signal.signal(signal.SIGINT, self.handle_exit)

    def start(self):
        """Start monitoring system, keyboard, and mouse."""
        logging.info("Monitoring started. Press Ctrl+C to stop.")
        logging.info(f"Monitoring data will be saved to: {self.file_path}")
        if self.mode == 'monitor':
            self.file_manager.open()
        self.keyboard_monitor.start()
        self.mouse_monitor.start()
        self.system_monitor.start()
        self.schedule_data_write()

    def stop(self):
        """Stop all monitors and close the output file."""
        if not self.running:
            return
        self.running = False

        self.keyboard_monitor.stop()
        self.mouse_monitor.stop()
        self.system_monitor.stop()
        self.file_manager.close()

        logging.info("Monitoring stopped and file closed.")

    def collect_all_metrics(self):
        """Collect metrics from all monitors."""
        system_metrics = self.system_monitor.performance_collect()
        keystrokes = self.keyboard_monitor.queue.pop()
        mouse_data = self.mouse_monitor.queue.pop()

        return system_metrics + mouse_data + [keystrokes, self.label]

    def data_write(self):
        """Write collected data to file and reschedule if running."""
        data = self.collect_all_metrics()
        self.lastValues = data[:-1]
        if self.mode == 'monitor':
            self.file_manager.write(data)

        if self.running:
            self.schedule_data_write()

    def schedule_data_write(self):
        """Schedule the next data write."""
        Timer(self.interval, self.data_write).start()

    def get_realtime_metrics(self):
        """Get current metrics (excluding label)."""
        return pd.DataFrame([self.lastValues])

    def handle_exit(self, signum, frame):
        """Handle graceful shutdown on SIGTERM or SIGINT."""
        logging.warning("Signal received. Shutting down...")
        self.stop()
        sys.exit(0)
