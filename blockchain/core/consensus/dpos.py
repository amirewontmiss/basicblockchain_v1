from typing import List, Dict, Optional
import random
import time
from ..block import Block

class DelegatedProofOfStake:
    def __init__(self, num_delegates: int = 21):
        self.num_delegates = num_delegates
        self.delegates: Dict[str, float] = {}  # address -> votes
        self.active_delegates: List[str] = []
        self.votes: Dict[str, str] = {}  # voter -> delegate
        self.round_time = 3  # seconds per delegate
        self.last_round_start = time.time()

    def vote(self, voter: str, delegate: str, voting_power: float) -> bool:
        if delegate not in self.delegates:
            self.delegates[delegate] = 0
        
        # Remove previous vote if exists
        if voter in self.votes:
            old_delegate = self.votes[voter]
            self.delegates[old_delegate] -= voting_power
        
        self.votes[voter] = delegate
        self.delegates[delegate] += voting_power
        self._update_active_delegates()
        return True

    def _update_active_delegates(self):
        sorted_delegates = sorted(self.delegates.items(), key=lambda x: x[1], reverse=True)
        self.active_delegates = [d[0] for d in sorted_delegates[:self.num_delegates]]

    def get_current_delegate(self) -> Optional[str]:
        if not self.active_delegates:
            return None
            
        current_time = time.time()
        elapsed = current_time - self.last_round_start
        round_position = int(elapsed / self.round_time) % len(self.active_delegates)
        return self.active_delegates[round_position]

    async def forge_block(self, delegate: str, block: Block) -> Optional[Block]:
        current_delegate = self.get_current_delegate()
        if delegate != current_delegate:
            return None

        block.hash = block.calculate_hash()
        return block
