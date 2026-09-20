from app.core.database import SessionLocal
from app.models import Goal
from app.services.scheduler import schedule_tasks


def main() -> None:
    db = SessionLocal()
    try:
        goal_id = int(input("Enter Goal ID: "))
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            print("Goal not found!")
            return
        tasks = schedule_tasks(db, goal)
        print("\nSchedule generated successfully!")
        for task in tasks:
            print(f"- {task.scheduled_date}: {task.title} ({task.estimated_minutes} min)")
    finally:
        db.close()


if __name__ == "__main__":
    main()
