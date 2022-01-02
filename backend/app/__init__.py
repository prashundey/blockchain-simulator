import os
import random
import requests

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.wallet import Wallet
from backend.pubsub import PubSub

app = Flask(__name__)
CORS(app, resources= { r'/*': {
    'origins': 'http://localhost:3000'
}})

blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()

pubsub = PubSub(blockchain, transaction_pool)

@app.route('/')
def default():
    return 'Blockchain'


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())

    blockchain.add_block(transaction_data)
    new_block = blockchain.chain[-1]
    pubsub.broadcast_block(new_block)

    transaction_pool.clear_blockchain_transactions(blockchain)

    return jsonify(new_block.to_json())


@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)
    
    if transaction:
        transaction.update(
            wallet, 
            transaction_data['recipient'], 
            transaction_data['amount']
        )

    else:
        transaction = Transaction(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
            )
    
    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())


@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({
        'address': wallet.address,
        'balance': wallet.balance
    })


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
