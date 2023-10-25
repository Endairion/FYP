import threading
import json
from UserCredential import UserCredentials
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


def handle_message(sock):
    # Receive JSON message from Peer1
    message_json = sock.recv(1024).decode()

    # Parse JSON message into dictionary object
    message = json.loads(message_json)

    # Extract user credentials from message
    credentials_json = message['data']
    credentials = json.loads(credentials_json)

    # Validate user credentials using UserCredentials class
    user_credentials = UserCredentials()
    is_valid = user_credentials.login(credentials['username'], credentials['password'])

    # Send response back to Peer1 indicating whether the login was successful
    response = {"type": "login_response", "data": {"success": is_valid}}
    response_json = json.dumps(response)
    sock.sendall(response_json.encode())