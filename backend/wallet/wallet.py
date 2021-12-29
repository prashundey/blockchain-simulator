import uuid
import pprint
import json

from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class Wallet:
    """
    Individual Wallet for Miner
    Tracks miner's balance
    Conduct and Authorize Transactions
    """
    def __init__(self) -> None:
        self.address = str(uuid.uuid4())[0:8]
        self.balance  = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()

    def sign(self, data : any) -> bytes:
        """
        Generate signature based on the data using local Private Key
        Stringify and Encode input data utf-8
        """
        return self.private_key.sign(
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256())
        )

    @staticmethod
    def verify(public_key : EllipticCurvePublicKey, 
                data : any, 
                signature : bytes) -> bool:
        """
        Verify signature based on the orginal public key and data input (needs encoding)
        """ 
        try:
            public_key.verify(
                signature, 
                json.dumps(data).encode('utf-8'), 
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False


def main():
    wallet = Wallet()
    pprint.pprint(wallet.__dict__)

    data = {'foo' : 'bar'}
    signature = wallet.sign(data)
    print(f'signature: {signature}')

    is_valid = Wallet.verify(wallet.public_key, data, signature)
    print(f'is valid: {is_valid}')

    is_not_valid = Wallet.verify(Wallet().public_key, data, signature)
    print(f'is not valid: {is_not_valid}')

if __name__ == '__main__':
    main()
