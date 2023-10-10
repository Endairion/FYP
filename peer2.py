# Contents of peer1.py
from node import Node
import threading

if __name__ == "__main__":
    peer2 = Node(54321)

    server_thread = threading.Thread(target=peer2.listen_for_connections)
    server_thread.start()
    
    # Connect to peer1
    peer2.connect_to_peer('127.0.0.1', 12345)