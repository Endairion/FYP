# fragment.py

class Fragment:
    def __init__(self, fragment_id, fragment_size, fragment_hash, sender_info, next_hash=None):
        self.fragment_id = fragment_id
        self.fragment_size = fragment_size
        self.fragment_hash = fragment_hash
        self.sender_info = sender_info
        self.next_hash = next_hash  # This will store the hash of the next fragment

    def to_dict(self):
        fragment_dict = {
            'fragment_id': self.fragment_id,
            'fragment_size': self.fragment_size,
            'fragment_hash': self.fragment_hash,
            'sender_info': self.sender_info
        }
        if self.next_hash:
            fragment_dict['next_hash'] = self.next_hash
        return fragment_dict
