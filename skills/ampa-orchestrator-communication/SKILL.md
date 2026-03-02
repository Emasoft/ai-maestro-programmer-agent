---
name: ampa-orchestrator-communication
description: Communication with AMOA Orchestrator via AI Maestro. Use when sending clarifications, status updates, blockers, or completions. Trigger with /ampa-orchestrator-comm.
license: MIT
compatibility: Requires AI Maestro running.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ampa-programmer-main-agent
user-invocable: false
workflow-instruction: "Steps 14, 15, 17, 19"
procedure: "proc-clarify-tasks, proc-handle-feedback, proc-complete-task"
---

# AMPA Orchestrator Communication Skill

This skill defines all communication protocols between the AI Maestro Programmer Agent (AMPA) and the AI Maestro Orchestrator Agent (AMOA). Use this skill whenever you need to interact with the orchestrator for clarifications, status updates, blocking issues, improvement proposals, or task completion notifications.

## Overview

The AMPA-AMOA communication channel uses asynchronous inter-agent messaging provided by the globally installed `agent-messaging` skill. That skill defines the current commands and syntax for sending, receiving, reading, replying to, and checking the status of messages. Always read the `agent-messaging` skill at runtime to determine the exact commands -- never hardcode messaging command names in your workflow.

## When to Use This Skill

Use this skill in the following situations:

| Situation | Operation | Reference File |
|-----------|-----------|----------------|
| Task requirements are unclear or ambiguous | Request Clarification | [op-request-clarification.md](references/op-request-clarification.md) |
| Need to report current development status | Report Status | [op-report-status.md](references/op-report-status.md) |
| Encountered a blocking issue that prevents progress | Report Blocker | [op-report-blocker.md](references/op-report-blocker.md) |
| Have suggestions for design or task improvements | Propose Improvement | [op-propose-improvement.md](references/op-propose-improvement.md) |
| Task implementation is complete and ready for review | Notify Completion | [op-notify-completion.md](references/op-notify-completion.md) |
| Received feedback from AMOA after PR review | Receive Feedback | [op-receive-feedback.md](references/op-receive-feedback.md) |

## Communication Architecture

```
AMPA (Programmer Agent)         AI Maestro           AMOA (Orchestrator Agent)
        |                           |                           |
        |--- Send Message --------->|                           |
        |                           |--- Deliver Message ------>|
        |                           |                           |
        |                           |<-- Response Message ------|
        |<--- Deliver Response -----|                           |
        |                           |                           |
```

## Message Priority Levels

| Priority | Use Case | Expected Response Time |
|----------|----------|------------------------|
| `urgent` | Blocking issues, critical failures | Immediate (within minutes) |
| `high` | Clarifications needed to continue, completion notifications | Within 30 minutes |
| `normal` | Status updates, improvement proposals | Within 2 hours |

## Message Types

All messages to AMOA must include a `type` field in the content object:

| Type | Description |
|------|-------------|
| `clarification-request` | Asking for task clarification |
| `status-update` | Reporting development progress |
| `blocker-report` | Reporting blocking issues |
| `improvement-proposal` | Suggesting design improvements |
| `completion-notification` | Task is done, ready for review |
| `feedback-acknowledgment` | Acknowledging received feedback |

## Prerequisites

Before using any operation in this skill:

1. **Messaging identity is initialized**: Read the `agent-messaging` skill and follow its initialization instructions. Verify your identity is set up before sending any messages.
2. **Messaging service is operational**: Use the `agent-messaging` skill's status check operation to confirm connectivity.
3. **AMOA is active**: The orchestrator agent session must be available.

## Operations Reference

### 1. Request Clarification (Step 14)

Use when task requirements are unclear or need additional information.

**Reference**: [op-request-clarification.md](references/op-request-clarification.md)

**Contents**:
- 1.1 When to Request Clarification
- 1.2 Clarification Request Format
- 1.3 Sending the Request
- 1.4 Handling the Response
- 1.5 Examples

### 2. Report Status (Step 17)

Use to send "in development" status updates to keep AMOA informed.

**Reference**: [op-report-status.md](references/op-report-status.md)

**Contents**:
- 2.1 When to Report Status
- 2.2 Status Message Format
- 2.3 Progress Indicators
- 2.4 Sending Status Updates
- 2.5 Examples

### 3. Report Blocker

Use when you encounter issues that prevent task progress.

**Reference**: [op-report-blocker.md](references/op-report-blocker.md)

