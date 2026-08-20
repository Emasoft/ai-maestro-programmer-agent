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
  version: 1.0.26
  workflow-instruction: "Steps 14, 15, 17, 19"
  procedure: "proc-clarify-tasks, proc-handle-feedback, proc-complete-task"
argument-hint: "[clarification|status|blocker|improvement|completion|feedback]"
---

# AMPA Orchestrator Communication Skill

## Overview

Defines all communication protocols between AMPA and AMOA. Uses asynchronous
inter-agent messaging via the frozen `amp-*` CLIs installed at `~/.local/bin`
(`amp-send.sh`, `amp-inbox.sh`, `amp-status.sh`, `amp-init.sh`). Call the CLIs
directly — never invoke the core skill by bare name, since plugin skills resolve
namespaced (`ai-maestro-plugin:agent-messaging`) and a bare name fails at runtime.

## Prerequisites

- **amp-* CLIs on PATH**: `amp-send.sh --help` resolves. Background reading, if
  needed: the `ai-maestro-plugin:agent-messaging` skill.
- **AMOA session name known**: Your assigned orchestrator must be active and
  registered.
- **Messaging identity verified**: Your session name is registered — check with
  `amp-identity.sh`, register with `amp-init.sh`.

## Instructions

Copy this checklist and track your progress:

1. **Initialize**: Run `amp-init.sh` to register your messaging identity
   (`amp-identity.sh` reports the identity already registered).
2. **Verify connectivity**: Run `amp-status.sh` to confirm the service is
   running.
3. **Identify operation type**: Determine which applies — clarification, status,
   blocker, improvement, completion, or feedback acknowledgment.
4. **Read reference file**: Open the corresponding reference file from Resources
   below to learn the exact message format and required fields.
5. **Compose message**: Build the message with correct `type`, `priority`,
   `subject`, and structured `content` as specified in the reference.
6. **Send message**: `amp-send.sh <amoa-address> "<subject>" "<message>"
   [--priority low|normal|high|urgent] [--type request|response|notification|task|status]`.
   Retry up to 3 times on failure.
7. **Verify delivery**: Confirm the send exited 0 and the message appears in
   your sent messages.
8. **Monitor for response**: Run `amp-inbox.sh` for AMOA replies. Process all
   unread messages before continuing other work.
9. **Acknowledge receipt**: Reply to AMOA confirming you received the response
   and stating your next action.

## Output

Sent/received messages to/from AMOA via the `amp-*` CLIs.

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
| [op-comprehension-handshake.md](references/op-comprehension-handshake.md) | The task-comprehension handshake answer (all 5 points, before coding) — replaces the bare ACK (R6 v3 / #17 M7a) |
| [op-request-clarification.md](references/op-request-clarification.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-report-status.md](references/op-report-status.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-report-blocker.md](references/op-report-blocker.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-propose-improvement.md](references/op-propose-improvement.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-notify-completion.md](references/op-notify-completion.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-pre-pr-gate.md](references/op-pre-pr-gate.md) | The "PR now?" pre-PR gate — ask AMOA for a green-light before opening a PR (R6 v3 / #17 M7c) |
| [op-receive-feedback.md](references/op-receive-feedback.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-report-missing-derived-trdd.md](references/op-report-missing-derived-trdd.md) | Report a missing derived TRDD (NPT/EHT) to the sender + author it — the MEMBER missing-derived duty (ai-maestro#61 Q1) |

**`amp-*` CLIs** (frozen, `~/.local/bin`) — `amp-send.sh` · `amp-inbox.sh` ·
`amp-status.sh` · `amp-init.sh` · `amp-identity.sh`. Contract:
`ai-maestro-plugin:agent-messaging` → `reference/detailed-guide.md`.

## Governance

This skill operates under the AI Maestro **approval requirements** — the
`min-approval-requirement:` ladder `none` (Tier-0 self-authority for in-scope
work + DERIVED NPT/EHT tasks, authored directly as a self-mandate) →
`chief-of-staff` → `manager` → `user`. The MEMBER op-set, the self-mandate rule,
and which moves need approval are in the `ampa-prrd-trdd-kanban` MEMBER-policy
skill; the mechanics are the core granular `ama-*` pillar skills. See also
`~/.claude/rules/trdd-approval-tiers.md`.
**A MEMBER never self-approves its own releases** — entering the release
pipeline (`publish`/`deploy`) is USER/MANAGER-authorized, and the INTEGRATOR
(not the MEMBER) owns the `→ complete` flip.

## Related

- **ampa-task-execution** — Core task implementation workflow triggering
  communication.
- **ampa-handoff-management** — Task handoff protocols depending on completion
  notifications.
