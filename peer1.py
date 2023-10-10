# Contents of peer1.py
from node import Node
import threading

if __name__ == "__main__":
    peer1 = Node(12345)

    server_thread = threading.Thread(target=peer1.listen_for_connections)
    server_thread.start()
    
    # Connect to peer1
    peer1.connect_to_peer('127.0.0.1', 54321)