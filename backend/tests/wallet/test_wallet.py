
from backend.blockchain.blockchain import Blockchain
from backend.config import STARTING_BALANCE
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_verify_valid_signature():
    data = {'key-test': 'value-test'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key, data, signature)

def test_verify_valid_signature():
    data = {'key-test': 'value-test'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(Wallet().public_key, data, signature)


def test_calculate_balance_through_different_blocks():
    block_chain = Blockchain()
    wallet = Wallet()
    
    assert Wallet.calculate_balance(block_chain, wallet.address) == STARTING_BALANCE

    #CASE1: current wallet is sender
    amount = 50.5
    transaction = Transaction(wallet, 'test-recipient-address', amount)
    block_chain.add_block([transaction.to_json()])

    assert Wallet.calculate_balance(block_chain, wallet.address) == STARTING_BALANCE - amount

    #CASE2: current wallet is recipient
    transaction2 = Transaction(Wallet(), wallet.address, amount)
    block_chain.add_block([transaction2.to_json()])
    assert Wallet.calculate_balance(block_chain, wallet.address) == STARTING_BALANCE


def test_calculate_balance_same_block_multiple_transactions():
    block_chain = Blockchain()
    wallet = Wallet()
    
    sent = 63.7
    recieved = 120.1

    transaction1 = Transaction(wallet, 'test-recipient-address', sent)
    transaction2 = Transaction(Wallet(), wallet.address, recieved)
    block_chain.add_block([transaction1.to_json(), transaction2.to_json()])

    assert Wallet.calculate_balance(block_chain, wallet.address) ==\
         STARTING_BALANCE - sent + recieved