import socket
import threading
class Node:
    def __init__(self):
        self.ip = None
        self.port = 8000
        self.peers = []
        self.connections = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        # Bind the socket to the node's IP address and port number
        self.socket.bind((self.get_internal_ip(), self.port))

        # Start listening for incoming connections
        self.socket.listen()
    
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Received connection from {client_address[0]}:{client_address[1]}")
            self.connections.append(client_socket)

    def connect_to_peer(self, peer_ip):
        try:
            socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_obj.connect((peer_ip, self.port))
            print(f"Connected to {peer_ip}:{self.port}")
            return socket_obj

        except Exception as e:
            print(f"Error in connect_to_peer: {str(e)}")
            return None

    def disconnect_from_peer(self, peer_socket):
        try:
            peer_socket.shutdown(socket.SHUT_RDWR)
            peer_socket.close()
            print(f"Disconnected from {peer_socket.getpeername()}")

        except Exception as e:
            print(f"Error in disconnect_from_peer: {str(e)}")

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