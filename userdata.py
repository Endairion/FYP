import time

class UserData:
    def __init__(self, user_id, username, hashed_password, email):
        self.user_id = user_id
        self.username = username
        self.hashed_password = hashed_password  # Store the hashed password
        self.email = email
        self.timestamp = time.time()  # A timestamp for when the user data was created

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'hashed_password': self.hashed_password,
            'email': self.email,
            'timestamp': self.timestamp
        }
    