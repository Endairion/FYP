import socket
import threading

class Node:
    def __init__(self, port):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        self.peers = []

    def listen_for_connections(self):
        print(f"Listening for incoming connections on port {self.port}...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received: {message}")
                # You can add message handling logic here

        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            client_socket.close()

    def connect_to_peer(self, peer_ip, peer_port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer_ip, peer_port))

        print(f"Connected to {peer_ip}:{peer_port}")

        # Start a thread to send messages
        send_thread = threading.Thread(target=self.send_messages, args=(client_socket,))
        send_thread.start()

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received: {message}")
                # You can add message handling logic here

        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            client_socket.close()

    def send_messages(self, client_socket):
        try:
            while True:
                message = input("Enter your message: ")
                client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {str(e)}")
