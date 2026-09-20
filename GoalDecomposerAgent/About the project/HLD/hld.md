# Goal Decomposer — High-Level Design

## 1. System Overview

**Goal Decomposer** is an agentic AI application that helps users convert a large goal into manageable milestones and tasks, generate a simple schedule, track progress, and receive daily task recommendations.

The system consists of five major parts:

1. **User Interface**
2. **Backend / Application Layer**
3. **AI Agent**
4. **Database**
5. **LLM Provider**

---

## 2. High-Level Architecture

```text
                         ┌──────────────────────┐
                         │        USER          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    USER INTERFACE    │
                         │                      │
                         │ • Create Goal        │
                         │ • View Plan          │
                         │ • Track Progress     │
                         │ • Get Daily Tasks    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   BACKEND / API      │
                         │                      │
                         │ • Request Handling   │
                         │ • Validation         │
                         │ • Business Logic     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      AI AGENT        │
                         │                      │
                         │ • Understand Goal    │
                         │ • Decompose Goal     │
                         │ • Generate Schedule  │
                         │ • Recommend Tasks    │
                         └───────┬───────┬──────┘
                                 │       │
                    ┌────────────┘       └────────────┐
                    ▼                                 ▼
          ┌──────────────────┐              ┌──────────────────┐
          │      TOOLS       │              │   LLM PROVIDER   │
          │                  │              │                  │
          │ • Date/Time      │              │ • Goal Analysis  │
          │ • Scheduling     │              │ • Decomposition  │
          │ • Progress       │              │ • Recommendations│
          │ • Task Management│              └──────────────────┘
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │     DATABASE     │
          │                  │
          │ • Goals          │
          │ • Milestones     │
          │ • Tasks          │
          │ • Progress       │
          └──────────────────┘
```

---

# 3. Major Components

## 3.1 User Interface

The UI is the interaction layer between the user and the system.

### Responsibilities

* Accept goal details from the user.
* Display generated milestones and tasks.
* Display the schedule.
* Allow the user to update task status.
* Display overall progress.
* Show recommended daily tasks.

### Example

```text
Goal:
Learn Full Stack Development

Deadline:
30 December 2026

Available Time:
2 hours/day
```

The UI sends these details to the backend.

---

## 3.2 Backend / API Layer

The backend acts as the central controller of the application.

### Responsibilities

* Receive requests from the UI.
* Validate user input.
* Communicate with the AI agent.
* Manage database operations.
* Return results to the UI.

### Example APIs

```text
POST   /goals
POST   /goals/{id}/decompose
POST   /goals/{id}/schedule
GET    /goals/{id}
PATCH  /tasks/{id}
GET    /goals/{id}/daily-tasks
```

The exact API design will be defined later during the **API Design phase**.

---

# 4. AI Agent

The AI Agent is the main intelligent component of the system.

Instead of simply asking an LLM:

> "Break this goal into tasks."

the agent uses the user's goal, deadline, available time, existing tasks, and progress to decide what action is required.

### Main responsibilities

```text
Understand Goal
      ↓
Decompose Goal
      ↓
Create Tasks
      ↓
Generate Schedule
      ↓
Check Progress
      ↓
Recommend Daily Tasks
```

The detailed agent architecture will be designed separately during the **Agent Design** phase.

---

# 5. Tools

The agent can use a small set of tools to perform deterministic operations.

### Initial tools

| Tool                         | Purpose                                   |
| ---------------------------- | ----------------------------------------- |
| `get_current_date()`         | Gets the current date                     |
| `calculate_available_days()` | Calculates time available before deadline |
| `create_milestone()`         | Creates a milestone                       |
| `create_task()`              | Creates a task                            |
| `generate_schedule()`        | Assigns tasks to available dates          |
| `update_task_status()`       | Updates task completion status            |
| `get_progress()`             | Calculates current progress               |
| `get_pending_tasks()`        | Retrieves unfinished tasks                |

The exact tool schemas will be designed later.

---

# 6. LLM Provider

The LLM provides the natural-language intelligence required by the agent.

It can be used for:

