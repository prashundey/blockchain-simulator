import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA

def test_blockchain_instance():
    '''
    Test initial block in blockchain is the genesis block
    '''
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data


@pytest.fixture
def blockchain_4_blocks() -> Blockchain:
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block(i)
    return blockchain

def test_is_valid_chain(blockchain_4_blocks : Blockchain):
    Blockchain.is_valid_chain(blockchain_4_blocks.chain)

def test_is_valid_chain_bad_genesis_block(blockchain_4_blocks : Blockchain):
    blockchain_4_blocks.chain[0].hash = 'incorrect-hash'
    with pytest.raises(Exception, match = 'Genesis Block must be valid'):
        Blockchain.is_valid_chain(blockchain_4_blocks.chain)


def test_replace_chain(blockchain_4_blocks : Blockchain):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_4_blocks.chain)

    assert blockchain.chain == blockchain_4_blocks.chain


def test_replace_chain_not_longer(blockchain_4_blocks : Blockchain):
    blockchain = Blockchain()
    with pytest.raises(Exception, match = 'Cannot Replace: incoming chain must be longer'):
        blockchain_4_blocks.replace_chain(blockchain.chain)


def test_replace_chain_not_formatted_correctly(blockchain_4_blocks : Blockchain):
    blockchain = Blockchain()
    blockchain_4_blocks.chain[1].hash = 'bad-hash'

    with pytest.raises(Exception, match = 'Cannot replace: incoming chain is invalid'):
         blockchain.replace_chain(blockchain_4_blocks.chain)