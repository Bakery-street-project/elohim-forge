#!/usr/bin/env python3
"""Elohim CLI — lore oracle and dev orchestrator for Code Elohim."""

import click
from elohim_cli.commands import lore, faction, shards, tools, forge, battle
from elohim_cli.commands.primax import primax
from elohim_cli.commands.github import github


@click.group()
@click.version_option("0.1.0", prog_name="elohim")
def cli():
    """Elohim — ancient code deity. Lore oracle + Super-Brain orchestrator.

    \b
    Backend priority: NIM_API_KEY → GEMINI_API_KEY → OPENAI_API_KEY → PRIMAX

    \b
    Quick start:
      elohim lore ask "What are the 13 shards?"
      elohim faction list
      elohim battle simulate
      elohim battle watch --delay 0.2
      elohim shards propose-event --season 1 --save
      elohim primax status
      elohim github org bakery-street-project
    """


cli.add_command(lore)
cli.add_command(faction)
cli.add_command(shards)
cli.add_command(tools)
cli.add_command(forge)
cli.add_command(battle)
cli.add_command(primax)
cli.add_command(github)


if __name__ == "__main__":
    cli()
