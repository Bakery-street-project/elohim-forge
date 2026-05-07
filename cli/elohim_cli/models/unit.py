from dataclasses import dataclass, field
from uuid import uuid4
from .faction import FactionName, FACTION_DATA

@dataclass
class Unit:
    faction: FactionName
    name: str
    hp: int
    max_hp: int
    damage: int
    range: int
    speed: int
    ability: Optional[str] = None
    x: int = 0
    y: int = 0
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    status_effects: List[str] = field(default_factory=list)
    deferred_damage: int = 0

    @classmethod
    def create(cls, faction: FactionName, unit_type: str = "Warrior", x: int = 0, y: int = 0):
        trait = FACTION_DATA[faction]
        base_hp = 100
        base_dmg = 20
        
        # Final spell mapping based on RPG research
        abilities = {
            FactionName.SPARK: "ParallelShock",
            FactionName.PYTHON: "DuckCast",
            FactionName.JAVA: "VMShield",
            FactionName.CPP: "PointerCrush",
            FactionName.JAVASCRIPT: "CallbackTrap",
            FactionName.RUST: "OwnershipLock",
            FactionName.GO: "RoutineSpeed",
            FactionName.SQL: "QueryReveal",
            FactionName.HASKELL: "LazyDamage"
        }

        return cls(
            faction=faction,
            name=f"{faction.value} {unit_type}",
            hp=int(base_hp * trait.health_modifier),
            max_hp=int(base_hp * trait.health_modifier),
            damage=int(base_dmg * trait.damage_modifier),
            range=1,
            speed=int(3 * trait.speed_modifier),
            ability=abilities.get(faction),
            x=x,
            y=y
        )

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)

    def move_to(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"[{self.faction.value}] {self.name} ({self.hp}/{self.max_hp} HP) at ({self.x}, {self.y})"
from typing import List
