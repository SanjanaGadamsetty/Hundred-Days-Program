def main() -> None:
    from app.core.database import SessionLocal
    from app.models import Goal, SubGoal
    db = SessionLocal()
    try:
        goal = db.query(Goal).first()
        if not goal:
            print("No goal exists.")
            return
        subgoal = SubGoal(
            goal_id=goal.id,
            title="Learn Python Basics",
            description="Learn variables, data types, conditions, loops, and functions.",
        )
        db.add(subgoal)
        db.commit()
        print("SubGoal added successfully!")
        print("SubGoal ID:", subgoal.id)
        print("Parent Goal ID:", subgoal.goal_id)
    finally:
        db.close()


if __name__ == "__main__":
    main()
