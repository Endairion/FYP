from node import Node

def main():
    node1 = Node()
    node1.ip = '10.148.0.3'  # set the IP address to the public IP of the machine
    node1.listen_and_connect()


if __name__ == "__main__":
    main()
