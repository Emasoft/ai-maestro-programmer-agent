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

- **[op-request-clarification.md](references/op-request-clarification.md)** —
  Clarification requests
- **[op-report-status.md](references/op-report-status.md)** — Status updates and
  progress
- **[op-report-blocker.md](references/op-report-blocker.md)** — Blocker reports
  and escalation
- **[op-propose-improvement.md](references/op-propose-improvement.md)** —
  Improvement proposals
- **[op-notify-completion.md](references/op-notify-completion.md)** — Completion
  notifications
- **[op-receive-feedback.md](references/op-receive-feedback.md)** — Process AMOA
  feedback
- `agent-messaging` skill (global) — Messaging commands

## Related

- **ampa-task-execution** — Core task implementation workflow triggering
  communication.
- **ampa-handoff-management** — Task handoff protocols depending on completion
  notifications.
