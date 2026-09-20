from datetime import date

from sqlalchemy.orm import Session

from app.models import Goal, Task


def create_goal(
    db: Session,
    title: str,
    description: str | None = None,
    deadline: date | None = None,
    available_hours_per_day: float | None = None,
) -> Goal:
    goal = Goal(
        title=title,
        description=description,
        deadline=deadline,
        available_hours_per_day=available_hours_per_day,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def get_goal(db: Session, goal_id: int) -> Goal | None:
    return db.query(Goal).filter(Goal.id == goal_id).first()


def get_progress(db: Session, goal_id: int) -> dict:
    goal = get_goal(db, goal_id)
    if not goal:
        raise ValueError("Goal not found")

    tasks = (
        db.query(Task)
        .join(Task.subgoal)
        .filter(Task.subgoal.has(goal_id=goal_id))
        .all()
    )
    total = len(tasks)
    completed = sum(task.status == "completed" for task in tasks)
    pending = total - completed
    percentage = round((completed / total) * 100, 1) if total else 0.0
    return {
        "goal_id": goal_id,
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "progress_percentage": percentage,
    }
