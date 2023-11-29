import pickle
from blockchain import Blockchain

def read_blockchain():
    # Load the blockchain from the file
    blockchain = Blockchain.load_from_file('blockchain.pkl')

    blocks = blockchain.extract_file_info()
    block_data = []
    
    if blockchain is not None:
        # Enumerate the blocks and print their types
        for i, block in enumerate(blocks):
            # Deserialize the block data into a FileMetadata object
            file_metadata = pickle.loads(block.data)
            block_data.append(file_metadata.to_dict())

        # Print each block of the blockchain
        print(block_data)
    else:
        print("No blockchain found in 'blockchain.pkl'")

# Call the function
read_blockchain()