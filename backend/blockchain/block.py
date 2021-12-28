import time

from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.util.hex_to_binary import hex_to_binary

"""
Genesis Block Hardcoded Fields  
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
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__

    def to_json(self) -> dict:
        """
        Serialize a block into dictionary of attributes
        """
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block until the block hash created using 
        previous block hash, current block data points and nonce
        statisfy the proof of work requirement

        Hashing Success Based on Proof of Work Difficulty
        - Leading Zeroes in Binary Representation not Hexidecimal 
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp);
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp);
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        Create Genesis block to serve as hardcoded inital block on the blockchain
        """
        return Block(**GENESIS_DATA)
    
    @staticmethod
    def adjust_difficulty(last_block, new_timestamp) -> int:
        """
        Increment or Decrement based on mining time 
        of new block in relation to Mine Rate
        """
        if new_timestamp - last_block.timestamp < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0: 
            return last_block.difficulty - 1

        return 1;

    @staticmethod
    def is_valid_block(last_block, block): 
        """
        Validate block:
            1. Block previous hash references correct hash of previous block 
            2. Block must meet proof of work requirement
            3. Difficulty in proof of work must differ by at most 1
            4. Block hash must be valid hash based on combination of current data points
                If regnerated hash does not match current hash, then data has been tampered with
        """
        if block.last_hash != last_block.hash:
            raise Exception('Current Block last_hash is not correct')

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('Proof of work requirement not statisfied')
        
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('Block difficulty must be adjusted by 1')

        regenerated_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )

        if regenerated_hash != block.hash:
            raise Exception('Block hash must be correct')


def main():
    genesis = Block.genesis()
    bad_block = Block.mine_block(genesis, 'bad-block')
    bad_block.data = 'bad-block-data-changed'
    try:
        Block.is_valid_block(genesis, bad_block)
    except Exception as e: 
        print(f'is_valid_block: {e}')

if __name__ == '__main__':
    main()