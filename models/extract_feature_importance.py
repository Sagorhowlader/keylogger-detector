import joblib
import pandas as pd
import matplotlib.pyplot as plt

from utils.file_manager import project_path

# === CONFIG ===
MODEL_PATH = project_path('models/trained_model/svm_model.pkl')

# === FEATURES USED DURING TRAINING ===
feature_names = [
    "cpu_usage", "ram_usage", "disk_write_bytes",
    "net_sent", "net_recv", "process_count", "keystrokes",
    "mouse_clicks", "mouse_moves"
]


def load_model(path):
    try:
        print(f"🔍 Loading model from: {path}")
        model = joblib.load(path)
        print("✅ Model loaded successfully.\n")
        return model
    except FileNotFoundError:
        print(f"❌ ERROR: Model file not found at: {path}")
        exit(1)


def extract_importance(model, features):
    print("📊 Extracting feature importances...\n")
    importances = model.feature_importances_
    df = pd.DataFrame({
        "Feature": features,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False).reset_index(drop=True)
    print(df)
    return df


def plot_importance(df):
    plt.figure(figsize=(10, 6))
    plt.barh(df["Feature"], df["Importance"], color="skyblue")
    plt.xlabel("Importance")
    plt.title("Feature Importances - Random Forest")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    rf_model = load_model(MODEL_PATH)
    importance_df = extract_importance(rf_model, feature_names)
    plot_importance(importance_df)
