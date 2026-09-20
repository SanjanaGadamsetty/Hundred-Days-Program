# Goal Decomposer — Agent Design

## 1. Purpose of the Agent

The Goal Decomposer Agent is responsible for understanding the user's goal, deciding what action is required, using appropriate tools, and producing a useful result.

The agent should not directly perform every operation itself.

Instead:

```text
Agent
  ↓
Decides what needs to happen
  ↓
Selects appropriate tool
  ↓
Tool performs the action
  ↓
Agent observes result
  ↓
Agent decides next step
```

This is the core agentic behavior of the system.

---

# 2. Agent Responsibilities

The Goal Decomposer Agent has four main responsibilities:

### 1. Understand

Understand the user's goal and available information.

### 2. Plan

Determine what needs to be done.

### 3. Act

Use tools to perform required operations.

### 4. Observe

Read the result of each action and decide whether another action is required.

```text
Understand
    ↓
Plan
    ↓
Act
    ↓
Observe
    ↓
Done / Continue
```

---

# 3. Agent vs LLM

This distinction is important.

An **LLM is not the entire agent**.

```text
                 AGENT
        ┌────────────────────┐
        │ Instructions        │
        │ State               │
        │ Decision Logic      │
        │ Tool Selection      │
        │ Tool Execution      │
        │ Observation         │
        └─────────┬──────────┘
                  │
                  ▼
                LLM
        ┌────────────────────┐
        │ Language reasoning │
        │ Goal understanding │
        │ Planning assistance│
        └────────────────────┘
```

### LLM

Provides reasoning and language understanding.

### Agent

Controls the complete process and decides what to do next.

---

# 4. Agent Inputs

The agent can receive:

```text
User Request
Goal Information
Deadline
Available Time
Current Date
Existing Milestones
Existing Tasks
Task Status
Progress
Previous Tool Results
```

Example:

```text
Goal:
Learn Full Stack Development

Deadline:
30 December 2026

Available Time:
2 hours/day

Current Progress:
35%

Pending Tasks:
12
```

The agent uses this information to decide what action is appropriate.

---

# 5. Agent State

The agent maintains a structured state during execution.

```text
AgentState
│
├── goal_id
├── user_request
├── goal
├── deadline
├── available_time
├── current_date
├── milestones
├── tasks
├── progress
├── current_action
├── tool_results
└── status
```

Example:

```text
goal_id = 101

goal = "Learn Full Stack Development"

deadline = "2026-12-30"

available_time = "2 hours/day"

progress = 35%

current_action = "generate_schedule"

status = "RUNNING"
```

---

# 6. Why Agent State Is Needed

Imagine the agent performs:

```text
Step 1 → Read Goal
Step 2 → Generate Milestones
Step 3 → Create Tasks
Step 4 → Generate Schedule
```

The agent needs to know what happened in previous steps.

Therefore:

```text
                    ┌──────────────┐
                    │ Agent State  │
                    ├──────────────┤
                    │ Goal         │
                    │ Milestones   │
                    │ Tasks        │
                    │ Progress     │
                    │ Tool Results │
                    └──────▲───────┘
                           │
                           │
                         Agent
```

State represents the agent's **current working context**.

---

# 7. Agent Tools

The agent should have access to a small set of tools.

### Goal Tools

```text
create_goal()
get_goal()
```

### Task Tools

```text
create_task()
get_pending_tasks()
update_task_status()
```

### Schedule Tools

```text
get_current_date()
calculate_available_days()
generate_schedule()
```

### Progress Tools

```text
get_progress()
get_completed_tasks()
```

---

# 8. Tool Responsibility

Each tool should perform **one clear operation**.

For example:

```text
generate_schedule()
```

should generate or calculate a schedule.

It should not:

```text
generate_schedule()
    ├── call LLM
    ├── create user
    ├── update authentication
    ├── send notification
    └── modify unrelated data
```

Instead:

```text
Agent
  ↓
generate_schedule()
  ↓
Schedule Result
  ↓
Agent
```

This makes tools easier to test and maintain.

