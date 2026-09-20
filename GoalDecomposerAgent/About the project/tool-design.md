Absolutely love ❤️ Let's do **Tool Design** next, keeping the same MVP scope and company-style architecture.

# Goal Decomposer — Tool Design

## 1. What is a Tool?

In our agentic system:

> **Agent decides what needs to be done → Tool actually performs the action.**

For example:

```text
User:
"Break my goal of learning Full Stack into tasks."

        ↓

      Agent
        ↓
  "I need the goal details"
        ↓
   get_goal()
        ↓
  "Now I need to create tasks"
        ↓
   create_task()
        ↓
    Database
```

The LLM should **not directly access the database**.

Instead:

```text
LLM
 ↓
Agent
 ↓
Tool
 ↓
Service / Repository
 ↓
Database
```

This gives us **control, validation, security, and traceability**.

---

# 2. Tool Categories

For our Goal Decomposer, we only need four tool groups:

```text
                 AGENT
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
     GOAL        TASK       SCHEDULE
     TOOLS       TOOLS        TOOLS
       │           │           │
       └───────────┼───────────┘
                   ↓
              PROGRESS TOOLS
```

### Goal Tools

Work with goal information.

### Task Tools

Create, retrieve, and update tasks.

### Schedule Tools

Calculate dates and generate schedules.

### Progress Tools

Calculate and retrieve progress.

---

# 3. Goal Tools

File:

```text
app/tools/goal_tools.py
```

## `create_goal()`

### Purpose

Creates a new goal.

```python
create_goal(
    description,
    deadline,
    available_hours_per_day
)
```

Example:

```text
create_goal(
    "Learn Full Stack Development",
    "2026-12-30",
    2
)
```

Returns:

```json
{
  "goal_id": 1,
  "status": "ACTIVE"
}
```

### Flow

```text
Agent
 ↓
create_goal()
 ↓
Goal Service
 ↓
Goal Repository
 ↓
Database
```

---

## `get_goal()`

### Purpose

Retrieves information about an existing goal.

```python
get_goal(goal_id)
```

Example:

```python
get_goal(1)
```

Returns:

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

# 4. Task Tools

File:

```text
app/tools/task_tools.py
```

## `create_task()`

### Purpose

Creates an actionable task.

```python
create_task(
    milestone_id,
    title,
    description,
    estimated_minutes
)
```

Example:

```python
create_task(
    10,
    "Learn CSS selectors",
    "Study basic CSS selectors and practice examples",
    45
)
```

Returns:

```json
{
  "task_id": 25,
  "status": "PENDING"
}
```

---

## `get_pending_tasks()`

### Purpose

Retrieves incomplete tasks.

```python
get_pending_tasks(goal_id)
```

Example:

```python
get_pending_tasks(1)
```

Returns:

```json
[
  {
    "task_id": 25,
    "title": "Learn CSS selectors",
    "status": "PENDING"
  },
  {
    "task_id": 26,
    "title": "Practice Flexbox",
    "status": "PENDING"
  }
]
```

This tool can be used when the agent needs to recommend today's work.

---

## `update_task_status()`

### Purpose

Changes the status of a task.

```python
update_task_status(
    task_id,
    status
)
```

Example:

```python
update_task_status(
    25,
    "COMPLETED"
)
```

Returns:

```json
{
  "task_id": 25,
  "status": "COMPLETED",
  "updated": true
}
```

### Important

The agent should **never invent task completion**.

The user or application must indicate that the task is complete.

---

# 5. Schedule Tools

File:

```text
app/tools/schedule_tools.py
```

These tools are especially useful because date calculations should be handled by normal code rather than asking an LLM to calculate dates.

---

## `get_current_date()`

### Purpose

Gets today's date.

```python
get_current_date()
```

Example result:

```json
{
  "date": "2026-09-20"
}
```

---

## `calculate_available_days()`

### Purpose

Calculates how many days are available before the deadline.

```python
calculate_available_days(
    current_date,
    deadline
)
```

Example:

```text
Current date: 2026-09-20
Deadline:     2026-09-30
```

Result:

```json
{
  "available_days": 10
}
```

