import pickle
from blockchain import Blockchain
from metadata import FileMetadata

def read_blockchain():
    # Load the blockchain from the file
    blockchain = Blockchain.load_from_file('blockchain.pkl')

    blocks = blockchain.extract_file_info()
    block_data = []
    
    if blockchain is not None:
        # Enumerate the blocks and print their types
        for i, block in enumerate(blocks):
            # Skip the genesis block
            if i == 0:
                continue

            # Check if block.data is a FileMetadata object
            if isinstance(block.data, FileMetadata):
                # Access the file_id attribute
                file_id = block.data.file_id
                block_data.append(file_id)

        # Print each block of the blockchain
        print(block_data)
    else:
        print("No blockchain found in 'blockchain.pkl'")

# Call the function
read_blockchain()