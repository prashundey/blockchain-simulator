from backend.wallet.transaction import Transaction

class TransactionPool:
    def __init__(self) -> None:
        '''
        Map using Transaction IDs as Keys
        '''
        self.transaction_map = {}

    def set_transaction(self, transaction: Transaction):
        """
        Set a transaction in the transaction pool

        Args:
            transaction (Transaction): [description]
        """
        self.transaction_map[transaction.id] = transaction
