import click
from ..llm_client import ElohimClient
from ..config import load_config
from pathlib import Path


@click.group()
@click.pass_context
def primax(ctx):
    """PRIMAX AI integration — MCP, Nexus, Scanner."""
    ctx.ensure_object(dict)


@primax.command("mcp")
@click.argument("query")
def primax_mcp(query: str):
    """Query via PRIMAX MCP server."""
    client = ElohimClient()
    click.echo(f"[{client.backend_name}]\n")
    answer = client.ask(query)
    click.echo(answer)


@primax.command("nexus")
@click.argument("task")
def primax_nexus(task: str):
    """Run Nexus multi-agent task."""
    import os
    os.environ["PRIMAX_BACKEND"] = "nexus"
    client = ElohimClient()
    click.echo(f"[{client.backend_name}]\n")
    answer = client.ask(task)
    click.echo(answer)


@primax.command("scan")
@click.option("--path", default=".", help="Path to scan")
def primax_scan(path: str):
    """Scan codebase with PRIMAX scanner."""
    import os
    os.environ["PRIMAX_BACKEND"] = "scanner"
    client = ElohimClient()
    click.echo(f"[{client.backend_name}]\n")
    answer = client.ask(f"Scan codebase at {path}")
    click.echo(answer)


@primax.command("status")
def primax_status():
    """Show PRIMAX AI status."""
    import subprocess
    import json
    
    click.echo("=== PRIMAX AI Status ===\n")
    
    # Check Ollama
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        click.echo("Ollama Models:")
        for line in result.stdout.strip().split("\n")[1:]:
            if line.strip():
                click.echo(f"  {line}")
    except Exception as e:
        click.echo(f"  Ollama: {e}")
    
    click.echo()
    
    # Check MCP
    try:
        result = subprocess.run(
            ["python", "-c", "import sys; sys.path.insert(0, '/home/kilisan/primax-ai/src'); from mcp_server.primax_mcp_server import server; print('MCP: OK')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        click.echo(f"MCP Server: {result.stdout.strip()}")
    except Exception as e:
        click.echo(f"MCP Server: Not running")
    
    click.echo()
    
    # Check Nexus adapter
    try:
        from src.nexus_adapter import create_primax_agents
        adapter = create_primax_agents()
        click.echo(f"Nexus Agents: {', '.join(adapter.agents.keys())}")
    except Exception as e:
        click.echo(f"Nexus: {e}")
    
    click.echo()
    
    # Check models
    click.echo("Available Models:")
    click.echo("  - primax-dragon-coder:latest (986MB) ✅")
    click.echo("  - qwen2.5-coder:1.5b (986MB) ✅")
    click.echo("  - qwen2.5:7b (4.7GB) ⚠️")
    click.echo("  - optimus-prime-24b (14GB) ⚠️")


if __name__ == "__main__":
    primax()