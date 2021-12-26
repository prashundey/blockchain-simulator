import hashlib
import json

def crypto_hash(*args):
    """
    Returns a sha-256 hash of all the given arguments, regardless of order
    """
    string_args = sorted(map(lambda data: json.dumps(data), args))
    joined_string = '^'.join(string_args)
    return hashlib.sha256(joined_string.encode('utf-8')).hexdigest()

def main():
    print( f"crypto_hash(): {crypto_hash('one', 2, [3])}")
    print( f"crypto_hash(): {crypto_hash('one', [3], 2)}")

if __name__ == '__main__':
    main()