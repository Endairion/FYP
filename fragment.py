class Fragment:
    def __init__(self, fragment_id, fragment_size, fragment_hash, sender_info):
        self.fragment_id = fragment_id
        self.fragment_size = fragment_size
        self.fragment_hash = fragment_hash
        self.sender_info = sender_info

    def to_dict(self):
        return {
            'fragment_id': self.fragment_id,
            'fragment_size': self.fragment_size,
            'fragment_hash': self.fragment_hash,
            'sender_info': self.sender_info
        }