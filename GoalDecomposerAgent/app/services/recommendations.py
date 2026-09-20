from datetime import date

from sqlalchemy.orm import Session

from app.models import Goal, Task


def daily_tasks(db: Session, goal_id: int, today: date | None = None) -> list[Task]:
    today = today or date.today()
    return (
        db.query(Task)
        .join(Task.subgoal)
        .filter(
            Task.subgoal.has(goal_id=goal_id),
            Task.status != "completed",
            Task.scheduled_date <= today,
        )
        .order_by(Task.scheduled_date, Task.id)
        .all()
    )
