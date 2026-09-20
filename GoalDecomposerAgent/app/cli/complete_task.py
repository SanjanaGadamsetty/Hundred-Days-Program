from app.core.database import SessionLocal
from app.models import Task


def main() -> None:
    db = SessionLocal()
    try:
        task_id = int(input("Enter Task ID: "))
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            print("Task not found!")
            return
        task.status = "completed"
        db.commit()
        print("\nTask completed!")
        print("Task:", task.title)
    finally:
        db.close()


if __name__ == "__main__":
    main()
