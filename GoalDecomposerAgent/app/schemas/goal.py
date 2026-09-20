from datetime import date

from pydantic import BaseModel, Field


class GoalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    deadline: date | None = None
    available_hours_per_day: float | None = Field(default=None, gt=0, le=24)


class GoalResponse(GoalCreate):
    id: int
    status: str

    model_config = {"from_attributes": True}
