def main() -> None:
    from app.core.database import SessionLocal
    from app.models import Task
    db = SessionLocal()
    try:
        task = db.query(Task).first()
        if task:
            print("Task:", task.title)
            print("Created At:", task.created_at)
    finally:
        db.close()


if __name__ == "__main__":
    main()
