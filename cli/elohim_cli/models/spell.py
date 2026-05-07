from dataclasses import dataclass
from typing import Optional

@dataclass
class Spell:
    code: str
    cost: int
    target_faction: Optional[str] = None
