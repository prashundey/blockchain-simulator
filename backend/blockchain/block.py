import time

from backend.util.crypto_hash import crypto_hash

"""
GLOBAL VARIABLES 
"""
GENESIS_DATA = {
    'timestamp' : 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data' : []
}

class Block:
    """
    Block: Storage of crypto transactions on blockchain
    """
    def __init__(self, timestamp, last_hash, hash, data) -> None:
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data

    def __repr__(self) -> str:
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data})'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block 
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        hash = crypto_hash(timestamp, last_hash, data)
        return Block(timestamp, last_hash, hash, data)

    @staticmethod
    def genesis():
        """
        Create Genesis block to serve as hardcoded inital block on the chain
        """
        return Block(**GENESIS_DATA)

def main():
    genesis_block = Block.genesis();
    block = Block.mine_block(genesis_block, 'a')
    print(block)

if __name__ == '__main__':
    main()