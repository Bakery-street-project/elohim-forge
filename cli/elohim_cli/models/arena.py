from typing import List, Dict, Optional, Tuple
from .unit import Unit

class Arena:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.units: List[Unit] = []
        self.shard_pos: Tuple[int, int] = (width // 2, height // 2)

    def add_unit(self, unit: Unit):
        self.units.append(unit)

    def get_unit_at(self, x: int, y: int) -> Optional[Unit]:
        for unit in self.units:
            if unit.x == x and unit.y == y and unit.is_alive():
                return unit
        return None

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.is_within_bounds(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def remove_dead_units(self):
        self.units = [u for u in self.units if u.is_alive()]

    def __repr__(self):
        return f"Arena({self.width}x{self.height}, Units: {len(self.units)})"
