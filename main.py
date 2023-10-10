# main.py
# Import necessary modules
from blockchain import Blockchain  # Assuming Blockchain class is defined in 'blockchain.py' file
from block import Block  # Assuming Block class is defined in 'block.py' file
from metadata import FileMetadata  # Import the FileMetadata class from 'metadata.py'
from fragment import Fragment  # Import the Fragment class from 'fragment.py'
import time

if __name__ == "__main__":
    # Load the existing blockchain from a file
    blockchain = Blockchain.load_from_file('blockchain.pkl')

    if blockchain is None:
        # If the file doesn't exist or is empty, create a new blockchain
        blockchain = Blockchain()

        # Create and add the genesis block
        genesis_block = blockchain.createGenesisBlock()
        blockchain.addBlock(genesis_block)

    # Create metadata entries for fragmented files
    file_metadata_entries = [
        # File 1
        FileMetadata("file_id_1", [
            Fragment("fragment_id_1_1", 1024, "hash1_1", "sender1_1", "hash1_2"),
            Fragment("fragment_id_1_2", 2048, "hash1_2", "sender1_2")
        ]),

        # File 2
        FileMetadata("file_id_2", [
            Fragment("fragment_id_2_1", 1024, "hash2_1", "sender2_1", "hash2_2"),
            Fragment("fragment_id_2_2", 2048, "hash2_2", "sender2_2")
        ]),

        # File 3
        FileMetadata("file_id_3", [
            Fragment("fragment_id_3_1", 1024, "hash3_1", "sender3_1", "hash3_2"),
            Fragment("fragment_id_3_2", 2048, "hash3_2", "sender3_2")
        ])
    ]

    # Create user data entries
    user_data_entries = [
        UserData("user_id_1", "user1", "hashed_password_1", "user1@email.com"),
        UserData("user_id_2", "user2", "hashed_password_2", "user2@email.com")
        # Add more user data entries as needed
    ]

    # Create a new block for each file's metadata and add them to the existing blockchain
    for file_metadata in file_metadata_entries:
        block = Block(time.time(), [file_metadata.to_dict()])
        blockchain.addBlock(block)

    # Create a new block for each user's data and add them to the existing blockchain
    for user_data in user_data_entries:
        block = Block(time.time(), [user_data.to_dict()])
        blockchain.addBlock(block)

    # Save the updated blockchain back to the file
    print(blockchain)
    blockchain.save_to_file('blockchain.pkl')
