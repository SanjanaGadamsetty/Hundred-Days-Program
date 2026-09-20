# Goal Decomposer — Low-Level Design (LLD)

## 1. Purpose

The Low-Level Design defines the internal modules, files, responsibilities, data flow, and interactions required to implement the Goal Decomposer system.

The design is intentionally modular so that the project can demonstrate practical **Agentic AI concepts** such as:

* Agent
* Tools
* Agent state
* Jobs
* Workers
* Task execution
* Memory
* Database persistence
* Traceability
* Synchronous and asynchronous processing

The project remains a small MVP and does not introduce unnecessary distributed-system complexity.

---

# 2. Proposed Project Structure

```text
goal-decomposer/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── goals.py
│   │   └── tasks.py
│   │
│   ├── agent/
│   │   ├── agent.py
│   │   ├── state.py
│   │   └── prompts.py
│   │
│   ├── tools/
│   │   ├── goal_tools.py
│   │   ├── task_tools.py
│   │   ├── schedule_tools.py
│   │   └── progress_tools.py
│   │
│   ├── jobs/
│   │   ├── job.py
│   │   └── job_queue.py
│   │
│   ├── workers/
│   │   └── worker.py
│   │
│   ├── services/
│   │   ├── goal_service.py
│   │   ├── schedule_service.py
│   │   └── progress_service.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── repositories.py
│   │
│   ├── llm/
│   │   └── client.py
│   │
│   └── logging/
│       └── tracer.py
│
├── tests/
│   ├── test_agent.py
│   ├── test_tools.py
│   ├── test_schedule.py
│   └── test_progress.py
│
├── .env
├── requirements.txt
└── README.md
```

---

# 3. Module Responsibilities

## 3.1 `main.py`

### Responsibility

Application entry point.

It starts the FastAPI application and initializes the required components.

```text
main.py
   │
   ├── Initialize database
   ├── Initialize job queue
   ├── Start worker
   └── Start API
```

It should **not** contain agent logic.

---

# 4. API Layer

## `api/goals.py`

Handles goal-related requests.

### Example endpoints

```text
POST /goals
GET  /goals/{goal_id}
POST /goals/{goal_id}/decompose
POST /goals/{goal_id}/schedule
```

### Example flow

```text
POST /goals/{id}/decompose
          ↓
      API Layer
          ↓
      Create Job
          ↓
      Job Queue
          ↓
       Worker
          ↓
      AI Agent
```

---

## `api/tasks.py`

Handles task-related operations.

```text
PATCH /tasks/{task_id}
GET   /goals/{goal_id}/progress
GET   /goals/{goal_id}/daily-tasks
```

---

# 5. Agent Layer

## `agent/agent.py`

This is the **brain/orchestrator** of the system.

The agent decides what needs to happen and which tools should be used.

### Simplified agent loop

```text
User Request
     ↓
Understand Request
     ↓
Read Agent State
     ↓
Decide Action
     ↓
Select Tool
     ↓
Execute Tool
     ↓
Observe Result
     ↓
Update State
     ↓
Return Result
```

### Example

User:

> "Break my Full Stack goal into tasks."

Agent:

```text
1. Understand goal
2. Read deadline
3. Read available time
4. Ask LLM for decomposition
5. Create milestones
6. Create tasks
7. Save tasks
8. Return plan
```

The agent should **not directly manipulate database tables everywhere**.

It should use tools/services.

---

# 6. Agent State

## `agent/state.py`

The agent needs a small amount of state while processing a request.

Example:

```text
AgentState

goal_id
user_request
current_goal
milestones
tasks
deadline
available_time
current_date
progress
last_action
tool_results
```

### Why state?

Without state:

```text
Agent → Tool
Agent → Tool
Agent → Tool
```

The agent would have no organized representation of what it already knows.

With state:

