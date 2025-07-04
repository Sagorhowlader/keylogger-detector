import joblib
import numpy as np
import pandas as pd

from utils.file_manager import FileManager, project_path


class RealTimeAnomalyDetector:
    def __init__(self, model_path, scaler_path, threshold=0.2):
        """
        Loads the trained model and scaler.
        """
        pkl_file_path = project_path(model_path)
        scaler_file_path = project_path(scaler_path)
        self.pkl_path = FileManager(file_path=model_path, file_format='pkl')
        self.scaler_path = FileManager(file_path=scaler_path, file_format='pkl')

        print(f"Loading model from... {pkl_file_path}")
        print(f"Loading scaler from... {scaler_file_path}")

        self.model = joblib.load(pkl_file_path)
        self.scaler = joblib.load(scaler_file_path)
        self.threshold = threshold
        # Feature order must match training
        self.feature_names = [
            'cpu_usage', 'ram_usage', 'disk_write_bytes', 'net_sent', 'net_recv',
            'process_count', 'keystrokes', 'mouse_clicks', 'mouse_moves'
        ]

    def preprocess(self, data):
        """
        Accepts a list or single-row DataFrame of features and returns scaled output.
        Ignores column names and assumes feature order matches training.
        """
        if isinstance(data, pd.DataFrame):
            data_array = data.values  # get the raw numeric data
        elif isinstance(data, list):
            data_array = np.array(data).reshape(1, -1)
        else:
            raise TypeError("Expected a list or DataFrame")

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
        return prediction

    def predict_probability(self, raw_data):
        scaled = self.preprocess(raw_data)
        prob = self.model.predict_proba(scaled)[0][1]
        return prob
