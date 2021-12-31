import pytest
from backend.config import MINING_REWARD, MINING_REWARD_INPUT, STARTING_BALANCE

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_transaction():
    sender_wallet = Wallet()
    recipient_addy = 'recipient-test-address'
    amount = 50
    transaction = Transaction(sender_wallet, recipient_addy, amount)

    assert transaction.output[recipient_addy] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount
    
    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key

    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match = 'Amount exceeds balance'):
        Transaction(Wallet(), 'recipient-test-address', STARTING_BALANCE + 1)


def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    recipient_address = 'recipient-test-address'
    transaction = Transaction(sender_wallet, recipient_address, 100)

    with pytest.raises(Exception, match = 'Amount exceeds balance'):
        transaction.update(sender_wallet, recipient_address, 1000000)


def test_transaction_update_sucessful():
    sender_wallet = Wallet()

    '''
    Testing updating transaction to same address as original recipient with new payment
    '''
    recipient_address_1 = 'recipient-test-address-1'
    first_amount = 50
    amount_update = 10
    transaction = Transaction(sender_wallet, recipient_address_1, first_amount)   
    transaction.update(sender_wallet, recipient_address_1, amount_update)

    assert recipient_address_1 in transaction.output
    assert transaction.output[recipient_address_1] == first_amount + amount_update
    assert transaction.output[sender_wallet.address] ==\
        sender_wallet.balance - first_amount - amount_update
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

    '''
    Testing updating transaction to new recipient with another payment
    '''
    recipient_address_2 = 'recipient-test-address-2'
    new_amount = 70
    transaction.update(sender_wallet, recipient_address_2, new_amount)

    assert recipient_address_2 in transaction.output
    assert transaction.output[recipient_address_2] == new_amount
    assert transaction.output[sender_wallet.address] ==\
        sender_wallet.balance - first_amount - amount_update - new_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_valid_transaction():
    transaction = Transaction(Wallet(), 'recipient-test-address', 50)
    Transaction.is_valid_transaction(transaction)


def test_invalid_transaction_changed_output():
    transaction = Transaction(Wallet(), 'recipient-test-address', 50)
    transaction.output['recipient-test-address'] = 100

    with pytest.raises(Exception, match='Invalid transaction - output values'):
        Transaction.is_valid_transaction(transaction)


def test_invalid_transaction_changed_output():
    '''
    Test signing valid transaction output with a different wallet 
    thus reassigning its signature
    '''
    transaction = Transaction(Wallet(), 'recipient-test-address', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)
    
    with pytest.raises(Exception, match='Invalid signature on transaction'):
        Transaction.is_valid_transaction(transaction)


def test_reward_transaction():
    miner_wallet = Wallet()
    transaction = Transaction.reward_transaction(miner_wallet)

    assert transaction.input == MINING_REWARD_INPUT
    assert transaction.output[miner_wallet.address] == MINING_REWARD

def test_valid_reward_transaction():
    mine_reward_transaction = Transaction.reward_transaction(Wallet())
    Transaction.is_valid_transaction(mine_reward_transaction)

def test_invalid_reward_transaction_invalid_amount():
    miner_wallet = Wallet()
    mine_reward_transaction = Transaction.reward_transaction(miner_wallet)
    mine_reward_transaction.output[miner_wallet.address] = MINING_REWARD + 1
    
    with pytest.raises(Exception, match='Invalid mining reward transaction'):
        Transaction.is_valid_transaction(mine_reward_transaction)

def test_invalid_reward_transaction_invalid_recipient():
    mine_reward_transaction = Transaction.reward_transaction(Wallet())
    mine_reward_transaction.output['test-extra-recipient'] = MINING_REWARD 
    
    with pytest.raises(Exception, match='Invalid mining reward transaction'):
        Transaction.is_valid_transaction(mine_reward_transaction)