# metadata.py
import time
from fragment import Fragment  # Import the Fragment class from fragment.py

class FileMetadata:
    def __init__(self, file_id, file_name, file_size, fragments, sender, file_hash):
        self.file_id = file_id
        self.file_name = file_name
        self.file_size = file_size
        self.fragments = fragments
        self.sender = sender
        self.timestamp = time.time()  # A timestamp for when the metadata was created
        self.file_hash = file_hash

    def __str__(self):
        return f"FileMetadata(file_id={self.file_id}, file_name={self.file_name}, file_size={self.file_size}, fragments={self.fragments}, sender={self.sender}, timestamp={self.timestamp}, file_hash={self.file_hash})"
    
    def to_dict(self):
        return {
            'file_id': self.file_id,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'fragments': self.fragments.to_dict(),  # directly call to_dict on the Fragment object
            'sender': self.sender,
            'timestamp': self.timestamp,
            'file_hash': self.file_hash
        }
    