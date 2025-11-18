import typer
from datetime import date
from sqlmodel import select

from .db import init_db, get_session
from .models import Challenge
from .coach.generator import generate_challenge
from .coach.grader import grade_solution
from .planner.planner import build_simple_plan

app = typer.Typer(help="Analytics Coach + Smart Day Organizer CLI")


@app.command()
def init() -> None:
    """Initialize the SQLite database."""
    init_db()
    typer.echo("DB initialized.")


@app.command()
def challenge(track: str = typer.Option("python", help="Track name, e.g. python or sql")) -> None:
    """Generate a new challenge via the LLM."""
    ch = generate_challenge(track)
    typer.echo(f"Created challenge #{ch.id}: {ch.title}")
    typer.echo("\nPrompt:\n" + ch.prompt_md)
    typer.echo(f"\nStarter file created: user_solution_{ch.id}.py")


@app.command()
def grade(challenge_id: int, user_code_path: str) -> None:
    """Run the tests for a challenge against your solution file."""
    with get_session() as s:
        ch = s.exec(select(Challenge).where(Challenge.id == challenge_id)).one()
    sub = grade_solution(ch, user_code_path)
    typer.echo(f"Passed: {sub.passed}")
    typer.echo(sub.feedback_md)


@app.command()
def plan() -> None:
    """Create a very small text plan for today based on tasks in the DB."""
    p = build_simple_plan(date.today())
    typer.echo(p.plan_md)


if __name__ == "__main__":  # pragma: no cover
    app()
