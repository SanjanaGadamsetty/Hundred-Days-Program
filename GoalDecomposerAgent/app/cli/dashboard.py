from app.core.database import SessionLocal
from app.models import Goal
from app.services.goal_service import get_progress


def main() -> None:
    db = SessionLocal()
    try:
        goals = db.query(Goal).order_by(Goal.id).all()
        print("\n" + "=" * 70)
        print("                 GOAL DECOMPOSER DASHBOARD")
        print("=" * 70)
        if not goals:
            print("\nNo goals yet. Create one with: python -m app.cli.create_goal")
        for goal in goals:
            progress = get_progress(db, goal.id)
            print(f"\n🎯 GOAL #{goal.id}: {goal.title}")
            print(f"   Status: {goal.status}")
            print(f"   Deadline: {goal.deadline or 'Not set'}")
            print(f"   Progress: {progress['progress_percentage']}% ({progress['completed_tasks']}/{progress['total_tasks']})")
            for subgoal in goal.subgoals:
                print(f"\n   📌 {subgoal.title}")
                for task in subgoal.tasks:
                    marker = "✓" if task.status == "completed" else "○"
                    schedule = f" [{task.scheduled_date}]" if task.scheduled_date else ""
                    print(f"      {marker} {task.title}{schedule}")
        print("\n" + "=" * 70)
    finally:
        db.close()


if __name__ == "__main__":
    main()
