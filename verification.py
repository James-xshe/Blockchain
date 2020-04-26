import hashlib
import json
from wallet import Wallet


class Verification:
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode('utf-8')
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[0:2] == '00'

    @staticmethod
    def hash_block(block):
        hashable_block = block.__dict__.copy()
        hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
        return hashlib.sha256(json.dumps(hashable_block, sort_keys=True).encode('utf-8')).hexdigest()

    @classmethod
    def verify_chain(cls, blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != cls.hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid!')
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        sender_balance = get_balance()
        return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
