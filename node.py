import json
import socket
import threading
import time
from DHT import DistributedHashTable
from UserCredential import UserCredentials

class Node:
    def __init__(self,ip):
        self.ip = ip
        self.port = 8000
        self.peers = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_peer(self, peer_ip, peer_port):
        try:
            socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_obj.connect((peer_ip, peer_port))
            print(f"Connected to {peer_ip}:{peer_port}")
            return socket_obj

        except Exception as e:
            print(f"Error in connect_to_peer: {str(e)}")
            return None

    def disconnect_from_peer(self, peer_ip, peer_port):
        try:
            self.socket.close()
            print(f"Disconnected from {peer_ip}:{peer_port}")
            return True

        except Exception as e:
            print(f"Error in disconnect_from_peer: {str(e)}")
            return False
        
    def start_peer_thread(self):
        peer_thread = threading.Thread(target=self.listen)
        peer_thread.start()
        while True:
            if self.listen():
                peer_thread.join()
                break

    def listen(self):
        try:
            internal_ip = self.get_internal_ip()
            self.socket.bind((internal_ip, self.port))
            self.socket.listen(1)

            print(f"Node listening for incoming connections on {internal_ip}:{self.port}")

            while True:
                relay_socket, client_address = self.socket.accept()
                print(f"Received connection from {client_address[0]}:{client_address[1]}")
                return True

        except Exception as e:
            print(f"Error in start: {str(e)}")

    @staticmethod
    def get_internal_ip():
        try:
            # Create a temporary socket object to retrieve the internal IP address
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.connect(("8.8.8.8", 80))
            internal_ip = temp_socket.getsockname()[0]
            temp_socket.close()
            return internal_ip

        except Exception as e:
            print(f"Error in get_internal_ip: {str(e)}")
            return None


    # def handle_client(self, conn):
    #     while True:
    #         data = conn.recv(1024)
    #         if not data:
    #             break
    #         message = json.loads(data.decode('utf-8'))
    #         print(f"Received message: {message}")
    #         self.broadcast(message)

    # def broadcast(self, message):
    #     encoded_message = json.dumps(message).encode('utf-8')
    #     for peer in self.peers:
    #         try:
    #             peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             peer_socket.connect(peer)
    #             peer_socket.send(encoded_message)
    #             peer_socket.close()
    #         except Exception as e:
    #             print(f"Error in broadcast: {str(e)}")

# class ClientNode(Node):
#     def __init__(self, dht):
#         super().__init__()
#         self.dht = dht

#     def get_relay_node(self):
#         relay_node = self.dht.get('relay_node')
#         if relay_node:
#             return relay_node['ip'], relay_node['port']
#         else:
#             return None

#     def send_file(self, file_path):
#         relay_node = self.get_relay_node()
#         if relay_node:
#             try:
#                 with open(file_path, 'rb') as f:
#                     file_data = f.read()

#                 message = {
#                     'type': 'file',
#                     'file_name': file_path.split('/')[-1],
#                     'file_data': file_data
#                 }

#                 peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 peer_socket.connect(relay_node)
#                 peer_socket.send(json.dumps(message).encode('utf-8'))
#                 peer_socket.close()

#             except Exception as e:
#                 print(f"Error in send_file: {str(e)}")
#         else:
#             print("Relay node not found in DHT")

class RelayNode(Node):
    def __init__(self):
        super().__init__(self.get_internal_ip())
        self.dht = DistributedHashTable()
        self.credentials = UserCredentials()

    def start(self):
        try:
            self.socket.bind((self.ip, self.port))
            self.socket.listen(5)

            print(f"Relay node listening for incoming connections on {self.ip}:{self.port}")

            while True:
                client_socket, client_address = self.socket.accept()
                print(f"Received connection from {client_address[0]}:{client_address[1]}")

                # Start a new thread to connect to the peer node
                t = threading.Thread(target=self.connect_to_peer, args=(client_address[0], self.port))
                t.start()

                while True:
                    if self.connect_to_peer is not None:
                        t.join()
                        break

        except Exception as e:
            print(f"Error in start: {str(e)}")


        except Exception as e:
            print(f"Error in connect_to_peer_and_authenticate: {str(e)}")

    def authenticate(self, client_socket):
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            client_socket.sendall(b"AUTHENTICATE\n")
            data = client_socket.recv(1024).decode().strip()

            if data != "READY":
                return False

            client_socket.sendall(b"1. LOGIN\n2. REGISTER\n")
            choice = client_socket.recv(1024).decode().strip()

            if choice == "1":
                client_socket.sendall(b"ENTER USERNAME:\n")
                username = client_socket.recv(1024).decode().strip()
                client_socket.sendall(b"ENTER PASSWORD:\n")
                password = client_socket.recv(1024).decode().strip()
                is_authenticated = self.credentials.login(username, password)
                if is_authenticated:
                    return username

            elif choice == "2":
                client_socket.sendall(b"ENTER USERNAME:\n")
                username = client_socket.recv(1024).decode().strip()
                client_socket.sendall(b"ENTER PASSWORD:\n")
                password = client_socket.recv(1024).decode().strip()
                is_registered = self.credentials.register(username, password)
                if is_registered:
                    return username

            attempts += 1
            time.sleep(5)

        return False
    
            
        
        
    
    # def handle_client(self, client_socket):
    #     try:
    #         request = client_socket.recv(1024).decode('utf-8')
    #         request = json.loads(request)

    #         if request['type'] == 'receive_file':
    #             file_name = request['file_name']
    #             file_data = request['file_data']

    #             # Process the file data and create a metadata object
    #             metadata = Metadata(file_name, file_data)

    #             # Fragment the file and distribute the fragments to the mining nodes
    #             fragments = fragment_file(file_data)
    #             for node_id in self.dht.getAll():
    #                 if node_id != self.dht.getSelfId():
    #                     node = self.dht.get(node_id)
    #                     message = {
    #                         'type': 'receive_fragment',
    #                         'file_name': file_name,
    #                         'fragment': fragments[node_id]
    #                     }
    #                     send_message(node, message)

    #             # Send the metadata to the mining node
    #             mining_node = self.dht.get('mining_node')
    #             if mining_node:
    #                 message = {
    #                     'type': 'receive_metadata',
    #                     'metadata': metadata.to_dict()
    #                 }
    #                 send_message(mining_node, message)

    #             else:
    #                 print("Mining node not found in DHT")

    #     except Exception as e:
    #         print(f"Error in handle_client: {str(e)}")

    #     finally:
    #         client_socket.close()