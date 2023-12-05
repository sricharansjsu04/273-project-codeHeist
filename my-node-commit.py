import time
from random import randint
import pickle
from multiprocessing import Process, Lock, Queue
from prettytable import PrettyTable
from mvcc_commit import MVCC  

def handle_transaction(node, key, value, transaction_queue):
    node.simulate_transaction(key, value, transaction_queue)
    time.sleep(1)  # Small delay to simulate processing time
    # Wait for the transaction ID to be put in the queue and then commit
    transaction_id = transaction_queue.get()
    node.simulate_commit(transaction_id)

def transaction_and_commit(node, key, value, transaction_queue):
    # Start a transaction
    node.simulate_transaction(key, value, transaction_queue)
    # Random delay to simulate processing time
    time.sleep(randint(1, 3))
    # Commit the transaction
    transaction_id, node_id = transaction_queue.get()
    node.simulate_commit(transaction_id)


class Node:
    def __init__(self, node_id, mvcc_lock, port):
        self.node_id = node_id
        self.mvcc_lock = mvcc_lock
        self.port = port
        self.mvcc_instance = None
        self.pending_transactions = {}

    def load_mvcc_instance(self):
        with self.mvcc_lock:
            try:
                with open('mvcc_data.pickle', 'rb') as f:
                    self.mvcc_instance = pickle.load(f)
            except FileNotFoundError:
                self.mvcc_instance = MVCC()

    def save_mvcc_instance(self):
        with self.mvcc_lock:
            with open('mvcc_data.pickle', 'wb') as f:
                pickle.dump(self.mvcc_instance, f)

    def simulate_transaction(self, key, value, queue):
        self.load_mvcc_instance()
        transaction_id = self.mvcc_instance.start_transaction()
        self.pending_transactions[transaction_id] = (key, value, self.node_id)  # Include node ID
        self.log_message("Transaction Simulated", f"ID: {transaction_id}, Key: {key}, Value: {value}")
        queue.put((transaction_id, self.node_id))


    def simulate_commit(self, transaction_id):
        print(f"Attempting to commit transaction: {transaction_id}")
        if transaction_id in self.pending_transactions:
            key, value, node_id = self.pending_transactions.pop(transaction_id)  # Unpack three values
            self.mvcc_instance.write(key, value, transaction_id)
            self.mvcc_instance.commit_transaction(transaction_id, {key: value}, node_id)  # Use node_id if needed
            self.save_mvcc_instance()
            # self.log_message("Transaction Committed", f"ID: {transaction_id}, Key: {key}, Value: {value}")


    def simulate_read(self, key):
        self.load_mvcc_instance()
        timestamp = int(time.time() * 1000)
        user_data = self.mvcc_instance.read(key, timestamp)
        self.log_message("Read Data", f"Key: {key}, Value: {user_data if user_data else 'None'}")

    def log_message(self, action, message):
        table = PrettyTable()
        table.title = f"Node {self.node_id} - {action}"
        table.field_names = ["Timestamp", "Message"]
        table.add_row([int(time.time() * 1000), message])
        print(table)

if __name__ == "__main__":
    mvcc_lock = Lock()
    transaction_queue = Queue()

    # Initialize nodes
    node1 = Node(node_id=1, mvcc_lock=mvcc_lock, port=5000)
    node2 = Node(node_id=2, mvcc_lock=mvcc_lock, port=5000)

    # Function to handle transactions and commit
    # def handle_transaction(node, key, value):
    #     transaction_id = node.simulate_transaction(key, value, transaction_queue)
    #     time.sleep(1)  # Small delay to simulate processing time
    #     node.simulate_commit(transaction_id)

    # Create and start processes for transactions and commits
    processes = [
        Process(target=transaction_and_commit, args=(node1, 'user1', {'name': 'User-1A', 'age': 25}, transaction_queue)),
        Process(target=node1.simulate_read, args=('user1',)),
        Process(target=transaction_and_commit, args=(node2, 'user2', {'name': 'User-2B', 'age': 35}, transaction_queue)),
        Process(target=node2.simulate_read, args=('user2',)),
        # Add more processes with different sequences of transactions, commits, and reads
    ]

    # Start and join processes
    for process in processes:
        process.start()
    for process in processes:
        process.join()