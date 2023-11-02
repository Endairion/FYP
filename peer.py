import threading
from node import Node

class Peer(Node):
    def __init__(self):
        super().__init__()
        self.relay_ip = '34.143.221.135'
        self.logged_in = False
        self.username = None
        self.thread = None
        self.thread_event = threading.Event()


    def start(self):
        # Bind the socket to the node's IP address and port number
        self.socket.bind((self.get_internal_ip(), self.port))

        # Start listening for incoming connections
        self.socket.listen()
    
        while True:
            try:
                connection, address = self.socket.accept()
                self.thread = threading.Thread(target=self.handle_data, args=(connection,))
                self.thread.start()
            except OSError:
                # Socket has been closed or deleted
                break
            
    def stop(self):
        # Set the socket object to None before closing it
        socket_to_close = self.socket
        self.socket = None

        # Close the bound socket and stop listening for incoming connections
        if socket_to_close is not None:
            socket_to_close.close()
        if self.thread is not None:
            self.thread.join()

    def login(self, username, password):
        # Connect to relay node
        relay_socket = self.connect_to_peer(self.relay_ip)

        if relay_socket is not None:
            # Send authentication message to relay node
            message = {"type": "login", "username": username, "password": password}
            self.send_message(message, relay_socket)
            # Receive response from relay node
            self.username = username
            print("Waiting for response")
            response = self.wait_for_response()
            self.disconnect_from_peer(relay_socket)
            return response

        else:
            # Connection to relay node failed
            return {"success": False, "message": "Could not connect to Relay Node."}
        
    def wait_for_response(self):
        # Wait for a response message from the relay node
        self.thread_event.clear()
        self.thread_event.wait()
        response = self.thread_event.data
        return response
        
    def register(self, username, password):
        # Connect to Relay Node
        relay_socket = self.connect_to_peer(self.relay_ip)

        if relay_socket is not None:
            # Send registration message to relay node
            message = {"type": "register", "username": username, "password": password}
            self.send_message(message, relay_socket)
            response = self.wait_for_response()
            self.disconnect_from_peer(relay_socket)
            return response
        else:
            return {"success": False, "message": "Could not connect to Relay Node."}
        
    def logout(self):
        # Connect to Relay Node
        relay_socket = self.connect_to_peer(self.relay_ip)

        if relay_socket is not None:
            # Send logout message to relay node
            message = {"type": "logout", "username": self.username}
            self.send_message(message, relay_socket)
            response = self.wait_for_response()
            self.disconnect_from_peer(relay_socket)
            return response
        else:
            return False

    def handle_data(self, connection):
        # Receive and handle messages from connected peer
        while True:
            message = self.receive_message(connection)

            if message is None:
                # Connection closed by peer
                break

            elif message['type'] == 'login':
                self.thread_event.data = message
                self.thread_event.set()

            elif message['type'] == 'register':
                self.thread_event.data = message
                self.thread_event.set()
            
            elif message['type'] == 'logout':
                # Handle logout response
                print(message['message'])
