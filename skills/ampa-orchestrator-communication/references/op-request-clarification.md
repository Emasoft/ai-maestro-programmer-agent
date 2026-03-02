---
name: op-request-clarification
description: Request task clarification from EOA when requirements are unclear or ambiguous.
parent-skill: ampa-orchestrator-communication
workflow-step: "Step 14"
message-type: clarification-request
priority: high
---

# Operation: Request Clarification

This operation describes how to request clarification from the AI Maestro Orchestrator Agent (EOA) when task requirements are unclear, ambiguous, or incomplete.

## Table of Contents

- 1.1 When to Request Clarification
- 1.2 Clarification Request Format
- 1.3 Sending the Request
- 1.4 Handling the Response
- 1.5 Examples

## 1.1 When to Request Clarification

Request clarification from EOA in these situations:

| Situation | Example |
|-----------|---------|
| **Ambiguous requirements** | Task says "improve performance" without specifying metrics or targets |
| **Missing technical details** | No API specification provided for integration task |
| **Conflicting instructions** | Task mentions two incompatible approaches |
| **Scope uncertainty** | Unclear whether refactoring should include tests |
| **Dependency questions** | Unknown if external service is available |
| **Priority conflicts** | Multiple tasks with unclear priority order |

**Do NOT request clarification for**:
- Issues you can resolve by reading existing documentation
- Standard implementation decisions within your authority
- Stylistic choices already covered by project conventions

## Prerequisites

Before requesting clarification:

1. **Read all task materials**: Ensure you have read the complete task description
2. **Check existing documentation**: Search for answers in project docs
3. **Review similar tasks**: Check if similar tasks provide context
4. **Formulate specific questions**: Prepare clear, answerable questions

## 1.2 Clarification Request Format

Structure your clarification request with these components:

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "to": "orchestrator-master",
  "subject": "CLARIFICATION: [Task ID] - [Brief Topic]",
  "priority": "high",
  "content": {
    "type": "clarification-request",
    "message": "[Structured clarification request]",
    "task_id": "[TASK-ID]",
    "questions": [
      "[Specific question 1]",
      "[Specific question 2]"
    ],
    "context": "[What you already understand]",
    "impact": "[How this affects your progress]"
  }
}
```

### Message Components

| Field | Description | Required |
|-------|-------------|----------|
| `task_id` | The identifier of the task needing clarification | Yes |
| `questions` | Array of specific, answerable questions | Yes |
| `context` | What you already understand about the task | Yes |
| `impact` | How lack of clarity affects your work | No |

## Procedure

Follow these steps to request clarification:

1. **Identify the unclear aspect**: Pinpoint exactly what is ambiguous
2. **Formulate specific questions**: Create clear, answerable questions (not vague requests)
3. **Document your current understanding**: Show what you already know
4. **Compose the message**: Use the format specified in section 1.2
5. **Send via the `agent-messaging` skill**: Use the skill's send operation to deliver the request to the orchestrator
6. **Wait for response**: Check your inbox using the `agent-messaging` skill for EOA reply
7. **Acknowledge receipt**: Confirm you received the clarification
8. **Update task understanding**: Incorporate clarification into your work

## Checklist

Use this checklist before sending a clarification request:

- [ ] I have read the complete task description
- [ ] I have checked project documentation for answers
- [ ] I have formulated specific, answerable questions
- [ ] I have documented what I already understand
- [ ] The questions are not about standard implementation decisions
- [ ] The message follows the required JSON format
- [ ] The subject line includes task ID and topic
- [ ] I am prepared to wait for a response before proceeding

## 1.3 Sending the Request

Send the clarification request to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "CLARIFICATION: [TASK_ID] - [Brief Topic]"
- **Content**: include the structured request with your specific questions, what you already understand (context), and how the lack of clarity affects your progress (impact)
- **Type**: request
- **Priority**: high

**Verify**: confirm the clarification request appears in your sent messages.

## 1.4 Handling the Response

When EOA responds to your clarification request:

1. **Read the complete response**: Do not skim; read carefully
2. **Verify understanding**: Ensure the answer addresses your questions
3. **Acknowledge receipt**: Send acknowledgment message
4. **Request follow-up if needed**: If still unclear, send follow-up questions
5. **Document the clarification**: Record the decision for future reference
6. **Resume work**: Continue with the task using the clarified requirements

### Acknowledgment Format

When you receive a clarification response, reply directly to it using the `agent-messaging` skill:
- **Action**: reply to the original message by its ID
- **Content**: confirm understanding and state how you will proceed based on the clarification

**Verify**: confirm the reply was sent.

Alternatively, send a new acknowledgment message using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "ACK: CLARIFICATION: [TASK_ID] - [Topic]"
- **Content**: confirm understanding and state your planned approach
- **Type**: ack
- **Priority**: normal

**Verify**: confirm the acknowledgment was delivered.

## 1.5 Examples

### Example 1: Unclear Performance Requirements

**Situation**: Task says "optimize database queries" without specifying targets.

Send a clarification request to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "CLARIFICATION: TASK-456 - Database Optimization Targets"
- **Content**: "I need clarification on the performance targets for database query optimization. Questions: 1) What is the target query response time? 2) Which specific queries should be prioritized? 3) Are there memory usage constraints to consider? Context: The task mentions optimizing database queries but does not specify performance targets or which queries are problematic. Current slowest query takes 2.3 seconds. Impact: Cannot determine optimization success criteria or prioritization without targets."
- **Type**: request
- **Priority**: high

**Verify**: confirm the clarification request was delivered.

### Example 2: Missing Dependency Information

**Situation**: Task requires integration with a service not mentioned in project docs.

Send a clarification request to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "CLARIFICATION: TASK-789 - PaymentGateway Service Details"
- **Content**: "I need details about the PaymentGateway service for integration. Questions: 1) What is the PaymentGateway API endpoint URL? 2) Is there existing client code I should reuse? 3) What test environment is available? Context: Task references PaymentGateway service but I found no documentation or existing code for it in the codebase. Impact: Cannot begin integration work without service details."
- **Type**: request
- **Priority**: high

**Verify**: confirm the clarification request was delivered.

### Example 3: Conflicting Requirements

**Situation**: Two parts of the task description contradict each other.

Send a clarification request to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "CLARIFICATION: TASK-101 - Conflicting Error Handling Requirements"
- **Content**: "The task contains conflicting requirements for error handling. Questions: 1) Should errors fail fast (as stated in section 2) or be silently logged (as stated in section 4)? 2) Which requirement takes precedence? Context: Section 2 says to implement fail-fast error handling. Section 4 says errors should be logged silently without disrupting the user. These approaches are mutually exclusive. Impact: Cannot implement error handling without knowing which approach to use."
- **Type**: request
- **Priority**: high

**Verify**: confirm the clarification request was delivered.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Identity not found | Messaging not initialized | Read the `agent-messaging` skill and follow its initialization instructions |
| Recipient not found | EOA session not registered | Wait for EOA to start or notify user |
| Messaging service offline | Messaging service not running | Use the `agent-messaging` skill's status check, restart AI Maestro |
| No response within 30 minutes | EOA busy or unavailable | Resend with urgent priority using the `agent-messaging` skill |
| `Response does not answer questions` | Miscommunication | Send follow-up with specific unanswered questions |

### Retry Logic

If message delivery fails:

1. Wait 5 seconds
2. Attempt to send the message again using the `agent-messaging` skill
3. If it fails again, wait 5 seconds and retry one more time (maximum 3 attempts total)
4. If all 3 attempts fail, report the messaging failure to the user

**Verify**: after each retry, check whether the message appears in your sent messages before retrying.
