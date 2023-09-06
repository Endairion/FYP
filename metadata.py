# metadata.py

class FileMetadata:
    def __init__(self, file_id, fragment_id, fragment_index, fragment_size, fragment_hash, timestamp, sender_info):
        self.file_id = file_id
        self.fragment_id = fragment_id
        self.fragment_index = fragment_index
        self.fragment_size = fragment_size
        self.fragment_hash = fragment_hash
        self.timestamp = timestamp
        self.sender_info = sender_info

    def to_dict(self):
        return {
            'file_id': self.file_id,
            'fragment_id': self.fragment_id,
            'fragment_index': self.fragment_index,
            'fragment_size': self.fragment_size,
            'fragment_hash': self.fragment_hash,
            'timestamp': self.timestamp,
            'sender_info': self.sender_info
        }
