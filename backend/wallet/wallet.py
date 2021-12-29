import uuid
import pprint
import json

from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives import hashes, serialization
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

        self.serialize_public_key()

    def sign(self, data : any) -> bytes:
        """
        Generate signature based on the data using local Private Key
        Stringify and Encode input data utf-8
        """
        return self.private_key.sign(
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256())
        )

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
    def verify(public_key : str, 
                data : any, 
                signature : bytes) -> bool:
        """
        Verify signature based on the orginal public key and data input
            - Public Key ipout as PEM encoded serialized string. 
                It is deserialized back into its EllipticCurvePublicKey object 
                by using provided serialization load PEM public key method
            - Data Input is encoded utf-8
        """ 
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )
        try:
            deserialized_public_key.verify(
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
