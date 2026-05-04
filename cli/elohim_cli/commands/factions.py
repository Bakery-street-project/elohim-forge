import re
import click
from datetime import datetime
from ..llm_client import ElohimClient
from ..config import load_config

_KNOWN_FACTIONS = ["Spark", "Python", "Java", "C++", "JavaScript", "Rust", "Go", "SQL", "Haskell"]


@click.group()
def faction():
    """Manage and design factions."""


@faction.command("list")
def faction_list():
    """List the 9 core factions."""
    cfg = load_config()
    doc = cfg.docs_root / "02_factions_and_heroes.md"
    if doc.exists():
        client = ElohimClient()
        answer = client.ask(
            "List all factions with a one-sentence description of each.",
            context_files=[doc],
        )
        click.echo(answer)
    else:
        for f in _KNOWN_FACTIONS:
            click.echo(f"  • {f}")


@faction.command("design")
@click.argument("brief")
@click.option("--save", is_flag=True, help="Save spec to forge/ideas/factions/.")
def faction_design(brief: str, save: bool):
    """Design a new faction from a brief description."""
    cfg = load_config()
    client = ElohimClient()

    prompt = (
        f"Design a new faction for Code Elohim based on this brief: '{brief}'.\n"
        "Include: name, origin story, primary ability, weaknesses, and hero unit.\n"
        "Format as a concise faction spec."
    )
    context = [cfg.docs_root / "02_factions_and_heroes.md"]
    click.echo(f"[{client.backend_name}]\n")
    spec = client.ask(prompt, context_files=context)
    click.echo(spec)

    if save:
        slug = re.sub(r"[^a-z0-9]+", "-", brief.lower())[:40].strip("-")
        out = cfg.forge_root / "ideas" / "factions" / f"{slug}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f"# Faction: {brief}\n_Generated: {datetime.now().isoformat()}_\n\n{spec}\n")
        click.echo(f"\n→ Saved to {out}")
