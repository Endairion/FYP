# Contents of peer1.py
from node import Node

if __name__ == "__main__":
    node2 = Node('35.240.242.166')
    peer_socket = node2.connect_to_peer('34.143.221.135', 8000)
    if peer_socket:
        # Start a new thread to handle the peer connection
        node2.start_peer_thread()