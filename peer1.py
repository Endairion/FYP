import threading
import json
from peer import Peer

def start_node(node):
    node.start()

def handle_login():
    # Prompt user for username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    node.login(username, password)
    

if __name__ == "__main__":
    node = Peer()

    # Start a thread for node2's start method
    node_thread = threading.Thread(target=start_node, args=(node,))
    node_thread.start()

    input("Press Enter to Login")

    handle_login()

    # You can add your user interaction code here

    # Wait for both threads to complete (optional)
    node_thread.join()


