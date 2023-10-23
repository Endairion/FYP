import threading
import json
from node import Node

def start_node(node):
    node.start()

def connect_peer(node):
    node.connect_to_peer('34.143.221.135')  # Connect to the other peer

def handle_login(sock):
    # Prompt user for username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Create dictionary object with user credentials
    credentials = {"username": username, "password": password}

    # Serialize dictionary object into JSON string
    credentials_json = json.dumps(credentials)

    # Create dictionary object with message type and JSON string
    message = {"type": "credentials", "data": credentials_json}

    # Serialize dictionary object into JSON string
    message_json = json.dumps(message)

    # Send JSON string to relay node using existing socket connection
    sock.sendall(message_json.encode())

if __name__ == "__main__":
    node = Node()

    # Start a thread for node2's start method
    node_thread = threading.Thread(target=start_node, args=(node,))
    node_thread.start()

    input("Press Enter to connect")

    # Start a thread to handle the connection setup
    relay_node_socket = connect_peer(node)

    handle_login(relay_node_socket)

    # You can add your user interaction code here

    # Wait for both threads to complete (optional)
    node_thread.join()


