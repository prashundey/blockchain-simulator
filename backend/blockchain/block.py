import time

from backend.util.crypto_hash import crypto_hash

"""
GLOBAL VARIABLES 
"""
GENESIS_DATA = {
    'timestamp' : 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce' : 'genesis_nonce'
}

class Block:
    """
    Block: Storage of crypto transactions on blockchain
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce) -> None:
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self) -> str:
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.data}, '
            f'nonce: {self.nonce})'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block until the block hash created using 
        previous block hash, current block data points and nonce
        statisfy the proof of work requirement
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = last_block.difficulty
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hash[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        Create Genesis block to serve as hardcoded inital block on the blockchain
        """
        return Block(**GENESIS_DATA)

def main():
    genesis_block = Block.genesis();
    block = Block.mine_block(genesis_block, 'a')
    print(block)

if __name__ == '__main__':
    main()