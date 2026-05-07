from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class FactionName(str, Enum):
    SPARK = "Spark"
    PYTHON = "Python"
    JAVA = "Java"
    CPP = "C++"
    JAVASCRIPT = "JavaScript"
    RUST = "Rust"
    GO = "Go"
    SQL = "SQL"
    HASKELL = "Haskell"

@dataclass
class FactionTrait:
    name: str
    description: str
    speed_modifier: float = 1.0
    damage_modifier: float = 1.0
    health_modifier: float = 1.0

FACTION_DATA = {
    FactionName.SPARK: FactionTrait("The Hive", "Swarm execution.", speed_modifier=1.4, health_modifier=1.0),
    FactionName.PYTHON: FactionTrait("Serpent Clan", "Generalist adaptability.", speed_modifier=1.0, damage_modifier=1.0),
    FactionName.JAVA: FactionTrait("Empire Builders", "Fortress and endurance.", health_modifier=0.1, speed_modifier=0.1, damage_modifier=0.01),

    FactionName.CPP: FactionTrait("Forge Warriors", "High burst damage.", damage_modifier=2.0, health_modifier=0.6),
    FactionName.JAVASCRIPT: FactionTrait("Web Weavers", "Trap mastery.", speed_modifier=1.1, health_modifier=0.9),
    FactionName.RUST: FactionTrait("Iron Guard", "Ownership tanks.", health_modifier=1.3, damage_modifier=0.9),
    FactionName.GO: FactionTrait("Concurrency Corps", "Coordination & speed.", speed_modifier=1.8, health_modifier=0.9),
    FactionName.SQL: FactionTrait("Query Keepers", "Information dominance.", damage_modifier=1.5, health_modifier=1.0),
    FactionName.HASKELL: FactionTrait("Monad Mystics", "Delayed effect chains.", damage_modifier=1.1, health_modifier=0.8),
}
