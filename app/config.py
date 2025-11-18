from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DB_URL = os.getenv("DB_URL", "sqlite:///agent.db")
