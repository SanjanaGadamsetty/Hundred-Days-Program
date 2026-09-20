# Goal Decomposer — API Design

## 1. API Architecture

```text
Frontend
   │
   │ HTTP Request
   ▼
FastAPI
   │
   ├── Goal APIs
   ├── Task APIs
   ├── Progress APIs
   └── Agent APIs
           │
           ▼
        Services
           │
           ▼
        Database
```

For agentic operations:

```text
Frontend
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
Worker
   │
   ▼
Agent
   │
   ├── LLM
   └── Tools
```

---

## 2. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/goals` | Create a new goal |
| `GET` | `/goals/{goal_id}` | Get goal details |
| `POST` | `/goals/{goal_id}/decompose` | Ask agent to decompose goal |
| `POST` | `/goals/{goal_id}/schedule` | Generate schedule |
| `GET` | `/goals/{goal_id}/tasks` | Get tasks |
| `PATCH` | `/tasks/{task_id}` | Update task status |
| `GET` | `/goals/{goal_id}/progress` | Get progress |
| `GET` | `/goals/{goal_id}/daily-tasks` | Get today's recommended tasks |
| `GET` | `/jobs/{job_id}` | Check background job status |

That's enough for the first version.

---

## 3. `POST /goals`

### Purpose

Creates a new goal.

### Request

```json
{
  "description": "Learn Full Stack Development",
  "deadline": "2026-12-30",
  "available_hours_per_day": 2
}
```

### Response

```json
{
  "goal_id": 1,
  "description": "Learn Full Stack Development",
  "deadline": "2026-12-30",
  "available_hours_per_day": 2,
  "status": "ACTIVE"
}
```

### Flow

```text
POST /goals
      ↓
Goal API
      ↓
Goal Service
      ↓
Goal Repository
      ↓
Database
      ↓
Response
```

This is a normal synchronous API.

---

## 4. `GET /goals/{goal_id}`

### Purpose

Retrieve a goal and its basic information.

Example:

```text
GET /goals/1
```

### Response

```json
{
  "goal_id": 1,
  "description": "Learn Full Stack Development",
  "deadline": "2026-12-30",
  "available_hours_per_day": 2,
  "status": "ACTIVE"
}
```

---

## 5. `POST /goals/{goal_id}/decompose`

This is one of the **main Agentic AI endpoints**.

### Request

```text
POST /goals/1/decompose
```

No large request body is necessary because the goal information already exists in the database.

### Response

Because decomposition may involve LLM processing, we can create a job:

```json
{
  "job_id": 101,
  "status": "QUEUED",
  "message": "Goal decomposition started"
}
```

### Internal flow

```text
POST /goals/1/decompose
          │
          ▼
     Create Job
          │
          ▼
      Job Queue
          │
          ▼
       Worker
          │
          ▼
        Agent
       /     \
      ▼       ▼
     LLM     Tools
      │       │
      └───┬───┘
          ▼
       Database
```

This endpoint gives practical experience with **jobs + workers**.

---

## 6. `GET /jobs/{job_id}`

The frontend can check whether the agent finished its work.

```text
GET /jobs/101
```

### Response while running

```json
{
  "job_id": 101,
  "status": "RUNNING"
}
```

### Response when completed

```json
{
  "job_id": 101,
  "status": "COMPLETED"
}
```

### Response when failed

```json
{
  "job_id": 101,
  "status": "FAILED",
  "error": "LLM request failed"
}
```

### Job lifecycle

```text
QUEUED → RUNNING → COMPLETED
                    │
                    └── or FAILED
```

---

## 7. `POST /goals/{goal_id}/schedule`

### Purpose

Generate a schedule from the existing tasks, deadline, and available time.

```text
POST /goals/1/schedule
```

### Response

For the MVP, this can also use a job:

```json
{
  "job_id": 102,
  "status": "QUEUED",
  "message": "Schedule generation started"
}
```

### Worker execution

```text
Worker
  ↓
Agent
  ↓
get_goal()
  ↓
get_tasks()
  ↓
get_current_date()
  ↓
calculate_available_days()
  ↓
generate_schedule()
  ↓
Database
```

---

## 8. `GET /goals/{goal_id}/tasks`

### Purpose

Retrieve all tasks belonging to a goal.

```text
GET /goals/1/tasks
```

### Response

