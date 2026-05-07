import click
from ..llm_client import ElohimClient
from ..config import load_config
import subprocess
import json


@click.group()
def github():
    """GitHub integration — repo analysis, PR workflows."""


@github.command("analyze")
@click.argument("repo")
def github_analyze(repo: str):
    """Analyze a GitHub repository."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", repo, "--json", "name,description,stargazerCount,forkCount,primaryLanguage,createdAt"],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            click.echo(f"Repository: {data['name']}")
            click.echo(f"Description: {data['description']}")
            click.echo(f"Stars: {data['stargazerCount']}")
            click.echo(f"Forks: {data['forkCount']}")
            click.echo(f"Language: {data['primaryLanguage']['name'] if data['primaryLanguage'] else 'N/A'}")
            click.echo(f"Created: {data['createdAt']}")
        else:
            click.echo(f"Error: {result.stderr}")
    except Exception as e:
        click.echo(f"Error: {e}")


@github.command("org")
@click.argument("org")
def github_org(org: str):
    """Analyze a GitHub organization."""
    try:
        result = subprocess.run(
            ["gh", "repo", "list", org, "--limit", "20", "--json", "name,description,stargazerCount,primaryLanguage"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            repos = json.loads(result.stdout)
            click.echo(f"\n{org} — {len(repos)} repositories\n")
            for r in repos:
                lang = r['primaryLanguage']['name'] if r['primaryLanguage'] else 'N/A'
                click.echo(f"  {r['name']:<30} {lang:<12} ⭐ {r['stargazerCount']}")
                if r['description']:
                    click.echo(f"    {r['description'][:80]}")
        else:
            click.echo(f"Error: {result.stderr}")
    except Exception as e:
        click.echo(f"Error: {e}")


@github.command("pr")
@click.option("--title", prompt="PR title", help="PR title")
@click.option("--body", prompt="PR body", help="PR description")
@click.option("--base", default="main", help="Base branch")
def github_pr(title: str, body: str, base: str):
    """Create a pull request."""
    try:
        result = subprocess.run(
            ["gh", "pr", "create", "--title", title, "--body", body, "--base", base],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            click.echo(f"PR created: {result.stdout.strip()}")
        else:
            click.echo(f"Error: {result.stderr}")
    except Exception as e:
        click.echo(f"Error: {e}")


if __name__ == "__main__":
    github()