* Understanding vague goals.
* Identifying milestones.
* Breaking milestones into tasks.
* Estimating task effort.
* Generating useful task recommendations.

The application should communicate with the LLM through a dedicated service/module rather than directly from every part of the application.

This makes it easier to change the model later.

---

# 7. Database

The database stores the persistent state of the application.

### Main entities

```text
GOAL
  │
  ├──── MILESTONE
  │          │
  │          └──── TASK
  │
  └──── Progress
```

### Main data stored

**Goal**

* Goal ID
* Description
* Deadline
* Available time
* Created date

**Milestone**

* Milestone ID
* Goal ID
* Title
* Description
* Order

**Task**

* Task ID
* Milestone ID
* Title
* Description
* Scheduled date
* Status
* Estimated effort

The detailed database schema and ER diagram will be created in the **Database Design** phase.

---

# 8. Main System Flows

## Flow 1 — Create and Decompose Goal

```text
User
 ↓
Enter Goal Details
 ↓
Backend
 ↓
AI Agent
 ↓
Analyze Goal
 ↓
Generate Milestones
 ↓
Generate Tasks
 ↓
Save to Database
 ↓
Display Plan
```

---

## Flow 2 — Generate Schedule

```text
User
 ↓
Request Schedule
 ↓
Backend
 ↓
AI Agent
 ↓
Read Goal + Tasks + Deadline
 ↓
Calculate Available Time
 ↓
Generate Schedule
 ↓
Save Schedule
 ↓
Display Schedule
```

---

## Flow 3 — Track Progress

```text
User
 ↓
Mark Task Complete
 ↓
Backend
 ↓
Update Database
 ↓
Calculate Progress
 ↓
Display Updated Progress
```

---

## Flow 4 — Daily Task Recommendation

```text
User
 ↓
Request Today's Tasks
 ↓
Backend
 ↓
AI Agent
 ↓
Read Pending Tasks
 ↓
Check Schedule + Current Date
 ↓
Select Suitable Tasks
 ↓
Return Recommendation
 ↓
Display to User
```

---

# 9. Technology Stack

For the first version, the stack can remain simple:

| Layer           | Technology                       |
| --------------- | -------------------------------- |
| Frontend        | HTML/CSS/JavaScript or Streamlit |
| Backend         | Python + FastAPI                 |
| Agent           | Python                           |
| LLM             | Any suitable LLM API             |
| Database        | SQLite                           |
| API Format      | REST                             |
| Version Control | Git + GitHub                     |

You can replace SQLite with PostgreSQL later if the project grows.

---

# 10. Deployment-Level View

For the initial MVP:

```text
             USER
               │
               ▼
        ┌─────────────┐
        │   Frontend  │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │   FastAPI   │
        │   Backend   │
        └──────┬──────┘
               │
       ┌───────┴────────┐
       ▼                ▼
 ┌──────────┐      ┌──────────┐
 │ AI Agent │      │  SQLite  │
 └────┬─────┘      └──────────┘
      │
      ▼
 ┌──────────┐
 │ LLM API  │
 └──────────┘
```

For the MVP, all application components can initially run on a single machine.

---

# 11. Design Principles

The HLD follows these principles:

### Separation of Concerns

Each component has a specific responsibility.

```text
UI          → User interaction
Backend     → Application logic
Agent       → Intelligent decision making
Tools       → Deterministic actions
Database    → Persistent data
LLM         → Language reasoning
```

### Modularity

The agent, tools, database operations, and API layer should be separated so that each part can be modified independently.

### Simplicity

The first version intentionally avoids:

* Authentication
* Notifications
* Calendar integration
* Multi-agent architecture
* Real-time collaboration
* Complex analytics
* Automatic replanning

These can be considered future extensions.

---

# 12. HLD Summary

The **Goal Decomposer** follows a simple layered architecture:

```text
User
 ↓
Frontend
 ↓
Backend / API
 ↓
AI Agent
 ├── LLM
 └── Tools
       ↓
    Database
```

The architecture is intentionally small enough for an MVP while keeping the components separated so that additional functionality can be added later without redesigning the entire application.
