import joblib
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from utils.file_manager import FileManager
from utils.file_manager import project_path


class TrainModel:
    def __init__(self, csv_path, output_dir="models/trained_model"):
        self.csv_path = project_path(csv_path)
        self.output_dir = project_path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.file_manager = FileManager(self.csv_path, file_format="csv")

        self.expected_columns = [
            "cpu_usage", "ram_usage", "disk_write_bytes",
            "net_sent", "net_recv", "process_count", "keystrokes",
            "mouse_clicks", "mouse_moves", "label"
        ]

        self.models = {
            "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "svm": SVC(probability=True, random_state=42),
            "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
            "gradient_boosting": GradientBoostingClassifier(random_state=42)
        }

    def load_data(self):
        print(f"[+] Loading data from: {self.csv_path}")
        df = self.file_manager.read_csv()

        if df.empty:
            raise ValueError("Input CSV is empty.")

        missing = [col for col in self.expected_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        X = df[self.expected_columns[:-1]]
        y = df["label"]
        return X, y

    def train_and_save_all(self):
        X, y = self.load_data()

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )

        # Feature scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        scaler_path = self.output_dir / "scaler.pkl"
        joblib.dump(scaler, scaler_path)
        print(f"✅ Scaler saved at: {scaler_path}\n")

        for name, model in self.models.items():
            print(f"🚀 Training `{name}`...")

            # Cross-validation on full scaled data
            X_scaled_full = scaler.transform(X)  # scale full data for CV
            cv_scores = cross_val_score(model, X_scaled_full, y, cv=5, scoring="accuracy")
            print(f"🔄 `{name}` Cross-Validation Accuracy Scores: {cv_scores}")
            print(f"📉 `{name}` Mean CV Accuracy: {cv_scores.mean():.4f}")

            # Train on training split
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)

            # Test set evaluation
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            print(f"📊 `{name}` Test Set Metrics:")
            print(f"  - Accuracy :  {acc:.4f}")
            print(f"  - Precision:  {prec:.4f}")
            print(f"  - Recall   :  {rec:.4f}")
            print(f"  - F1 Score :  {f1:.4f}")

            model_path = self.output_dir / f"{name}_model.pkl"
            joblib.dump(model, model_path)
            print(f"✅ Model saved at: {model_path}\n")
