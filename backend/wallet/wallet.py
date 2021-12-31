import uuid
import pprint
import json

from backend.config import STARTING_BALANCE

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)

class Wallet:
    """
    - Individual Wallet for Miner
    - Tracks miner's balance
    - Conduct and Authorize Transactions
    """

    def __init__(self, blockchain = None) -> None:
        self.blockchain = blockchain
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()

        self.serialize_public_key()

    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)

    def sign(self, data: any) -> tuple:
        """
         Generate signature based on the data using local Private Key
            - Stringifies and Encodes input data utf-8
            - Then decodes using Digital signature standard (DSS)
        
        Args:
            data (any): Data to be signed

        Returns:
            tuple: Coordinates (r,s) on randomly generated Elliptic Curve that represents decoded signature 
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256())
        ))

    def serialize_public_key(self):
        """
        Serialize Public Key from its byte representation
            - Public Key PEM encoded to created byte string
            - Decode byte string 
        """
        self.public_key = self.public_key.public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')


    @staticmethod
    def verify(public_key: str, data: any, signature: tuple) -> bool:
        """
        Verify signature based on the orginal public key and data input
            - It is deserialized back into its EllipticCurvePublicKey object by using provided serialization load PEM public key method
            - Data parameter is encoded utf-8

        Args:
            public_key (str): Public Key input as PEM encoded serialized string
            data (any): Data used for signature
            signature (tuple): Signature as cooridnates on Elliptic Curve via Sign Method

        Returns:
            bool: True 
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        # Coordinates on Elliptic Curve that represent decoded signature
        (r, s) = signature

        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s), 
                json.dumps(data).encode('utf-8'), 
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

    @staticmethod
    def calculate_balance(blockchain, address: str) -> float:
        """
        Calculate balance of given address using the history of the blockchain
            - Balance is summing the output values that are associated with that 
            address throughout the chain

        Args:
            blockchain (Blockchain): Blockchain to iterate
            address (str): Target Address to calculate balance
        
        Returns:
            float: Current balance of wallet
        """
        balance = STARTING_BALANCE

        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                #CASE 1: current address is sender
                if transaction['input']['address'] == address:
                    # Balance is reset to settlement of funds for the sender because output dict,
                    # represents how the sender's balance was split for this transaction
                    balance = transaction['output'][address]
                
                #CASE 2: current address is recipient
                elif address in transaction['output']:
                    balance += transaction['output'][address]
        return balance



def main():
    wallet = Wallet()
    pprint.pprint(wallet.__dict__)

    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    print(f'signature: {signature}')

    is_valid = Wallet.verify(wallet.public_key, data, signature)
    print(f'is valid: {is_valid}')

    is_not_valid = Wallet.verify(Wallet().public_key, data, signature)
    print(f'is not valid: {is_not_valid}')

if __name__ == '__main__':
    main()
