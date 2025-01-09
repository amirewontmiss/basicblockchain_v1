import asyncio
from typing import Optional
from ..block import Block, Transaction

class ProofOfWork:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.target_block_time = 10  # seconds
        self.adjustment_period = 10  # blocks

    async def mine(self, block: Block) -> Optional[Block]:
        target = "0" * self.difficulty

        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()
            await asyncio.sleep(0)  # Yield to other coroutines

        return block

    def adjust_difficulty(self, blocks: list, current_time: float) -> None:
        if len(blocks) % self.adjustment_period != 0:
            return

        start_time = blocks[-self.adjustment_period].timestamp
        end_time = blocks[-1].timestamp
        actual_time = end_time - start_time
        expected_time = self.target_block_time * self.adjustment_period

        if actual_time < expected_time * 0.5:
            self.difficulty += 1
        elif actual_time > expected_time * 2:
            self.difficulty = max(1, self.difficulty - 1)
