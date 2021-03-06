import uuid
import time

from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT

class Transaction:
    """
    Document of exchange of currency from a sender to one or more recipients

    Dictionary Outline
        - output: {
            {recipient address}: amount to be paid
            {sender wallet address}: amount to be settled back into sender
        }

        - input: {
            'timestamp': timestamp epoch ns,
            'amount': {sender wallet balance},
            'address': {sender wallet address},
            'public_key': {sender wallet public key}
            'signature': {signature tuple of sender wallet signing output dict}
        }
    """
    def __init__(
        self, 
        sender_wallet = None, 
        recipient = None, 
        amount = None,
        id = None,
        output = None,
        input = None,
        ) -> None:

        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = input or self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet: Wallet, recipient, amount: float) -> dict:
        """ 
        Structures output data for the transaction
            - Change of Transaction
            - sender orginal balance = amount to be paid to recipient + amount to be settled back into sender
        
        Args:
            sender_wallet (Wallet): Sender's Wallet 
            recipient ([type]): Recipient's Digital Address
            amount ([float]): Amount of curreny to be Sent

        Raises:
            Exception: Amount exceeds balance

        Returns:
            dict: Map of recipient_address and sender_address as keys and settlement of sender's balances as keys
        """
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance')

        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount
        return output

    def create_input(self, sender_wallet: Wallet, output: dict) -> dict:
        """
        Structure input data for transaction
            - Signs the transaction and include sender's public key and address
                Other wallets in system will be able to verify transaction signature
                using public key as input
            - Sender Wallet signs Output Dictionary

        Args:
            sender_wallet (Wallet): Sender's Wallet
            output (dict): Map of recipient_address and sender_address as keys and 
                            settlement of sender's balances as keys

        Returns:
            dict: Map of Transaction Input, including signature of output
        """
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }

    def update(self, sender_wallet: Wallet, recipient_address, amount: float):
        """
        Update Transaction with existing or new recipient and resigns the Transaction 
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance')
        
        if recipient_address in self.output:
            self.output[recipient_address] += amount
        else:
            self.output[recipient_address] = amount
        
        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet, self.output)

    def to_json(self):
        """
        Serialize Transaction
        """
        return self.__dict__

    @staticmethod
    def from_json(transaction_json: dict):
        """
        Deserialize transaction json representation into Transaction instance
            
        Args:
            transaction_json (dict): JSON containing transaction data: id, output, input
        """
        return Transaction(**transaction_json)

    @staticmethod
    def is_valid_transaction(transaction):
        """
        Validate transaction or Raise Exception for invalid ones
            - Seperate logic for Mining Reward
                - Checks input and output maps of transaction vs. global configs
            - All other transactions
                - Check if Output structure is valid:
                Amounts should sum to original sender balance
                - Verify the signature of transaction
        """
        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise Exception('Invalid mining reward transaction')
            return 

        output_total = sum(transaction.output.values())

        if output_total != transaction.input['amount']:
            raise Exception('Invalid transaction - output values')

        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception('Invalid signature on transaction')

    @staticmethod
    def reward_transaction(miner_wallet: Wallet):
        output = {}
        output[miner_wallet.address] = MINING_REWARD

        return Transaction(input = MINING_REWARD_INPUT, output = output)

def main():
    transaction = Transaction(Wallet(), 'recipient-addy', 15)
    print(f'transaction_dict: {transaction.__dict__}')

    transaction_json = transaction.to_json()
    restored = Transaction.from_json(transaction_json)
    print(f'restored_dict: {restored.__dict__}')

if __name__ == '__main__':
    main()
