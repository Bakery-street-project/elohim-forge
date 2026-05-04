import shutil
import subprocess
import click


def _check(cmd: list[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        first_line = (result.stdout or result.stderr).strip().splitlines()[0]
        return first_line[:60] if first_line else "installed"
    except FileNotFoundError:
        return None
    except Exception:
        return None


@click.group()
def tools():
    """Check and query the Super-Brain dev toolchain."""


@tools.command("status")
def tools_status():
    """Show status of all Super-Brain tools."""
    checks = [
        ("ramalama",   ["ramalama", "--version"]),
        ("uv",         ["uv", "--version"]),
        ("podman",     ["podman", "--version"]),
        ("docker",     ["docker", "--version"]),
        ("godot",      ["godot", "--version"]),
        ("adb",        ["adb", "--version"]),
        ("python",     ["python3", "--version"]),
        ("go",         ["go", "version"]),
        ("deno",       ["deno", "--version"]),
        ("supabase",   ["supabase", "--version"]),
        ("git",        ["git", "--version"]),
    ]

    click.echo("\n Super-Brain Toolchain Status\n" + "─" * 44)
    for name, cmd in checks:
        version = _check(cmd)
        if version:
            click.echo(f"  {'OK':>3}  {name:<12} {version}")
        else:
            click.echo(click.style(f"  {'--':>3}  {name:<12} not found", fg="yellow"))

    # Python venv check
    venv = shutil.which("python3")
    click.echo("\n  Venv: " + (venv or "none"))
    click.echo()


@tools.command("suggest")
@click.argument("goal")
def tools_suggest(goal: str):
    """Get step-by-step guidance for a dev task using your toolchain."""
    from ..llm_client import ElohimClient
    client = ElohimClient()
    prompt = (
        f"I want to: {goal}\n\n"
        "Using my Super-Brain stack (openSUSE Tumbleweed, uv, RamaLama, Podman, Godot 4, "
        "Android SDK/adb, Supabase CLI, NVIDIA GPU), give me a concrete step-by-step plan "
        "with exact shell commands. Be specific to my stack."
    )
    click.echo(f"[{client.backend_name}]\n")
    click.echo(client.ask(prompt))
