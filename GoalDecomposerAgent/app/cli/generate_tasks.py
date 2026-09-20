from app.core.database import SessionLocal
from app.models import SubGoal, Task
from app.services.task_generator import generate_tasks


def main() -> None:
    db = SessionLocal()
    try:
        subgoal_id = int(input("Enter SubGoal ID: "))
        subgoal = db.query(SubGoal).filter(SubGoal.id == subgoal_id).first()
        if not subgoal:
            print("SubGoal not found!")
            return
        titles = generate_tasks(subgoal.title)
        for title in titles:
            db.add(Task(subgoal_id=subgoal.id, title=title, estimated_minutes=45))
        db.commit()
        print("\nTasks generated successfully!")
        for title in titles:
            print("-", title)
    finally:
        db.close()


if __name__ == "__main__":
    main()
