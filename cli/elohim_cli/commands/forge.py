import re
import click
from datetime import datetime
from ..llm_client import ElohimClient
from ..config import load_config


@click.group()
def forge():
    """Idea inbox and roadmap for Code Elohim."""


@forge.command("idea")
@click.argument("description")
@click.option("--area", default="general", show_default=True,
              help="Area tag: ai, backend, game, factions, shards, art, lore")
@click.option("--title", default="", help="Optional title override.")
def forge_idea(description: str, area: str, title: str):
    """Submit a new idea to the Forge."""
    cfg = load_config()
    slug = re.sub(r"[^a-z0-9]+", "-", description.lower())[:50].strip("-")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = title or description[:60]

    out_dir = cfg.forge_root / "ideas" / area
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{ts}_{slug}.md"

    content = (
        f"# {safe_title}\n"
        f"_Area: {area} | Created: {datetime.now().isoformat()}_\n\n"
        f"{description}\n"
    )
    out.write_text(content)
    click.echo(f"Idea saved → {out}")


@forge.command("list")
@click.option("--area", default="", help="Filter by area tag.")
def forge_list(area: str):
    """List all ideas in the Forge."""
    cfg = load_config()
    base = cfg.forge_root / "ideas"
    pattern = f"**/{area}/**/*.md" if area else "**/*.md"
    files = sorted(base.glob(pattern if area else "**/*.md"))

    if not files:
        click.echo("No ideas yet. Use `elohim forge idea` to add one.")
        return

    click.echo(f"\n Forge Ideas ({len(files)} total)\n" + "─" * 44)
    for f in files:
        area_tag = f.parent.name
        click.echo(f"  [{area_tag}] {f.stem}")
    click.echo()


@forge.command("cluster")
@click.option("--save", is_flag=True, help="Write roadmap to docs/06_roadmap.md.")
def forge_cluster(save: bool):
    """Read all ideas and generate a clustered roadmap."""
    cfg = load_config()
    base = cfg.forge_root / "ideas"
    files = sorted(base.glob("**/*.md"))

    if not files:
        click.echo("No ideas to cluster yet.")
        return

    ideas_text = ""
    for f in files:
        ideas_text += f"\n### {f.stem} [{f.parent.name}]\n{f.read_text()}\n"

    client = ElohimClient()
    prompt = (
        "Here are all current Elohim Forge ideas:\n\n"
        f"{ideas_text}\n\n"
        "Cluster these into 4-6 themes. For each theme: name it, list the ideas under it, "
        "and write a 2-sentence roadmap statement. Output as clean markdown."
    )
    click.echo(f"[{client.backend_name}]\n")
    roadmap = client.ask(prompt)
    click.echo(roadmap)

    if save:
        out = cfg.docs_root / "06_roadmap.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            f"# Elohim Forge Roadmap\n_Generated: {datetime.now().isoformat()}_\n\n{roadmap}\n"
        )
        click.echo(f"\n→ Saved to {out}")
