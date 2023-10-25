import socket
import json
class Node:
    def __init__(self):
        self.ip = None
        self.port = 8000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

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

    def send_message(self, message, peer_socket):
        try:
            # Convert message dictionary to JSON string
            message_json = json.dumps(message)

            # Send JSON message to socket
            peer_socket.sendall(message_json.encode())

        except Exception as e:
            print(f"Error in send_message: {str(e)}")

    def receive_message(self, connection):
        # Receive JSON message from socket
        message_json = connection.recv(1024).decode()

        # Parse JSON message into dictionary object
        message = json.loads(message_json)

        # Return message dictionary
        return message

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