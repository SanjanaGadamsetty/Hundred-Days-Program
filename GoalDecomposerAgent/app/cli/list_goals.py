from app.core.database import SessionLocal
from app.models import Goal


def main() -> None:
    db = SessionLocal()
    try:
        goals = db.query(Goal).order_by(Goal.id).all()
        print("\n--- YOUR GOALS ---")
        for goal in goals:
            print(f"\nID: {goal.id}")
            print(f"Title: {goal.title}")
            print(f"Description: {goal.description}")
            print(f"Status: {goal.status}")
            print(f"Deadline: {goal.deadline or 'Not set'}")
            print(f"Hours/day: {goal.available_hours_per_day or 'Not set'}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