```text
             ┌──────────────┐
             │  Agent State │
             ├──────────────┤
             │ Goal         │
             │ Deadline     │
             │ Tasks        │
             │ Progress     │
             │ Tool Results │
             └──────────────┘
                    ▲
                    │
              ┌─────┴─────┐
              │   Agent   │
              └───────────┘
```

---

# 7. Prompt Layer

## `agent/prompts.py`

Contains the instructions given to the LLM.

For example:

```text
SYSTEM INSTRUCTION

You are a goal planning agent.

Your job is to:
1. Understand the user's goal.
2. Identify meaningful milestones.
3. Break milestones into actionable tasks.
4. Consider the user's deadline and available time.
5. Produce structured output.
```

Keeping prompts in a separate file makes them easier to test and modify.

---

# 8. Tool Layer

The agent should interact with the application through tools.

## `tools/goal_tools.py`

Possible tools:

```text
create_goal()
get_goal()
```

---

## `tools/task_tools.py`

```text
create_task()
get_pending_tasks()
update_task_status()
```

---

## `tools/schedule_tools.py`

```text
get_current_date()
calculate_available_days()
generate_schedule()
```

---

## `tools/progress_tools.py`

```text
get_progress()
get_completed_tasks()
```

---

# 9. Tool Execution

A simple tool registry can be used.

```text
TOOL_REGISTRY

"create_goal"       → create_goal()
"create_task"       → create_task()
"get_progress"      → get_progress()
"generate_schedule" → generate_schedule()
```

The agent can select a tool by name.

```text
Agent
  │
  │ "generate_schedule"
  ▼
Tool Registry
  │
  ▼
generate_schedule()
  │
  ▼
Result
  │
  ▼
Agent
```

This gives you practical experience with **dynamic tool dispatch**.

---

# 10. Job System

Since you're learning Agentic AI infrastructure, we'll introduce a small job system.

## `jobs/job.py`

A job represents **one unit of work that needs to be executed**.

Example:

```text
Job

job_id
job_type
goal_id
payload
status
created_at
completed_at
```

Example job:

```text
job_id: 101
job_type: DECOMPOSE_GOAL
goal_id: 25
status: QUEUED
```

---

# 11. Job Queue

## `jobs/job_queue.py`

The queue temporarily stores jobs waiting for execution.

```text
                JOB QUEUE

        ┌─────────────────────┐
        │ Job 101             │
        │ DECOMPOSE_GOAL      │
        ├─────────────────────┤
        │ Job 102             │
        │ GENERATE_SCHEDULE   │
        ├─────────────────────┤
        │ Job 103             │
        │ DAILY_RECOMMENDATION│
        └─────────────────────┘
```

For your MVP, this can simply be an **in-memory Python queue**.

No Redis or Kafka is required.

---

# 12. Worker

## `workers/worker.py`

The worker continuously looks for jobs and executes them.

```text
             ┌──────────────┐
             │   Job Queue  │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │    Worker    │
             └──────┬───────┘
                    │
              Pick a Job
                    │
                    ▼
             ┌──────────────┐
             │ Execute Job  │
             └──────┬───────┘
                    │
                    ▼
                 Agent
```

### Worker loop

```text
while application_running:

    job = queue.get()

    if job exists:
        execute(job)
        mark_job_completed()
```

This teaches you the fundamental relationship:

```text
JOB = WHAT needs to be done

WORKER = WHO executes it

QUEUE = WHERE pending work waits
```

---

# 13. Example Job Execution

Suppose the user clicks:

> "Decompose Goal"

The flow becomes:

```text
User
 │
 ▼
API
 │
 ▼
Create Job
 │
 ▼
Job Queue
 │
 ▼
Worker picks Job
 │
 ▼
Agent
 │
 ├── Read Goal
 │
 ├── Call LLM
 │
 ├── Create Milestones
 │
 └── Create Tasks
 │
 ▼
Database
 │
 ▼
Job Completed
```

This gives your project a genuine **agent + worker + job** workflow.

---

# 14. Synchronous vs Asynchronous Processing

Not every operation needs a background job.

### Simple operations

These can be synchronous:

