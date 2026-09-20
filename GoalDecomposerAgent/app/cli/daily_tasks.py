from datetime import date

from app.core.database import SessionLocal
from app.models import Goal
from app.services.recommendations import daily_tasks


def main() -> None:
    db = SessionLocal()
    try:
        goal_id = int(input("Enter Goal ID: "))
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            print("Goal not found!")
            return
        tasks = daily_tasks(db, goal_id, date.today())
        print(f"\n--- TASKS FOR {date.today()} ---")
        if not tasks:
            print("No scheduled pending tasks for today.")
        for task in tasks:
            print(f"- #{task.id} {task.title} ({task.estimated_minutes or '?'} min)")
    finally:
        db.close()


if __name__ == "__main__":
    main()
