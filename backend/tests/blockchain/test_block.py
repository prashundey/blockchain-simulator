import time
import pytest

from backend.blockchain.block import GENESIS_DATA, Block
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary

def test_mine_block():
    '''
    Test mining of blocks using genesis block method and sample data
    '''
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty


def test_genesis():
    '''
    Test creation of genesis block (first block in chain)
    '''
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value


def test_mined_block_inc_difficulty(): 
    '''
    Test incrementing diffculty of mining block
    '''
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, '2-foo')

    assert mined_block.difficulty == last_block.difficulty + 1


def test_mined_block_dec_difficulty():
    '''
    Test decrementing difficulty of mining block 
    by putting thread to sleep to replicate mine rate of current block > Accepted MINE RATE
    '''
    last_block = Block.mine_block(Block.genesis(), 'foo')

    # Delay by 4 seconds, since Mine Rate is 4 seconds in nanoseconds
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, '2-foo')

    assert mined_block.difficulty == last_block.difficulty - 1


def test_mined_block_difficulty_limits_at_1():
    '''
    Test that the lowest difficulty will always be 1
    by creating a hard coded block with a difficulty of 1 already and 
    replicate mine rate of current block > Accepted MINE RATE to
    to test if it will decrement
    '''
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'foo',
        1,
        0
    )
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == 1


@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'test-data')


def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)
    

def test_is_valid_block_bad_last_hash(last_block, block):
    block.last_hash = 'incorrect-last-hash'
    with pytest.raises(Exception, match='Current Block last_hash is not correct'):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_current_hash(last_block, block):
    block.data = 'incorrect-data'
    with pytest.raises(Exception, match='Block hash must be correct'):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_proof_of_work(last_block, block):
    block.hash = 'fff'
    with pytest.raises(Exception, match='Proof of work requirement not statisfied'):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_adjust_difficulty(last_block, block):
    block.difficulty = 10
    block.hash = f'{"0" * block.difficulty}fff'
    with pytest.raises(Exception, match='Block difficulty must be adjusted by 1'):
        Block.is_valid_block(last_block, block)