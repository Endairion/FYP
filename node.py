import upnpy
import socket
import threading

class Node:
    def __init__(self):
        self.ip = None
        self.upnp = upnpy.UPnP()
        self.configure_upnp_port_forwarding()

    def configure_upnp_port_forwarding(self):
        try:
            devices = self.upnp.discover()
            print(f'Discovering UPnP port...')
            device = self.upnp.get_igd()
            device.get_services()
            
            
            external_port = 81  # Replace with the desired external port
            internal_port = 8081  # Replace with the port your node is listening on
            protocol = "TCP"

            service.AddPortMapping.get_input_arguments()

        except Exception as e:
            print(f"Exception:", e)

    def connect_to_peer(self, peer_ip, peer_port):
        try:
            self.socket.connect((peer_ip, peer_port))
            print(f"Connected to {peer_ip}:{peer_port}")

            while True:
                message = input("Enter your message: ")
                if message == "exit":
                    break
                self.socket.send(message.encode('utf-8'))

            self.socket.close()

        except Exception as e:
            print(f"Error in connect_to_peer: {str(e)}")

    def listen_and_connect(self):
        try:
            self.socket.bind((self.ip, self.port))
            self.socket.listen(5)

            print(f"Listening for incoming connections on {self.ip}:{self.port}")

            while True:
                client_socket, client_address = self.socket.accept()
                print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()

        except Exception as e:
            print(f"Error in listen_and_connect: {str(e)}")

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received: {message}")
                # Implement your message handling logic here

        except Exception as e:
            print(f"Error in handle_client: {str(e)}")
        finally:
            client_socket.close()
