import hashlib
from metadata import FileMetadata

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

    def mineBlock(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.getHash()

    def getHash(self):
        data_string = str(self.data)  # treat self.data as an object, not a list
        return SHA256(
            data_string + str(self.timestamp) + str(self.lastHash) + str(self.nonce)
        )

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data.to_dict() if hasattr(self.data, 'to_dict') else self.data,
            'lastHash': self.lastHash,
            'nonce': self.nonce,
            'hash': self.hash,
        }