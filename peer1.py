from node import RelayNode

def main():
    node1 = RelayNode()
    node1.ip = '10.148.0.4'  # set the IP address to the public IP of the machine
    node1.start()


if __name__ == "__main__":
    main()