**Contents**:
- 3.1 Identifying Blockers
- 3.2 Blocker Report Format
- 3.3 Severity Levels
- 3.4 Escalation Procedure
- 3.5 Examples

### 4. Propose Improvement (Step 15)

Use to suggest design or implementation improvements.

**Reference**: [op-propose-improvement.md](references/op-propose-improvement.md)

**Contents**:
- 4.1 When to Propose Improvements
- 4.2 Improvement Proposal Format
- 4.3 Justification Requirements
- 4.4 Awaiting Approval
- 4.5 Examples

### 5. Notify Completion (Step 19)

Use when task implementation is complete and ready for review.

**Reference**: [op-notify-completion.md](references/op-notify-completion.md)

**Contents**:
- 5.1 Completion Criteria
- 5.2 Completion Notification Format
- 5.3 Deliverables Summary
- 5.4 Sending Notification
- 5.5 Examples

### 6. Receive Feedback

Use to handle feedback from AMOA after PR review.

**Reference**: [op-receive-feedback.md](references/op-receive-feedback.md)

**Contents**:
- 6.1 Monitoring for Feedback
- 6.2 Feedback Message Types
- 6.3 Processing Feedback
- 6.4 Acknowledgment Protocol
- 6.5 Examples

## Messaging Quick Reference

All messaging operations below are performed using the `agent-messaging` skill. Read that skill to learn the current command syntax.

### Send Message to AMOA

Send a message to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: the subject line for this message
- **Content**: the message body text
- **Type**: the message type (see Message Types table above)
- **Priority**: the priority level (see Message Priority Levels table above)

**Verify**: confirm the message appears in your sent messages.

### Check for Messages from AMOA

Check your inbox using the `agent-messaging` skill. Process all unread messages before proceeding.

### Read a Specific Message

Read the message by its ID using the `agent-messaging` skill to see its full content.

### Reply to a Message (Acknowledge)

Reply to the message using the `agent-messaging` skill, confirming receipt and stating your next action.

### Check Messaging Status

Use the `agent-messaging` skill's status check operation to verify the messaging service is running and your identity is configured.

### Verify Messaging Identity

Use the `agent-messaging` skill's identity check operation to confirm your session name is registered as your messaging identity.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Identity not found | Messaging not initialized | Read the `agent-messaging` skill and follow its initialization instructions |
| Recipient not found | AMOA session not registered | Wait for AMOA to start or notify user |
| Message delivery failed | Network or service issue | Retry the send operation using the `agent-messaging` skill |
| Messaging service offline | Service not running | Use the `agent-messaging` skill's status check, restart AI Maestro service |

## Checklist

Copy this checklist and track your progress:

- [ ] Initialize messaging identity via agent-messaging skill
- [ ] Verify messaging service status
- [ ] Confirm AMOA is active and reachable
- [ ] Determine communication type (clarification, status, blocker, improvement, completion, feedback)
- [ ] Read the operation reference file for the chosen type
- [ ] Compose and send the message with correct type, priority, and content
- [ ] Verify delivery in sent messages list
- [ ] Monitor for and process AMOA response
- [ ] Acknowledge receipt of any AMOA reply

## Troubleshooting

### Messaging Connection Issues

If messaging operations fail:

1. Use the `agent-messaging` skill's status check operation to verify connectivity
2. Use the `agent-messaging` skill's identity check operation to verify your identity is set up
3. Re-initialize your identity following the `agent-messaging` skill's initialization instructions

### AMOA Not Responding

If AMOA does not respond within expected time:

1. Check the messaging service status using the `agent-messaging` skill
2. Escalate to user if AMOA is unavailable
3. Document the delay in status update

### Message Delivery Failures

If message delivery fails:

1. Verify recipient name is correct
2. Check messaging service status using the `agent-messaging` skill
3. Retry up to 3 times with 5-second delays
4. Report to user if all retries fail

## Instructions

Follow these numbered steps whenever you need to communicate with the AI Maestro Orchestrator Agent (AMOA):

