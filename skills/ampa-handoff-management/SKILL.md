---
name: ampa-handoff-management
description: Create and receive handoff documents for context transfer. Use when transferring work, resuming sessions, or filing bug reports. Trigger with /ampa-handoff.
license: MIT
compatibility: Requires AI Maestro running.
metadata:
  author: AI Maestro
  version: 1.0.16
  workflow-instruction: "support"
  procedure: "proc-handoff-management"
context: fork
agent: ampa-programmer-main-agent
user-invocable: false
---

# AMPA Handoff Management Skill

## Overview

Context transfer between AMPA sessions via structured handoff documents (Markdown + YAML frontmatter). Enables seamless work state transfer across agent transitions, session boundaries, bug discoveries, and work interruptions.

## Prerequisites

- **AI Maestro running** on `localhost:23000` for inter-agent messaging notifications.
- **Handoff directory exists** at `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/` (create with `mkdir -p` if needed).
- **Valid session name** registered with AI Maestro (format: `<project>-programmer-<number>`).
- **`$CLAUDE_PROJECT_DIR` set** to the project root (set automatically by Claude Code).

## Instructions

Copy this checklist and track your progress:

1. **Determine the handoff operation needed.** Match your situation to Read, Create, Bug Report, or Document Work State.
2. **Read the corresponding reference file** from `references/` before proceeding.
3. **Verify the handoff directory exists.** Run `mkdir -p "$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/ampa-<task-name>/"`.
4. **Execute the operation.** All handoff documents require YAML frontmatter with fields: `type`, `from`, `to`, `task`, `created`, `priority`, `status`. Bug reports (type: `bug-report`) have modified fields: `type`, `from`, `task`, `bug-id`, `severity`, `created`.
5. **Validate the handoff document.** Re-read to confirm all required fields are present and content is accurate.
6. **Send notification.** Use the globally installed `agent-messaging` skill to notify the receiving agent, including the handoff file path.
7. **Archive previous versions.** If updating an existing handoff, move `current.md` to `archive/` with a timestamp suffix before writing the new version.

## Output

- **Handoff documents** stored at `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/ampa-<task-name>/current.md`.
- **Notification** sent to receiving agent via agent-messaging skill.

## Token Budget

- **Lazy reference loading**: Only read a reference file when executing that specific operation.
- **Creation confirmation**: Report only `[DONE] Handoff created: <path>`. Do not echo content back.

## Error Handling

| Error | Resolution |
|-------|------------|
| Handoff directory missing | Run `mkdir -p "$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/ampa-<task-name>/"` |
| AI Maestro notification fails | Verify running with `curl -s "http://localhost:23000/api/health"`, start if needed |
| YAML frontmatter parse error | Ensure `---` delimiters on own lines, quote special characters in values |
| Receiving agent not found | Use the `agent-messaging` skill to list registered agents |
| Handoff document is stale | Archive existing `current.md` to `archive/` with timestamp, then create new |

## Examples

- [ ] Input: Task complete, need to transfer context to another agent
- [x] Output: `current.md` with YAML frontmatter, modified files, test status, next steps. Notification sent.

## Resources

- **[op-read-handoff-document.md](references/op-read-handoff-document.md)** — Parse and process incoming handoffs
  Sections: When to Use · Prerequisites · Procedure · Checklist · Examples · Error Handling
- **[op-create-handoff-document.md](references/op-create-handoff-document.md)** — Create outgoing handoff documents
  Sections: When to Use · Prerequisites · Procedure · Checklist · Examples · Error Handling
- **[op-write-bug-report.md](references/op-write-bug-report.md)** — Structured bug reporting during implementation
  Sections: When to Use · Prerequisites · Procedure · Checklist · Examples · Error Handling
- **[op-document-work-state.md](references/op-document-work-state.md)** — Capture in-progress work state for session resume
  Sections: When to Use · Prerequisites · Procedure · Checklist · Examples · Error Handling
- **`agent-messaging` skill** (globally installed) — Send handoff notifications, list registered agents
- **AMOA Orchestrator Agent** — Source of task delegations, escalation target for bug reports
- **AMIA Integrator Agent** — Recipient of implementation-complete handoffs for code review

## Related Skills

- **ampa-task-execution** — Core implementation workflow that produces handoff-worthy work state.
- **ampa-orchestrator-communication** — Messaging patterns for AMOA coordination and status reporting.
