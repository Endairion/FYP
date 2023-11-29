import hashlib
import json
import threading
import base64
import time
import uuid
from block import Block
from blockchain import Blockchain
from fragment import Fragment
from metadata import FileMetadata
from node import Node
from UserCredential import UserCredentials
from DHT import DistributedHashTable

class RelayNode(Node):
    def __init__(self):
        super().__init__()
        self.users = {}
        self.userCredentials = UserCredentials()
        self.dht = DistributedHashTable()
        self.thread = None
        self.thread_event = threading.Event()

    def start(self):
        # Bind the socket to the node's IP address and port number
        self.socket.bind((self.get_internal_ip(), self.port))

        # Start listening for incoming connections
        self.socket.listen()
    
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Received connection from {client_address[0]}:{client_address[1]}")

            # Start a thread to handle the connection
            print("Starting thread to handle connection.")
            self.thread = threading.Thread(target=self.handle_data, args=(client_socket,))
            self.thread.start()

    def wait_for_response(self):
        # Wait for a response message from the relay node
        self.thread_event.clear()
        self.thread_event.wait()
        response = self.thread_event.data

        return response
    
    def handle_data(self, connection):
        # Receive and handle messages from connected peer
        while True:
            message = self.receive_message(connection)
            ip = connection.getpeername()[0]
            peer_socket = self.connect_to_peer(ip)
            print("Received message:", message)

            if message is None:
                # Connection closed by peer
                break

            elif message['type'] == 'login':
                # Handle authentication message
                username = message['username']
                password = message['password']

                if self.dht.search(username):
                    print("Someone is already logged in to the account.")
                    result = {'success': False, 'message': 'Someone is already logged in to the account.'}
                else:
                    result = self.userCredentials.login(username, password)

                self.send_message(result, peer_socket)
                if result['success']:
                    print("Login successful for", username)
                    self.dht.put(username, ip)
                else:
                    print(result['message'])
                

            elif message['type'] == 'register':
                # Handle registration message
                username = message['username']
                password = message['password']

                result = self.userCredentials.register(username, password)
                self.send_message(result, peer_socket)
                if result['success']:
                    print("Registration successful for ", username)
                    print("Credentials added into DHT")
                else:
                    print(result['message'])

            elif message['type'] == 'logout':
                # Handle logout message
                username = message['username']

                result = self.dht.delete(username)
                if result['success']:
                    print("Logout successful for ", username)
                    result = {"type": "logout", "success": True, "message": "Logout successful"}
                else:
                    print(result['message'])
                    result = {"type": "logout", "success": False, "message": "Logout unsuccessful"}

                self.send_message(result, peer_socket)

            elif message['type'] == 'upload_start':
                # Prepare for file upload
                self.file_size = message['file_size']
                self.file_name = message['file_name']
                self.sender = message['username']
                self.file_data = b''

                print("Received 'upload_start' message from peer:", message)
                print("Prepared for file upload. File size:", self.file_size, "File name:", self.file_name, "Sender:", self.sender)

                # Start handling the upload
                self.handle_upload(peer_socket)

            elif message['type'] == 'update_blockchain':
                self.send_blockchain(peer_socket)

            elif message['type'] == 'download':
                file_data, file_metadata = self.assemble_file(message['file_id'])

                filename = file_metadata.filename
                file_size = file_metadata.file_size
                # Send the file data to the client
                self.upload(file_data, filename, file_size, peer_socket)
            elif message['type'] == 'upload_chunk':
                self.receive_chunks(message, peer_socket)
            elif message['type'] == 'upload_end':
                metadata, fragment_data_list = self.fragment_file(self.file_data)
                print("Fragmented file data.")
                print("Metadata:", metadata)
                print("Fragment data list:", fragment_data_list)
                self.distribute_file(metadata, fragment_data_list)
                self.add_to_blockchain(metadata)
            elif message['type'] == 'fragment_received_confirmation':
                self.thread_event.data = message
                self.thread_event.set()
        

            

    def upload(self, file_data, filename, file_size, peer_socket):
        initial_message = {"type": "upload_start", "filename": filename, "file_size": file_size}
        self.send_message(initial_message, peer_socket)

        if peer_socket is not None:
            # Get file size
            initial_message = {"type": "upload_start", "file_size": file_size, "file_name": filename}
            start = 0
            chunk_size = 1024  # Size of each chunk in bytes
            while start < len(file_data):
                # Get the next chunk of file data
                chunk = file_data[start : start + chunk_size]

                # Convert file chunk to base64 string
                chunk_b64 = base64.b64encode(chunk).decode()

                # Send upload message to peer with file data chunk
                message = {"type": "upload_chunk", "file_data": chunk_b64}
                self.send_message(message, peer_socket)

                # Move to the next chunk
                start += chunk_size

            response = self.wait_for_response()
            return response
        else:
            return {"success": False, "message": "Could not connect to Peer Node."}

    def receive_chunks(self, message, peer_socket):
            print("Waiting for more file data...")
            print("Received message:", message)

            if message['type'] == 'upload_chunk':
                # Append received chunk to file data
                self.file_data += base64.b64decode(message['file_data'])
                print("Received file chunk, current file data length:", len(self.file_data))
                self.send_message({"type":"chunk_received","success": True}, peer_socket)
                print("Sent confirmation to peer.")

    def handle_upload(self, peer_socket):
        print("Started handling the upload.")
        confirmation = {"type": "upload_start_confirmation","success": True}
        time.sleep(1)
        self.send_message(confirmation, peer_socket)
        print("Sent confirmation to client.")
    

        # # Check if all chunks have been received
        # if len(self.file_data) == self.file_size:
        #     print("All file chunks received.")

        #     # Send response to client
        #     result = {"type": "upload_complete", "success": True, "message": "File upload successful"}
        #     self.send_message(result, peer_socket)
        #     print("Sent upload complete message to client.")

        #     # Process file data for distribution
        #     metadata, fragment_data_list = self.fragment_file(self.file_data)
        #     print("Fragmented file data.")

        #     self.distribute_file(metadata, fragment_data_list)
        #     print("Distributed file fragments.")

        #     self.add_to_blockchain(metadata)
        #     print("Added file metadata to blockchain.")
        # else:
        #     print("Not all file chunks received.")

        #     # Send error response to client
        #     result = {"type": "upload_error", "success": False, "message": "File upload unsuccessful, not all chunks received"}
        #     self.send_message(result, peer_socket)
        #     print("Sent upload error message to client.")

        # # Reset file data
        # self.file_data = b''
        # self.file_size = 0
        # self.file_name = None
        # self.sender = None
        # print("Reset file data.")

    def assemble_file(self, file_id):
        # Load the blockchain
        blockchain = Blockchain.load_from_file('blockchain.pkl')

        file_list = blockchain.extract_file_info()

        # Find the FileMetadata with the given file_id
        for file_metadata in file_list:
            if file_metadata.file_id == file_id:
                break
        else:
            raise ValueError(f"No FileMetadata found with file_id {file_id}")

        # Get the list of all nodes except the sender
        fragment_hashes = file_metadata.fragment_hashes
        sender = file_metadata.sender
        nodes = self.dht.get_all_except_sender(sender)

        # Retrieve the fragments from the nodes
        fragments = []
        for node in nodes:
            for fragment_hash in fragment_hashes:
                # Send a request message to the node with the fragment hash
                self.send_request(node, fragment_hash)

                # Receive the fragment from the node
                fragment = self.receive_fragment(node)

                # If the fragment is found, add it to the fragments list and break the loop
                if fragment is not None:
                    fragments.append(fragment)
                    break

        # Assemble the fragments in the order of their hashes in fragment_hashes
        fragments = sorted(fragments, key=lambda fragment: fragment_hashes.index(fragment.hash))

        # Join the fragments to get the file data
        file_data = b''.join(fragment.data for fragment in fragments)

        return file_data, file_metadata

    def fragment_file(self, file_data):
        file_id = str(uuid.uuid4())
        num_fragments = 3
        fragment_size = (len(file_data) + num_fragments - 1) // num_fragments
        fragment_hashes = []
        fragment_data_list = []
        file_hash = hashlib.sha256()
        for i in range(num_fragments):
            start = i * fragment_size
            end = (i + 1) * fragment_size if i != num_fragments - 1 else len(file_data)
            fragment_data = file_data[start:end]
            fragment_hash = hashlib.sha256(fragment_data).hexdigest()
            fragment_hashes.append(fragment_hash)
            fragment_data_list.append(fragment_data)
            file_hash.update(fragment_data)
        fragments = Fragment(fragment_hashes, num_fragments)
        file_metadata = FileMetadata(file_id, self.file_name, self.file_size, fragments, self.sender, file_hash.hexdigest())
        return file_metadata, fragment_data_list
    
    def distribute_file(self, metadata, fragment_data_list):
        # Get the list of IPs
        IPList = self.dht.get_all_except_sender(self.sender)

        # Get the fragment hashes from the metadata
        fragment_hashes = metadata.fragments.fragment_hashes

        # Distribute the fragments to the IPs
        for ip, fragment_data, fragment_hash in zip(IPList, fragment_data_list, fragment_hashes):
            # Send the fragment and its hash to the IP
            self.send_fragment(ip, fragment_data, fragment_hash)

    def send_fragment(self, ip, fragment_data, fragment_hash):
        # Split the fragment data into chunks
        chunk_size = 512 
        chunks = [fragment_data[i:i+chunk_size] for i in range(0, len(fragment_data), chunk_size)]
        print(f"Split fragment into {len(chunks)} chunks of size {chunk_size} bytes.")

        peer = self.connect_to_peer(ip)
        print(f"Connected to peer at {ip}.")

        # Send each chunk to the peer
        for i, chunk in enumerate(chunks):
            # Create a message with the chunk data
            fragment_data_base64 = base64.b64encode(chunk).decode()
            print(f"Sending chunk {i+1} of {len(chunks)} (size: {len(chunk)} bytes).")
            message = {
                'type': 'receive_fragment',
                'fragment_data': fragment_data_base64,
            }

            # Send the message to the IP
            self.send_message(message, peer)
            print(f"Sent chunk {i+1} of {len(chunks)} to relay node.")
            response = self.wait_for_response()
            if response is not None:
                continue


        # Send an 'upload_end' message to the relay node
        end_message = {"type": "fragment_end", "fragment_hash": fragment_hash}
        self.send_message(end_message, peer)
        print("Sent 'fragment_end' message to relay node.")


    def add_to_blockchain(self, metadata):
        # Load the blockchain from the file
        self.blockchain = Blockchain.load_from_file('blockchain.pkl')

        # Check if the blockchain is empty or doesn't exist
        if self.blockchain is None or len(self.blockchain.chain) == 0:
            # If the blockchain is empty or doesn't exist, create a new blockchain and a genesis block
            self.blockchain = Blockchain()
            genesis_block = self.blockchain.createGenesisBlock()
            self.blockchain.addBlock(genesis_block)

        # Convert the metadata to a dictionary
        metadata_dict = metadata.to_dict()

        timestamp = time.time()

        # Create a new block with the metadata
        new_block = Block(timestamp, metadata_dict)

        # Add the new block to the blockchain
        self.blockchain.addBlock(new_block)

        # Save the blockchain to the file
        self.blockchain.save_to_file('blockchain.pkl')

        # Distribute the blockchain to all online nodes
        self.distribute_blockchain()

    def distribute_blockchain(self):
        # Get the list of IPs
        IPList = self.dht.get_all()

        # Distribute the blockchain to the IPs
        for ip in IPList:
            # Send the blockchain to the IP
            self.send_blockchain(ip)

    def send_blockchain(self, ip):
        # Read the blockchain data
        with open('blockchain.pkl', 'rb') as file:
            blockchain_data = file.read()

        # Split the blockchain data into chunks
        chunk_size = 512  # Set chunk size to 512 bytes
        chunks = [blockchain_data[i:i+chunk_size] for i in range(0, len(blockchain_data), chunk_size)]

        peer = self.connect_to_peer(ip)

        # Send each chunk to the peer
        for i, chunk in enumerate(chunks):
            # Convert the chunk data to base64
            chunk_data_base64 = base64.b64encode(chunk).decode()

            # Create a message with the chunk data
            message = {
                'type': 'blockchain_chunk',
                'chunk_data': chunk_data_base64,
            }

            # Send the message to the IP
            self.send_message(message, peer)

    def update_blockchain(self, socket):
        # Read the blockchain data
        with open('blockchain.pkl', 'rb') as file:
            blockchain_data = file.read()

        # Split the blockchain data into chunks
        chunk_size = 512  # Set chunk size to 512 bytes
        chunks = [blockchain_data[i:i+chunk_size] for i in range(0, len(blockchain_data), chunk_size)]

        # Send each chunk to the socket
        for i, chunk in enumerate(chunks):
            # Convert the chunk data to base64
            chunk_data_base64 = base64.b64encode(chunk).decode()

            # Create a message with the chunk data
            message = {
                'type': 'blockchain_chunk',
                'chunk_data': chunk_data_base64,
            }

            # Send the message to the socket
            self.send_message(message, socket)



    