This should be deterministic Python code.

---

## `generate_schedule()`

### Purpose

Assigns tasks to available dates based on:

- task duration
- available hours per day
- deadline
- task ordering

```python
generate_schedule(
    tasks,
    available_hours_per_day,
    current_date,
    deadline
)
```

Example output:

```json
[
  {
    "task_id": 25,
    "scheduled_date": "2026-09-21"
  },
  {
    "task_id": 26,
    "scheduled_date": "2026-09-21"
  },
  {
    "task_id": 27,
    "scheduled_date": "2026-09-22"
  }
]
```

### Important design principle

The LLM can suggest **what should be learned first**, but actual date allocation should preferably be deterministic.

```text
LLM
 ↓
Task ordering / reasoning
 ↓
generate_schedule()
 ↓
Deterministic date calculation
```

---

# 6. Progress Tools

File:

```text
app/tools/progress_tools.py
```

## `get_progress()`

### Purpose

Calculates the current progress of a goal.

```python
get_progress(goal_id)
```

Example:

```json
{
  "goal_id": 1,
  "total_tasks": 20,
  "completed_tasks": 8,
  "pending_tasks": 12,
  "progress_percentage": 40
}
```

Formula:

```text
progress_percentage =
    completed_tasks / total_tasks × 100
```

No LLM is needed.

---

## `get_completed_tasks()`

### Purpose

Retrieves completed tasks.

```python
get_completed_tasks(goal_id)
```

Example:

```json
[
  {
    "task_id": 1,
    "title": "Learn HTML",
    "status": "COMPLETED"
  }
]
```

---

# 7. Tool Registry

Instead of writing:

```python
if tool_name == "create_goal":
    ...
elif tool_name == "create_task":
    ...
elif tool_name == "get_progress":
    ...
```

we can use a **tool registry**.

```python
TOOLS = {
    "create_goal": create_goal,
    "get_goal": get_goal,
    "create_task": create_task,
    "get_pending_tasks": get_pending_tasks,
    "update_task_status": update_task_status,
    "get_current_date": get_current_date,
    "calculate_available_days": calculate_available_days,
    "generate_schedule": generate_schedule,
    "get_progress": get_progress,
    "get_completed_tasks": get_completed_tasks
}
```

Then the agent can dynamically select the required tool.

```python
tool = TOOLS[action.tool_name]

result = tool(**action.arguments)
```

This is called **dynamic tool dispatch**.

---

# 8. Tool Schema

The LLM shouldn't just receive:

```text
create_task
```

It should know:

- what the tool does
- what parameters it accepts
- what each parameter means
- what type each parameter has

Example:

```json
{
  "name": "create_task",
  "description": "Create an actionable task for a milestone",
  "parameters": {
    "type": "object",
    "properties": {
      "milestone_id": {
        "type": "integer"
      },
      "title": {
        "type": "string"
      },
      "description": {
        "type": "string"
      },
      "estimated_minutes": {
        "type": "integer"
      }
    },
    "required": [
      "milestone_id",
      "title",
      "estimated_minutes"
    ]
  }
}
```

The LLM can then produce something like:

```json
{
  "tool": "create_task",
  "arguments": {
    "milestone_id": 10,
    "title": "Learn CSS selectors",
    "description": "Study basic CSS selectors",
    "estimated_minutes": 45
  }
}
```

The agent reads this and performs the actual function call.

---

# 9. Complete Tool Flow

Suppose the user says:

> "Break my Full Stack goal into actionable tasks."

The flow becomes:

```text
                 USER
                   │
                   ▼
                AGENT
                   │
                   ▼
             Understand Goal
                   │
                   ▼
                LLM
                   │
                   ▼
          Decide Required Action
                   │
                   ▼
          get_goal(goal_id)
                   │
                   ▼
             Goal Information
                   │
                   ▼
                 LLM
                   │
                   ▼
         Generate Milestones
                   │
                   ▼
            create_task()
                   │
                   ▼
               DATABASE
                   │
                   ▼
             Tool Result
                   │
                   ▼
             Update State
                   │
                   ▼
              More Tasks?
              /         \
            YES          NO
             │            │
             └──→ Tool    ▼
                    Calls Final Result
```

