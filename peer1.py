from node import Node

if __name__ == "__main__":
    node = Node()  # Create a Node instance for Peer 1
    node.start()  # Start listening for incoming connections
    
    input("Press Enter to connect")
    node.connect_to_peer('34.143.221.135')  # Connect to Peer 2 on port 8002