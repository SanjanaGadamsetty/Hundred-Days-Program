def main() -> None:
    from app.core.database import SessionLocal
    from app.models import Goal
    db = SessionLocal()
    try:
        goal = db.query(Goal).first()
        if goal:
            print("Goal found!")
            print("ID:", goal.id)
            print("Title:", goal.title)
            print("Description:", goal.description)
            print("Status:", goal.status)
    finally:
        db.close()


if __name__ == "__main__":
    main()
