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
            print(type(block.data))  # Prints the type of block.data
            print(block.data)  # Prints the value of block.data

        # Print each block of the blockchain
    else:
        print("No blockchain found in 'blockchain.pkl'")

# Call the function
read_blockchain()