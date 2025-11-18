from datetime import date
import json
from typing import Dict, Any

from ..db import get_session
from ..models import Challenge
from ..llm import complete_json
from . import templates

def _parse_json_or_raise(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            "Model did not return valid JSON. Raw text was:\n" + text
        ) from e

def generate_challenge(track: str = "python") -> Challenge:
    """Ask the LLM for a challenge, store it, and create DB row."""
    system_prompt = templates.CHALLENGE_SYSTEM_PROMPT
    user_prompt = templates.challenge_user_prompt(track)
    raw = complete_json(system_prompt, user_prompt)
    data = _parse_json_or_raise(raw)

    ch = Challenge(
        date=date.today(),
        track=track,
        title=data["title"],
        prompt_md=data["prompt_md"],
        solution_stub=data.get("solution_stub", ""),
        tests_py=data.get("tests_py", ""),
        difficulty=data.get("difficulty", "normal"),
    )
    with get_session() as s:
        s.add(ch)
        s.commit()
        s.refresh(ch)

    # Also write a starter file next to where the CLI is run from.
    file_name = f"user_solution_{ch.id}.py"
    with open(file_name, "w", encoding="utf-8") as f:
        stub = ch.solution_stub or "# Write your solution here\n"
        f.write(stub)

    return ch
