import threading
import json
from peer import Peer

def start_node(node):
    node.start()

def handle_authentication():
    # Prompt user to choose between login and register
    while not node.logged_in:
        choice = input("Enter '1' to login or '2' to register: ")
        if choice == '1':
            # Prompt user for username and password
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            node.login(username, password)
        elif choice == '2':
            # Prompt user to register a new account
            username = input("Enter a new username: ")
            password = input("Enter a new password: ")

            node.register(username, password)
        elif choice == 'exit':
            # Exit the loop
            break
        else:
            print("Invalid choice. Please enter '1' to login or '2' to register.")
    

if __name__ == "__main__":
    node = Peer()

    # Start a thread for node2's start method
    node_thread = threading.Thread(target=start_node, args=(node,))
    node_thread.start()

    input("Press Enter to Authenticate")

    handle_authentication()

    if node.logged_in:
        print("Successfully logged in as", node.username)

    # You can add your user interaction code here

    # Wait for both threads to complete (optional)
    node_thread.join()


