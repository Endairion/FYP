import hashlib
from metadata import Metadata

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
        data_string = ''.join(str(metadata) for metadata in self.data)
        return SHA256(
            data_string + str(self.timestamp) + str(self.lastHash) + str(self.nonce)
        )

    def mineBlock(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.getHash()

    def __str__(self):
        data_string = '\n'.join(str(metadata) for metadata in self.data)
        return (
            f"Block {self.index}:\n"
            f"Timestamp: {self.timestamp}\n"
            f"Data:\n{data_string}\n"
        )