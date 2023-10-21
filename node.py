import json
import socket
import threading
from DHT import DistributedHashTable

class Node:
    def __init__(self):
        self.ip = None
        self.port = 8000
        self.peers = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_peer(self, peer_ip, peer_port):
        try:
            self.socket.connect((peer_ip, peer_port))
            print(f"Connected to {peer_ip}:{peer_port}")
            self.peers.append((peer_ip, peer_port))
            return True

        except Exception as e:
            print(f"Error in connect_to_peer: {str(e)}")
            return False

    def disconnect_from_peer(self, peer_ip, peer_port):
        try:
            self.socket.close()
            self.peers.remove((peer_ip, peer_port))
            print(f"Disconnected from {peer_ip}:{peer_port}")
            return True

        except Exception as e:
            print(f"Error in disconnect_from_peer: {str(e)}")
            return False

    def handle_client(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = json.loads(data.decode('utf-8'))
            print(f"Received message: {message}")
            self.broadcast(message)

    def broadcast(self, message):
        encoded_message = json.dumps(message).encode('utf-8')
        for peer in self.peers:
            try:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.connect(peer)
                peer_socket.send(encoded_message)
                peer_socket.close()
            except Exception as e:
                print(f"Error in broadcast: {str(e)}")

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
    def __init__(self, ip):
        super().__init__(ip)
        self.dht = DistributedHashTable()

    def start(self):
        try:
            self.socket.bind((self.ip, self.port))
            self.socket.listen(5)

            print(f"Relay node listening for incoming connections on {self.ip}:{self.port}")

            while True:
                client_socket, client_address = self.socket.accept()
                print(f"Received connection from {client_address[0]}:{client_address[1]}")
                self.dht.put("IP",client_address[0])

        except Exception as e:
            print(f"Error in start: {str(e)}")

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