import threading
import time
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
        self.fragment_data = b''
        self.blockchain_data = b''


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
                    self.handle_blockchain(message, connection)
                elif message['type'] == 'update_blockchain':
                    self.thread_event.data = message
                    self.thread_event.set()
                elif message['type'] == 'upload_start_confirmation':
                    self.thread_event.data = message
                    self.thread_event.set()
                elif message['type'] == 'chunk_received':
                    self.thread_event.data = message
                    self.thread_event.set()
                elif message['type'] == 'receive_fragment':
                    self.receive_fragment(message, connection)
                elif message['type'] == 'fragment_end':
                    self.save_fragment(message)
                elif message['type'] == 'blockchain_end':
                    self.save_blockchain()
                
                
    def save_fragment(self, message):
        # Ensure the 'fragments' directory exists
        if not os.path.exists('fragments'):
            os.makedirs('fragments')

        # Save the fragment data to a file in the 'fragments' directory
        with open(os.path.join('fragments', message['fragment_hash']), 'wb') as file:
            file.write(self.fragment_data)

        # Reset the fragment data
        self.fragment_data = b''

    def receive_fragment(self, message, connection):
        # Decode the fragment data
        self.fragment_data += base64.b64decode(message['fragment_data'])
        print(f"Received fragment, current fragment data length: {len(self.fragment_data)}")

        # Create a confirmation message
        confirmation_message = {
            'type': 'fragment_received_confirmation',
        }

        # Sleep for 1 second
        time.sleep(1)
        ip = connection.getpeername()[0]
        peer_socket = self.connect_to_peer(ip)

        # Send the confirmation message back to the sender
        self.send_message(confirmation_message, peer_socket)
        print(f"Sent confirmation to {ip} for received fragment.")


    def handle_blockchain(self, message, connection):
        # Decode the base64 data back into binary data
        self.blockchain_data += base64.b64decode(message['chunk_data'])
        print(f"Received blockchain chunk, current blockchain data length: {len(self.blockchain_data)}")
        print(self.blockchain_data)
        time.sleep(1)
        ip = connection.getpeername()[0]
        peer_socket = self.connect_to_peer(ip)

        # Create a confirmation message
        confirmation_message = {
            'type': 'blockchain_received_confirmation',
        }

        # Send the confirmation message back to the sender
        self.send_message(confirmation_message, peer_socket)
        print(f"Sent confirmation to {ip} for received fragment.")

    def update_blockchain(self):
        # Connect to Relay Node
        relay_socket = self.connect_to_peer(self.relay_ip)

        if relay_socket is not None:
            # Send blockchain request to relay node
            message = {"type": "update_blockchain"}
            self.send_message(message, relay_socket)
        else:
            return {"success": False, "message": "Could not connect to Relay Node."}

    def save_blockchain(self):
        # Create a new Blockchain object
        blockchain = Blockchain()

        # Set the chain of the Blockchain object to the blockchain_data
        blockchain.chain = self.blockchain_data

        # Save the Blockchain object to 'blockchain.pkl'
        blockchain.save_to_file('blockchain.pkl')

        # Reset the blockchain data
        self.blockchain_data = b''

                    

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
            chunk_size = 512
            chunks = [file_data[i:i+chunk_size] for i in range(0, len(file_data), chunk_size)]

            # Send each chunk to the relay node
            for i, chunk in enumerate(chunks):
                base64_string = base64.b64encode(chunk).decode()
                print(f"Sending chunk {i+1} of {len(chunks)} (size: {len(chunk)} bytes)")

                chunk_message = {"type": "upload_chunk", "file_data": base64_string}
                self.send_message(chunk_message, relay_socket)
                print(f"Sent chunk {i+1} of {len(chunks)} to relay node.")
                received = self.wait_for_response()
                if received is not None:
                    continue

            # Send an 'upload_end' message to the relay node
            end_message = {"type": "upload_end"}
            self.send_message(end_message, relay_socket)
            print("Sent 'upload_end' message to relay node.")
