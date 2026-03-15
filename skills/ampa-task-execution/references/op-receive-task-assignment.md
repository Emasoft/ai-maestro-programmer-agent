---
name: op-receive-task-assignment
description: Receive and validate task assignments from the Orchestrator
parent-skill: ampa-task-execution
---

# Receive Task Assignment

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

Parse and validate incoming task assignments from AI Maestro messages.

## When to Use

Use this operation when:
- You see the AI Maestro inbox notification banner
- You receive a message with subject containing "TASK:" or "ASSIGNMENT:"
- The orchestrator sends you work to perform

## Prerequisites

Before executing this operation:
1. AI Maestro service must be running (verify using the `agent-messaging` skill's health check feature)
2. You must have a valid session name configured
3. The message must be in the expected JSON format

## Procedure

### Step 1.1: Read Incoming AI Maestro Message

Check your inbox using the `agent-messaging` skill. Process all unread messages.

Look for messages where:
- `content.type` is `"task"` or `"assignment"`
- `subject` contains task identification

### Step 1.2: Extract Task Identifier and Metadata

From the message body, extract:

| Field | Location | Description |
|-------|----------|-------------|
| Task ID | `content.task_id` | UUID from AI Maestro (or free-form string). May include `externalRef` mapping to a GitHub issue number. |
| Task Name | `content.task_name` | Human-readable task description |
| Priority | `priority` field | URGENT, HIGH, NORMAL, LOW |
| Deadline | `content.deadline` | Optional completion deadline |
| From Agent | `from` field | Orchestrator that assigned the task |

Example message structure:

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "from": "orchestrator-master",
  "to": "<project>-programmer-<NNN>",  // Session name follows the naming convention from AGENT_OPERATIONS.md: <project>-programmer-<NNN>
  "subject": "TASK: Implement user authentication",
  "priority": "high",
  "content": {
    "type": "task",
    "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "externalRef": "#42",
    "task_name": "Implement user authentication",
    "message": "Implement the login endpoint...",
    "requirements": [...],
    "acceptance_criteria": [...]
  }
}
```

### Step 1.3: Validate Message Format and Required Fields

Verify the message contains all required fields:

| Required Field | Validation |
|----------------|------------|
| `content.type` | Must be "task" or "assignment" |
| `content.task_id` | Must be non-empty string |
| `content.message` | Must contain task description |
| `content.acceptance_criteria` | Must be an array with at least one criterion |

If validation fails:
- Do NOT proceed with the task
- Report the validation error back to sender
- Request a properly formatted task assignment

### Step 1.4: Verify Task in Kanban (Optional)

If the `$AIMAESTRO_API` environment variable is set, verify the task assignment against the kanban system:

```bash
curl -s "$AIMAESTRO_API/api/teams/{teamId}/tasks?assignee={agentId}" | jq '.tasks[]'
```

This provides independent verification that:
- The task exists in the kanban system (not just in an AMP message)
- The task is assigned to this agent
- The task status is `pending` or `in_progress`

If the task is NOT found in the kanban:
- Do NOT reject the task — AMP messages are authoritative
- Log the discrepancy in `docs_dev/task-verification-<task_id>.md`
- Notify the orchestrator: "Task received via AMP but not found in kanban. Proceeding with AMP assignment."

> **Note**: This step is optional. If the API endpoint is unavailable or `$AIMAESTRO_API` is not set, skip verification and proceed with the AMP-received task.

### Step 1.5: Acknowledge Receipt to Orchestrator

Send an acknowledgment message to the orchestrator using the `agent-messaging` skill:
- **Recipient**: the sender's session name (from the incoming message)
- **Subject**: "ACK: [TASK_ID] received"
- **Content**: "Task received and validated. Beginning work."
- **Type**: acknowledgment
- **Priority**: normal

**Verify**: confirm the acknowledgment appears in your sent messages.

## Checklist

- [ ] Checked AI Maestro inbox for unread messages
- [ ] Identified task assignment message
- [ ] Extracted task ID and metadata
- [ ] Validated all required fields present
- [ ] Verified task in kanban (if API available)
- [ ] Sent acknowledgment to orchestrator
- [ ] Recorded task start time for tracking

## Examples

### Example 1: Valid Task Assignment

Incoming message:

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "from": "orchestrator-master",
  "subject": "TASK: Add validation to user form",
  "priority": "high",
  "content": {
    "type": "task",
    "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "message": "Add email validation to the user registration form",
    "acceptance_criteria": [
      "Email format is validated on submit",
      "Invalid email shows error message",
      "Valid email allows form submission"
    ]
  }
}
```

Response:

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "to": "orchestrator-master",
  "subject": "ACK: a1b2c3d4-e5f6-7890-abcd-ef1234567890 received",
  "content": {
    "type": "acknowledgment",
    "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "message": "Task received. 3 acceptance criteria identified.",
    "status": "in_progress"
  }
}
```

### Example 2: Invalid Task Assignment

Incoming message missing acceptance criteria:

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "from": "orchestrator-master",
  "content": {
    "type": "task",
    "task_id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
    "message": "Fix the bug"
  }
}
```

Response:

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "to": "orchestrator-master",
  "subject": "INVALID: b2c3d4e5-f6a7-8901-bcde-f23456789012 missing required fields",
  "priority": "high",
  "content": {
    "type": "error",
    "task_id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
    "message": "Task assignment missing required field: acceptance_criteria",
    "status": "blocked"
  }
}
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No messages in inbox | No tasks assigned yet | Wait for orchestrator assignment |
| Message missing task_id | Malformed message | Report error, request resubmission |
| Missing acceptance_criteria | Incomplete task definition | Request criteria from orchestrator |
| AI Maestro unreachable | Service not running | Verify AI Maestro connectivity using the `agent-messaging` skill |

## Related Operations

- [op-parse-task-requirements.md](op-parse-task-requirements.md) - Next step after receiving task
- [op-validate-acceptance-criteria.md](op-validate-acceptance-criteria.md) - Final validation step
