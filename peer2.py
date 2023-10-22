# Contents of peer1.py
from node import Node

if __name__ == "__main__":
    node2 = Node('35.240.242.166')
    internal_ip = node2.get_internal_ip()
    print(f"Internal IP: {internal_ip}")