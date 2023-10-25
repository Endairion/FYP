import threading
from node import Node

class Peer(Node):
    def __init__(self):
        super().__init__()
        self.relay_ip = '34.143.221.135'

    def start(self):
        # Bind the socket to the node's IP address and port number
        self.socket.bind((self.get_internal_ip(), self.port))

        # Start listening for incoming connections
        self.socket.listen()
    
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Received connection from {client_address[0]}:{client_address[1]}")
            connection_thread = threading.Thread(target=self.handle_data, args=(client_socket,))
            connection_thread.start()

    def login(self, username, password):
        # Connect to relay node
        relay_socket = self.connect_to_peer(self.relay_ip)

        if relay_socket is not None:
            # Send authentication message to relay node
            message = {"type": "login", "username": username, "password": password}
            self.send_message(message, relay_socket)

            # Receive response from relay node
            response = self.receive_message(relay_socket)

            # Close socket
            self.disconnect_from_peer(relay_socket)

            # Return authentication result
            return response['success']

        else:
            # Connection to relay node failed
            return False
        
    def register(self, username, password):
        # Connect to Relay Node
        relay_socket = self.connect_to_peer(self.relay_ip)

        if relay_socket is not None:
            # Send registration message to relay node
            message = {"type": "register", "username": username, "password": password}
            self.send_message(message, relay_socket)

    def handle_data(self, connection):
        # Receive and handle messages from connected peer
        while True:
            message = self.receive_message(connection)

            if message['type'] == 'login':
                # Handle authentication response
                print(message['message'])
                break

            elif message['type'] == 'register':
                # Handle registration response
                print(message['message'])
                break

            elif message['type'] == 'data':
                # Handle data message
                print(f"Received message from {connection.getpeername()}: {message['data']}")

                # Send response back to sending peer
                response = {"type": "data", "data": "Hello, Peer!"}
                self.send_message(response, connection)
            else:
                print("Invalid message type")
                break