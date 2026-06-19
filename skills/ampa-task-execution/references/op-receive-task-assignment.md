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

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

Parse and validate incoming task assignments from AI Maestro messages.

## When to Use

Use this operation when:

- You see the AI Maestro inbox notification banner
- You receive a message with subject containing "TASK:" or "ASSIGNMENT:"
- The orchestrator sends you work to perform

## Prerequisites

Before executing this operation:

1. AI Maestro service must be running (verify using the `agent-messaging`
   skill's health check feature)
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

| Field      | Location            | Description                                                                                             |
| ---------- | ------------------- | ------------------------------------------------------------------------------------------------------- |
| Task ID    | `content.task_id`   | UUID from AI Maestro (or free-form string). May include `externalRef` mapping to a GitHub issue number. |
| Task Name  | `content.task_name` | Human-readable task description                                                                         |
| Priority   | `priority` field    | URGENT, HIGH, NORMAL, LOW                                                                               |
| Deadline   | `content.deadline`  | Optional completion deadline                                                                            |
| From Agent | `from` field        | Orchestrator that assigned the task                                                                     |

Example message structure:

> **Note**: The structure below shows the conceptual message content. Use the
> `agent-messaging` skill to send messages - it handles the exact API format
> automatically.

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

| Required Field                | Validation                                   |
| ----------------------------- | -------------------------------------------- |
| `content.type`                | Must be "task" or "assignment"               |
| `content.task_id`             | Must be non-empty string                     |
| `content.message`             | Must contain task description                |
| `content.acceptance_criteria` | Must be an array with at least one criterion |

If validation fails:

- Do NOT proceed with the task
- Report the validation error back to sender
- Request a properly formatted task assignment

### Step 1.4: Verify Task in Kanban (Optional)

If AI Maestro is running, verify the task assignment against the kanban board
using the frozen `amp-kanban-list` CLI — never the server `/api/` directly
(R23 frozen-CLI decoupling). The CLI resolves your team and identity from your
registration:

```bash
amp-kanban-list --assignee {agentId}
```

This provides independent verification that:

- The task exists in the kanban system (not just in an AMP message)
- The task is assigned to this agent
- The task status is `pending` or `in_progress`

If the task is NOT found in the kanban:

- Do NOT reject the task — AMP messages are authoritative
- Log the discrepancy in `docs_dev/task-verification-<task_id>.md`
- Notify the orchestrator: "Task received via AMP but not found in kanban.
  Proceeding with AMP assignment."

> **Note**: This step is optional. If AI Maestro is not running or the
> `amp-kanban-list` CLI is unavailable, skip verification and proceed with the
> AMP-received task.

### Step 1.5: Answer the Task-Comprehension Handshake (NOT a bare ACK)

**The task-comprehension handshake (loop (a) of the corrected workflow model /
#17 M7a) replaces the bare "Task received" acknowledgment.** Coding MUST NOT
start until you have answered ALL FIVE handshake points and AMOA has confirmed
your understanding. A bare ACK tells the orchestrator nothing about whether you
understood the task — the handshake catches misunderstandings BEFORE tokens are
burned on a wrong implementation.

Send the handshake answer to the orchestrator using the `agent-messaging`
skill — full template and reply semantics in
`op-comprehension-handshake.md` (`ampa-orchestrator-communication` skill):

- **Recipient**: the sender's session name (from the incoming message)
- **Subject**: "HANDSHAKE: [TASK_ID] — comprehension answer"
- **Content**: answer ALL FIVE points:
  1. **Restate the task** in your own words (not a copy of the assignment)
  2. **Files / domains you will touch** (paths, modules, configs)
  3. **Ambiguities** — anything underspecified (or "none identified")
  4. **Foreseen risks / issues** — what could go wrong
  5. **Anticipated NPT / EHT** — prerequisite tasks and effect-handling tasks
     the assignment implies
- **Type**: status
- **Priority**: normal

**WAIT for AMOA's confirmation before coding.** If AMOA flags a wrong
restatement or an unresolved ambiguity turns out to be a design flaw, the issue
routes back through AMOA (design flaw → AMAA revises or authors new TRDDs) —
never silently improvise around it.

**Verify**: confirm the handshake answer appears in your sent messages.

## Checklist

- [ ] Checked AI Maestro inbox for unread messages
- [ ] Identified task assignment message
- [ ] Extracted task ID and metadata
- [ ] Validated all required fields present
- [ ] Verified task in kanban (if AI Maestro running)
- [ ] Answered the comprehension handshake (all 5 points) to orchestrator
- [ ] Received AMOA confirmation BEFORE starting to code
- [ ] Recorded task start time for tracking

## Examples

### Example 1: Valid Task Assignment

Incoming message:

> **Note**: The structure below shows the conceptual message content. Use the
> `agent-messaging` skill to send messages - it handles the exact API format
> automatically.

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

> **Note**: The structure below shows the conceptual message content. Use the
> `agent-messaging` skill to send messages - it handles the exact API format
> automatically.

```json
{
  "to": "orchestrator-master",
  "subject": "HANDSHAKE: a1b2c3d4-e5f6-7890-abcd-ef1234567890 — comprehension answer",
  "content": {
    "type": "status",
    "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "message": "1) RESTATE: add client+server email-format validation to the user registration form so invalid emails are rejected on submit with a visible error. 2) FILES: src/forms/register.tsx, src/validation/email.ts, tests/forms/register.test.tsx. 3) AMBIGUITIES: should validation also normalize case (Foo@Bar.com -> foo@bar.com)? 4) RISKS: existing users with legacy invalid emails may fail re-login flows that reuse the validator. 5) NPT/EHT: NPT none; EHT update docs/forms.md + re-run the signup e2e suite.",
    "status": "awaiting-confirmation"
  }
}
```

AMOA replies confirming (or correcting) the restatement and answering the
ambiguity — only then does work begin.

### Example 2: Invalid Task Assignment

Incoming message missing acceptance criteria:

> **Note**: The structure below shows the conceptual message content. Use the
> `agent-messaging` skill to send messages - it handles the exact API format
> automatically.

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

> **Note**: The structure below shows the conceptual message content. Use the
> `agent-messaging` skill to send messages - it handles the exact API format
> automatically.

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

| Error                       | Cause                      | Resolution                                                       |
| --------------------------- | -------------------------- | ---------------------------------------------------------------- |
| No messages in inbox        | No tasks assigned yet      | Wait for orchestrator assignment                                 |
| Message missing task_id     | Malformed message          | Report error, request resubmission                               |
| Missing acceptance_criteria | Incomplete task definition | Request criteria from orchestrator                               |
| AI Maestro unreachable      | Service not running        | Verify AI Maestro connectivity using the `agent-messaging` skill |

## Related Operations

- [op-parse-task-requirements.md](op-parse-task-requirements.md) - Next step
  after receiving task
- [op-validate-acceptance-criteria.md](op-validate-acceptance-criteria.md) -
  Final validation step
