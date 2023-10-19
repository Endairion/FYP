class Fragment:
    def __init__(self, fragment_id, fragment_hash, fragment_size, next_fragment_hash=None, num_fragments=None):
        self.fragment_id = fragment_id
        self.fragment_hash = fragment_hash
        self.fragment_size = fragment_size
        self.next_fragment_hash = next_fragment_hash
        self.num_fragments = num_fragments

    def __repr__(self):
        return f"Fragment({self.fragment_id}, {self.fragment_hash}, {self.fragment_size}, {self.next_fragment_hash}, {self.num_fragments})"