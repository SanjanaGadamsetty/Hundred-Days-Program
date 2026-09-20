from app.agent.agent import GoalAgent
from app.core.database import SessionLocal
from app.jobs.service import mark_completed, mark_failed, mark_running
from app.models import Job, Goal
from app.observability.tracer import trace


def run_job(job_id: int) -> None:
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        db.close()
        return

    try:
        mark_running(db, job)
        if job.job_type == "decompose_goal":
            goal = db.query(Goal).filter(Goal.id == job.goal_id).first()
            if not goal:
                raise ValueError("Goal not found")
            GoalAgent().run(db, goal)
        elif job.job_type == "schedule":
            goal = db.query(Goal).filter(Goal.id == job.goal_id).first()
            if not goal:
                raise ValueError("Goal not found")
            from app.services.scheduler import schedule_tasks
            schedule_tasks(db, goal)
        else:
            raise ValueError(f"Unknown job type: {job.job_type}")
        mark_completed(db, job)
    except Exception as exc:
        db.rollback()
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            mark_failed(db, job, str(exc))
        trace("Worker error for job %s: %s", job_id, exc)
    finally:
        db.close()
