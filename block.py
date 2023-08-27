import hashlib

def SHA256(message):
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

class Block:
    def __init__(self, timestamp, data):
        self.index = 0
        self.timestamp = timestamp
        self.data = data
        self.lastHash = ''
        self.nonce = 0
        self.hash = self.getHash()

    def getHash(self):
        return SHA256(
            str(self.data) + str(self.timestamp) + str(self.lastHash) + str(self.nonce)
        )

    def mineBlock(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.getHash()

    def __str__(self):
        return (
            f"Block {self.index}:\n"
            f"Timestamp: {self.timestamp}\n"
            f"Data: {self.data}\n"
            f"Last Hash: {self.lastHash}\n"
            f"Nonce: {self.nonce}\n"
            f"Hash: {self.hash}\n"
        )
