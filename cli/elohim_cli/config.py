import os
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent.parent


@dataclass
class ElohimConfig:
    backend: str
    api_key: str
    base_url: str
    model: str
    docs_root: Path
    forge_root: Path


def load_config() -> ElohimConfig:
    docs_root = Path(os.getenv("ELOHIM_DOCS_ROOT", _REPO_ROOT / "docs"))
    forge_root = Path(os.getenv("ELOHIM_FORGE_ROOT", _REPO_ROOT / "forge"))

    nim_key = os.getenv("NIM_API_KEY")
    nim_url = os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
    nim_model = os.getenv("NIM_MODEL", "meta/llama-3.1-8b-instruct")
    
    primax_key = os.getenv("PRIMAX_API_KEY")
    primax_backend = os.getenv("PRIMAX_BACKEND", "nim")  # nim, primax, nexus, scanner

    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if primax_key:
        from .backends.primax_backend import PrimaxMCPBackend, PrimaxNexusBackend, PrimaxScannerBackend
        if primax_backend == "nexus":
            return ElohimConfig("primax-nexus", primax_key, "", "", docs_root, forge_root)
        elif primax_backend == "scanner":
            return ElohimConfig("primax-scanner", primax_key, "", "", docs_root, forge_root)
        else:
            return ElohimConfig("primax", primax_key, "http://localhost:8000", "primax-dragon-coder:latest", docs_root, forge_root)
    if nim_key:
        return ElohimConfig("nim", nim_key, nim_url, nim_model, docs_root, forge_root)
    if gemini_key:
        return ElohimConfig(
            "gemini",
            gemini_key,
            "https://generativelanguage.googleapis.com/v1beta/openai",
            "gemini-2.0-flash",
            docs_root,
            forge_root,
        )
    if openai_key:
        return ElohimConfig(
            "openai", openai_key, "https://api.openai.com/v1", "gpt-4o-mini", docs_root, forge_root
        )

    raise RuntimeError(
        "No LLM backend configured.\n"
        "Set one of: NIM_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY."
    )