---

# 9. Tool Calling

The agent can determine which tool it needs.

Example:

User:

> "What should I work on today?"

Agent reasoning:

```text
I need:
- current date
- pending tasks
- schedule
```

It can then use:

```text
get_current_date()
        ↓
get_pending_tasks()
        ↓
generate / read schedule
        ↓
recommend tasks
```

---

# 10. Dynamic Tool Dispatch

A simple tool registry can be used.

```text
TOOL_REGISTRY

create_goal        → create_goal()
create_task        → create_task()
get_progress       → get_progress()
generate_schedule  → generate_schedule()
get_pending_tasks  → get_pending_tasks()
```

The agent receives a tool name:

```text
"get_progress"
```

The system dynamically finds the corresponding function.

```text
Agent
  ↓
"get_progress"
  ↓
Tool Registry
  ↓
get_progress()
  ↓
Result
  ↓
Agent
```

This gives the project practical experience with **dynamic dispatch**.

---

# 11. Agent Loop

The core agent loop is:

```text
             ┌──────────────────────┐
             │     Receive Input    │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │    Read State        │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │   Decide Next Action │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │      Call Tool       │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │   Observe Result     │
             └──────────┬───────────┘
                        ↓
                 More work needed?
                    /          \
                  YES           NO
                   │             │
                   └──→ Loop     ↓
                              Return
                              Result
```

This is the main **Perceive → Plan → Act → Observe** cycle.

---

# 12. Example Agent Loop

User says:

> "Create a plan to learn Python in 30 days."

### Iteration 1

Agent understands:

```text
Goal = Learn Python
Deadline = 30 days
```

Action:

```text
create_goal()
```

---

### Iteration 2

Agent decides:

```text
Need to break goal into milestones.
```

Action:

```text
LLM → generate milestones
```

---

### Iteration 3

Agent decides:

```text
Milestones exist.
Now create tasks.
```

Action:

```text
create_task()
```

---

### Iteration 4

Agent decides:

```text
Tasks exist.
Need schedule.
```

Action:

```text
generate_schedule()
```

---

### Iteration 5

Agent observes:

```text
Goal
✓ Created

Milestones
✓ Created

Tasks
✓ Created

Schedule
✓ Created
```

Agent returns:

```text
Plan successfully created.
```

---

# 13. Agent Decision Types

For the MVP, the agent only needs a few actions.

```text
CREATE_GOAL
DECOMPOSE_GOAL
GENERATE_SCHEDULE
TRACK_PROGRESS
RECOMMEND_TASKS
```

The agent maps the user's request to one of these actions.

Example:

| User Request                  | Agent Action      |
| ----------------------------- | ----------------- |
| "I want to learn Python"      | CREATE_GOAL       |
| "Break this into steps"       | DECOMPOSE_GOAL    |
| "Make a plan for these tasks" | GENERATE_SCHEDULE |
| "How much have I completed?"  | TRACK_PROGRESS    |
| "What should I do today?"     | RECOMMEND_TASKS   |

---

# 14. Agent Workflow by Use Case

## Use Case 1 — Create Goal

```text
User
 ↓
API
 ↓
Agent
 ↓
Validate goal information
 ↓
create_goal()
 ↓
Database
 ↓
Result
```

---

## Use Case 2 — Decompose Goal

```text
User
 ↓
API
 ↓
Job
 ↓
Worker
 ↓
Agent
 ↓
Read Goal
 ↓
LLM
 ↓
Generate Milestones
 ↓
Generate Tasks
 ↓
create_milestone()
create_task()
 ↓
Database
 ↓
Result
```

---

## Use Case 3 — Generate Schedule

```text
User
 ↓
Agent
 ↓
Read Goal
 ↓
Read Tasks
 ↓
Read Deadline
 ↓
get_current_date()
 ↓
calculate_available_days()
 ↓
generate_schedule()
 ↓
Database
 ↓
Schedule
```

---

## Use Case 4 — Track Progress

