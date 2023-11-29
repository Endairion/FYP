from blockchain import Blockchain

def read_blockchain():
    # Load the blockchain from the file
    blockchain = Blockchain.load_from_file('blockchain.pkl')

    if blockchain is not None:
        # Print the chain of the blockchain
        print(blockchain.chain)
    else:
        print("No blockchain found in 'blockchain.pkl'")

# Call the function
read_blockchain()