```json
{
  "goal_id": 1,
  "tasks": [
    {
      "task_id": 1,
      "title": "Learn HTML basics",
      "status": "COMPLETED",
      "scheduled_date": "2026-09-21"
    },
    {
      "task_id": 2,
      "title": "Learn CSS selectors",
      "status": "PENDING",
      "scheduled_date": "2026-09-22"
    }
  ]
}
```

---

## 9. `PATCH /tasks/{task_id}`

### Purpose

Update the status of a task.

Example:

```text
PATCH /tasks/2
```

### Request

```json
{
  "status": "COMPLETED"
}
```

### Response

```json
{
  "task_id": 2,
  "status": "COMPLETED",
  "updated": true
}
```

This does **not need the LLM**.

```text
User
 ↓
API
 ↓
Task Service
 ↓
Database
 ↓
Response
```

This is a good example of a deterministic operation that should remain normal code.

---

## 10. `GET /goals/{goal_id}/progress`

### Purpose

Show overall goal progress.

```text
GET /goals/1/progress
```

### Response

```json
{
  "goal_id": 1,
  "total_tasks": 20,
  "completed_tasks": 8,
  "pending_tasks": 12,
  "progress_percentage": 40
}
```

The percentage can simply be calculated:

```text
progress =
completed_tasks / total_tasks × 100
```

No LLM is required.

---

## 11. `GET /goals/{goal_id}/daily-tasks`

This is another small **Agentic AI use case**.

```text
GET /goals/1/daily-tasks
```

The agent can:

```text
Get Current Date
       ↓
Get Pending Tasks
       ↓
Read Schedule
       ↓
Consider Available Time
       ↓
Recommend Tasks
```

### Response

```json
{
  "goal_id": 1,
  "date": "2026-09-21",
  "recommended_tasks": [
    {
      "task_id": 2,
      "title": "Learn CSS selectors",
      "estimated_minutes": 45
    },
    {
      "task_id": 3,
      "title": "Practice Flexbox",
      "estimated_minutes": 60
    }
  ]
}
```

---

## 12. API Status Codes

Use standard HTTP status codes.

| Status | Meaning | Example |
|---|---|---|
| `200` | Successful request | Get goal |
| `201` | Resource created | Create goal |
| `202` | Request accepted for background processing | Start decomposition |
| `400` | Invalid request | Invalid deadline |
| `404` | Resource not found | Goal doesn't exist |
| `422` | Validation error | Missing required field |
| `500` | Server error | Unexpected failure |

For background jobs, the initial creation can return:

```text
202 Accepted
```

because the request has been accepted but the actual agent work hasn't finished yet.

---

## 13. API Request Flow

### Normal operation

```text
Client
  │
  │ HTTP Request
  ▼
FastAPI Endpoint
  │
  ▼
Service
  │
  ▼
Repository
  │
  ▼
Database
  │
  ▼
JSON Response
```

### Agent operation

```text
Client
  │
  ▼
FastAPI
  │
  ▼
Create Job
  │
  ▼
Queue
  │
  ▼
Worker
  │
  ▼
Agent
  │
  ├──────► LLM
  │
  └──────► Tools
             │
             ▼
          Database
             │
             ▼
        Job Completed
```

---

## 14. API → Agent → Tool Relationship

Suppose the user requests:

> "Break my goal into tasks."

The API **doesn't directly call every tool**.

Instead:

```text
POST /goals/1/decompose
          ↓
       API Layer
          ↓
       Create Job
          ↓
        Worker
          ↓
        Agent
          ↓
    "I need to decompose
        this goal."
          ↓
        LLM
          ↓
    Structured Plan
          ↓
      create_task()
          ↓
       Database
```

So:

**API receives the request.  
Worker executes the job.  
Agent decides what to do.  
LLM helps with reasoning.  
Tools perform actions.  
Database stores the result.**

---

## 15. Final API List

```text
GOAL APIs
─────────
POST   /goals
GET    /goals/{goal_id}

AGENT APIs
──────────
POST   /goals/{goal_id}/decompose
POST   /goals/{goal_id}/schedule
GET    /goals/{goal_id}/daily-tasks

TASK APIs
─────────
GET    /goals/{goal_id}/tasks
PATCH  /tasks/{task_id}

PROGRESS API
────────────
GET    /goals/{goal_id}/progress

JOB API
───────
GET    /jobs/{job_id}
```

This is the **clean MVP API design**: enough endpoints to implement every agreed functional requirement while giving practical exposure to **REST APIs + background jobs + workers + agents + tools + LLMs** without overengineering the project.
