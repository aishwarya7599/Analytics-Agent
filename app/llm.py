import os
from .config import OPENAI_API_KEY, OPENAI_MODEL

def _get_client():
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Put it in a .env file or environment variable."
        )
    # Lazy import so that the package imports even if openai is not installed yet.
    from openai import OpenAI  # type: ignore
    return OpenAI(api_key=OPENAI_API_KEY)

def complete_json(system_prompt: str, user_prompt: str) -> str:
    """Call the chat model and *ask* for JSON.

    The model is instructed to respond with JSON only. We still do a small
    best-effort clean‑up on the returned text.
    """
    client = _get_client()
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )
    text = resp.choices[0].message.content or ""
    # Best-effort trim to the outermost JSON object
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text
