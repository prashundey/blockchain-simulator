import os
import random
import requests

from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)

@app.route('/')
def default():
    return 'Blockchain'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed-transaction-data'
    blockchain.add_block(transaction_data)

    new_block = blockchain.chain[-1]
    pubsub.broadcast_block(new_block)
    return jsonify(new_block.to_json())

# Root Node Port
ROOT_PORT = 5000
PORT = 5000

'''
Peer instances, startup
    1. Establish startup on different port: random between 5001 and 6000
    2. Synchronize a Peer on startup to catch up with root node chain
'''
if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

    res = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    res_blockchain = Blockchain.from_json(res.json())

    try:
        blockchain.replace_chain(res_blockchain.chain)
        
    except Exception as e:
        print(f'Could not synchronize local chain: {e}')

app.run(port = PORT)
