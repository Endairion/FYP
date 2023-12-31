import threading
import json
from UserCredential import UserCredentials
from relay import RelayNode

def start_node(node):
    node.start()


if __name__ == "__main__":
    node2 = RelayNode()

    # Start a thread for node2's start method
    node_thread = threading.Thread(target=start_node, args=(node2,))
    node_thread.start()
    node_thread.join()
