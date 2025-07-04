import os

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_file_path(path_segments):
    return os.path.join(BASE_DIR, path_segments)


import os
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def project_path(*segments) -> Path:
    """
    Build an absolute path from the project root.

    Supports:
        project_path("data", "log.txt")
        project_path("data/log.txt")
    """
    if len(segments) == 1 and isinstance(segments[0], str):
        return PROJECT_ROOT / Path(segments[0])
    return PROJECT_ROOT.joinpath(*segments)


class FileManager:
    def __init__(self, file_path, file_format='csv', header=None, mode='a'):
        self.file_path = project_path(file_path)
        self.file_format = file_format
        self.header = header
        self.mode = mode
        self.file_handle = None
        self.writer = None

    def open(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        file_exists = self.file_path.exists()

        self.file_handle = self.file_path.open(self.mode, newline='', encoding='utf-8')

        if self.file_format == 'csv':
            self.writer = csv.writer(self.file_handle)
            if self.header and (not file_exists or self.file_path.stat().st_size == 0):
                self.writer.writerow(self.header)

    def write(self, data):
        if self.file_format == 'csv' and self.writer:
            self.writer.writerow(data)
        elif self.file_format == 'text' and self.file_handle:
            if isinstance(data, list):
                self.file_handle.writelines(
                    line if line.endswith('\n') else line + '\n' for line in data
                )
            else:
                self.file_handle.write(data if data.endswith('\n') else data + '\n')

        if self.file_handle:
            self.file_handle.flush()

    def close(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
            self.writer = None

    def read_csv(self, path=None):
        target_path = Path(path) if path else self.file_path
        if not target_path.exists():
            raise FileNotFoundError(f"CSV file not found: {target_path}")
        return pd.read_csv(target_path)

    def save_dataframe(self, df):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.file_path, index=False)
