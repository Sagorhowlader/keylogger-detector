import os
import re
from pathlib import Path

import pandas as pd
from sklearn.utils import shuffle

from utils.file_manager import FileManager


class DatasetPreparer:
    def __init__(self, data_dir='data', output_file='data/prepared_dataset.csv'):
        # Get project root using FileManager
        project_root = Path(FileManager(file_path=output_file).get_file_path())

        # Resolve paths relative to project root
        self.data_dir = project_root / data_dir
        self.output_file = project_root / output_file

        # Set up FileManager to save the prepared dataset
        self.file_manager = FileManager(str(self.output_file), file_format='csv', header=None, mode='w')

        print('[*] Data directory:', self.data_dir)
        print('[*] Output file:', self.output_file)

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
        print(f"[✓] Prepared dataset saved to: {self.output_file}")


if __name__ == "__main__":
    preparer = DatasetPreparer(data_dir="data", output_file="data/prepared_dataset.csv")
    preparer.prepare()
