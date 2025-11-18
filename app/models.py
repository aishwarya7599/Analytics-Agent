from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime

class Challenge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    track: str
    title: str
    prompt_md: str
    solution_stub: str
    tests_py: str
    difficulty: str = "normal"

class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    challenge_id: int
    timestamp: datetime
    status: str
    passed: bool
    feedback_md: str
    runtime_ms: Optional[int] = None

class LearningJournal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    bullets_md: str

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    text: str
    impact: int
    urgency: int
    duration_min: int
    status: str = "todo"

class Plan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    plan_md: str
