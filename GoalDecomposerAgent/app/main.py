from datetime import date

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.jobs.queue import enqueue
from app.jobs.service import create_job
from app.models import Goal, Job, Task
from app.schemas import GoalCreate, GoalResponse, TaskResponse, TaskUpdate
from app.services.goal_service import create_goal, get_goal, get_progress
from app.services.recommendations import daily_tasks
from app.services.scheduler import schedule_tasks

app = FastAPI(title="Goal Decomposer Agent", version="1.0.0")


def _goal_response(goal: Goal) -> dict:
    return {
        "id": goal.id,
        "title": goal.title,
        "description": goal.description,
        "deadline": goal.deadline,
        "available_hours_per_day": goal.available_hours_per_day,
        "status": goal.status,
    }


@app.get("/")
def home():
    return {"message": "Goal Decomposer Agent API is running!"}


@app.post("/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal_endpoint(goal_data: GoalCreate, db: Session = Depends(get_db)):
    return create_goal(
        db,
        title=goal_data.title,
        description=goal_data.description,
        deadline=goal_data.deadline,
        available_hours_per_day=goal_data.available_hours_per_day,
    )


@app.get("/goals/{goal_id}")
def get_goal_endpoint(goal_id: int, db: Session = Depends(get_db)):
    goal = get_goal(db, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return _goal_response(goal)


@app.post("/goals/{goal_id}/decompose", status_code=status.HTTP_202_ACCEPTED)
def decompose_goal_endpoint(goal_id: int, db: Session = Depends(get_db)):
    goal = get_goal(db, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    job = create_job(db, goal_id, "decompose_goal")
    enqueue(job.id)
    return {"job_id": job.id, "status": job.status, "message": "Goal decomposition started"}


@app.get("/jobs/{job_id}")
def get_job_endpoint(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job_id": job.id,
        "goal_id": job.goal_id,
        "type": job.job_type,
        "status": job.status,
        "error": job.error,
    }


@app.post("/goals/{goal_id}/schedule", status_code=status.HTTP_202_ACCEPTED)
def schedule_goal_endpoint(goal_id: int, db: Session = Depends(get_db)):
    goal = get_goal(db, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    job = create_job(db, goal_id, "schedule")
    enqueue(job.id)
    return {"job_id": job.id, "status": job.status, "message": "Schedule generation started"}


@app.get("/goals/{goal_id}/tasks", response_model=list[TaskResponse])
def get_goal_tasks(goal_id: int, db: Session = Depends(get_db)):
    goal = get_goal(db, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return (
        db.query(Task)
        .join(Task.subgoal)
        .filter(Task.subgoal.has(goal_id=goal_id))
        .order_by(Task.id)
        .all()
    )


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = update.status
    db.commit()
    db.refresh(task)
    return {"task_id": task.id, "status": task.status, "updated": True}


@app.get("/goals/{goal_id}/progress")
def goal_progress(goal_id: int, db: Session = Depends(get_db)):
    try:
        return get_progress(db, goal_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Goal not found")


@app.get("/goals/{goal_id}/daily-tasks")
def goal_daily_tasks(goal_id: int, db: Session = Depends(get_db)):
    goal = get_goal(db, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    tasks = daily_tasks(db, goal_id, date.today())
    return {
        "goal_id": goal_id,
        "date": date.today(),
        "recommended_tasks": [
            {
                "task_id": task.id,
                "title": task.title,
                "estimated_minutes": task.estimated_minutes,
                "scheduled_date": task.scheduled_date,
            }
            for task in tasks
        ],
    }
