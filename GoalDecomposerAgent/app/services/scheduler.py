from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models import Goal, Task


def schedule_tasks(db: Session, goal: Goal) -> list[Task]:
    tasks = (
        db.query(Task)
        .join(Task.subgoal)
        .filter(Task.subgoal.has(goal_id=goal.id), Task.status != "completed")
        .order_by(Task.id)
        .all()
    )
    if not tasks:
        return []

    start = date.today()
    end = goal.deadline or (start + timedelta(days=max(len(tasks) - 1, 0)))
    available_days = max((end - start).days + 1, 1)
    daily_minutes = max(int((goal.available_hours_per_day or 1) * 60), 1)

    current_date = start
    used_today = 0
    for task in tasks:
        minutes = task.estimated_minutes or 45
        if used_today and used_today + minutes > daily_minutes:
            current_date += timedelta(days=1)
            used_today = 0
        if current_date > end:
            current_date = end
            used_today = 0
        task.estimated_minutes = minutes
        task.scheduled_date = current_date
        used_today += minutes

    db.commit()
    return tasks
