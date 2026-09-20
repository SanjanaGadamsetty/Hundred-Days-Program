def main() -> None:
    from app.core.database import SessionLocal
    from app.models import Goal
    db = SessionLocal()
    try:
        goal = Goal(
            title="Learn Python",
            description="Learn Python from beginner to intermediate level.",
        )
        db.add(goal)
        db.commit()
        print("Goal added successfully!")
        print("Goal ID:", goal.id)
    finally:
        db.close()


if __name__ == "__main__":
    main()
