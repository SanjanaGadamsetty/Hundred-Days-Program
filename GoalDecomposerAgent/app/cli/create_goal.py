from datetime import date

from app.core.database import SessionLocal
from app.services.goal_service import create_goal


def main() -> None:
    title = input("Enter your goal: ").strip()
    description = input("Enter a description: ").strip() or None
    deadline_input = input("Enter deadline (YYYY-MM-DD) or press Enter to skip: ").strip()
    hours_input = input("Enter available hours per day or press Enter to skip: ").strip()

    deadline = date.fromisoformat(deadline_input) if deadline_input else None
    hours = float(hours_input) if hours_input else None

    db = SessionLocal()
    try:
        goal = create_goal(db, title, description, deadline, hours)
        print("\nGoal created successfully!")
        print("ID:", goal.id)
        print("Title:", goal.title)
        print("Description:", goal.description)
        print("Deadline:", goal.deadline)
        print("Hours/day:", goal.available_hours_per_day)
    finally:
        db.close()


if __name__ == "__main__":
    main()
