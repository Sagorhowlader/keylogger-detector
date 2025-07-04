import os
import re

import pandas as pd
from sklearn.utils import shuffle

from utils.file_manager import FileManager, project_path


class DatasetPreparer:
    def __init__(self, output_file='data/prepared_dataset.csv'):
        # Get project root using FileManager
        self.file_path = project_path(output_file)
        self.data_dir = project_path('data')
        # Resolve paths relative to project root
        # Set up FileManager to save the prepared dataset
        self.file_manager = FileManager(str(self.file_path), file_format='csv', header=None, mode='w')
        print('[*] Output file:', self.file_path)

    def load_labeled_data(self, label_value, prefix):
        """Load and label all CSV files matching the given prefix."""
        pattern = re.compile(rf".*{re.escape(prefix)}.*", re.IGNORECASE)
        files = [f for f in os.listdir(self.data_dir) if pattern.search(f) and f.endswith('.csv')]
        print(f"[*] Found {prefix} files:", files)

        all_data = []
        for file in files:
            path = self.data_dir / file
            df = pd.read_csv(path)
            df['label'] = label_value
            all_data.append(df)

        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

    def prepare(self):
        print("[+] Preparing dataset...")

        # Load normal and anomaly data
        normal_df = self.load_labeled_data(label_value=0, prefix='normal')
        anomaly_df = self.load_labeled_data(label_value=1, prefix='anomaly')

        # Combine and shuffle
        combined_df = pd.concat([normal_df, anomaly_df], ignore_index=True)

        if 'timestamp' in combined_df.columns:
            combined_df.drop(columns=['timestamp'], inplace=True)

        combined_df = shuffle(combined_df, random_state=42)
        print("[*] Preview of prepared data:\n", combined_df.head())

        # Save using FileManager
        self.file_manager.save_dataframe(combined_df)
        self.file_manager.close()
        print(f"[✓] Prepared dataset saved to: {self.file_path}")


if __name__ == "__main__":
    preparer = DatasetPreparer(output_file="data/prepared_dataset.csv")
    preparer.prepare()
