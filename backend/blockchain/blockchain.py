from backend.blockchain.block import Block
from backend.config import MINING_REWARD_INPUT
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


class Blockchain: 
    """
    Blockchain: Public ledger of transactions
    """
    def __init__(self) -> None:
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))
    
    def __repr__(self) -> str:
        return f'Blockchain: {self.chain}'

    def replace_chain(self, incoming_chain: list):
        """
        Replace the local chain with incoming chain if it meets the following
            1. Incoming chain is longer than the local
            2. Incoming chain is formatted correctly
        
        Args:
            incoming_chain (list of Blocks)

        Raises:
            Exception: If incoming chain is not longer or incoming chain itself is invalid
        """
        if (len(incoming_chain) <= len(self.chain)):
            raise Exception('Cannot Replace: incoming chain must be longer')
        
        try:
            Blockchain.is_valid_chain(incoming_chain)
        except Exception as e:
            raise Exception(f'Cannot replace: incoming chain is invalid - {e}')
        
        self.chain = incoming_chain

    def to_json(self) -> list:
        """
        Serialize the blockchain into list of blocks which are each serialized themsleves
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into a Blockchain instance
        The resulting Blockchain instance will contain a list of Block instances
        """
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json), chain_json)
        )
        return blockchain

    @staticmethod
    def is_valid_chain(chain: list):
        """
        Validate incoming chain based on blockchain rules
            1. Chain should start with genesis block
            2. Blocks themselves must statify block validation rules

        Args:
            chain (list of Blocks)

        Raises:
            Exception: If genesis block is invalid or any block in the chain is not valid
        """
        if chain[0] != Block.genesis():
            raise Exception('Genesis Block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)
        
        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain: list):
        """
        Validate rules of a blockchain composed of blocks of transactions
            - Each transaction is unique and appears once in the chain
            - Only a single mine reawrd transaction per block
            - Each transaction must be valid themselves
            - Total sum of balances along the chain at each block should 
                equal to current block's wallet balance
        Args:
            chain (list of blocks): [description]
        """

        transaction_ids = set()

        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False
            
            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)
                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction {transaction.id} is not unique')

                Transaction.is_valid_transaction(transaction)
                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            'There must be one mining reward per block'
                            f'Check Block with hash: {block.hash} '
                            )
                    has_mining_reward = True
                
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )

                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction {transaction.id} has invalid input amount')
                
                
               
                


def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    print(blockchain)

if __name__ == '__main__':
    main()