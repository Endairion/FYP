# Contents of peer1.py
from node import Node

if __name__ == "__main__":
    node2 = Node()
    node2.ip = '0.0.0.0'  # set the IP address to the public IP of the machine
    node2.connect_to_peer('ip_address_of_node1', 8000)  # replace 'ip_address_of_node1' with the public IP of the first machine