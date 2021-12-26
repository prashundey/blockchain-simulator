from backend.util.crypto_hash import crypto_hash

"""
Convert Hexidecimal hash to Binary Hash for more 
valuable proof of work. Resulting average block rate 
should converge closer to MINE_RATE
"""

def hex_to_binary(hex_str : str) -> str:
    return bin(int('1'+ hex_str, 16))[3:]

def main():
    num = 451
    hex_num = hex(num)[2:]
    print(f'hex rep: {hex_num}')

    bin_num = hex_to_binary(hex_num)
    print(f'binary rep: {bin_num}')

    og_num = int(bin_num, 2)
    print(f'orginal num: {og_num}')

    bin_hash = hex_to_binary(crypto_hash('test-data'))
    print(f'binary hash num: {bin_hash}')
    print(len(bin_hash))

if __name__ == '__main__':
    main()