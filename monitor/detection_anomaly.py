import psutil
import joblib
import pandas as pd
from pynput import keyboard, mouse
from utils.file_manager import get_file_path, write_file
import datetime


class KeyloggerAnomalyDetector:
    def __init__(self, model_path, scaler_path):
        """
        Initializes the KeyloggerAnomalyDetector with the trained model and scaler.
        """
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

        # Initialize counters for key/mouse events
        self.key_count = 0
        self.mouse_click_count = 0

        # Start listeners for keyboard and mouse events
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)

        self.keyboard_listener.start()
        self.mouse_listener.start()

    def on_key_press(self, key):
        """Callback function when a key is pressed."""
        self.key_count += 1

    def on_mouse_click(self, x, y, button, pressed):
        """Callback function when a mouse click is detected."""
        if pressed:
            self.mouse_click_count += 1

    def get_system_metrics(self):
        """
        Collects and returns real-time system metrics (8 features as expected by the model).
        """
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk_write = psutil.disk_io_counters().write_bytes
        net_sent = psutil.net_io_counters().bytes_sent
        net_recv = psutil.net_io_counters().bytes_recv
        process_count = len(psutil.pids())  # Number of processes running

        # Collect the metrics into a list of exactly 8 features
        metrics = [cpu, ram, disk_write, net_sent, net_recv, process_count, self.key_count, self.mouse_click_count]

        # Reset counters after collection
        self.key_count = 0
        self.mouse_click_count = 0

        return metrics

    def predict_anomaly(self, metrics):
        """
        Takes system metrics, scales them, and predicts whether the behavior is normal or anomalous.
        """
        metrics_df = pd.DataFrame([metrics],
                                  columns=['cpu', 'ram', 'disk_write', 'net_sent', 'net_recv', 'process_count',
                                           'key_count', 'mouse_click_count'])

        # Scale the incoming metrics using the pre-trained scaler
        metrics_scaled = self.scaler.transform(metrics_df)

        # Predict anomaly (0 = normal, 1 = anomaly)
        return self.model.predict(metrics_scaled)

    def monitor_system(self):
        """
        Monitors the system indefinitely, checking for anomalies at a specified interval.
        """
        while True:
            # Collect metrics and make a prediction
            metrics = self.get_system_metrics()
            prediction = self.predict_anomaly(metrics)

            if prediction[0] == 1:
                print("⚠️ Keylogger-like behavior detected!")
            else:
                print("✅ Normal behavior detected.")


# Example usage
if __name__ == "__main__":
    model_path = get_file_path("models/random_forest_model.pkl")
    scaler_path = get_file_path("models/scaler.pkl")

    detector = KeyloggerAnomalyDetector(model_path, scaler_path)
    detector.monitor_system()  # Starts monitor in real-time
