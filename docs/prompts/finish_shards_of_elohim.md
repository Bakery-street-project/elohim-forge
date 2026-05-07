# Super-Engineer Prompt: Finish Shards of Elohim Locally and in Codespaces

You are Codex working in `/workspaces/elohim-forge` on the proprietary PRIMAX AI project Elohim Forge. Preserve the watermark `PRIMAX-AI-ELOHIM-BSP-2025`, keep secrets out of commits, and follow `AGENTS.md`.

## Mission

Finish a playable local vertical slice of **Shards of Elohim** that works both on the developer machine and in GitHub Codespaces. The game must run without GPU, Ollama, paid APIs, Supabase, or blockchain services. Cloud AI backends may remain optional.

## Product Definition

Build a deterministic turn-based arena game based on the lore:

- 13 Shards of Syntax from `docs/01_lore_elohim_shards.md`.
- 9 factions from `docs/02_factions_and_heroes.md`.
- Weekly shard event structure and local NFT-style metadata from `docs/04_shard_events_and_nfts.md`.
- Python CLI is the authoritative game engine.
- Electron UI is a playable/preview shell over the same mechanics.

## First Actions

1. Read `AGENTS.md`, `README.md`, `IMPLEMENTATION_SUMMARY.md`, and the three core docs in `docs/`.
2. Inspect the current CLI engine under `cli/elohim_cli/engine/`, models under `cli/elohim_cli/models/`, and battle command under `cli/elohim_cli/commands/battle.py`.
3. Run:

```bash
cd /workspaces/elohim-forge
python -m pip install -e ./cli
npm install
python cli/elohim.py --help
python cli/elohim.py battle simulate
```

If a command fails, fix the project setup before adding features.

## Scope To Implement

Make the game complete enough that a user can run a local match, watch it, and export results.

- Add a seeded battle mode: `elohim battle simulate --seed <seed> --factions Python,Rust,C++ --shard memory`.
- Add shard definitions as structured data, not loose strings.
- Add faction ability behavior for all nine factions. Use the existing lore names and keep effects simple, readable, and balanced.
- Add shard holding/crystallisation: holding the shard for 3 consecutive turns wins, unless only one faction remains first.
- Add local event generation: seed, shard, arena modifier, participating factions, winner, logs, and metadata JSON.
- Add `elohim battle export --out <path>` or an equivalent flag that writes the latest event result to JSON.
- Add tests for deterministic seed behavior, victory conditions, shard definitions, and at least three faction abilities.
- Make the Electron app able to trigger a simulation and display winner, shard, turn log, and exported metadata without needing API keys.

## Codespaces Requirements

- Keep `.devcontainer/devcontainer.json` working with Python 3.12 and Node 20.
- Do not require desktop GUI support for basic verification in Codespaces. Provide a CLI path and, if needed, a browser/static preview path.
- Document Codespaces launch commands in `README.md`:

```bash
python -m pip install -e ./cli
npm install
python cli/elohim.py battle simulate --seed demo --factions Python,Rust,C++ --shard memory
```

## Quality Bar

- Deterministic output for the same seed.
- No hidden dependency on `.env`, Supabase, Ollama, or paid APIs.
- No broad rewrites unrelated to game completion.
- Use structured data classes/enums where they clarify rules.
- Keep turn logs human-readable.
- Keep docs honest: update README only for commands that actually work.

## Verification Before Final Answer

Run and report:

```bash
python -m pip install -e ./cli
python cli/elohim.py --help
python cli/elohim.py battle simulate --seed demo --factions Python,Rust,C++ --shard memory
python -m pytest cli/tests
npm install
npm start
```

If Electron cannot be launched in Codespaces, state that and verify the CLI plus any browser-safe preview instead. Finish with a concise summary of files changed, commands run, and remaining risks.
