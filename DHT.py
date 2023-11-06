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
    
    def search(self, key):
        return key in self.data

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data()
            return {"success": True, "message": f"Key '{key}' deleted successfully."}
        else:
            return {"success": False, "message": f"Key '{key}' not found."}
        
    def get_all(self):
        # Get the values (associated data)
        associated_data = list(self.data.values())

        return associated_data
        
    def get_all_except_sender(self, sender):
        # Copy the data
        all_nodes = self.data.copy()

        # Remove the sender from the dictionary
        all_nodes.pop(sender, None)

        # Get the values (associated data)
        associated_data = list(all_nodes.values())

        return associated_data