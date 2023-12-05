import time
from prettytable import PrettyTable

class MVCC:
    def __init__(self):
        self.versioned_data = {}

    def start_transaction(self):
        return int(time.time() * 1000)

    def write(self, key, value, transaction_id):
        if key not in self.versioned_data:
            self.versioned_data[key] = {}
        self.versioned_data[key][transaction_id] = value

    def commit_transaction(self, transaction_id, data, node_id):
        # Assuming data is already written in the versioned_data by write method
        self.log_data(f"Transaction Committed by Node {node_id}", {transaction_id: data})
        self.log_snapshot("MVCC Data Snapshot after Commit")

    def read(self, key, timestamp):
        versions = self.versioned_data.get(key, {})
        print(f"Available versions for {key}:\n")  # Debugging print
        for key, version_list in versions.items():
            print(f"- {key}:----- {version_list}")
        latest_version_id = max(versions.keys(), default=None)
        print(f"Reading {key} at {timestamp}. latest vesrion: {latest_version_id}")
        return versions.get(latest_version_id)

    def log_data(self, title, data):
        table = PrettyTable()
        table.title = title
        table.field_names = ["Transaction ID", "Key", "Value"]

        for transaction_id, versions in data.items():
            for key, value in versions.items():
                table.add_row([transaction_id, key, value])
        print(table)

    def log_snapshot(self, title):
        table = PrettyTable()
        table.title = title
        table.field_names = ["Key", "Transaction ID", "Value"]

        for key, versions in self.versioned_data.items():
            for transaction_id, value in versions.items():
                table.add_row([key, transaction_id, value])
        print(table)