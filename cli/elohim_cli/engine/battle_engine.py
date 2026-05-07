import random
from typing import List, Dict, Tuple
from ..models.arena import Arena
from ..models.unit import Unit
from ..models.faction import FactionName

from ..sandbox.sandbox import DragonDreamSandbox
from ..models.spell import Spell

from ..engine.shard_event import ShardEvent

class BattleEngine:
    def __init__(self, arena: Arena):
        self.arena = arena
        self.turn_count = 0
        self.logs: List[str] = []
        self.is_over = False
        self.winner: Optional[FactionName] = None
        self.sandbox = DragonDreamSandbox()
        self.event = ShardEvent("Refactor Storm", season=1)

    def cast_spell(self, spell: Spell, caster: Unit):
        self.log(f"{caster.name} is casting a spell!")
        # Define context with limited access to game state
        context = {
            "caster": caster,
            "arena": self.arena,
            "log": self.log
        }
        success, error = self.sandbox.execute(spell.code, context)
        if success:
            self.log("Spell cast successfully.")
        else:
            self.log(f"Spell failed: {error}")

    def log(self, message: str):
        self.logs.append(f"Turn {self.turn_count}: {message}")

    def step(self):
        if self.is_over:
            return

        self.turn_count += 1
        self.log(f"--- Turn {self.turn_count} Start ---")
        
        # Every 5 turns, trigger event
        if self.turn_count % 5 == 0:
            msg = self.event.apply_effect(self.arena)
            self.log(f"EVENT: {msg}")

        # Order units by speed
        active_units = sorted([u for u in self.arena.units if u.is_alive()], 
                             key=lambda u: u.speed, reverse=True)

        for unit in active_units:
            if not unit.is_alive():
                continue
            
            # Status effect cleanup (reduce duration)
            if "Shielded" in unit.status_effects:
                # The logic was removing all occurrences, let's refine:
                unit.status_effects = [s for s in unit.status_effects if s != "Shielded"]
            
            self._handle_unit_turn(unit)

        self._check_victory_conditions()
        self.arena.remove_dead_units()

    def _handle_unit_turn(self, unit: Unit):
        # Handle deferred damage for Haskell / Lazy Evaluation
        if unit.deferred_damage > 0:
            self.log(f"Lazy Evaluation resolved: {unit.name} takes {unit.deferred_damage} deferred damage.")
            unit.take_damage(unit.deferred_damage)
            unit.deferred_damage = 0
            if not unit.is_alive():
                self.log(f"{unit.name} has been eliminated by deferred side-effects!")
                return

        # Check for status effects (e.g., Borrow Checker)
        if "Borrowed" in unit.status_effects:
            self.log(f"{unit.name} is locked by the Borrow Checker and cannot move!")
            unit.status_effects.remove("Borrowed")
            return

        # 1. Simple AI: Move towards the shard
        target_x, target_y = self.arena.shard_pos
        
        # If already at shard, maybe attack nearby enemies
        if (unit.x, unit.y) != (target_x, target_y):
            self._move_towards(unit, target_x, target_y)

        # 2. Use Ability if available
        if unit.ability:
            self._use_ability(unit)
        
        # 3. Standard Attack if ability didn't consume turn or wasn't used
        self._unit_attack_nearby(unit)

    def _use_ability(self, unit: Unit):
        # Implementation of RPG-derived abilities
        if unit.ability == "ParallelShock":
            # Hits all units in a 2x2 area
            for neighbor in self.arena.get_neighbors(unit.x, unit.y):
                target = self.arena.get_unit_at(*neighbor)
                if target and target.faction != unit.faction:
                    target.take_damage(unit.damage // 2)

        elif unit.ability == "DuckCast":
            # Copy a neighbor's ability
            for neighbor in self.arena.get_neighbors(unit.x, unit.y):
                target = self.arena.get_unit_at(*neighbor)
                if target and target.ability and target.ability != "DuckCast":
                    original = unit.ability
                    unit.ability = target.ability
                    self._use_ability(unit)
                    unit.ability = original
                    return

        elif unit.ability == "VMShield":
            # Just Armor (temporary health boost removed)
            if "Shielded" not in unit.status_effects:
                # Add defense buff instead of heal
                unit.status_effects.append("Shielded")
                unit.status_effects.append("Shielded")
                self.log(f"{unit.name} casts VMShield; armor hardened.")
            else:
                self.log(f"{unit.name} attempts VMShield, but it's on cooldown.")

        elif unit.ability == "PointerCrush":
            # Ignore defense - high damage
            for neighbor in self.arena.get_neighbors(unit.x, unit.y):
                target = self.arena.get_unit_at(*neighbor)
                if target and target.faction != unit.faction:
                    target.take_damage(int(unit.damage * 1.8))
                    return

        elif unit.ability == "CallbackTrap":
            # Set a trap on self (if enemy steps on it, take damage)
            unit.status_effects.append("TrapSet")
            self.log(f"{unit.name} set a CallbackTrap.")

        elif unit.ability == "OwnershipLock":
            # Immobilize (limit to 1 turn)
            for neighbor in self.arena.get_neighbors(unit.x, unit.y):
                target = self.arena.get_unit_at(*neighbor)
                if target and target.faction != unit.faction:
                    self.log(f"{unit.name} uses Borrow Checker on {target.name}!")
                    if "Borrowed" not in target.status_effects:
                        target.status_effects.append("Borrowed")
                    return

        elif unit.ability == "RoutineSpeed":
            # Haste: double movement this turn
            unit.speed *= 2
            self.log(f"{unit.name} gains haste!")

        elif unit.ability == "QueryReveal":
            # Reveal all (AOE hit)
            for other in self.arena.units:
                if other.faction != unit.faction:
                    other.take_damage(5)

        elif unit.ability == "LazyDamage":
            # Bank damage (penalized for being lazy)
            for neighbor in self.arena.get_neighbors(unit.x, unit.y):
                target = self.arena.get_unit_at(*neighbor)
                if target and target.faction != unit.faction:
                    self.log(f"{unit.name} thunks {target.name} (damage deferred)!")
                    target.deferred_damage += (unit.damage // 2)
                    return

    def _move_towards(self, unit: Unit, tx: int, ty: int):
        # Move up to unit.speed steps
        for _ in range(unit.speed):
            dx = 1 if tx > unit.x else (-1 if tx < unit.x else 0)
            dy = 1 if ty > unit.y else (-1 if ty < unit.y else 0)
            
            new_x, new_y = unit.x + dx, unit.y + dy
            
            if self.arena.is_within_bounds(new_x, new_y) and not self.arena.get_unit_at(new_x, new_y):
                unit.move_to(new_x, new_y)
            else:
                # Try moving only X or only Y if diagonal is blocked
                if dx != 0 and self.arena.is_within_bounds(unit.x + dx, unit.y) and not self.arena.get_unit_at(unit.x + dx, unit.y):
                    unit.move_to(unit.x + dx, unit.y)
                elif dy != 0 and self.arena.is_within_bounds(unit.x, unit.y + dy) and not self.arena.get_unit_at(unit.x, unit.y + dy):
                    unit.move_to(unit.x, unit.y + dy)
                else:
                    break # Blocked

    def _unit_attack_nearby(self, unit: Unit):
        # Find closest enemy within range
        for neighbor in self.arena.get_neighbors(unit.x, unit.y):
            target = self.arena.get_unit_at(*neighbor)
            if target and target.faction != unit.faction:
                damage = unit.damage
                # Apply shield reduction
                if "Shielded" in target.status_effects:
                    damage = max(1, damage // 3)
                    self.log(f"{target.name} shield absorbs damage!")
                
                # Vulnerability phase: If target recently had a shield but doesn't now, they are 'brittle'
                # (We track this by a 'Shielded' status effect and a 'Brittle' status effect)
                
                self.log(f"{unit.name} attacks {target.name} for {damage} damage.")
                target.take_damage(damage)
                if not target.is_alive():
                    self.log(f"{target.name} has been eliminated!")
                return # Only one attack per turn

    def _check_victory_conditions(self):
        # Victory if only one faction remains or someone holds the shard for 5 turns
        alive_factions = set(u.faction for u in self.arena.units if u.is_alive())
        
        if len(alive_factions) == 1:
            self.winner = list(alive_factions)[0]
            self.is_over = True
            self.log(f"VICTORY: {self.winner.value} faction has conquered the arena!")
        elif len(alive_factions) == 0:
            self.is_over = True
            self.log("DRAW: All factions have been eliminated.")

    def run_to_completion(self, max_turns: int = 100):
        while not self.is_over and self.turn_count < max_turns:
            self.step()
        if self.turn_count >= max_turns:
            self.log("TIMEOUT: The battle ended in a stalemate.")
        
        if self.winner:
            from ..services.supabase_service import log_battle
            log_battle(self.winner.value, self.logs)

from typing import Optional
