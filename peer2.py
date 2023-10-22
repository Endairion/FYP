import threading
from node import Node

def start_node(node):
    node.start()

def connect_peer(node):
    node.connect_to_peer('35.240.242.166')  # Connect to the other peer

if __name__ == "__main__":
    node2 = Node()

    # Start a thread for node2's start method
    node_thread = threading.Thread(target=start_node, args=(node2,))
    node_thread.start()

    input("Press Enter to connect")

    # Start a thread to handle the connection setup
    connection_thread = threading.Thread(target=connect_peer, args=(node2,))
    connection_thread.start()

    # You can add your user interaction code here

    # Wait for both threads to complete (optional)
    node_thread.join()
    connection_thread.join()
