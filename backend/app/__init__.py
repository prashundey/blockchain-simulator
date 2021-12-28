from flask import Flask

from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

for i in range(3):
    blockchain.add_block(i)

@app.route('/')
def default():
    return 'Blockchain'

@app.route('/blockchain')
def route_blockchain():
    return blockchain.chain.__repr__()


app.run(port = 5000)
