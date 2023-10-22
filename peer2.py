from node import Node

if __name__ == "__main__":
    node2 = Node()
    node2.start()

    input("Press Enter to connect")
    node2.connect_to_peer('35.240.242.166')
