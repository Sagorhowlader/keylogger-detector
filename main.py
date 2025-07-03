import platform

import winsound
import time
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
    interval = 2
    monitor_only = True
    anomaly_detector_software = True

    try:
        if monitor_only:
            monitor = SystemMonitor(interval=interval)

            # Load detector once
            detector = anomaly_detector.RealTimeAnomalyDetector(
                model_path="models/trained_model/svm_model.pkl",
                scaler_path="models/trained_model/scaler.pkl"
            )

            while True:
                time.sleep(interval)
                real_time_data = monitor.get_realtime_metrics()
                print("Real time data ", real_time_data)

                prob = detector.predict_probability(real_time_data)
                print(f"Anomaly Probability: {prob:.2f}")

                if detector.alert_if_anomaly(real_time_data) == 1:
                    beep()
                else:
                    print("✅ Normal Detected")

        else:
            file_name_input = input("Enter output file name: ").strip()
            file_name = f"data/{file_name_input}"
            file_format = file_name.split('.')[-1].lower()
            monitor = SystemMonitor(interval=5, file_path=file_name, label=0, file_format='csv')
            monitor.start()

    except KeyboardInterrupt:
        print("🛑 Monitoring stopped by user.")
