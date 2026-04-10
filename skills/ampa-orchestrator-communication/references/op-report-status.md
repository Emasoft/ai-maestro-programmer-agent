---
name: op-report-status
description: Send status updates to AMOA
parent-skill: ampa-orchestrator-communication
---

# Report Status

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

This operation describes how to send "in development" status updates to the AI
Maestro Orchestrator Agent (AMOA) to keep the orchestrator informed of your
progress on assigned tasks.

## 2.1 When to Report Status

Send status updates to AMOA in these situations:

| Situation                     | Frequency                        | Priority |
| ----------------------------- | -------------------------------- | -------- |
| **Starting a task**           | Once at beginning                | `normal` |
| **Major milestone reached**   | When significant progress made   | `normal` |
| **Phase transition**          | Moving from one phase to another | `normal` |
| **Extended task (> 2 hours)** | Every 1-2 hours                  | `normal` |
| **About to go offline**       | Before ending session            | `high`   |
| **Significant delay**         | When timeline affected           | `high`   |

**Status Update Triggers**:

1. **Task Start**: When you begin working on a task
2. **Test Phase Complete**: When tests are written and passing/failing as
   expected
3. **Implementation Complete**: When code implementation is done
4. **Refactoring Complete**: When code cleanup is finished
5. **Ready for Review**: When all work is complete

## Prerequisites

Before sending a status update:

1. **Have active task**: You must be working on an assigned task
2. **Know current progress**: Assess your actual progress percentage
3. **Identify blockers**: Note any issues affecting progress
4. **Estimate completion**: Have realistic time estimate

## 2.2 Status Message Format

Structure your status update with these components:

> **Note**: The structure below shows the conceptual message content. Use the
> `agent-messaging` skill to send messages - it handles the exact API format
> automatically.

```json
{
  "to": "orchestrator-master",
  "subject": "STATUS: [UUID] - [Current Phase]",
  "priority": "normal",
  "content": {
    "type": "status-update",
    "message": "[Brief status summary]",
    "task_id": "[UUID-FORMAT]",
    "phase": "[current-phase]",
    "progress_percent": [0-100],
    "completed": [
      "[Completed item 1]",
      "[Completed item 2]"
    ],
    "in_progress": "[Current work item]",
    "remaining": [
      "[Remaining item 1]",
      "[Remaining item 2]"
    ],
    "blockers": [],
    "estimated_completion": "[Time estimate]"
  }
}
```

### Message Components

| Field                  | Description                                 | Required |
| ---------------------- | ------------------------------------------- | -------- |
| `task_id`              | The identifier of the task (UUID format)    | Yes      |
| `phase`                | Current development phase (see section 2.3) | Yes      |
| `progress_percent`     | Percentage complete (0-100)                 | Yes      |
| `completed`            | Array of completed items                    | Yes      |
| `in_progress`          | Current work item                           | Yes      |
| `remaining`            | Array of remaining items                    | Yes      |
| `blockers`             | Array of blocking issues (empty if none)    | Yes      |
| `estimated_completion` | Time estimate to completion                 | No       |

## 2.3 Progress Indicators

### Development Phases

Use these standardized phase names:

| Phase            | Description                               | Typical Progress % |
| ---------------- | ----------------------------------------- | ------------------ |
| `planning`       | Analyzing requirements, planning approach | 0-10%              |
| `test-writing`   | Writing failing tests (TDD)               | 10-25%             |
| `implementation` | Writing code to pass tests                | 25-60%             |
| `refactoring`    | Code cleanup and optimization             | 60-80%             |
| `documentation`  | Writing/updating documentation            | 80-90%             |
| `review-prep`    | Preparing for review, final checks        | 90-100%            |

### Progress Calculation

Calculate progress based on completed items:

```text
progress_percent = (completed_items / total_items) * 100
```

**Example**:

- Task has 5 items: tests, core logic, edge cases, refactoring, docs
- Completed: tests, core logic (2 items)
- Progress: (2 / 5) \* 100 = 40%

## Procedure

Follow these steps to report status:

1. **Assess current state**: Determine phase, progress, and remaining work
2. **Identify blockers**: Note any issues preventing progress
3. **Estimate completion**: Calculate realistic time estimate
4. **Compose message**: Use the format specified in section 2.2
5. **Send via the `agent-messaging` skill**: Use the skill's send operation to
   deliver the status update to the orchestrator
6. **Continue work**: Resume task after sending update

## Checklist

Use this checklist before sending a status update:

- [ ] I know the current development phase
- [ ] I have calculated the progress percentage accurately
- [ ] I have listed all completed items
- [ ] I have identified the current work item
- [ ] I have listed all remaining items
- [ ] I have noted any blockers (or confirmed none exist)
- [ ] I have a realistic completion estimate
- [ ] The message follows the required JSON format

## 2.4 Sending Status Updates

