---
name: op-report-blocker
description: Report blocking issues to AMOA
parent-skill: ampa-orchestrator-communication
---

# Report Blocker

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

This operation describes how to report blocking issues to the AI Maestro
Orchestrator Agent (AMOA) when you encounter problems that prevent you from
making progress on an assigned task.

## 3.1 Identifying Blockers

A blocker is an issue that completely prevents you from continuing work on a
task. Blockers must be reported immediately to AMOA.

### What Qualifies as a Blocker

| Type                        | Examples                                              | Is Blocker?                   |
| --------------------------- | ----------------------------------------------------- | ----------------------------- |
| **Missing credentials**     | API keys, database passwords, service accounts        | Yes                           |
| **Missing access**          | Repository access, server access, cloud console       | Yes                           |
| **Missing dependency**      | Required service not available, package not published | Yes                           |
| **Unclear requirements**    | Cannot proceed without clarification                  | Yes (use clarification first) |
| **Technical impossibility** | Requested feature cannot be implemented as specified  | Yes                           |
| **External dependency**     | Waiting on external team or third party               | Yes                           |
| **Environment issue**       | Build system broken, CI/CD pipeline down              | Yes                           |
| **Difficult problem**       | Takes longer than expected but progress possible      | No                            |
| **Missing documentation**   | Can be discovered through code exploration            | No                            |
| **Minor tooling issue**     | Workaround available                                  | No                            |

### Blocker vs. Delay

| Characteristic             | Blocker          | Delay                      |
| -------------------------- | ---------------- | -------------------------- |
| Can you make any progress? | No               | Yes, slowly                |
| Is there a workaround?     | No               | Possibly                   |
| Do you need external help? | Yes              | Maybe                      |
| Report as                  | `blocker-report` | `status-update` with delay |

## Prerequisites

Before reporting a blocker:

1. **Verify it is a blocker**: Confirm no workaround exists
2. **Attempt resolution**: Try to resolve independently first
3. **Document attempts**: Note what you tried
4. **Identify root cause**: Understand why you are blocked
5. **Propose solutions**: Think of possible resolutions

## 3.2 Blocker Report Format

Structure your blocker report with these components:

> **Note**: The structure below shows the conceptual message content. Use the
> `agent-messaging` skill to send messages - it handles the exact API format
> automatically.

```json
{
  "to": "orchestrator-master",
  "subject": "BLOCKER: [Task ID] - [Brief Description]",
  "priority": "urgent",
  "content": {
    "type": "blocker-report",
    "message": "[Brief summary of blocking issue]",
    "task_id": "[TASK-ID]",
    "severity": "[critical|high|medium]",
    "blocker_type": "[blocker-type]",
    "description": "[Detailed description of the issue]",
    "impact": "[How this affects task completion]",
    "attempted_resolutions": ["[What you tried]"],
    "proposed_solutions": [
      "[Possible resolution 1]",
      "[Possible resolution 2]"
    ],
    "unblocking_requirements": "[What is needed to proceed]",
    "progress_before_block": "[What was completed before block]"
  }
}
```

### Message Components

| Field                     | Description                        | Required |
| ------------------------- | ---------------------------------- | -------- |
| `task_id`                 | The identifier of the blocked task | Yes      |
| `severity`                | Severity level (see section 3.3)   | Yes      |
| `blocker_type`            | Category of blocker                | Yes      |
| `description`             | Detailed description of the issue  | Yes      |
| `impact`                  | How this affects completion        | Yes      |
| `attempted_resolutions`   | What you tried to resolve it       | Yes      |
| `proposed_solutions`      | Possible resolutions               | Yes      |
| `unblocking_requirements` | What is needed to proceed          | Yes      |
| `progress_before_block`   | Work completed before block        | No       |

### Blocker Types

Use these standardized blocker type values:

