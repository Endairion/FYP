import pickle

def read_blockchain():
    # Open the file in read-binary mode
    with open('blockchain.pkl', 'rb') as file:
        # Load the blockchain from the file
        blockchain = pickle.load(file)

        print(blockchain)

# Call the function
read_blockchain()