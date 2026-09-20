from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Job
from app.observability.tracer import trace


def create_job(db: Session, goal_id: int, job_type: str) -> Job:
    job = Job(
        goal_id=goal_id,
        job_type=job_type,
        status="queued",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    trace("Job created: %s (%s)", job.id, job_type)
    return job


def mark_running(db: Session, job: Job) -> None:
    job.status = "running"
    job.updated_at = datetime.now(timezone.utc)
    db.commit()
    trace("Job running: %s", job.id)


def mark_completed(db: Session, job: Job) -> None:
    job.status = "completed"
    job.updated_at = datetime.now(timezone.utc)
    db.commit()
    trace("Job completed: %s", job.id)


def mark_failed(db: Session, job: Job, error: str) -> None:
    job.status = "failed"
    job.error = error
    job.updated_at = datetime.now(timezone.utc)
    db.commit()
    trace("Job failed: %s - %s", job.id, error)
