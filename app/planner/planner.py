from datetime import date, datetime, timedelta
from ..db import get_session
from ..models import Task, Plan

def build_simple_plan(today: date) -> Plan:
    """Very small heuristic day plan over tasks in the DB.

    You can insert tasks manually into the DB for now or extend this later.
    """
    with get_session() as s:
        tasks = s.query(Task).filter(Task.date == today, Task.status == "todo").all()  # type: ignore

    tasks_sorted = sorted(tasks, key=lambda t: (-(0.7 * t.impact + 0.3 * t.urgency)))
    blocks = []
    start = datetime.combine(today, datetime.min.time()).replace(hour=9, minute=0)
    for task in tasks_sorted[:5]:
        end = start + timedelta(minutes=task.duration_min)
        blocks.append(f"{start.strftime('%H:%M')}–{end.strftime('%H:%M')}  {task.text}")
        start = end + timedelta(minutes=10)

    if tasks_sorted:
        focus = "\n".join(f"• {t.text}" for t in tasks_sorted[:3])
    else:
        focus = "• Deep work block\n• Learning challenge\n• Ship 1 tiny improvement"

    plan_md = f"""
### Today's Focus (Top 3)
{focus}

### Time‑boxed Plan
{chr(10).join(blocks) or '09:00–10:30 Deep work\n10:45–11:30 Learning\n11:30–12:00 Journal'}

> Keep ~20% buffer. Say no to new work until the top 3 are done.
"""

    p = Plan(date=today, plan_md=plan_md)
    with get_session() as s:
        s.add(p)
        s.commit()
        s.refresh(p)
    return p