| Type                      | Description                             |
| ------------------------- | --------------------------------------- |
| `missing-credentials`     | API keys, passwords, tokens             |
| `missing-access`          | Repository, server, or service access   |
| `missing-dependency`      | Required service or package unavailable |
| `unclear-requirements`    | Cannot proceed without clarification    |
| `technical-impossibility` | Cannot implement as specified           |
| `external-dependency`     | Waiting on external team                |
| `environment-issue`       | Build, CI/CD, or infrastructure problem |
| `resource-unavailable`    | Required resource does not exist        |

## 3.3 Severity Levels

### Critical Severity

**Definition**: Complete stop, no progress possible on any part of the task.

**Characteristics**:

- No workaround exists
- Cannot work on any related items
- Time-sensitive resolution needed

**Example**: Production credentials revoked, cannot deploy or test.

### High Severity

**Definition**: Major functionality blocked, but minor progress possible.

**Characteristics**:

- Some unrelated work can continue
- Core functionality blocked
- Resolution needed within hours

**Example**: API endpoint returning 500 errors, can continue writing tests but
cannot verify integration.

### Medium Severity

**Definition**: Partial block, significant workaround required.

**Characteristics**:

- Workaround exists but is inefficient
- Progress significantly slowed
- Resolution needed within a day

**Example**: CI/CD pipeline slow, can test locally but deployment delayed.

## Procedure

Follow these steps to report a blocker:

1. **Confirm blocker status**: Verify no workaround exists
2. **Document the issue**: Note exact error messages, conditions
3. **Note attempted resolutions**: List what you tried
4. **Determine severity**: Use criteria from section 3.3
5. **Identify blocker type**: Use standardized types
6. **Propose solutions**: Think of possible resolutions
7. **Compose message**: Use the format from section 3.2
8. **Send with urgent priority**: Send the blocker report using the
   `agent-messaging` skill with urgent priority
9. **Verify**: confirm message delivery via the `agent-messaging` skill's sent
   messages feature
10. **Wait for response**: Check your inbox using the `agent-messaging` skill
    for AMOA reply
11. **Continue if possible**: Work on unblocked items if any exist

## Checklist

Use this checklist before reporting a blocker:

- [ ] I have confirmed this is a blocker (no workaround exists)
- [ ] I have attempted to resolve it independently
- [ ] I have documented the exact error or issue
- [ ] I have identified the root cause
- [ ] I have categorized the blocker type
- [ ] I have assessed the severity level
- [ ] I have proposed possible solutions
- [ ] I have listed what is needed to unblock
- [ ] The message uses urgent priority
- [ ] The subject line clearly indicates BLOCKER

## 3.4 Escalation Procedure

### Escalation Timeline

| Severity | Initial Report | First Escalation | Second Escalation |
| -------- | -------------- | ---------------- | ----------------- |
| Critical | Immediate      | +15 minutes      | +30 minutes       |
| High     | Immediate      | +1 hour          | +2 hours          |
| Medium   | Immediate      | +4 hours         | +8 hours          |

### Escalation Actions

1. **First Escalation**: Resend with reminder, confirm AMOA received original
2. **Second Escalation**: Request AMOA to escalate to user
3. **Final Escalation**: Send direct notification to user (if configured)

### Escalation Message

Send an escalation message to the orchestrator using the `agent-messaging`
skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "ESCALATION: BLOCKER: [TASK_ID] - [Description]"
- **Content**: describe that this is an escalation of a previously sent blocker
  report, how long ago the original was sent, that the task remains blocked, the
  severity level, and the escalation level. Request acknowledgment and a
  resolution path.
- **Type**: alert
- **Priority**: urgent

**Verify**: confirm the escalation message was delivered.

## 3.5 Examples

### Example 1: Missing API Credentials

**Situation**: Cannot access external API due to missing credentials.

Send a blocker report to the orchestrator using the `agent-messaging` skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "BLOCKER: a1b2c3d4-e5f6-7890-abcd-ef1234567890 - Missing
  PaymentGateway API Credentials"
