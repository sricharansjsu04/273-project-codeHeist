import time
import pickle
import zmq
from multiprocessing import Process, Lock
from prettytable import PrettyTable
from mvcc import MVCC

# Initializes a new node instance.
class Node:
    def __init__(self, node_id, mvcc_lock, port):
        self.node_id = node_id
        self.mvcc_lock = mvcc_lock
        self.port = port
        self.mvcc_instance = None

 # Loads the MVCC instance from a file or creates a new one if the file doesn't exist.
    def load_mvcc_instance(self):
        with self.mvcc_lock:
            try:
                with open('mvcc_data.pickle', 'rb') as f:
                    self.mvcc_instance = pickle.load(f)
            except FileNotFoundError:
                self.mvcc_instance = MVCC()

    # Saves the current state of the MVCC instance to a file.
    def save_mvcc_instance(self):
        with self.mvcc_lock:
            with open('mvcc_data.pickle', 'wb') as f:
                pickle.dump(self.mvcc_instance, f)

    # Simulates a transaction on the MVCC instance.
    def simulate_transaction(self, key, value):
        self.load_mvcc_instance()
        transaction_id = self.mvcc_instance.start_transaction()
        self.mvcc_instance.write(key, value, transaction_id)
        self.mvcc_instance.commit_transaction(transaction_id, {key: value})
        self.save_mvcc_instance()
        self.log_message("Write Display", f"TimeStamp : {transaction_id}, Key for user: {key}, user Info: {value}")

    # Simulates a read operation from the MVCC instance.
    def simulate_read(self, key):
        timestamp = int(time.time() * 1000)
        self.load_mvcc_instance()
        user_data = self.mvcc_instance.read(key, timestamp)
        self.log_message("Read Display", f"Key for user: {key}, user Info: {user_data if user_data else 'None'}")

    # Logs a message with a timestamp and action detail.
    def log_message(self, action, message):
        table = PrettyTable()
        table.title = f"Node {self.node_id} - {action}"
        table.field_names = ["Timestamp during display", "Saved transaction with timestamp"]
        table.add_row([int(time.time() * 1000), message])
        print(table)
        print()

if __name__ == "__main__":
    mvcc_lock = Lock()

    # Initialize nodes
    node1 = Node(node_id=1, mvcc_lock=mvcc_lock, port=5000)
    node2 = Node(node_id=2, mvcc_lock=mvcc_lock, port=6000)

    processes = []

    while True:
        operation = input("Enter 'read', 'write', or 'exit' to terminate: ")

        if operation.lower() == 'exit':
            break
        elif operation.lower() == 'read':
            key = input("Enter key for read operation: ")
            node_number = int(input("Enter node number for read operation (1 or 2): "))
            processes.append(Process(target=getattr(Node, f"simulate_read"), args=(globals()[f"node{node_number}"], key)))
        elif operation.lower() == 'write':
            key = input("Enter key for write operation: ")
            node_number = int(input("Enter node number for write operation (1 or 2): "))
            name = input("Enter name for write operation: ")
            age = int(input("Enter age for write operation: "))
            value = {'name': name, 'age': age}
            processes.append(Process(target=getattr(Node, f"simulate_transaction"), args=(globals()[f"node{node_number}"], key, value)))


    # Start and join transaction processes
    for process in processes:
        process.start()
    for process in processes:
        process.join()

    # Create processes for reads and writes
    # processes = [
    #     Process(target=node1.simulate_read, args=('user1',)),
    #     # Process(target=node2.simulate_transaction, args=('user2', {'name': 'User-2B', 'age': 35})),
    #     # Process(target=node2.simulate_read, args=('user2',)),
    #     # Process(target=node1.simulate_transaction, args=('user1', {'name': 'User-1C', 'age': 30})),
    #     # Process(target=node1.simulate_read, args=('user2',)),
    #     # Process(target=node2.simulate_read, args=('user1',))
    # ]

    # # Start and join read processes
    # for process in processes:
    #     process.start()
    # for process in processes:
    #     process.join()