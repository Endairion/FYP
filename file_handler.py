from block import Block
from blockchain import Blockchain
from metadata import Metadata

def add_file_to_blockchain(blockchain, file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    metadata = Metadata(file_path, file_data)
    block = Block(time.time(), [metadata])
    blockchain.addBlock(block)

def retrieve_file_from_blockchain(blockchain, file_name):
    blocks_with_file = search_blocks(blockchain, file_name)
    file_data = retrieve_file(blocks_with_file)
    return file_data