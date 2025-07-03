from pathlib import Path

import joblib
import numpy as np

from utils.file_manager import FileManager


class RealTimeAnomalyDetector:
    def __init__(self, model_path, scaler_path, threshold=0.2):
        """
        Loads the trained model and scaler.
        """
        self.pkl_path = Path(FileManager(file_path=model_path, file_format='pkl').get_file_path())
        self.scaler_path = Path(FileManager(file_path=scaler_path, file_format='pkl').get_file_path())

        print(f"Loading model from... {self.pkl_path / model_path}")
        print(f"Loading scaler from... {self.scaler_path / scaler_path}")

        self.model = joblib.load(self.pkl_path / model_path)
        self.scaler = joblib.load(self.scaler_path / scaler_path)
        self.threshold = threshold

        # Feature order must match training
        self.feature_names = [
            'cpu_usage', 'ram_usage', 'disk_write_bytes', 'net_sent', 'net_recv',
            'process_count', 'keystrokes', 'mouse_clicks', 'mouse_moves'
        ]

    def preprocess(self, data):
        """
        Accepts a list of feature values in the same order as training.
        Scales the input using the saved scaler.
        """
        if len(data) != len(self.feature_names):
            raise ValueError(f"Expected {len(self.feature_names)} features, got {len(data)}")

        data_array = np.array(data).reshape(1, -1)  # Make it 2D for scaler
        scaled_data = self.scaler.transform(data_array)
        return scaled_data

    def predict(self, raw_data):
        """
        Preprocesses and predicts if the input is normal (0) or anomaly (1).
        """
        scaled = self.preprocess(raw_data)
        prediction = self.model.predict(scaled)[0]
        return int(prediction)

    def alert_if_anomaly(self, raw_data):
        """
        Prints alert if anomaly is detected.
        """
        prediction = self.predict(raw_data)
        if prediction == 1:
            print("🚨 ALERT: Anomaly (possible keylogger) detected!")
        else:
            print("✅ Normal behavior.")
        return prediction

    def predict_probability(self, raw_data):
        scaled = self.preprocess(raw_data)
        prob = self.model.predict_proba(scaled)[0][1]
        return prob


if __name__ == "__main__":
    detector = RealTimeAnomalyDetector(
        model_path="models/trained_model/svm_model.pkl",
        scaler_path="models/trained_model/scaler.pkl"
    )

    # Simulated real-time input: [cpu, ram, disk_write, net_sent, net_recv, process_count, keystrokes, clicks, moves]
    live_data = [7.1, 91.2, 38637526528, 51180203, 269329368, 219, 0, 0, 0]
    prob = detector.predict_probability(live_data)
    print(f"Anomaly Probability: {prob:.2f}")
    detector.alert_if_anomaly(live_data)
