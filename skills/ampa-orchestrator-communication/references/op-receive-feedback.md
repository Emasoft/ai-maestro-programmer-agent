---
name: op-receive-feedback
description: Handle feedback from AMOA after PR review or task evaluation.
parent-skill: ampa-orchestrator-communication
workflow-step: "Feedback Loop"
message-type: feedback-acknowledgment
priority: high
---

# Operation: Receive Feedback

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

This operation describes how to handle feedback from the AI Maestro Orchestrator Agent (AMOA) after PR review, task evaluation, or quality assessment.

## Table of Contents

- 6.1 Monitoring for Feedback
- 6.2 Feedback Message Types
- 6.3 Processing Feedback
- 6.4 Acknowledgment Protocol
- 6.5 Examples

## 6.1 Monitoring for Feedback

After sending a completion notification, actively monitor for AMOA feedback.

### Checking for Messages

Check your inbox using the `agent-messaging` skill. Look for unread messages from the orchestrator.

To read a specific message, use the `agent-messaging` skill's read operation with the message ID to see its full content.

### Polling Interval

| After Event | Poll Interval | Duration |
|-------------|---------------|----------|
| Completion notification | Every 5 minutes | 2 hours |
| Urgent blocker report | Every 2 minutes | 30 minutes |
| Status update | Every 15 minutes | 4 hours |

### Message Priority Handling

When multiple messages arrive:

1. **Read all messages first**: Do not act on partial information
2. **Process by priority**: URGENT > HIGH > NORMAL
3. **Oldest first within priority**: FIFO within same priority level

## Prerequisites

Before processing feedback:

1. **Read complete message**: Do not skim or skip content
2. **Understand the context**: Know which task the feedback relates to
3. **Assess scope**: Determine the extent of required changes
4. **Plan response**: Decide on action before responding

## 6.2 Feedback Message Types

AMOA may send different types of feedback:

### Approval Feedback

**Subject Pattern**: `APPROVED: [Task ID]`

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "type": "approval",
  "message": "Task implementation approved. PR can be merged.",
  "task_id": "TASK-123",
  "decision": "approved",
  "notes": "[Optional notes]"
}
```

**Action**: Acknowledge and proceed to merge (if authorized) or wait for merge.

### Revision Request

**Subject Pattern**: `REVISION: [Task ID]`

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "type": "revision-request",
  "message": "Changes requested before approval.",
  "task_id": "TASK-123",
  "decision": "revision-required",
  "changes_required": [
    {
      "file": "[file path]",
      "line": [line number],
      "issue": "[Description of issue]",
      "suggestion": "[Suggested fix]"
    }
  ],
  "severity": "[critical|major|minor]",
  "deadline": "[Optional deadline]"
}
```

**Action**: Acknowledge, implement changes, re-submit for review.

### Rejection Feedback

**Subject Pattern**: `REJECTED: [Task ID]`

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "type": "rejection",
  "message": "Implementation does not meet requirements.",
  "task_id": "TASK-123",
  "decision": "rejected",
  "reasons": [
    "[Reason 1]",
    "[Reason 2]"
  ],
  "next_steps": "[What to do next]"
}
```

**Action**: Acknowledge, understand reasons, request clarification if needed, rework.

### Clarification Response

**Subject Pattern**: `RE: CLARIFICATION: [Task ID]`

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "type": "clarification-response",
  "message": "Response to your clarification request.",
  "task_id": "TASK-123",
  "answers": [
    {
      "question": "[Your question]",
      "answer": "[AMOA's answer]"
    }
  ]
}
```

**Action**: Acknowledge, incorporate answers, continue work.

### Improvement Decision

