from sqlalchemy.orm import Session

from app.agent.state import AgentState
from app.models import Goal
from app.observability.tracer import trace
from app.services.scheduler import schedule_tasks
from app.tools.goal_tools import create_subgoals, create_tasks


class GoalAgent:
    """Small deterministic agent orchestrating tools and services.

    The architecture is intentionally provider-neutral so an LLM can replace
    the rule-based services later without changing the database/API layers.
    """

    def run(self, db: Session, goal: Goal) -> dict:
        state = AgentState(
            goal_id=goal.id,
            goal_title=goal.title,
            deadline=goal.deadline,
            available_hours_per_day=goal.available_hours_per_day,
        )
        trace("Agent started for goal: %s", state.goal_id)

        subgoals = create_subgoals(db, goal)
        task_count = 0
        for subgoal in subgoals:
            task_count += len(create_tasks(db, subgoal))
        db.commit()

        scheduled = schedule_tasks(db, goal)
        trace("Agent finished for goal: %s", state.goal_id)
        return {
            "goal_id": goal.id,
            "subgoals_created": len(subgoals),
            "tasks_created": task_count,
            "tasks_scheduled": len(scheduled),
        }
