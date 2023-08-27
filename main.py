from blockchain import Blockchain  # Assuming Blockchain class is defined in 'blockchain.py' file
from block import Block  # Assuming Block class is defined in 'block.py' file
import time

if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Create and add the genesis block
    genesis_block = blockchain.createGenesisBlock()
    blockchain.addBlock(genesis_block)
    
    # Add subsequent blocks
    block1 = Block(time.time(), ["Hello", "World"])
    blockchain.addBlock(block1)

    block2 = Block(time.time(), ["Hello", "Wurld"])
    blockchain.addBlock(block2)

    block3 = Block(time.time(), ["Hello", "Werld"])
    blockchain.addBlock(block3)

    block4 = Block(time.time(), ["Hello", "Wirld"])
    blockchain.addBlock(block4)
    
    block5 = Block(time.time(), ["Hello", "Wirld"])
    blockchain.addBlock(block5)

    block6 = Block(time.time(), ["Hello", "Wirld"])
    blockchain.addBlock(block6)

    print(blockchain)