- **Content**: "Cannot proceed with PaymentGateway integration - API credentials
  not found. Severity: critical. Blocker type: missing-credentials. The task
  requires integration with PaymentGateway API. I searched the codebase,
  environment variables, and secrets store but found no credentials. API returns
  401 Unauthorized. Impact: Cannot implement, test, or verify any API
  integration functionality. Task is 100% blocked. Attempted: Searched .env
  files, checked secrets manager, searched codebase, checked project docs.
  Proposed solutions: 1) Provide API credentials via secrets manager 2) Provide
  test/sandbox credentials 3) Grant access to credentials documentation.
  Unblocking requirement: PaymentGateway API key and secret. Progress before
  block: Unit tests written with mocks, local logic implemented, ready for real
  integration."
- **Type**: alert
- **Priority**: urgent

**Verify**: confirm the blocker report was delivered.

### Example 2: External Service Down

**Situation**: Required external service is unavailable.

Send a blocker report to the orchestrator using the `agent-messaging` skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "BLOCKER: b2c3d4e5-f6a7-8901-bcde-f23456789012 - AuthService
  Down"
- **Content**: "AuthService is returning 503 errors. Cannot test authentication
  flow. Severity: high. Blocker type: external-dependency. The AuthService at
  auth.internal.example.com returns 503 Service Unavailable. Checked service
  status page - no reported outages. Issue started approximately 30 minutes ago.
  Impact: Cannot test any authentication functionality. Can continue writing
  code but cannot verify it works. Attempted: Verified service URL, checked
  network connectivity, tried different endpoints, checked status page. Proposed
  solutions: 1) Wait for service recovery 2) Use staging AuthService if
  available 3) Contact infrastructure team. Unblocking requirement: AuthService
  restored to operational status. Progress before block: Authentication module
  80% complete, blocked on integration testing."
- **Type**: alert
- **Priority**: urgent

**Verify**: confirm the blocker report was delivered.

### Example 3: Technical Impossibility

**Situation**: Requested feature cannot be implemented as specified.

Send a blocker report to the orchestrator using the `agent-messaging` skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "BLOCKER: c3d4e5f6-a7b8-9012-cdef-345678901234 - Technical
  Impossibility in Specification"
- **Content**: "The specified requirement is technically impossible with the
  current architecture. Severity: critical. Blocker type:
  technical-impossibility. Task requires real-time synchronous response within
  50ms, but the required data source has minimum latency of 200ms. This is a
  fundamental constraint of the external system that cannot be reduced. Impact:
  Cannot implement the feature as specified. Either the timing requirement or
  the data source must change. Attempted: Researched data source performance
  limits, tested with caching (still exceeds 50ms on cache miss), consulted data
  source documentation, tested connection pooling and optimization. Proposed
  solutions: 1) Relax timing requirement to 250ms 2) Use cached/stale data for
  real-time response 3) Change to asynchronous pattern 4) Use alternative data
  source. Unblocking requirement: Revised specification with achievable timing
  requirements."
- **Type**: alert
- **Priority**: urgent

**Verify**: confirm the blocker report was delivered.

## Error Handling

| Error                     | Cause                         | Resolution                                                                          |
| ------------------------- | ----------------------------- | ----------------------------------------------------------------------------------- |
| Messaging service offline | Messaging service not running | Use the `agent-messaging` skill's status check, start AI Maestro immediately        |
| AMOA not responding       | AMOA session inactive         | Escalate to user directly                                                           |
| Message delivery failed   | Network issue                 | Retry the send operation immediately using the `agent-messaging` skill, max 3 times |

### Critical Blocker Protocol

For critical severity blockers:

1. Send blocker report immediately
2. Set timer for 15 minutes
3. If no response, send escalation
4. If still no response after 30 minutes, notify user directly (if possible)
5. Document all attempts and timestamps
