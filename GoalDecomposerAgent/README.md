# Goal Decomposer Agent

A terminal-first Goal Decomposer application built with Python, SQLAlchemy, SQLite, Alembic, and FastAPI.

## What the MVP can do

- Create goals with an optional deadline and available hours per day.
- Decompose a goal into subgoals and actionable tasks.
- Estimate task effort and generate a simple schedule.
- Mark tasks completed and calculate goal progress.
- Recommend scheduled pending tasks for today.
- Run decomposition/scheduling as lightweight background jobs.
- Track job status and errors.
- Log important agent actions for traceability.
- Expose the same core functionality through a small FastAPI API.

The decomposition engine is intentionally deterministic for now. The `app/llm/` layer provides a clean place to add an LLM provider later without rewriting the database or API.

## Project structure

```text
app/
├── agent/           # Agent orchestration and state
├── cli/             # Terminal commands
├── core/            # Configuration and database connection
├── jobs/            # Job records, queue, and worker
├── llm/             # Provider-neutral LLM abstraction
├── models/          # SQLAlchemy models
├── observability/   # Trace/logging helpers
├── schemas/         # Pydantic API schemas
├── services/        # Deterministic business logic
├── tools/           # Actions used by the agent
└── tests/           # Smoke and service tests
```

## Setup

Create/activate a virtual environment, then install:

```powershell
python -m pip install -r requirements.txt
```

Apply migrations:

```powershell
alembic upgrade head
```

**Do not delete or recreate `goal_decomposer.db`.** Alembic upgrades preserve existing data.

## Terminal commands

```powershell
python -m app.cli.create_goal
python -m app.cli.create_subgoal
python -m app.cli.create_task
python -m app.cli.list_goals
python -m app.cli.run_decomposer
python -m app.cli.decompose_goal
python -m app.cli.generate_tasks
python -m app.cli.schedule_goal
python -m app.cli.daily_tasks
python -m app.cli.progress
python -m app.cli.complete_task
python -m app.cli.dashboard
```

The recommended end-to-end terminal flow is:

```text
create_goal
   ↓
run_decomposer
   ↓
schedule_goal
   ↓
daily_tasks
   ↓
complete_task
   ↓
progress / dashboard
```

## API

Start FastAPI with:

```powershell
uvicorn app.main:app --reload
```

Useful endpoints:

```text
POST  /goals
GET   /goals/{goal_id}
POST  /goals/{goal_id}/decompose
POST  /goals/{goal_id}/schedule
GET   /jobs/{job_id}
GET   /goals/{goal_id}/tasks
PATCH /tasks/{task_id}
GET   /goals/{goal_id}/progress
GET   /goals/{goal_id}/daily-tasks
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Verification

Compile all application code:

```powershell
python -m compileall app
```

Run the database check:

```powershell
python -m app.tests.test_database
```

Run the application tests without pytest:

```powershell
python -m unittest discover -s app/tests -p "test_*.py"
```

Check migration state:

```powershell
alembic current
alembic heads
```

## Database safety

The SQLite database and existing Alembic migrations are part of the project. New functionality is added through Alembic migrations rather than dropping/recreating tables.
