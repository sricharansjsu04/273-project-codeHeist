# 273-project-codeHeist
## Implement MVCC for Python Pickle

Implementing Multi-Version Concurrency Control (MVCC) for Python objects serialized with pickle involves creating a system where each object can have multiple versions, each representing the state of the object at a different point in time. 

MVCC is a concurrency control method used to provide concurrent access to the database and to enhance performance by allowing transactions to use old snapshots of data.

# Code Details:

The code consists of three Python scripts which together implement a simple version of Multi-Version Concurrency Control (MVCC), a method used in database systems to achieve concurrency control.

<ul>
<li> <h3>my-node.py</h3>
This script defines a Node class representing a node in a distributed system or database cluster that can handle transactions and read operations using MVCC.

Node Class:
__init__(self, node_id, mvcc_lock, port): Initializes a new node instance.

**node_id**: Identifier for the node.
**mvcc_lock**: A multiprocessing lock to ensure thread-safe operations.
**port**: Network port the node operates on.
**mvcc_instance**: The MVCC instance associated with this node.
**load_mvcc_instance(self)**: Loads the MVCC instance from a file or creates a new one if the file doesn't exist.

**save_mvcc_instance(self)**: Saves the current state of the MVCC instance to a file.

**simulate_transaction(self, key, value)**: Simulates a transaction on the MVCC instance.

**key**: The key to write in the transaction.
**value**: The value to write in the transaction.
**simulate_read(self, key)**: Simulates a read operation from the MVCC instance.

key: The key to read.
log_message(self, action, message): Logs a message with a timestamp and action detail.

Main Execution Block:
It initializes two nodes and executes a series of write and read operations in separate processes.
</li>
<li><h3>picke-dump.py.py</h3>
This script demonstrates how to serialize (pickle) an instance of the MVCC class and save it to a file. This is useful for persisting the state of the MVCC instance.
  
</li>
  <li>
    <h3>mvcc.py</h3>
Defines the MVCC class, implementing the basic functionality of Multi-Version Concurrency Control.

MVCC Class:
__init__(self): Initializes the MVCC instance with an empty dictionary to store versioned data.

start_transaction(self): Starts a new transaction and returns a unique transaction ID based on the current timestamp.

write(self, key, value, transaction_id): Writes a value to a key under a specific transaction ID.

key: The key to write.
value: The value to write.
transaction_id: The ID of the transaction under which this write occurs.
commit_transaction(self, transaction_id, data): Commits a transaction.

transaction_id: The ID of the transaction to commit.
data: The data to commit under this transaction.
read(self, key, timestamp): Reads the value of a key as of a specific timestamp.

key: The key to read.
timestamp: The timestamp at which to read the key.
log_data(self, title, data): Logs the data in a structured table format.

title: Title for the log table.
data: The data to log.
General Observations:
The code demonstrates basic operations of an MVCC system, such as starting transactions, writing data, committing transactions, and reading data.
The use of multiprocessing and locks suggests an attempt to simulate a distributed environment.
Serialization with Pickle is used for persisting the state of the MVCC instance.
The code includes debugging prints and pretty-printed tables for visualizing operations, useful for understanding the flow of transactions and data changes.
    
  </li>
</ul>




# How to run:

<code>
Python3 pickle-dump.py
Python3 my-node.py
</code>




