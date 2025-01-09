import random
from typing import Dict, Optional
from ..block import Block

class ProofOfStake:
    def __init__(self):
        self.validators: Dict[str, float] = {}
        self.minimum_stake = 1000
        self.block_time = 5  # seconds

    def add_validator(self, address: str, stake: float) -> bool:
        if stake >= self.minimum_stake:
            self.validators[address] = stake
            return True
        return False

    def remove_validator(self, address: str) -> bool:
        if address in self.validators:
            del self.validators[address]
            return True
        return False

    def select_validator(self) -> Optional[str]:
        if not self.validators:
            return None

        total_stake = sum(self.validators.values())
        target = random.uniform(0, total_stake)
        current_sum = 0

        for address, stake in self.validators.items():
            current_sum += stake
            if current_sum >= target:
                return address

        return None

    async def forge_block(self, validator: str, block: Block) -> Optional[Block]:
        if validator not in self.validators:
            return None

        # Validator is selected, they can forge the block immediately
        block.hash = block.calculate_hash()
        return block
