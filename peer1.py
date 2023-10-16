from node import Node

def main():
    node_ip = "NODE1_IP"  # Replace with the actual IP address of node1
    node_port = 8080  # Change to the port node1 is listening on

    peer1 = Node()
    peer1.connect_to_peer(node_ip, node_port)

if __name__ == "__main__":
    main()
