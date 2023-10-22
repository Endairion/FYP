import threading
from node import Node

def connect_peer(node):
    node.connect_to_peer('34.143.221.135')  # Connect to Peer 2 on port 8002

if __name__ == "__main__":
    node = Node()  # Create a Node instance for Peer 1
    node.start()  # Start listening for incoming connections

    # Start a thread to handle the connection setup
    connection_thread = threading.Thread(target=connect_peer, args=(node,))
    connection_thread.start()

    input("Press Enter to interact with the program")

    # You can add your user interaction code here

    # Wait for the connection setup thread to complete (optional)
    connection_thread.join()
