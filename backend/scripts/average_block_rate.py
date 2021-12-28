import time

from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS

blockchain = Blockchain()
times = []

for i in range(1000):
    start_time = time.time_ns()
    blockchain.add_block(i)
    end_time = time.time_ns()
    mining_time = (end_time - start_time) / SECONDS
    
    times.append(mining_time)
    average_time = sum(times) / len(times)

    print(f'Lastest Difficulty: {blockchain.chain[-1].difficulty}')
    print(f'Lastest Mine Rate: {mining_time}s')
    print(f'AVERAGE MINE RATE: {average_time} \n')

'''
HexiDecimal Form Hashes:
    Average Mine Rate Converges to 2.5 seconds but MINE_RATE = 4 seconds

    Change hashes to Binary Representation, because mining leading zeros for 
    Hexidecimal hashes to easy to for CPU
'''