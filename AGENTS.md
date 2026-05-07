# AGENTS.md - Elohim Forge

Elohim Forge is a proprietary PRIMAX AI project. Preserve the `PRIMAX-AI-ELOHIM-BSP-2025` watermark and do not remove sponsorship, license, or ownership language.

## Project Shape

- Root Electron shell: `main.js`, `index.html`, `package.json`.
- Python CLI: `cli/elohim.py`, package code under `cli/elohim_cli/`.
- Game battle logic: `cli/elohim_cli/engine/`, `cli/elohim_cli/models/`, `cli/elohim_cli/commands/battle.py`.
- Lore and game design source of truth: `docs/01_lore_elohim_shards.md`, `docs/02_factions_and_heroes.md`, `docs/04_shard_events_and_nfts.md`, and `docs/lore/`.

## Local Commands

Run Python commands from `elohim-forge/cli/` unless stated otherwise.

```bash
python -m pip install -e .
python elohim.py --help
python elohim.py faction list
python elohim.py battle simulate
python elohim.py battle watch --delay 0.2
```

Run Electron commands from `elohim-forge/`.

```bash
npm install
npm start
npm run build:linux
```

## Engineering Rules

- Keep Python dependencies in `cli/pyproject.toml`; do not add Poetry or Pipenv.
- Keep Node dependencies in root `package.json`.
- Prefer deterministic game mechanics with optional seeded randomness so battles can be tested.
- Add focused tests when changing shared game logic. If no test harness exists yet, create small unit tests close to the Python engine rather than broad integration tests.
- Keep Electron security in mind. Avoid widening `nodeIntegration` or command execution surfaces; prefer explicit IPC commands over shell-string parsing.
- Treat API keys, sponsor data, Supabase config, and `.env` files as sensitive. Do not print or commit secrets.
- Codespaces has no local GPU/Ollama guarantee. Cloud API backends may be wired by environment variables, but the game must run without them.

## Product Direction

The near-term target is a playable local "Shards of Elohim" experience:

- A deterministic turn-based arena around the 13 Shards of Syntax.
- Nine factions with distinct, readable mechanics from the lore docs.
- A useful CLI loop and an Electron preview that can run in Codespaces.
- Save/export battle logs and shard event outcomes.
- No blockchain minting required for the first playable slice; model NFT metadata locally as JSON.
