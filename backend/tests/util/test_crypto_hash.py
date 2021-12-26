from backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
    '''
    Assert that arguments of the same type but different order, return same hash
    '''
    assert crypto_hash('1',[1],2) == crypto_hash('1',2,[1])
    
    '''
    Assert correct hash is being generated
    '''
    assert crypto_hash('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'
