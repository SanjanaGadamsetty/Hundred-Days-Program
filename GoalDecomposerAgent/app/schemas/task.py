from datetime import date

from pydantic import BaseModel, Field


class TaskUpdate(BaseModel):
    status: str = Field(pattern="^(pending|in_progress|completed)$")


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    due_date: date | None
    estimated_minutes: int | None
    scheduled_date: date | None

    model_config = {"from_attributes": True}
