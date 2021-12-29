from backend.blockchain.block import Block
from backend.tests.blockchain.test_block import block


class Blockchain: 
    """
    Blockchain: Public ledger of transactions
    Implmentation: List of blocks (set of transactions)
    """
    def __init__(self) -> None:
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))
    
    def __repr__(self) -> str:
        return f'Blockchain: {self.chain}'

    def replace_chain(self, incoming_chain : list):
        """
        :type: list of Blocks

        Replace the local chain with incoming chain if it meets the following
            1. Incoming chain is longer than the local
            2. Incoming chain is formatted correctly
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
        Serialize the blockchain into list of blocks which are also serialized 
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def is_valid_chain(chain : list):
        """
        :type: list of Blocks

        Validate incoming chain based on blockchain rules
            1. Chain should start with genesis block
            2. Blocks themselves must statify block validation rules
        """
        if chain[0] != Block.genesis():
            raise Exception('Genesis Block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)

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

def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    print(blockchain)

if __name__ == '__main__':
    main()