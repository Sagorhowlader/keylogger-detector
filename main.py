import platform
import time

import winsound

from monitor.system_monitor import SystemMonitor
from real_time_anomaly_detector import anomaly_detector

monitor_only = False


def beep():
    try:
        if platform.system() == 'Windows':
            winsound.Beep(frequency=1000, duration=300)
        else:
            print("Beep not supported for this platform.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    interval = 0.5
    monitor_only = False
    anomaly_detector_software = True

    try:
        if monitor_only:
            monitor = SystemMonitor(interval=interval)
            monitor.start()
            while True:
                time.sleep(5)
                real_time_data = monitor.get_realtime_metrics()
                print("real_time_data:", real_time_data)

                detector = anomaly_detector.RealTimeAnomalyDetector(
                    model_path="models/trained_model/random_forest_model.pkl",
                    scaler_path="models/trained_model/scaler.pkl"
                )
                prob = detector.predict_probability(real_time_data)
                print(f"Anomaly Probability: {prob:.2f}")

                if detector.alert_if_anomaly(real_time_data) == 1:
                    beep()
                    print("🛑  Anamoly Detected.")
                else:
                    print("✅ Normal Detected")
        else:
            monitor = SystemMonitor(interval=interval, label=0, file_name='normal.csv',mode="monitor")
            monitor.start()

    except KeyboardInterrupt:
        print("🛑 Monitoring stopped by user.")
