class Fragment:
    def __init__(self, fragment_hashes, num_fragments=None):
        self.fragment_hashes = fragment_hashes
        self.num_fragments = num_fragments

    def __repr__(self):
        return f"Fragment({self.fragment_hashes}, {self.num_fragments})"

    def to_dict(self):
        return {f"Fragment {i+1}": hash for i, hash in enumerate(self.fragment_hashes)}