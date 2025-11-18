import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path

from ..db import get_session
from ..models import Submission, Challenge


# We build a temporary test file that:
#   1) loads the user's code from whatever path they pass in
#   2) registers it as the module name "user_solution"
#   3) appends the tests stored in the Challenge row
PYTEST_WRAPPER = """\
import importlib.util
import sys
from pathlib import Path

USER_CODE_PATH = Path({user_code_path!r})

spec = importlib.util.spec_from_file_location("user_solution", USER_CODE_PATH)
module = importlib.util.module_from_spec(spec)

# Make the module importable as "user_solution" for the tests
sys.modules["user_solution"] = module

spec.loader.exec_module(module)  # type: ignore

# ---- tests from the challenge ----
{tests}
"""


def grade_solution(challenge: Challenge, user_code_path: str) -> Submission:
    """
    Run the hidden tests for a challenge against the user's solution file.

    Parameters
    ----------
    challenge : Challenge
        The Challenge row whose tests we should run.
    user_code_path : str
        Path to the user's solution file (anything, e.g. 'user_solution_1.py').

    Returns
    -------
    Submission
        A Submission row containing pass/fail, feedback, and runtime.
    """
    # Build the full test file source
    tests_source = PYTEST_WRAPPER.format(
        user_code_path=str(Path(user_code_path).resolve()).replace("\\", "/"),
        tests=challenge.tests_py,
    )

    # Write tests to a temporary file
    with tempfile.NamedTemporaryFile(
        "w", suffix="_tests.py", delete=False, encoding="utf-8"
    ) as tf:
        tf.write(tests_source)
        tests_file = tf.name

    # Run pytest on the temp file
    start = time.time()
    proc = subprocess.run(
        ["pytest", tests_file, "-q"],
        capture_output=True,
        text=True,
    )
    runtime_ms = int((time.time() - start) * 1000)

    passed = proc.returncode == 0
    feedback = proc.stdout
    if proc.stderr:
        feedback += "\n" + proc.stderr

    # Store submission in the DB
    sub = Submission(
        challenge_id=challenge.id,
        timestamp=datetime.utcnow(),
        status="graded",
        passed=passed,
        feedback_md=f"```\n{feedback}\n```",
        runtime_ms=runtime_ms,
    )
    with get_session() as s:
        s.add(sub)
        s.commit()
        s.refresh(sub)

    return sub
