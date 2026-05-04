import click
from ..llm_client import ElohimClient
from ..config import load_config


@click.group()
def lore():
    """Query the Code Elohim lore and universe."""


@lore.command("ask")
@click.argument("question")
@click.option("--all-docs", is_flag=True, help="Load all lore docs as context.")
def lore_ask(question: str, all_docs: bool):
    """Ask Elohim a lore question."""
    cfg = load_config()
    client = ElohimClient()

    doc_files = []
    if all_docs:
        doc_files = sorted(cfg.docs_root.glob("*.md"))
    else:
        doc_files = [cfg.docs_root / "01_lore_elohim_shards.md"]

    click.echo(f"[{client.backend_name}]\n")
    answer = client.ask(question, context_files=doc_files)
    click.echo(answer)
