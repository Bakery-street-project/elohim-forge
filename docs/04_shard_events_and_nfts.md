# Shard Events & NFT System

## Weekly Shard Events

Every **Sunday at midnight UTC** a shard manifests in the Digital Cosmos. The event runs for 24h.

### Event Structure
1. **Spawn Phase (0h):** A shard appears in a procedurally generated arena. Arena seed is derived
   from block hash + shard domain to ensure unpredictability.
2. **Battle Phase (0–20h):** Factions deploy heroes and armies. Turn-based combat. Shard node
   must be held for 3 consecutive turns to begin crystallisation.
3. **Crystallisation Phase (20–23h):** Holding faction locks the shard. Other factions can still
   raid but face a defence bonus.
4. **Mint Phase (23–24h):** Shard is minted as ERC-721 NFT to the winning faction's treasury.

### Arena Modifiers (rolled per event)
- **Fog of War** — enemy positions hidden until adjacent
- **Gravity Storm** — all units move 1 tile backwards per turn
- **Syntax Error Zone** — random ability misfire chance 20%
- **Overclock Arena** — all units get +1 action per turn
- **Memory Leak Field** — all units lose 2 HP per turn regardless of shields

## Shard NFT System

Each crystallised shard is an ERC-721 token with the following on-chain metadata:

```json
{
  "name": "The Shard of Recursion #47",
  "domain": "recursion",
  "rarity": "legendary",
  "season": 1,
  "winning_faction": "Haskell",
  "arena_seed": "0x4a3f...",
  "buffs": {
    "recursion_depth": "+2",
    "stack_resistance": "+15%"
  },
  "lore": "Claimed in the Fog of War arena by the Monad Mystics on the 13th Sunday."
}
```

### Rarity Tiers & Drop Rates
| Tier | Probability | Max Supply |
|------|-------------|------------|
| Common | 40% | Unlimited |
| Uncommon | 30% | 10,000 |
| Rare | 20% | 1,000 |
| Epic | 7% | 100 |
| Legendary | 2.5% | 13 |
| Mythic | 0.5% | 1 (The Shard of Origin) |

### In-Game Use
Holding a shard NFT in your wallet grants permanent passive buffs during battle.
Shards can be staked in the Saloon for yield (faction treasury funding).
Three shards of the same domain can be fused into a higher-rarity version.
