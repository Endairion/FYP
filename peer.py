import threading
from blockchain import Blockchain
from node import Node
import base64
import os

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
            elif 'type' in message:
                if message['type'] == 'login':
                    self.thread_event.data = message
                    self.thread_event.set()
                elif message['type'] == 'register':
                    self.thread_event.data = message
                    self.thread_event.set()
                elif message['type'] == 'logout':
                    # Handle logout response
                    self.thread_event.data = message
                    self.thread_event.set()
                elif message['type'] == 'fragment':
                    # Handle download fragment from relay node
                    self.handle_fragment(message)
                elif message['type'] == 'blockchain':
                    self.handle_blockchain(message)
                elif message['type'] == 'update_blockchain':
                    self.thread_event.data = message
                    self.thread_event.set()
                elif message['type'] == 'upload_start_confirmation':
                    self.thread_event.data = message
                    self.thread_event.set()
                
            

    def handle_fragment(self, message):
        # Decode the fragment data
        fragment_data = base64.b64decode(message['fragment_data'])

        # Extract the fragment hash from the message
        fragment_hash = message['fragment_hash']

        # Use the fragment hash as the filename
        fragment_filename = os.path.join('fragments', fragment_hash)

        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(fragment_filename), exist_ok=True)

        # Write the fragment data to a file
        with open(fragment_filename, 'wb') as f:
            f.write(fragment_data)

    def handle_blockchain(self, message):
        # Decode the base64 data back into binary data
        blockchain_data = base64.b64decode(message['blockchain_data'])

        # Write the binary data to a file
        with open('blockchain.pkl', 'wb') as file:
            file.write(blockchain_data)

    def update_blockchain(self):
        # Connect to Relay Node
        relay_socket = self.connect_to_peer(self.relay_ip)

        if relay_socket is not None:
            # Send blockchain request to relay node
            message = {"type": "update_blockchain"}
            self.send_message(message, relay_socket)
        else:
            return {"success": False, "message": "Could not connect to Relay Node."}

                    

    def upload(self, file_path):
        # Connect to Relay Node
        relay_socket = self.connect_to_peer(self.relay_ip)

        if relay_socket is not None:
            # Get file size
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)

            # Send initial message to relay node
            initial_message = {"type": "upload_start", "username": self.username, "file_size": file_size, "file_name": file_name}
            self.send_message(initial_message, relay_socket)
            print("Sent initial upload message to relay node:", initial_message)

            # Wait for confirmation from relay node
            print("Waiting for confirmation from relay node...")
            confirmation = self.wait_for_response()
            print("Received confirmation from relay node:", confirmation)

            if not confirmation.get('success'):
                print("Failed to start upload.")
                return {"success": False, "message": "Failed to start upload."}

            # Open the file and read its data
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Split the file data into chunks
            chunks = [file_data[i:i+1024] for i in range(0, len(file_data), 1024)]

            # Send each chunk to the relay node
            for i, chunk in enumerate(chunks):
                chunk_message = {"type": "upload_chunk", "file_data": base64.b64encode(chunk).decode()}
                self.send_message(chunk_message, relay_socket)
                print(f"Sent chunk {i+1} of {len(chunks)} to relay node.")

            # Send an 'upload_end' message to the relay node
            end_message = {"type": "upload_end"}
            self.send_message(end_message, relay_socket)
            print("Sent 'upload_end' message to relay node.")
