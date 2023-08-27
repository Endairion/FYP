from block import Block
import time

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
    
    def __str__(self):
        chain_info = "\n".join(str(block) for block in self.chain)
        return f"Blockchain:\n{chain_info}"
