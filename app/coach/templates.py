CHALLENGE_SYSTEM_PROMPT = """
You are an experienced analytics mentor.
You generate *small* coding or data challenges that can be solved in under 20 minutes.
Always respond with a single JSON object and nothing else.
"""

def challenge_user_prompt(track: str) -> str:
    track = track.lower()
    if track == "python":
        domain_hint = "Python data wrangling / small algorithms"
    elif track == "sql":
        domain_hint = "SQL queries over a small schema"
    else:
        domain_hint = f"Basic {track} analytics practice"

    return f"""
Create one small {track} challenge.

Return **only** a JSON object with the following keys:

- "title": short title string
- "prompt_md": markdown instructions for the user
- "solution_stub": starter code (for Python) or empty string
- "tests_py": pytest tests that import from `user_solution`
- "difficulty": "easy" | "normal" | "hard"

The task should be realistic and focused on {domain_hint}.
"""