```text
Mark Task Complete
      ↓
Update Database
      ↓
Return Response
```

### Longer agent operations

These can use a job:

```text
Goal Decomposition
        ↓
Create Job
        ↓
Queue
        ↓
Worker
        ↓
Agent
        ↓
LLM
        ↓
Database
```

This lets you learn **why asynchronous processing exists**, rather than adding async code everywhere without a reason.

---

# 15. Service Layer

## `services/`

The service layer contains application/business logic that shouldn't belong inside the API or agent.

### `goal_service.py`

Responsible for:

```text
create_goal()
get_goal()
```

### `schedule_service.py`

Responsible for:

```text
calculate_available_days()
generate_schedule()
```

### `progress_service.py`

Responsible for:

```text
update_progress()
calculate_progress()
```

The agent can call tools, and tools can call services.

```text
Agent
  ↓
Tool
  ↓
Service
  ↓
Database
```

This separation keeps the project maintainable.

---

# 16. Database Layer

## `database/database.py`

Responsible for creating the database connection.

For the MVP:

```text
SQLite
```

---

## `database/models.py`

Contains database models:

```text
Goal
Milestone
Task
Job
```

---

## `database/repositories.py`

Handles database operations.

Example:

```text
GoalRepository
TaskRepository
JobRepository
```

Instead of writing SQL everywhere:

```text
Agent
  ↓
Tool
  ↓
Service
  ↓
Repository
  ↓
Database
```

---

# 17. LLM Layer

## `llm/client.py`

This module communicates with the selected LLM provider.

Example:

```text
Agent
  ↓
LLM Client
  ↓
LLM API
  ↓
Structured Response
  ↓
Agent
```

The agent should not contain provider-specific API code.

This means you can later change:

```text
Provider A
     ↓
Provider B
```

without rewriting the agent.

---

# 18. Memory

For this MVP, memory can be simple.

The **database itself acts as persistent application memory**.

For example:

```text
Goal
 ↓
Milestones
 ↓
Tasks
 ↓
Task Status
 ↓
Progress
```

When the agent receives a new request, it retrieves the relevant information.

```text
New Request
     ↓
Retrieve Goal
     ↓
Retrieve Tasks
     ↓
Retrieve Progress
     ↓
Build Agent State
     ↓
Agent
```

We don't need a vector database or RAG for this project.

---

# 19. Traceability

## `logging/tracer.py`

The system should record important agent actions.

Example:

```text
[10:30:01] Job created: 101
[10:30:02] Worker picked job: 101
[10:30:02] Agent started
[10:30:03] Tool called: get_goal
[10:30:03] Tool called: generate_schedule
[10:30:04] Database updated
[10:30:04] Job completed: 101
```

This helps you understand:

* What the agent did
* Which tools it used
* Which job was running
* Where an error occurred
* How long operations took

This directly connects to the **traceability** concept you've been learning.

---

# 20. Complete Internal Architecture

```text
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │  Frontend   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │     API     │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │             │
             Simple Request    Agent Job
                    │             │
                    ▼             ▼
                Services      Job Queue
                    │             │
                    │             ▼
                    │          Worker
                    │             │
                    │             ▼
                    │           Agent
                    │          /  |  \
                    │         /   |   \
                    │      State Tools LLM
                    │          │
                    └──────────┼─────────┐
                               ▼         │
                           Services      │
                               │         │
                               ▼         │
                          Repository     │
                               │         │
                               ▼         │
                           Database ◄────┘

                         Tracer
                    monitors important
                     system operations
```

---

# 21. Example: Complete Agentic Flow

User says:

> "I want to learn Full Stack Development in 3 months. I can spend 2 hours every day."

### Step 1 — API

```text
POST /goals
```

Goal is stored.

### Step 2 — Job

The API creates:

```text
Job {
    type: DECOMPOSE_GOAL
    goal_id: 1
}
```

### Step 3 — Queue

```text
Job Queue
   ↓
[DECOMPOSE_GOAL]
```

