# Contents of peer1.py
from node import Node

if __name__ == "__main__":
    node2 = Node('35.240.242.166')
    node2.connect_to_peer('34.143.221.135', 8000)  # replace 'ip_address_of_node1' with the public IP of the first machine