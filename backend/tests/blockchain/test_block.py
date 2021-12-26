from backend.blockchain.block import GENESIS_DATA, Block

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


def test_genesis():
    '''
    Test creation of genesis block (first block in chain)
    '''
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value
