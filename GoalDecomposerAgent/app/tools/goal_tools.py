from sqlalchemy.orm import Session

from app.models import Goal, SubGoal, Task
from app.services.decomposer import decompose_goal
from app.services.task_generator import generate_tasks


def create_subgoals(db: Session, goal: Goal) -> list[SubGoal]:
    subgoals = []
    for title in decompose_goal(goal.title):
        subgoal = SubGoal(goal_id=goal.id, title=title)
        db.add(subgoal)
        db.flush()
        subgoals.append(subgoal)
    return subgoals


def create_tasks(db: Session, subgoal: SubGoal) -> list[Task]:
    tasks = []
    for title in generate_tasks(subgoal.title):
        task = Task(subgoal_id=subgoal.id, title=title, estimated_minutes=45)
        db.add(task)
        tasks.append(task)
    return tasks
