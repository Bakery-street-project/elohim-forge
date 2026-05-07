import click
import time
from ..engine.battle_engine import BattleEngine
from ..models.arena import Arena
from ..models.unit import Unit
from ..models.faction import FactionName
from rich.console import Console
from rich.table import Table
from rich.live import Live
from collections import Counter
from ..services.supabase_service import get_all_battles

console = Console()

@click.group()
def battle():
    """Simulate and watch shard battles."""

@battle.command("simulate")
@click.option("--factions", default="Python,Rust,C++", help="Comma-separated list of factions.")
@click.option("--size", default=10, help="Arena size.")
def battle_simulate(factions: str, size: int):
    """Run a full battle simulation and show the winner."""
    faction_list = [f.strip() for f in factions.split(",")]
    arena = Arena(width=size, height=size)
    
    for i, fname in enumerate(faction_list):
        try:
            fn = FactionName(fname)
            x = 0 if i % 2 == 0 else size - 1
            y = 0 if i < 2 else size - 1
            arena.add_unit(Unit.create(fn, x=x, y=y))
        except ValueError:
            click.echo(f"Warning: Unknown faction {fname}")

    engine = BattleEngine(arena)
    click.echo(f"Starting battle between: {', '.join(faction_list)}")
    engine.run_to_completion()

    for entry in engine.logs:
        click.echo(entry)

    if engine.winner:
        click.echo(f"\n🏆 WINNER: {engine.winner.value}")
    else:
        click.echo("\n🤝 DRAW: No clear winner.")

@battle.command("watch")
@click.option("--factions", default="Python,Rust,C++", help="Comma-separated list of factions.")
@click.option("--size", default=10, help="Arena size.")
@click.option("--delay", default=0.5, help="Delay between turns in seconds.")
def battle_watch(factions: str, size: int, delay: float):
    """Watch a battle step-by-step using a Rich TUI."""
    faction_list = [f.strip() for f in factions.split(",")]
    arena = Arena(width=size, height=size)
    
    for i, fname in enumerate(faction_list):
        try:
            fn = FactionName(fname)
            x = 0 if i % 2 == 0 else size - 1
            y = 0 if i < 2 else size - 1
            arena.add_unit(Unit.create(fn, x=x, y=y))
        except ValueError:
            click.echo(f"Warning: Unknown faction {fname}")

    engine = BattleEngine(arena)
    
    with Live(_draw_arena_rich(arena), refresh_per_second=4) as live:
        while not engine.is_over and engine.turn_count < 100:
            engine.step()
            live.update(_draw_arena_rich(arena))
            time.sleep(delay)
    
    console.print(f"\n[bold green]Winner: {engine.winner.value}[/bold green]")

@battle.command("leaderboard")
def battle_leaderboard():
    """Display the Shard Wars Leaderboard."""
    data = get_all_battles()
    if not data:
        console.print("[bold red]No battle data available yet.[/bold red]")
        return

    winners = Counter([row['winner'] for row in data])
    
    table = Table(title="Shard Wars Leaderboard")
    table.add_column("Faction", style="cyan")
    table.add_column("Wins", justify="right", style="green")

    for faction, wins in winners.most_common():
        table.add_row(faction, str(wins))
    
    console.print(table)

def _draw_arena_rich(arena: Arena) -> Table:
    table = Table(title="Arena", show_header=False)
    for y in range(arena.height):
        row = []
        for x in range(arena.width):
            if (x, y) == arena.shard_pos:
                row.append("[bold yellow]💎[/bold yellow]")
            else:
                unit = arena.get_unit_at(x, y)
                if unit:
                    row.append(f"[bold red]{unit.faction.value[0]}[/bold red]")
                else:
                    row.append(".")
        table.add_row(*row)
    return table