```text
User
 ↓
update_task_status()
 ↓
Database
 ↓
get_progress()
 ↓
Agent / Service
 ↓
Progress Result
 ↓
User
```

---

## Use Case 5 — Daily Task Recommendation

```text
User
 ↓
Agent
 ↓
get_current_date()
 ↓
get_pending_tasks()
 ↓
Read Schedule
 ↓
Analyze Tasks
 ↓
Recommend Tasks
 ↓
User
```

---

# 15. Agent + Job + Worker

For longer operations, the agent can run through a job.

```text
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
           ┌──────┼──────┐
           ▼      ▼      ▼
         Tools   LLM   State
           │      │      │
           └──────┼──────┘
                  ▼
               Result
```

### Important distinction

```text
Job
= A unit of work

Worker
= Executes the job

Agent
= Decides what actions are needed

Tool
= Performs a specific action
```

---

# 16. Synchronous Agent Operation

Some operations are quick.

Example:

```text
User marks task complete
          ↓
API
          ↓
update_task_status()
          ↓
Database
          ↓
Response
```

There is no need to create a background job.

---

# 17. Asynchronous Agent Operation

Goal decomposition may involve multiple LLM/tool operations.

Therefore:

```text
User requests decomposition
          ↓
API
          ↓
Create Job
          ↓
Return Job ID
          ↓
Worker
          ↓
Agent
          ↓
LLM + Tools
          ↓
Database
```

The job allows the API and agent execution to be separated.

---

# 18. Agent Memory

The project does not need a vector database.

For the MVP:

```text
Persistent Memory
       ↓
    SQLite
       ↓
Goals
Milestones
Tasks
Progress
```

When the agent needs information:

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
 ↓
Agent State
```

So the database provides **persistent application memory**.

---

# 19. Agent Instructions

The agent receives system-level instructions.

Example:

```text
You are the Goal Decomposer Agent.

Your responsibilities are:

1. Understand the user's goal.
2. Consider the deadline and available time.
3. Break the goal into meaningful milestones.
4. Break milestones into actionable tasks.
5. Generate a practical schedule.
6. Recommend pending tasks when requested.
7. Use tools for database operations.
8. Do not invent database state.
9. Return structured results.
```

The agent should follow these instructions consistently.

---

# 20. Structured Agent Output

The agent should preferably produce structured information rather than arbitrary text.

Example:

```json
{
  "action": "DECOMPOSE_GOAL",
  "goal_id": 101,
  "milestones": [
    {
      "title": "HTML & CSS",
      "tasks": [
        "Learn HTML basics",
        "Learn CSS selectors",
        "Practice Flexbox"
      ]
    }
  ]
}
```

This makes it easier for the application to process the result.

---

# 21. Guardrails

The agent should have basic restrictions.

### It should not:

* Modify unrelated goals.
* Create duplicate tasks unnecessarily.
* Invent task completion.
* Mark tasks complete without user confirmation.
* Expose API keys.
* Directly execute arbitrary database queries.
* Claim an operation succeeded when the tool failed.

### Example

If the user says:

> "Mark all my tasks complete."

The agent should not blindly do it.

It should follow the application's task-update rules and require the appropriate user action/confirmation if needed.

---

# 22. Error Handling

Agent execution can fail.

Possible failures:

```text
LLM failure
Tool failure
Database failure
Invalid input
Timeout
Malformed LLM response
```

Example:

```text
Agent
 ↓
Call Tool
 ↓
Tool Failure
 ↓
Catch Error
 ↓
Log Error
 ↓
Update Job = FAILED
 ↓
Return Meaningful Error
```

The system should never do:

```text
Tool failed
    ↓
Pretend success
```

---

# 23. Traceability

Every important agent action should be traceable.

Example:

```text
JOB_CREATED
      ↓
AGENT_STARTED
      ↓
LLM_REQUEST
      ↓
TOOL_CALLED: get_goal
      ↓
TOOL_CALLED: create_task
      ↓
DATABASE_UPDATED
      ↓
AGENT_COMPLETED
      ↓
