import os
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from utils.file_manager import FileManager


class TrainModel:
    def __init__(self, csv_path, output_dir='models'):
        project_root = Path(FileManager(file_path=output_dir).get_file_path())
        self.file_manager = FileManager(file_path=output_dir, file_format='csv')
        self.csv_path = project_root / csv_path
        self.output_dir = project_root /  output_dir
        self.expected_columns = [
            "cpu_usage", "ram_usage", "disk_write_bytes",
            "net_sent", "net_recv", "process_count", "keystrokes",
            "mouse_clicks", "mouse_moves", "label"
        ]

        self.models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'svm': SVC(probability=True),
            'logistic_regression': LogisticRegression(max_iter=1000),
            'gradient_boosting': GradientBoostingClassifier()
        }

    def load_data(self):
        print(f"[+] Model Training Started...")
        print(f"[+] Prepared data load from ... {self.csv_path}")
        df = self.file_manager.read_csv(self.csv_path)
        missing = [col for col in self.expected_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        X = df[self.expected_columns[:-1]]
        y = df['label']
        return X, y

    def train_and_save_all(self):
        X, y = self.load_data()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        print(f"[+] Model Training Scaler...{self.output_dir}")
        joblib.dump(scaler, os.path.join(self.output_dir, "scaler.pkl"))
        print("Scaler saved.\n")

        for name, model in self.models.items():
            print(f"🚀 Training {name}...")
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            print(f"📊 {name} results:")
            print(f"  Accuracy:  {acc:.4f}")
            print(f"  Precision: {prec:.4f}")
            print(f"  Recall:    {rec:.4f}")
            print(f"  F1 Score:  {f1:.4f}\n")

            # Save the model
            model_path = os.path.join(self.output_dir, f"{name}_model.pkl")
            joblib.dump(model, model_path)
            print(f"✅ Saved: {model_path}\n")
