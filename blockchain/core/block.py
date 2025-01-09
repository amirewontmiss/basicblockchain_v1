
from dataclasses import dataclass
from typing import List, Dict
import hashlib
import json
import time

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
    signature: str = None
    timestamp: float = time.time()

    def to_dict(self) -> Dict:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "signature": self.signature,
            "timestamp": self.timestamp
        }

class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str):
        self.index = index
        self.transactions = transactions
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.nonce = 0
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self) -> str:
        if not self.transactions:
            return hashlib.sha256("empty".encode()).hexdigest()
        
        transaction_hashes = [hashlib.sha256(json.dumps(tx.to_dict(), sort_keys=True).encode()).hexdigest() 
                            for tx in self.transactions]
        
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 == 1:
                transaction_hashes.append(transaction_hashes[-1])
            
            transaction_hashes = [hashlib.sha256((h1 + h2).encode()).hexdigest()
                                for h1, h2 in zip(transaction_hashes[::2], transaction_hashes[1::2])]
        
        return transaction_hashes[0]

    def calculate_hash(self) -> str:
        block_dict = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "merkle_root": self.merkle_root
        }
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self) -> Dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "merkle_root": self.merkle_root,
            "hash": self.hash
        }