### Step 4 — Worker

Worker picks the job.

```text
Worker
   ↓
DECOMPOSE_GOAL
```

### Step 5 — Agent

Agent loads the goal.

```text
Goal
 ↓
3 months
 ↓
2 hours/day
```

### Step 6 — LLM

Agent asks the LLM to identify appropriate milestones and tasks.

### Step 7 — Tools

Agent uses:

```text
create_milestone()
create_task()
```

### Step 8 — Database

The generated plan is stored.

### Step 9 — Job completion

```text
Job Status
QUEUED
   ↓
RUNNING
   ↓
COMPLETED
```

### Step 10 — User

The user sees:

```text
Full Stack Development

Milestone 1: HTML & CSS
  ├── Learn HTML basics
  ├── Forms
  ├── CSS selectors
  └── Flexbox

Milestone 2: JavaScript
  ├── Variables
  ├── Functions
  ├── DOM
  └── Events

...
```

---

# 22. Error Handling

Each important layer should handle failures appropriately.

```text
LLM Failure
    ↓
Agent catches error
    ↓
Job marked FAILED
    ↓
Error logged
    ↓
User receives meaningful message
```

A failed operation must never be reported as successful.

Example:

```text
Job Status:

QUEUED
  ↓
RUNNING
  ↓
FAILED
```

The job can later support retries, but **automatic retry is not required for the first MVP**.

---

# 23. What Each Concept Teaches

| Component         | Agentic AI Concept           |
| ----------------- | ---------------------------- |
| `agent.py`        | Agent / orchestration        |
| `state.py`        | Agent state                  |
| `tools/`          | Tool calling                 |
| `prompts.py`      | Agent instructions           |
| `llm/client.py`   | Model interaction            |
| `job.py`          | Background work unit         |
| `job_queue.py`    | Queuing                      |
| `worker.py`       | Job execution                |
| `services/`       | Business logic               |
| `repositories.py` | Data access                  |
| `database/`       | Persistent memory            |
| `tracer.py`       | Traceability / observability |
| `tests/`          | Reliability / evaluation     |

---

# 24. MVP Scope

The first implementation should contain:

### Core

* Goal creation
* Goal decomposition
* Schedule generation
* Progress tracking
* Daily task recommendation

### Agentic concepts

* Agent
* LLM
* Tools
* State
* Job
* Queue
* Worker
* Database memory
* Traceability

### Deliberately excluded for now

* Authentication
* Multiple users
* Multi-agent systems
* Redis
* Kafka
* Vector database
* RAG
* Notifications
* Calendar integration
* Automatic replanning
* Complex distributed workers

The goal is to **understand the architecture**, not to make a huge production system.

---

# 25. Final LLD Architecture

```text
                    ┌──────────────┐
                    │     USER     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   FRONTEND   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │     API      │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │   SERVICES   │          │   JOB QUEUE  │
       └──────┬───────┘          └──────┬───────┘
              │                         │
              │                         ▼
              │                  ┌──────────────┐
              │                  │    WORKER    │
              │                  └──────┬───────┘
              │                         │
              │                         ▼
              │                  ┌──────────────┐
              │                  │    AGENT     │
              │                  └──────┬───────┘
              │                    ┌────┼────┐
              │                    │    │    │
              │                    ▼    ▼    ▼
              │                  STATE TOOLS LLM
              │                    │    │    │
              └────────────────────┼────┘    │
                                   ▼         │
                              ┌──────────┐   │
                              │DATABASE  │◄──┘
                              └────┬─────┘
                                   │
                                   ▼
                              ┌──────────┐
                              │ TRACER   │
                              └──────────┘
```

## Design Principle

The important idea behind this LLD is:

**The API receives the request → a job represents the work → a worker executes the job → the agent decides what to do → tools perform actions → services handle business logic → the database stores state → the tracer records what happened.**

That gives you a small project while letting you **actually see how the Agentic AI pieces you've been learning fit together in one system**.
