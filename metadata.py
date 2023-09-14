# metadata.py
import time
from fragment import Fragment  # Import the Fragment class from fragment.py

class FileMetadata:
    def __init__(self, file_id, fragments):
        self.file_id = file_id
        self.fragments = fragments
        self.timestamp = time.time()  # A timestamp for when the metadata was created

    def to_dict(self):
        return {
            'file_id': self.file_id,
            'fragments': [fragment.to_dict() for fragment in self.fragments],
            'timestamp': self.timestamp
        }