1. **Initialize messaging identity**: Read the `agent-messaging` skill and follow its initialization instructions. Verify your session name is registered before proceeding.
2. **Verify messaging service status**: Use the `agent-messaging` skill's status check operation to confirm the service is running and reachable.
3. **Confirm AMOA is active**: Check that the orchestrator agent session is registered and available to receive messages.
4. **Determine the communication type**: Identify which operation applies to your situation using the "When to Use This Skill" table above (clarification request, status update, blocker report, improvement proposal, completion notification, or feedback acknowledgment).
5. **Read the operation reference file**: Open the corresponding reference file listed in the Operations Reference section to learn the exact message format and required fields for that operation type.
6. **Compose the message**: Build the message with the correct `type` field, appropriate `priority` level, descriptive `subject` line, and structured `content` body as specified in the reference file.
7. **Send the message**: Use the `agent-messaging` skill's send operation to deliver the message to your assigned AMOA session name.
8. **Verify delivery**: Confirm the message appears in your sent messages list using the `agent-messaging` skill.
9. **Monitor for response**: Periodically check your inbox for replies from AMOA. Process all unread messages before continuing other work.
10. **Acknowledge receipt**: When you receive a response from AMOA, reply using the `agent-messaging` skill to confirm you received it and state your next planned action.

## Output

This skill produces the following artifacts and outcomes:

- **Outbound AI Maestro messages**: Structured JSON messages sent from AMPA to AMOA, each containing a `type` field (one of the six message types), a `priority` level, a `subject` line, and a formatted `content` body.
- **Delivery confirmations**: Verification that each sent message was accepted by the AI Maestro messaging service and appears in the sent messages list.
- **Acknowledgment replies**: Reply messages sent back to AMOA confirming receipt of feedback or instructions, stating the AMPA's next action.
- **Communication audit trail**: A chronological record of all AMPA-AMOA exchanges visible in both agents' message histories, providing traceability for task progress and decisions.

## Examples

### Example 1: Requesting Clarification on Ambiguous Task Requirements

The AMPA receives a task to "implement data validation" but the acceptance criteria do not specify which fields require validation or what validation rules to apply.

**Action**: Send a clarification request message to AMOA:
- **Type**: `clarification-request`
- **Priority**: `high`
- **Subject**: "Clarification needed: data validation scope for task PROJ-42"
- **Content**: "Task PROJ-42 says 'implement data validation' but does not specify which fields need validation or what rules apply. Questions: (1) Which input fields require validation? (2) Should validation be schema-based or custom rule-based? (3) Are there existing validation patterns in the codebase to follow?"

**Expected outcome**: AMOA replies with specific field names, validation rules, and a pointer to existing patterns.

### Example 2: Reporting a Blocking Issue

The AMPA discovers that a required dependency package is not available in the project environment and cannot proceed with implementation.

**Action**: Send a blocker report message to AMOA:
- **Type**: `blocker-report`
- **Priority**: `urgent`
- **Subject**: "BLOCKER: Missing dependency 'pydantic-settings' for task PROJ-42"
- **Content**: "Cannot proceed with task PROJ-42. The package 'pydantic-settings>=2.0' is required for config validation but is not listed in pyproject.toml and is not installed in the project environment. Attempted workarounds: none (adding dependencies is outside AMPA scope). Requesting AMOA to authorize adding this dependency or provide an alternative approach."

**Expected outcome**: AMOA authorizes the dependency addition or reassigns the task with updated instructions.

### Example 3: Notifying Task Completion

The AMPA finishes implementing the feature, all tests pass, and the code is committed and pushed to a feature branch.

**Action**: Send a completion notification message to AMOA:
- **Type**: `completion-notification`
- **Priority**: `high`
- **Subject**: "Task PROJ-42 complete: data validation implemented"
- **Content**: "Task PROJ-42 is complete and ready for review. Branch: feature/proj-42-data-validation. Commit: abc1234. Deliverables: (1) src/validators/data_validator.py - new validation module, (2) tests/test_data_validator.py - 12 passing tests, (3) Updated pyproject.toml with pydantic-settings dependency. All tests pass locally. PR created: #87."

**Expected outcome**: AMOA acknowledges receipt and routes the PR to the AI Maestro Integrator Agent (AMIA) for code review.

## Resources

- [op-request-clarification.md](references/op-request-clarification.md) - Detailed format and procedure for sending clarification requests to AMOA
- [op-report-status.md](references/op-report-status.md) - Format and timing guidelines for development status updates
- [op-report-blocker.md](references/op-report-blocker.md) - Blocker report format, severity levels, and escalation procedure
- [op-propose-improvement.md](references/op-propose-improvement.md) - Format for design and implementation improvement proposals
- [op-notify-completion.md](references/op-notify-completion.md) - Completion notification format and deliverables summary requirements
- [op-receive-feedback.md](references/op-receive-feedback.md) - How to monitor, process, and acknowledge feedback from AMOA
- `agent-messaging` skill (globally installed) - Provides the actual messaging commands and syntax used by all operations in this skill
