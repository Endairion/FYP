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
            connection_thread.join()

    def handle_data(self, connection):
        # Receive and handle messages from connected peer
        while True:
            message = self.receive_message(connection)
            ip = connection.getpeername()[0]
            peer_socket = self.connect_to_peer(ip)

            if message is None:
                # Connection closed by peer
                break

            elif message['type'] == 'login':
                # Handle authentication message
                username = message['username']
                password = message['password']

                result = self.userCredentials.login(username, password)
                self.send_message(result, peer_socket)
                self.disconnect_from_peer(peer_socket)

            elif message['type'] == 'register':
                # Handle registration message
                username = message['username']
                password = message['password']

                result = self.userCredentials.register(username, password)
                self.send_message(result, peer_socket)
                self.disconnect_from_peer(peer_socket)


            elif message['type'] == 'data':
                # Handle data message
                print(f"Received message from {connection.getpeername()}: {message['data']}")

                # Send response back to sending peer
                response = {"type": "data", "data": "Hello, Peer!"}
                self.send_message(response, connection)
