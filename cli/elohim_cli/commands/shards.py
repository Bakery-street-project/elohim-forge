import click
from datetime import datetime
from ..llm_client import ElohimClient
from ..config import load_config


@click.group()
def shards():
    """Explain and propose shard events."""


@shards.command("explain")
def shards_explain():
    """Explain the shard system."""
    cfg = load_config()
    client = ElohimClient()
    doc = cfg.docs_root / "04_shard_events_and_nfts.md"
    answer = client.ask(
        "Explain the Shard system in Code Elohim: what shards are, how they are earned, "
        "their rarity tiers, the ERC-721 NFT mechanic, and how weekly shard events work.",
        context_files=[doc],
    )
    click.echo(f"[{client.backend_name}]\n")
    click.echo(answer)


@shards.command("propose-event")
@click.option("--season", default=1, show_default=True, help="Season number.")
@click.option("--save", is_flag=True, help="Save proposal to forge/ideas/shards/.")
def shards_propose_event(season: int, save: bool):
    """Generate a new shard event proposal."""
    cfg = load_config()
    client = ElohimClient()
    doc = cfg.docs_root / "04_shard_events_and_nfts.md"

    prompt = (
        f"Propose a new shard event for Season {season} of Code Elohim.\n"
        "Include: event name, theme, special rules, shard reward tier, arena modifiers, "
        "and one unique twist that hasn't appeared before."
    )
    click.echo(f"[{client.backend_name}]\n")
    proposal = client.ask(prompt, context_files=[doc])
    click.echo(proposal)

    if save:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = cfg.forge_root / "ideas" / "shards" / f"season{season}_event_{ts}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f"# Shard Event — Season {season}\n_Generated: {datetime.now().isoformat()}_\n\n{proposal}\n")
        click.echo(f"\n→ Saved to {out}")
