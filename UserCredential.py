import hashlib
from cryptography.fernet import Fernet
import json

class UserCredentials:
    def __init__(self):
        self.filename = 'uc.enc'
        self.encryption_key = b'HBh2b7Cqd_-9xzVrx_nCNg9rp6_TJGsbCI5CcpOWscI='
        self.credentials = {}

        try:
            with open(self.filename, "rb") as file:
                encrypted_data = file.read()
                decrypted_data = self.decrypt(encrypted_data)
                self.credentials = json.loads(decrypted_data)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save(self):
        encrypted_data = self.encrypt(json.dumps(self.credentials).encode())
        with open(self.filename, "wb") as file:
            file.write(encrypted_data)

    def register(self, username, password):
        hashed_username = self.hash(username)
        # Check if the username already exists
        if hashed_username in self.credentials:
            raise ValueError("Username already exists")

        hashed_password = self.hash(password)

        self.credentials[hashed_username] = hashed_password
        self.save()

    def login(self, username, password):
        hashed_username = self.hash(username)
        hashed_password = self.hash(password)

        if hashed_username in self.credentials and self.credentials[hashed_username] == hashed_password:
            return True
        else:
            return False

    def hash(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def encrypt(self, data):
        cipher_suite = Fernet(self.encryption_key)
        return cipher_suite.encrypt(data)

    def decrypt(self, data):
        cipher_suite = Fernet(self.encryption_key)
        return cipher_suite.decrypt(data)