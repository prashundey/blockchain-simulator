import uuid
import time

from backend.wallet.wallet import Wallet

class Transaction:
    """
    Document of exchange of currency from a sender to one or more recipients
    """
    def __init__(self, sender_wallet : Wallet, recipient, amount) -> None:
        self.id = str(uuid.uuid4())[0:8]
        self.output = self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet : Wallet, recipient, amount) -> dict:
        """
        Structures output data for the transaction
            - Change of Transaction
        
        @returns
        Output Dictionary: {
            recipient_address: amount to be delivered,
            sender_address: amount to be delivered
        }
        """
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds sender balance')

        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount
        return output

    def create_input(self, sender_wallet : Wallet, output : dict) -> dict:
        """
        Structure input data for transaction
            - Signs the transaction and include sender's public key and address
                Other wallets in system will be able to verify transaction signature
                using public key as input
            - Sender Wallet signs Output Dictionary
        """
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }


def main():
    transaction = Transaction(Wallet(), 'recipient-addy', 15)
    print(f'transaction_dict: {transaction.__dict__}')

if __name__ == '__main__':
    main()
