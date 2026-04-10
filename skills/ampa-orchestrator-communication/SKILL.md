---
name: ampa-orchestrator-communication
description:
  Communication with AMOA Orchestrator via AI Maestro. Use when sending
  clarifications, status updates, blockers, or completions. Trigger with
  /ampa-orchestrator-comm. Loaded by ai-maestro-programmer-agent-main-agent.
license: MIT
compatibility: Requires AI Maestro running.
metadata:
  author: AI Maestro
  version: 1.0.20
  workflow-instruction: "Steps 14, 15, 17, 19"
  procedure: "proc-clarify-tasks, proc-handle-feedback, proc-complete-task"
context: fork
agent: ai-maestro-programmer-agent-main-agent
user-invocable: false
---

# AMPA Orchestrator Communication Skill

## Overview

Defines all communication protocols between AMPA and AMOA. Uses asynchronous
inter-agent messaging via the globally installed `agent-messaging` skill. Read
that skill once during initialization to learn messaging commands and syntax.

## Prerequisites

- **agent-messaging skill installed**: Read it to learn send/receive/reply
  commands.
- **AMOA session name known**: Your assigned orchestrator must be active and
  registered.
- **Messaging identity verified**: Your session name is registered via
  agent-messaging initialization.

## Instructions

Copy this checklist and track your progress:

1. **Initialize**: Read the `agent-messaging` skill and follow its
   initialization to register your messaging identity.
2. **Verify connectivity**: Use agent-messaging status check to confirm the
   service is running.
3. **Identify operation type**: Determine which applies — clarification, status,
   blocker, improvement, completion, or feedback acknowledgment.
4. **Read reference file**: Open the corresponding reference file from Resources
   below to learn the exact message format and required fields.
5. **Compose message**: Build the message with correct `type`, `priority`,
   `subject`, and structured `content` as specified in the reference.
6. **Send message**: Use agent-messaging send operation to deliver to AMOA.
   Retry up to 3 times on failure.
7. **Verify delivery**: Confirm the message appears in your sent messages list.
8. **Monitor for response**: Check inbox for AMOA replies. Process all unread
   messages before continuing other work.
9. **Acknowledge receipt**: Reply to AMOA confirming you received the response
   and stating your next action.

## Output

Sent/received messages to/from AMOA via agent-messaging skill.

## Error Handling

If message delivery fails after 3 retries, write the message content to
`docs_dev/unsent-<timestamp>.md` and report the delivery failure to your local
log. Resume when connectivity is restored.

## Examples

- [ ] Input: Need to report progress on task #42
- [x] Output:
      `{"type": "status-update", "message": "Task #42: 3/5 criteria met. Details: docs_dev/status-42.md"}`

## Resources

| Document | Description |
|----------|-------------|
| [op-request-clarification.md](references/op-request-clarification.md) | 1.1 When to Request Clarification, Prerequisites, 1.2 Clarification Request Format, Procedure, Checklist, 1.3 Sending the Request, 1.4 Handling the Response, 1.5 Examples, Error Handling |
| [op-report-status.md](references/op-report-status.md) | 2.1 When to Report Status, Prerequisites, 2.2 Status Message Format, 2.3 Progress Indicators, Procedure, Checklist, 2.4 Sending Status Updates, 2.5 Examples, Error Handling |
| [op-report-blocker.md](references/op-report-blocker.md) | 3.1 Identifying Blockers, Prerequisites, 3.2 Blocker Report Format, 3.3 Severity Levels, Procedure, Checklist, 3.4 Escalation Procedure, 3.5 Examples, Error Handling |
| [op-propose-improvement.md](references/op-propose-improvement.md) | 4.1 When to Propose Improvements, Prerequisites, 4.2 Improvement Proposal Format, 4.3 Justification Requirements, Procedure, Checklist, 4.4 Awaiting Approval, 4.5 Examples, Error Handling |
| [op-notify-completion.md](references/op-notify-completion.md) | 5.1 Completion Criteria, Prerequisites, 5.2 Completion Notification Format, 5.3 Deliverables Summary, Procedure, Checklist, 5.4 Sending Notification, 5.5 Examples, Error Handling |
| [op-receive-feedback.md](references/op-receive-feedback.md) | 6.1 Monitoring for Feedback, Prerequisites, 6.2 Feedback Message Types, 6.3 Processing Feedback, Procedure, Checklist, 6.4 Acknowledgment Protocol, 6.5 Examples, Error Handling |

**`agent-messaging` skill** (global) — Messaging commands.

## Related

- **ampa-task-execution** — Core task implementation workflow triggering
  communication.
- **ampa-handoff-management** — Task handoff protocols depending on completion
  notifications.
