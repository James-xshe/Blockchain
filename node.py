from blockchain import Blockchain
from uuid import uuid4
from verification import Verification
from wallet import Wallet

class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_key()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_transaction_value(self):
        recipient = input('Your recipient is: ')
        amount = float(input('Your transaction amount is: '))
        return recipient, amount

    def get_user_choice(self):
        user_input = input('Yourt choice: ')
        return user_input

    def print_blockchain_elements(self):
        for block in self.blockchain.get_chain():
            print('Outputting Block')
            print(block)

    def listen_for_input(self):
        while True:
            print('Please choose')
            print('1: Add a new transcation value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check transaction validity')
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save wallet')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')
                print(self.blockchain.get_open_tx())
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('No wallet, mining failed!')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_tx(), self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There is invalid transaction')
            elif user_choice == '5':
                self.wallet.create_key()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                break
            else:
                print('Input was invalid')
            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                break
            print('Balacne of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))
        else:
            print('User left!')

        print('Done!')

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