---

# 10. Tool vs LLM

This distinction is **very important** for your agentic AI learning.

| ResponsibilityLLMTool    |   |   |
| ------------------------ | - | - |
| Understand vague goal    | ✅ | ❌ |
| Suggest milestones       | ✅ | ❌ |
| Suggest actionable tasks | ✅ | ❌ |
| Calculate dates          | ❌ | ✅ |
| Create database record   | ❌ | ✅ |
| Read database            | ❌ | ✅ |
| Calculate progress       | ❌ | ✅ |
| Recommend tasks          | ✅ | ❌ |
| Update task status       | ❌ | ✅ |

### Easy rule

> **LLM thinks/reasons. Tools perform controlled actions.**

---

# 11. Tool Safety

Tools are powerful because they can change application data.

Therefore, tools should have boundaries.

### The agent should NOT be able to:

```text
❌ Execute arbitrary SQL
❌ Delete the entire database
❌ Modify unrelated goals
❌ Mark tasks complete without confirmation
❌ Access API keys
❌ Call unknown functions
❌ Modify files outside the application
```

Instead:

```text
Agent
  ↓
Allowed Tool
  ↓
Validated Parameters
  ↓
Service
  ↓
Repository
  ↓
Database
```

---

# 12. Tool Error Handling

Every tool should handle failures.

Example:

```python
try:
    result = create_task(...)
except Exception as e:
    return {
        "success": False,
        "error": str(e)
    }
```

Better structured result:

```json
{
  "success": false,
  "tool": "create_task",
  "error": "Milestone does not exist"
}
```

The agent can then observe the failure:

```text
Tool Call
   ↓
Tool Failed
   ↓
Observation
   ↓
Agent State Updated
   ↓
Agent decides next action
```

This is an important part of the **Observe** stage of the agent loop.

---

# 13. Tool Traceability

Every important tool call should be recorded.

Example:

```text
AGENT_STARTED
      ↓
TOOL_CALLED: get_goal
      ↓
TOOL_COMPLETED: get_goal
      ↓
TOOL_CALLED: create_task
      ↓
TOOL_COMPLETED: create_task
      ↓
TOOL_CALLED: create_task
      ↓
TOOL_FAILED: create_task
      ↓
AGENT_COMPLETED
```

Our `AGENT_TRACE` table can store this information.

Example:

```json
{
  "event_type": "TOOL_CALLED",
  "tool_name": "create_task",
  "status": "SUCCESS",
  "duration_ms": 124
}
```

This helps with:

- debugging
- monitoring
- understanding agent behavior
- finding failed tool calls
- evaluating the agent

---

# 14. Final Tool Architecture

```text
                         AGENT
                           │
                           ▼
                    Tool Selection
                           │
                           ▼
                    Tool Registry
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
       ▼                   ▼                   ▼
  Goal Tools          Task Tools        Schedule Tools
       │                   │                   │
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                           ▼
                    Progress Tools
                           │
                           ▼
                      Services
                           │
                           ▼
                     Repositories
                           │
                           ▼
                       DATABASE
```

---

# 15. Final Tool List for MVP

```text
GOAL TOOLS
───────────
create_goal()
get_goal()

TASK TOOLS
──────────
create_task()
get_pending_tasks()
update_task_status()

SCHEDULE TOOLS
──────────────
get_current_date()
calculate_available_days()
generate_schedule()

PROGRESS TOOLS
───────────────
get_progress()
get_completed_tasks()
```

That's **10 tools total**, which is enough for our current MVP.

The important thing is that we're **not adding tools just to make the project look "agentic."** Each tool has a clear responsibility and is connected to an actual agent workflow.

### The mental model to remember ❤️

```text
        LLM
         │
   "What should I do?"
         ↓
       AGENT
         │
   "Which action?"
         ↓
       TOOL
         │
   "Perform action"
         ↓
      DATABASE
         │
   "Here is the result"
         ↓
       AGENT
         │
      OBSERVE
         ↓
   Continue / Finish
```

This is the core **Tool Design** for your Goal Decomposer.