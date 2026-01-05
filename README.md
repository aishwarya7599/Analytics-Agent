Analytics Coach 
====================================================

Quick start
-----------

1. Create and activate a virtual env in this folder.

   On Windows (PowerShell):

       python -m venv .venv
       .venv\Scripts\Activate.ps1

   On macOS / Linux (bash/zsh):

       python -m venv .venv
       source .venv/bin/activate

2. Install dependencies:

       pip install -r requirements.txt

3. Add your OpenAI key to `.env`:

       OPENAI_API_KEY=sk-...

4. Initialize the local SQLite database:

       python -m app.cli init

5. Generate a challenge:

       python -m app.cli challenge --track python

   This prints the prompt and creates a starter file like `user_solution_1.py`.

6. After you solve the challenge, grade it:

       python -m app.cli grade --challenge-id 1 --user-code-path user_solution_1.py

7. Create a simple daily plan:

       python -m app.cli plan
