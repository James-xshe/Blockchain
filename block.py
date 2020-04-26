from time import time


class Block:
    def __init__(self, previous_hash, index, transactions, proof, time=time()):
        self.previous_hash = previous_hash
        self.index = index
        self.transactions = transactions
        self.timestamp = time
        self.proof = proof

    def __repr__(self):
        return str(self.__dict__)