# Contents of peer1.py
from node import Node
import threading

if __name__ == "__main__":
    # Create a Node instance for Peer 2 with a desired port
    peer2 = Node(12346)

    # Start listening for incoming connections and connecting to peers
    listener_and_connector_thread = threading.Thread(target=peer2.listen_and_connect)
    listener_and_connector_thread.start()