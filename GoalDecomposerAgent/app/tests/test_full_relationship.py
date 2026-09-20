def main() -> None:
    from app.core.database import SessionLocal
    from app.models import Goal
    db = SessionLocal()
    try:
        goal = db.query(Goal).first()
        if goal:
            print("Goal:", goal.title)
            for subgoal in goal.subgoals:
                print("  SubGoal:", subgoal.title)
                for task in subgoal.tasks:
                    print("    Task:", task.title)
    finally:
        db.close()


if __name__ == "__main__":
    main()