JOB_COMPLETED
```

A trace record can contain:

```text
timestamp
job_id
goal_id
agent_action
tool_name
status
duration
error
```

This helps during debugging and evaluation.

---

# 24. Agent Architecture Diagram

```text
                         USER REQUEST
                              │
                              ▼
                     ┌─────────────────┐
                     │   Agent Input   │
                     └────────┬────────┘
                              ▼
                     ┌─────────────────┐
                     │  Agent State    │
                     └────────┬────────┘
                              ▼
                     ┌─────────────────┐
                     │  Agent Planner  │
                     │   / Decision    │
                     └────────┬────────┘
                              │
                     What should I do?
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         ┌─────────┐    ┌───────────┐   ┌──────────┐
         │   LLM   │    │   Tools   │   │ Database │
         └────┬────┘    └─────┬─────┘   └────┬─────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                     ┌─────────────────┐
                     │    Observe      │
                     │     Result      │
                     └────────┬────────┘
                              ▼
                       More work?
                       /         \
                     YES          NO
                      │            │
                      └─── LOOP    ▼
                              Final Result
```

---

# 25. Agent Execution Example

Consider:

> "I want to learn Machine Learning in 60 days and have 2 hours every day."

The agent's internal process is conceptually:

```text
REQUEST
   ↓
Understand goal
   ↓
Read deadline
   ↓
Read available time
   ↓
Calculate available days
   ↓
Ask LLM for milestone structure
   ↓
Validate result
   ↓
Create milestones
   ↓
Create tasks
   ↓
Generate schedule
   ↓
Save state
   ↓
Return plan
```

The important point is that the agent is not just generating a paragraph.

It is:

**understanding → deciding → acting → observing → updating state.**

---

# 26. What Makes This Agentic?

A simple LLM application might look like:

```text
User
 ↓
LLM
 ↓
Text Response
```

Your Goal Decomposer looks more like:

```text
User
 ↓
Agent
 ↓
Understand Request
 ↓
Decide Action
 ↓
Use Tools
 ↓
Read State
 ↓
Call LLM when needed
 ↓
Observe Results
 ↓
Update Database
 ↓
Continue / Finish
 ↓
User
```

That distinction is the main learning objective of this project.

---

# 27. Agent Design Principles

### 1. Tool-based actions

The agent should use tools instead of directly modifying application state.

### 2. Explicit state

Important context should be represented in structured state.

### 3. Small action space

The MVP agent should have only a small number of meaningful actions.

### 4. Deterministic operations stay deterministic

Date calculations, progress calculations, and database updates should be handled by normal code/tools rather than asking the LLM to calculate everything.

### 5. LLM handles language and planning

The LLM is most useful for:

* Understanding goals
* Identifying milestones
* Generating task ideas
* Producing recommendations

### 6. Trace everything important

Agent decisions and tool calls should be observable.

### 7. Fail safely

A failed tool call should produce a failed/partial result rather than fabricated success.

---

# 28. Final Agent Design

```text
                    GOAL DECOMPOSER AGENT
                              │
              ┌───────────────┴───────────────┐
              │                               │
         Agent State                     Instructions
              │                               │
              └───────────────┬───────────────┘
                              │
                              ▼
                       Decision / Planner
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
            LLM             Tools           Database
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                          Observation
                              │
                              ▼
                       Update State
                              │
                              ▼
                        Continue / End
```

### Core mental model

```text
          ┌───────────────────────────┐
          │           AGENT           │
          │                           │
          │  Understand               │
          │      ↓                    │
          │  Decide                   │
          │      ↓                    │
          │  Act                      │
          │      ↓                    │
          │  Observe                  │
          │      ↓                    │
          │  Update State             │
          │      ↓                    │
          │  Continue / Finish        │
          └───────────────────────────┘
```

This is the core architecture we'll implement in the Goal Decomposer.

The **LLM is the reasoning component**, the **agent is the orchestrator**, the **tools perform actions**, the **worker executes jobs**, the **queue holds jobs**, the **database provides persistent memory**, and the **tracer tells us what happened**.
