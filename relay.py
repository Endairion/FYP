import json
import threading
from node import Node
from UserCredential import UserCredentials

class RelayNode(Node):
    def __init__(self):
        super().__init__()
        self.users = {}
        self.userCredentials = UserCredentials()

    def start(self):
        # Bind the socket to the node's IP address and port number
        self.socket.bind((self.get_internal_ip(), self.port))

        # Start listening for incoming connections
        self.socket.listen()
    
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Received connection from {client_address[0]}:{client_address[1]}")

            # Start a thread to handle the connection
            connection_thread = threading.Thread(target=self.handle_data, args=(client_socket,))
            connection_thread.start()

    def handle_data(self, connection):
        # Receive and handle messages from connected peer
        while True:
            message = self.receive_message(connection)

            if message['type'] == 'login':
                # Handle authentication message
                username = message['username']
                password = message['password']

                result = self.userCredentials.login(username, password)

                return result
        
            elif message['type'] == 'register':
                # Handle registration message
                username = message['username']
                password = message['password']

                result = self.userCredentials.register(username, password)

                return result

            elif message['type'] == 'data':
                # Handle data message
                print(f"Received message from {connection.getpeername()}: {message['data']}")

                # Send response back to sending peer
                response = {"type": "data", "data": "Hello, Peer!"}
                self.send_message(response, connection)

            # Add more message types and handling code here

    def add_user(self, username, password):
        self.users[username] = password

    def remove_user(self, username):
        if username in self.users:
            del self.users[username]