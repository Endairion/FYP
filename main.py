# Import necessary modules
from blockchain import Blockchain  # Assuming Blockchain class is defined in 'blockchain.py' file
from block import Block  # Assuming Block class is defined in 'block.py' file
from metadata import FileMetadata  # Import the FileMetadata class from 'metadata.py'
from fragment import Fragment  # Import the Fragment class from 'fragment.py'
import time

if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Create and add the genesis block
    genesis_block = blockchain.createGenesisBlock()
    blockchain.addBlock(genesis_block)

    # Create metadata entries for fragmented files
    file_id = "unique_file_identifier"
    fragments = [
        Fragment("fragment_id_1", 1024, "hash1", "sender1"),
        Fragment("fragment_id_2", 2048, "hash2", "sender2"),
        Fragment("fragment_id_3", 4096, "hash3", "sender3")
    ]

    # Create a single FileMetadata object to encapsulate all fragments
    file_metadata = FileMetadata(file_id, fragments)

    # Create a new block with the metadata
    block = Block(time.time(), [file_metadata.to_dict()])

    # Add the new block to the blockchain
    blockchain.addBlock(block)

    # Print the blockchain
    print(blockchain)
