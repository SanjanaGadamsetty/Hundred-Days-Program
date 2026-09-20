from app.core.database import SessionLocal
from app.services.goal_service import get_progress


def main() -> None:
    db = SessionLocal()
    try:
        goal_id = int(input("Enter Goal ID: "))
        try:
            progress = get_progress(db, goal_id)
        except ValueError:
            print("Goal not found!")
            return
        print("\n--- GOAL PROGRESS ---")
        print("Total tasks:", progress["total_tasks"])
        print("Completed:", progress["completed_tasks"])
        print("Pending:", progress["pending_tasks"])
        print("Progress:", f'{progress["progress_percentage"]}%')
    finally:
        db.close()


if __name__ == "__main__":
    main()
