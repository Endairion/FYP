# Contents of peer1.py
from node import Node

if __name__ == "__main__":
    node2 = Node()
    node2.ip = '34.143.221.135'  # set the IP address to the public IP of the machine
    node2.connect_to_peer('35.240.242.166', 8000)  # replace 'ip_address_of_node1' with the public IP of the first machine