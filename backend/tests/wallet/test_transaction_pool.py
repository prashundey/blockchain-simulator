from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'test-recipient-address', 50)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction
    
def test_clear_blockchain_transactions():
    transaction_pool = TransactionPool()
    transaction1 = Transaction(Wallet(), 'test-recipient-address', 1)
    transaction2 = Transaction(Wallet(), 'test-recipient-address', 2)
    
    transaction_pool.set_transaction(transaction1)
    transaction_pool.set_transaction(transaction2)

    block_chain = Blockchain()
    block_chain.add_block([transaction1.to_json(), transaction2.to_json()])

    assert transaction1.id in transaction_pool.transaction_map
    assert transaction2.id in transaction_pool.transaction_map

    transaction_pool.clear_blockchain_transactions(block_chain)

    assert not transaction1.id in transaction_pool.transaction_map
    assert not transaction2.id in transaction_pool.transaction_map
    