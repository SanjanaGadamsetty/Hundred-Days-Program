## Use Case Diagram — Goal Decomposer

### Actor

**User**

### Use Cases

**UC-01: Create Goal**

* User enters a goal description.
* User provides a deadline.
* User specifies available time.
* System creates and stores the goal.

**UC-02: Decompose Goal**

* Agent analyzes the goal.
* Agent identifies suitable milestones.
* Agent breaks milestones into actionable tasks.
* System stores the generated plan.

**UC-03: Generate Schedule**

* Agent considers the deadline and available time.
* System assigns tasks across the available period.
* System generates a simple schedule.

**UC-04: Track Progress**

* User marks tasks as completed or pending.
* System updates task status.
* System calculates and displays overall progress.

**UC-05: Get Daily Task Recommendation**

* User requests today's tasks.
* Agent checks the current plan and pending tasks.
* System recommends tasks the user can work on.