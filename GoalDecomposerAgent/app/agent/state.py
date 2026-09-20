from dataclasses import dataclass
from datetime import date


@dataclass
class AgentState:
    goal_id: int
    goal_title: str
    deadline: date | None
    available_hours_per_day: float | None
