def main() -> None:
    from app.core.database import SessionLocal
    from app.models import SubGoal
    db = SessionLocal()
    try:
        subgoal = db.query(SubGoal).first()
        if subgoal:
            print("SubGoal:", subgoal.title)
            print("Parent Goal:", subgoal.goal.title)
    finally:
        db.close()


if __name__ == "__main__":
    main()
