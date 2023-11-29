import threading
import json
from peer import Peer

def start_node(node):
    node.start()
    
if __name__ == "__main__":
    node = Peer()

    # Start a thread for node's start method
    node_thread = threading.Thread(target=start_node, args=(node,))
    node_thread.start()

    while not node.logged_in:
        choice = input("Enter '1' to login or '2' to register: ")
        if choice == '1':
            # Prompt user for username and password
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            response = node.login(username, password)
            if response["success"]:
                # Login successful
                node.logged_in = True
                break

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

    if node.logged_in:
        print("Successfully logged in as", node.username)

    # Wait for both threads to complete (optional)
    node_thread.join()