**Subject Pattern**: `RE: PROPOSAL: [Task ID]`

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "type": "improvement-decision",
  "message": "Decision on your improvement proposal.",
  "task_id": "TASK-123",
  "decision": "[approved|rejected|modified]",
  "notes": "[Decision reasoning]",
  "modifications": "[If modified, what changes]"
}
```

**Action**: Acknowledge, implement approved/modified proposal or continue with original.

## 6.3 Processing Feedback

### Step-by-Step Processing

1. **Read the full message**: Understand complete context
2. **Identify feedback type**: Determine which type of feedback
3. **Extract action items**: List all required actions
4. **Prioritize actions**: Order by severity and dependency
5. **Plan implementation**: Estimate effort for each action
6. **Send acknowledgment**: Confirm receipt and understanding
7. **Execute actions**: Implement required changes
8. **Report completion**: Notify when revisions complete

### Processing Revision Requests

For each change request:

| Step | Action |
|------|--------|
| 1 | Read the issue description |
| 2 | Locate the relevant code |
| 3 | Understand why the change is needed |
| 4 | Implement the suggested fix (or better alternative) |
| 5 | Test the change |
| 6 | Commit with descriptive message |

### Handling Multiple Changes

When multiple changes are requested:

1. **Categorize by severity**: Critical > Major > Minor
2. **Identify dependencies**: Some changes may depend on others
3. **Address critical first**: Fix blockers before enhancements
4. **Batch commits logically**: Group related changes
5. **Test after each batch**: Verify no regressions

## Procedure

Follow these steps when receiving feedback:

1. **Check inbox**: Monitor for new messages
2. **Read feedback completely**: Do not skim
3. **Identify feedback type**: Determine category
4. **Extract action items**: List all required actions
5. **Send acknowledgment**: Confirm receipt immediately
6. **Plan response**: Estimate effort and timeline
7. **Implement changes**: Address all action items
8. **Test changes**: Verify all changes work
9. **Commit and push**: Update the branch
10. **Send update**: Notify AMOA of completed revisions

## Checklist

Use this checklist when processing feedback:

- [ ] I have read the complete feedback message
- [ ] I understand the feedback type
- [ ] I have listed all action items
- [ ] I have sent an acknowledgment
- [ ] I have prioritized actions by severity
- [ ] I have planned the implementation approach
- [ ] I have implemented all required changes
- [ ] I have tested all changes
- [ ] I have committed and pushed changes
- [ ] I have sent an update notification

## 6.4 Acknowledgment Protocol

### Immediate Acknowledgment

Send acknowledgment within 5 minutes of receiving feedback. Reply directly to the feedback message using the `agent-messaging` skill:
- **Action**: reply to the original message by its ID
- **Content**: "Feedback received and understood. Processing now. Action items: [number]. Estimated completion: [Time estimate]."

**Verify**: confirm the reply appears in your sent messages.

Alternatively, send a new acknowledgment message using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "ACK: [Original Subject]"
- **Content**: "Feedback received and understood. Processing now. Action items: [number]. Estimated completion: [Time estimate]."
- **Type**: ack
- **Priority**: normal

**Verify**: confirm the acknowledgment was delivered.

### Acknowledgment Components

| Field | Description | Required |
|-------|-------------|----------|
| `original_subject` | Subject of the feedback message | Yes |
| `task_id` | Task identifier | Yes |
| `action_items_count` | Number of items to address | Yes |
| `estimated_completion` | When revisions will be done | Yes |
| `questions` | Any clarifications needed | No |

### After Completing Revisions

Send a revision complete notification to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "REVISED: [Task ID] - Revisions Complete"
- **Content**: list all completed revisions with commit hashes and confirm the work is ready for review
- **Type**: notification
- **Priority**: high

**Verify**: confirm the revision notification was delivered.

## 6.5 Examples

### Example 1: Processing Approval

**Situation**: AMOA approved the task.

Reply to the approval message using the `agent-messaging` skill:
- **Action**: reply to the original message by its ID
- **Content**: "Approval received. Thank you for the review. Awaiting merge authorization or will merge if authorized."

**Verify**: confirm the reply was sent.

### Example 2: Processing Revision Request

**Situation**: AMOA requested changes.

Reply to the revision request using the `agent-messaging` skill:
- **Action**: reply to the original message by its ID
- **Content**: "Revision request received. Will address all 3 items: 1) Add input validation for order quantity 2) Fix edge case when order total is zero 3) Update error message for clarity. Estimated completion: 1 hour."

**Verify**: confirm the acknowledgment was sent.

After completing revisions, send a notification to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "REVISED: TASK-456 - Revisions Complete"
- **Content**: "All 3 requested revisions have been completed and tested. Changes: 1) Add input validation for order quantity - completed (commit a1b2c3d) - Added validation to reject quantities < 1. 2) Fix edge case when order total is zero - completed (commit e4f5g6h) - Now returns 400 error for zero-total orders. 3) Update error message for clarity - completed (commit i7j8k9l) - Error messages now include specific field names. All tests passing. Ready for review."
- **Type**: notification
- **Priority**: high

**Verify**: confirm the revision notification was delivered.

### Example 3: Handling Rejection with Rework

**Situation**: Task was rejected, need to rework.

Reply to the rejection message using the `agent-messaging` skill:
- **Action**: reply to the original message by its ID
- **Content**: "Rejection received. I understand the issues and will rework the implementation. Understanding: The implementation did not handle the required multi-currency support. Will rework to include currency conversion. Question: Should I use the existing CurrencyConverter service or implement new conversion logic? Estimated rework time: 3 hours."

**Verify**: confirm the reply was sent.

### Example 4: Processing Clarification Response

**Situation**: AMOA answered clarification questions.

Reply to the clarification response using the `agent-messaging` skill:
- **Action**: reply to the original message by its ID
- **Content**: "Clarification received and understood. Will use PostgreSQL JSONB columns for flexible metadata storage as clarified. Resuming implementation with clarified approach."

**Verify**: confirm the reply was sent.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Feedback message unclear` | Incomplete or ambiguous | Request clarification |
| `Cannot implement change` | Technical constraint | Report blocker |
| `Conflicting feedback` | Multiple contradictory items | Request prioritization |
| `Deadline too short` | Insufficient time | Negotiate timeline |

### Requesting Clarification on Feedback

If feedback is unclear, send a clarification request to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "RE: REVISION: [TASK_ID] - Clarification Needed"
- **Content**: describe which revision item is unclear and list specific questions
- **Type**: request
- **Priority**: high

**Verify**: confirm the clarification request was delivered.

### Reporting Inability to Implement

If a requested change cannot be implemented, send an alert to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "CANNOT IMPLEMENT: [TASK_ID] - [Revision Item]"
- **Content**: describe the technical constraint preventing implementation, explain why it is impossible, and propose an alternative approach
- **Type**: alert
- **Priority**: urgent

**Verify**: confirm the alert was delivered.
