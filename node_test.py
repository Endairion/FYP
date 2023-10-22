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
        self.connected_socket = []
        self.peers = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def initiate():
        pass
    
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
        peer_thread.join()

    def listen(self):
        try:
            internal_ip = self.get_internal_ip()
            self.socket.bind((internal_ip, self.port))
            self.socket.listen(1)

            print(f"Node listening for incoming connections on {internal_ip}:{self.port}")

            while True:
                relay_socket, client_address = self.socket.accept()
                print(f"Received connection from {client_address[0]}:{client_address[1]}")
                self.peers.append(relay_socket)
                break

        except Exception as e:
            print(f"Error in start: {str(e)}")


    def establish_two_way_connection(self, peer_ip, peer_port):
        # Connect to the peer
        peer_socket = self.connect_to_peer(peer_ip, peer_port)

        if peer_socket is not None:
            # Append the peer socket to the peers list
            self.peers.append(peer_socket)

            # Listen for incoming connections
            self.socket.listen(1)
            print(f"Node listening for incoming connections on {self.ip}:{self.port}")

            while True:
                relay_socket, client_address = self.socket.accept()
                print(f"Received connection from {client_address[0]}:{client_address[1]}")
                self.peers.append(relay_socket)

                # Start a new thread to handle incoming data from the peer
                t = threading.Thread(target=self.handle_peer_data, args=(peer_socket,))
                t.start()

            # Return the peer socket
            return peer_socket

        else:
            return None

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
                t.join()
                self.peers.append(client_socket)
                

        except Exception as e:
            print(f"Error in start: {str(e)}")

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