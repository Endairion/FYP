import json

class DistributedHashTable:
    def __init__(self):
        self.file_path = 'dht.json'
        self.data = {}
        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f)

    def put(self, key, value):
        self.data[key] = value
        self.save_data()

    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data()