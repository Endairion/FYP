import threading
from node import Node

def connect_peer(node):
    node.connect_to_peer('35.240.242.166')  # Connect to the other peer

if __name__ == "__main__":
    node2 = Node()
    node2.start()  # Start listening for incoming connections

    # Start a thread to handle the connection setup
    connection_thread = threading.Thread(target=connect_peer, args=(node2,))
    connection_thread.start()

    input("Press Enter to interact with the program")

    # You can add your user interaction code here

    # Wait for the connection setup thread to complete (optional)
    connection_thread.join()