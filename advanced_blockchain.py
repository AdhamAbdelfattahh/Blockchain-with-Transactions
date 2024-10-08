import hashlib
import json
from time import time

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()  # Calculate hash upon initialization

    def calculate_hash(self):
        block_string = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        block = Block(len(self.chain) + 1, self.current_transactions, time(), previous_hash)
        self.chain.append(block)
        print(f"Created Block {block.index} with Transactions: {self.current_transactions}")
        self.current_transactions = []  # Clear current transactions after mining
        return block

    def add_transaction(self, sender, recipient, amount):
        transaction = Transaction(sender, recipient, amount)
        self.current_transactions.append(transaction)
        print(f"Added Transaction: {transaction.to_dict()}")
        return self.last_block.hash

    @property
    def last_block(self):
        return self.chain[-1]

    def display_chain(self):
        for block in self.chain:
            transactions = [tx.to_dict() for tx in block.transactions]  # Get transaction details
            print(f"Block {block.index} | Hash: {block.hash} | Previous Hash: {block.previous_hash} | Transactions: {transactions}")

if __name__ == "__main__":
    blockchain = Blockchain()

    while True:
        print("\nOptions:")
        print("1. Add Transaction")
        print("2. Mine Block")
        print("3. Display Blockchain")
        print("4. Exit")
        choice = input("Select an option (1/2/3/4): ")

        if choice == '1':
            sender = input("Enter sender: ")
            recipient = input("Enter recipient: ")
            amount = float(input("Enter amount: "))
            blockchain.add_transaction(sender, recipient, amount)
            print("Transaction added!")

        elif choice == '2':
            previous_hash = blockchain.last_block.hash
            blockchain.create_block(previous_hash)
            print("Block mined!")

        elif choice == '3':
            blockchain.display_chain()

        elif choice == '4':
            break

        else:
            print("Invalid option. Please try again.")
