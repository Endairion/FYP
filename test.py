import hashlib
from cryptography.fernet import Fernet
import json

# In-memory database for storing user information (username and hashed passwords)
user_database = {}

# File to store encrypted hashed user credentials
credentials_file = "user_credentials.encrypted"

# Encryption key (you should keep this key safe)
encryption_key = Fernet.generate_key()

# Initialize the Fernet cipher with the encryption key
cipher_suite = Fernet(encryption_key)

def load_credentials():
    try:
        with open(credentials_file, "rb") as file:
            encrypted_data = file.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            return json.loads(decrypted_data)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_credentials():
    encrypted_data = cipher_suite.encrypt(json.dumps(user_database).encode())
    with open(credentials_file, "wb") as file:
        file.write(encrypted_data)
def register():
    username = input("Enter your username: ")
    hashed_username = hashlib.sha256(username.encode()).hexdigest()
    # Check if the username already exists
    if hashed_username in user_database:
        print("Username already exists. Please choose a different username.")
        return
    
    password = input("Enter your password: ")
    
    # Hash the username and password before storing them

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    user_database[hashed_username] = hashed_password
    print("Registration successful!")

    # Save the updated user database to a file
    save_credentials()

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    hashed_username = hashlib.sha256(username.encode()).hexdigest()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if hashed_username in user_database and user_database[hashed_username] == hashed_password:
        print(f"Login successful! Welcome, {username}.")
    else:
        print("Incorrect username or password. Login failed.")

def main():
    global user_database
    user_database = load_credentials()

    while True:
        print("\nOptions:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()