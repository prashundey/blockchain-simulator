import pytest
from backend.config import STARTING_BALANCE

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
    with pytest.raises(Exception, match = 'Amount exceeds sender balance'):
        Transaction(Wallet(), 'recipient-test-address', STARTING_BALANCE + 1)