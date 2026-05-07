import random
from typing import List

class ShardEvent:
    def __init__(self, name: str, season: int):
        self.name = name
        self.season = season

    def apply_effect(self, arena):
        # Implementation of Refactor Storm: Shuffle all units
        units_to_move = [u for u in arena.units if u.is_alive()]
        for u in units_to_move:
            u.move_to(random.randint(0, arena.width-1), random.randint(0, arena.height-1))
        return "The Refactor Storm shuffles the arena!"
