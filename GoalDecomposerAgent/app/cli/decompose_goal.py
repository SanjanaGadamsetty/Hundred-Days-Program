from app.core.database import SessionLocal
from app.models import Goal
from app.agent.agent import GoalAgent


def main() -> None:
    db = SessionLocal()
    try:
        goal_id = int(input("Enter Goal ID: "))
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            print("Goal not found!")
            return
        result = GoalAgent().run(db, goal)
        print("\nGoal decomposed successfully!")
        print("SubGoals created:", result["subgoals_created"])
        print("Tasks created:", result["tasks_created"])
        print("Tasks scheduled:", result["tasks_scheduled"])
    finally:
        db.close()


if __name__ == "__main__":
    main()
