import pickle
import os  # Import the 'os' module to check if a file exists
import time
from block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 3
        self.blocktime = 10

    def createGenesisBlock(self):
        return Block(time.time(), 'Genesis block')

    def getLastBlock(self):
        return self.chain[-1]

    def getLastBlockIndex(self):
        return len(self.chain) - 1

    def addBlock(self, newBlock):
        if not self.chain:
            newBlock.lastHash = ''
        else:
            newBlock.lastHash = self.getLastBlock().hash
            newBlock.index = self.getLastBlock().index + 1

        newBlock.hash = newBlock.getHash()

        newBlock.mineBlock(self.difficulty)

        self.chain.append(newBlock)

        if (time.time() - self.getLastBlock().timestamp) < self.blocktime:
            self.difficulty += 1
            print(time.time() - self.getLastBlock().timestamp)
        else:
            self.difficulty -= 1
            print(time.time() - self.getLastBlock().timestamp)

    def isChainValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            lastBlock = self.chain[i - 1]

            if currentBlock.hash != currentBlock.getHash():
                return False

            if currentBlock.lastHash != lastBlock.hash:
                return False
        return True
    
    def extract_file_info(self):
        file_info_list = []

        # Iterate over each block in the chain
        for i, block in enumerate(self.chain):
            print(f"Block {i} is of type {type(block)}")

            # Extract the file information from the block's data
            file_info = block.data  # Modify this line if the file information is stored differently

            # Add the file information to the list
            file_info_list.append(file_info)

        return file_info_list

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.chain, file)

    @classmethod
    def load_from_file(cls, filename):
        try:
            with open(filename, 'rb') as file:
                blockchain = cls()
                blockchain.chain = pickle.load(file)
                return blockchain
        except (FileNotFoundError, EOFError):
            return None
    
    def __str__(self):
            return '\n'.join(str(block) for block in self.chain)
    
    def print_blocks(self):
        for i, block in enumerate(self.chain):
            print(f"Block {i}: {block.to_dict()}")
