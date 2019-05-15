import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4
from flask import Flask



class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # creating the genesis block
        self.new_block(previous_hash=1,proof=100)

    def proof_of_work(self, last_proof):
        """
        - Find a number p' such that has(pp') contains leading 5 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof

        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1

        return proof

    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "00000"

    def new_block(self,proof,previous_hash=None):

        block = {
            "index": len(self.chain) +1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions=[]

        self.chain.append(block)
        return block

    def new_transaction(self):
        self.current_transactions.append({
            "sender": sender,
            "recipient":recipient,
            "amount":amount,
        })
        return self.last_block["index"] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    app = Flask(__name__)

    node_identifier = str(uuid4()).replace("-","")
    blockchain = Blockchain()

    @app.route("/mine",methods=["GET"])
    def mine():
        return "We'll mine a new Block"

    @app.route("/transactions/new",methods=["GET"])
    def new_transaction():
        return "We'll add a new transaction"

    @app.route("/chain",methods=["GET"])
    def full_chain():
        response = {
            "chain" : blockchain.chain,
            "length": len(blockchain.chain)
        }
        return jsonify(response), 200

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000)
