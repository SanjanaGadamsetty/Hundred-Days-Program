"""add planning fields and jobs

Revision ID: 8c7f4f2e1a9b
Revises: dca28c3645f3
Create Date: 2026-09-21
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "8c7f4f2e1a9b"
down_revision: Union[str, Sequence[str], None] = "dca28c3645f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("goals", sa.Column("deadline", sa.Date(), nullable=True))
    op.add_column(
        "goals", sa.Column("available_hours_per_day", sa.Float(), nullable=True)
    )
    op.add_column("tasks", sa.Column("estimated_minutes", sa.Integer(), nullable=True))
    op.add_column("tasks", sa.Column("scheduled_date", sa.Date(), nullable=True))
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("goal_id", sa.Integer(), nullable=True),
        sa.Column("job_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["goal_id"], ["goals.id"]),
    )


def downgrade() -> None:
    op.drop_table("jobs")
    op.drop_column("tasks", "scheduled_date")
    op.drop_column("tasks", "estimated_minutes")
    op.drop_column("goals", "available_hours_per_day")
    op.drop_column("goals", "deadline")
