def main() -> None:
    from app.core.database import SessionLocal
    from app.models import SubGoal, Task
    db = SessionLocal()
    try:
        subgoal = db.query(SubGoal).first()
        if not subgoal:
            print("No subgoal exists.")
            return
        task = Task(
            subgoal_id=subgoal.id,
            title="Practice Python variables",
            description="Write simple programs using different variable types.",
        )
        db.add(task)
        db.commit()
        print("Task added successfully!")
        print("Task ID:", task.id)
        print("Parent SubGoal ID:", task.subgoal_id)
    finally:
        db.close()


if __name__ == "__main__":
    main()
