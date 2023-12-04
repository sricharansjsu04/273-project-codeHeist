import time
import pickle
from typing import Dict
from prettytable import PrettyTable

class MVCC:
    def __init__(self):
        self.versioned_data: Dict[str, Dict[int, dict]] = {}

    def start_transaction(self):
        return int(time.time() * 1000)  # Unique timestamp-based transaction ID

    def write(self, key, value, transaction_id):
        if key not in self.versioned_data:
            self.versioned_data[key] = {}
        self.versioned_data[key][transaction_id] = value
        print(f"Write: {key} at {transaction_id} = {value}")  # Debugging print

    def commit_transaction(self, transaction_id, data):
        for key, value in data.items():
            self.write(key, value, transaction_id)
        self.log_data("Transaction Committed", {transaction_id: data})
        print(f"Commit Transaction: {transaction_id} with data {data}")  # Debugging print

    def read(self, key, timestamp):
        versions = self.versioned_data.get(key, {})
        print(f"Available versions for {key}: {versions}")  # Debugging print
        latest_version_id = max((v for v in versions if v <= timestamp), default=None)
        print(f"Reading {key} at {timestamp}, latest version: {latest_version_id}")  # Debugging print
        return versions.get(latest_version_id)

    def log_data(self, title, data):
        table = PrettyTable()
        table.title = title
        table.field_names = ["Transaction ID", "Key", "Value"]

        for transaction_id, versions in data.items():
            for key, value in versions.items():
                table.add_row([transaction_id, key, value])

        print(table)