Send a status update to the orchestrator using the `agent-messaging` skill:

- **Recipient**: your assigned orchestrator agent (e.g., "orchestrator-master")
- **Subject**: "STATUS: [UUID] - [Current Phase]"
- **Content**: include all fields from the format in section 2.2 (phase,
  progress percentage, completed items, in-progress items, remaining items,
  blockers, estimated completion)
- **Type**: status
- **Priority**: normal

**Verify**: confirm the status message appears in your sent messages.

### Status Update When Delayed

If progress is slower than expected, send a delayed status update using the
`agent-messaging` skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "STATUS: [TASK-ID] - Implementation Delayed"
- **Content**: include the same fields as a regular status update, plus the
  delay reason and revised completion estimate
- **Type**: status
- **Priority**: high (elevated because of the delay)

**Verify**: confirm the delayed status message was delivered.

## 2.5 Examples

### Example 1: Task Start Status

**Situation**: Beginning work on a new task.

Send a message to the orchestrator using the `agent-messaging` skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "STATUS: b2c3d4e5-f6a7-8901-bcde-f23456789012 - Starting
  Development"
- **Content**: "Starting work on b2c3d4e5-f6a7-8901-bcde-f23456789012. Analyzed
  requirements, beginning test writing. Phase: test-writing. Progress: 5%.
  Completed: Requirements analysis, Approach planning. In progress: Writing unit
  tests. Remaining: Complete test suite, Implementation, Refactoring,
  Documentation. Blockers: none. Estimated completion: 3 hours."
- **Type**: status
- **Priority**: normal

**Verify**: confirm the message appears in your sent messages.

### Example 2: Milestone Reached

**Situation**: All tests written and passing.

Send a message to the orchestrator using the `agent-messaging` skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "STATUS: b2c3d4e5-f6a7-8901-bcde-f23456789012 - Tests Complete"
- **Content**: "All tests written and implementation complete. Moving to
  refactoring. Phase: refactoring. Progress: 65%. Completed: Unit tests (15
  tests), Core implementation, Edge case handling, Error handling. In progress:
  Code cleanup and refactoring. Remaining: Refactoring, Documentation update,
  Final review prep. Blockers: none. Estimated completion: 1 hour. Task:
  b2c3d4e5-f6a7-8901-bcde-f23456789012"
- **Type**: status
- **Priority**: normal

**Verify**: confirm the message was delivered successfully.

### Example 3: Ready for Review

**Situation**: All work complete, ready for AMOA review.

Send a message to the orchestrator using the `agent-messaging` skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "STATUS: b2c3d4e5-f6a7-8901-bcde-f23456789012 - Ready for Review"
- **Content**: "Task complete. All tests passing, code refactored, documentation
  updated. Phase: review-prep. Progress: 100%. Completed: Unit tests (15 tests,
  all passing), Core implementation, Edge case handling, Error handling,
  Refactoring, Documentation update. In progress: None - awaiting review.
  Remaining: none. Blockers: none. Task: b2c3d4e5-f6a7-8901-bcde-f23456789012"
- **Type**: status
- **Priority**: normal

**Verify**: confirm the message was delivered successfully.

### Example 4: Status with Blockers

**Situation**: Progress blocked by external dependency.

Send a message to the orchestrator using the `agent-messaging` skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "STATUS: c3d4e5f6-a7b8-9012-cdef-345678901234 - Partially
  Blocked"
- **Content**: "Implementation partially blocked. Completed independent work,
  waiting on API access. Phase: implementation. Progress: 40%. Completed: Unit
  tests written, Local logic implemented, Mock integration tests. In progress:
  Blocked - cannot complete API integration. Remaining: Real API integration,
  End-to-end testing, Refactoring, Documentation. Blockers: Waiting for API
  credentials from external team (ETA unknown). Estimated completion: Unknown
  until blocker resolved. Task: c3d4e5f6-a7b8-9012-cdef-345678901234"
- **Type**: status
- **Priority**: high

**Verify**: confirm the message was delivered successfully.

## Error Handling

| Error                      | Cause                         | Resolution                                                               |
| -------------------------- | ----------------------------- | ------------------------------------------------------------------------ |
| Messaging service offline  | Messaging service not running | Use the `agent-messaging` skill's status check, start AI Maestro service |
| `Message delivery failed`  | Network issue                 | Retry after 5 seconds                                                    |
| `Invalid progress_percent` | Value outside 0-100           | Use integer between 0 and 100                                            |
| `Empty completed array`    | No work done yet              | Include at least "Task analysis"                                         |

### Best Practices

1. **Be accurate**: Do not inflate progress percentage
2. **Be consistent**: Use standardized phase names
3. **Be honest about blockers**: Report issues early
4. **Update regularly**: Do not go silent for extended periods
5. **Include context**: Explain what "in progress" means specifically
