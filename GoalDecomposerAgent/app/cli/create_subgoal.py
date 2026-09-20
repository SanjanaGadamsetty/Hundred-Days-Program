from app.core.database import SessionLocal
from app.models import Goal, SubGoal


def main() -> None:
    db = SessionLocal()
    try:
        goal_id = int(input("Enter Goal ID: "))
        title = input("Enter subgoal title: ").strip()
        description = input("Enter description: ").strip() or None
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            print("Goal not found!")
            return
        subgoal = SubGoal(goal_id=goal_id, title=title, description=description)
        db.add(subgoal)
        db.commit()
        db.refresh(subgoal)
        print("\nSubGoal created successfully!")
        print("ID:", subgoal.id)
        print("Parent Goal:", goal.title)
    finally:
        db.close()


if __name__ == "__main__":
    main()
