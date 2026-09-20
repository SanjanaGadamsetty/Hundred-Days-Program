from datetime import date

from app.core.database import SessionLocal
from app.models import SubGoal, Task


def main() -> None:
    db = SessionLocal()
    try:
        subgoal_id = int(input("Enter SubGoal ID: "))
        title = input("Enter task title: ").strip()
        description = input("Enter description: ").strip() or None
        due_date_input = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
        minutes_input = input("Enter estimated minutes or press Enter for 45: ").strip()

        subgoal = db.query(SubGoal).filter(SubGoal.id == subgoal_id).first()
        if not subgoal:
            print("SubGoal not found!")
            return

        due_date = date.fromisoformat(due_date_input) if due_date_input else None
        estimated_minutes = int(minutes_input) if minutes_input else 45
        task = Task(
            subgoal_id=subgoal_id,
            title=title,
            description=description,
            due_date=due_date,
            estimated_minutes=estimated_minutes,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        print("\nTask created successfully!")
        print("ID:", task.id)
        print("Task:", task.title)
        print("Due Date:", task.due_date)
        print("Estimated Minutes:", task.estimated_minutes)
    finally:
        db.close()


if __name__ == "__main__":
    main()
