from pathlib import Path
from .config import ElohimConfig, load_config
from .backends import (
    BaseBackend, NvidiaNimBackend, GeminiBackend, OpenAIBackend,
    PrimaxMCPBackend, PrimaxNexusBackend, PrimaxScannerBackend
)

_ELOHIM_SYSTEM = """You are Elohim — an ancient code deity and lore oracle of the Code Elohim universe.

You know everything about:
- The 9 Factions: Spark, Python, Java, C++, JavaScript, Rust, Go, SQL, Haskell.
- The Shard system: weekly shard events, ERC-721 shard NFTs, rarity tiers, spawning rules.
- The Battle system: turn-based card/dice combat, faction abilities, hero units.
- The Dragon Dream Engine: containerised code execution sandbox within the game world.
- The Super-Brain toolchain: RamaLama, uv, LangGraph, CrewAI, AutoGen, SNN frameworks,
  Godot game engine, Android toolchain, openSUSE Tumbleweed, Podman/Docker.
- The Forge: the idea pipeline and roadmap for Code Elohim.

Speak with authority and precision. When asked lore questions, stay in-universe.
When asked tooling questions, give concrete shell commands and configs.
Keep answers focused and actionable."""


def _build_backend(cfg: ElohimConfig) -> BaseBackend:
    if cfg.backend == "nim":
        return NvidiaNimBackend(cfg.base_url, cfg.api_key, cfg.model)
    if cfg.backend == "gemini":
        return GeminiBackend(cfg.api_key, cfg.model)
    if cfg.backend == "openai":
        return OpenAIBackend(cfg.api_key, cfg.model)
    if cfg.backend == "primax":
        return PrimaxMCPBackend(cfg.base_url)
    if cfg.backend == "primax-nexus":
        return PrimaxNexusBackend()
    if cfg.backend == "primax-scanner":
        return PrimaxScannerBackend()
    raise ValueError(f"Unknown backend: {cfg.backend}")


def _read_doc(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


class ElohimClient:
    def __init__(self):
        self.cfg = load_config()
        self.backend = _build_backend(self.cfg)

    def chat(self, messages: list[dict], context_files: list[Path] | None = None) -> str:
        system = _ELOHIM_SYSTEM
        if context_files:
            docs = "\n\n---\n\n".join(
                f"# {f.name}\n{_read_doc(f)}" for f in context_files if f.exists()
            )
            if docs:
                system += f"\n\n## Relevant documents\n\n{docs}"
        return self.backend.chat(messages, system=system)

    def ask(self, prompt: str, context_files: list[Path] | None = None) -> str:
        return self.chat([{"role": "user", "content": prompt}], context_files)

    @property
    def backend_name(self) -> str:
        return self.backend.name
