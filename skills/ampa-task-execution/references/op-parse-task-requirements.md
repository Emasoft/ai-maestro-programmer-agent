---
operation: op-parse-task-requirements
procedure: proc-execute-task
workflow-step: "Step 17.2 - Parse Task Requirements"
parent-skill: ampa-task-execution
parent-plugin: ai-maestro-programmer-agent
version: 1.0.0
---

# Operation: Parse Task Requirements


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 2.1: Extract Acceptance Criteria List](#step-21-extract-acceptance-criteria-list)
  - [Step 2.2: Identify Dependencies on Other Tasks](#step-22-identify-dependencies-on-other-tasks)
  - [Step 2.3: Determine Target Files and Components](#step-23-determine-target-files-and-components)
  - [Step 2.4: Clarify Ambiguities with Orchestrator](#step-24-clarify-ambiguities-with-orchestrator)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: Complete Requirements Analysis](#example-1-complete-requirements-analysis)
  - [Example 2: Blocked by Dependency](#example-2-blocked-by-dependency)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

Understand acceptance criteria, dependencies, and scope of the assigned task.

## When to Use

Use this operation when:
- You have received and acknowledged a task assignment
- You need to understand what exactly needs to be implemented
- You must identify dependencies before starting work

## Prerequisites

Before executing this operation:
1. Task assignment must be received (op-receive-task-assignment completed)
2. Task must have passed validation
3. You must have access to the task's acceptance criteria

## Procedure

### Step 2.1: Extract Acceptance Criteria List

Parse the `acceptance_criteria` array from the task message:

```json
{
  "acceptance_criteria": [
    "Criterion 1: Description of expected behavior",
    "Criterion 2: Another expected outcome",
    "Criterion 3: Edge case handling requirement"
  ]
}
```

For each criterion, create a trackable item:

| Criterion ID | Description | Status |
|--------------|-------------|--------|
| AC-001 | Criterion 1 description | PENDING |
| AC-002 | Criterion 2 description | PENDING |
| AC-003 | Criterion 3 description | PENDING |

### Step 2.2: Identify Dependencies on Other Tasks

Check if the task message includes dependency information:

```json
{
  "dependencies": {
    "required_tasks": ["TASK-001", "TASK-002"],
    "required_files": ["src/utils/helper.py"],
    "required_apis": ["UserService", "AuthService"]
  }
}
```

Dependency types to identify:

| Type | Description | Action if Unmet |
|------|-------------|-----------------|
| Task Dependencies | Other tasks that must complete first | Wait or report blocker |
| File Dependencies | Files that must exist | Verify or request creation |
| API Dependencies | Services that must be available | Verify accessibility |
| Data Dependencies | Data that must be present | Verify or request setup |

If dependencies are unmet, report blocker to orchestrator before proceeding.

### Step 2.3: Determine Target Files and Components

Analyze the task description to identify:

1. **Target Files**: Which files need to be created or modified
2. **Target Components**: Which functions, classes, or modules are affected
3. **Scope Boundaries**: What is explicitly out of scope

Use SERENA MCP to locate existing components:

```
mcp__serena__find_symbol("UserService")
mcp__serena__get_codebase_structure()
```

Create a file impact map:

| File Path | Action | Components Affected |
|-----------|--------|---------------------|
| src/auth/login.py | MODIFY | login_user(), validate_credentials() |
| src/auth/session.py | CREATE | Session class |
| tests/test_auth.py | MODIFY | Add new test cases |

### Step 2.4: Clarify Ambiguities with Orchestrator

If any requirements are unclear, send a clarification request to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent session
- **Subject**: "CLARIFY: [TASK_ID] - Ambiguous requirement"
- **Content**: describe what is unclear and list specific questions that need answering
- **Type**: clarification
- **Priority**: high

**Verify**: confirm the clarification request appears in your sent messages.

Do NOT proceed with implementation until clarifications are received if the ambiguity affects core functionality.

## Checklist

- [ ] All acceptance criteria extracted and numbered
- [ ] Dependency check completed (tasks, files, APIs, data)
- [ ] All dependencies met or blockers reported
- [ ] Target files identified using SERENA
- [ ] Target components mapped
- [ ] Scope boundaries documented
- [ ] All ambiguities clarified or escalated

## Examples

### Example 1: Complete Requirements Analysis

Task: "Add password reset functionality"

**Acceptance Criteria Extraction:**
| ID | Criterion | Type |
|----|-----------|------|
| AC-001 | User can request password reset via email | Functional |
| AC-002 | Reset link expires after 24 hours | Security |
| AC-003 | Password must meet complexity requirements | Validation |
| AC-004 | User receives confirmation after reset | UX |

**Dependencies Identified:**
- Task Dependency: User email verification (TASK-045) - COMPLETED
- API Dependency: EmailService - AVAILABLE
- File Dependency: src/auth/user.py - EXISTS

**Target Files:**
| File | Action | Reason |
|------|--------|--------|
| src/auth/password.py | CREATE | New password reset logic |
| src/auth/user.py | MODIFY | Add reset token field |
| src/email/templates/reset.html | CREATE | Email template |
| tests/test_password.py | CREATE | Test coverage |

### Example 2: Blocked by Dependency

Task: "Integrate payment gateway"

**Dependency Check:**
- API Dependency: PaymentService - NOT CONFIGURED

**Blocker Message Sent:**

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "to": "orchestrator-master",
  "subject": "BLOCKED: AMPA-005 - Missing dependency",
  "content": {
    "type": "blocker",
    "task_id": "AMPA-005",
    "message": "Cannot proceed: PaymentService API is not configured",
    "resolution_needed": "Configure PaymentService credentials",
    "status": "blocked"
  }
}
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Empty acceptance_criteria | Task poorly defined | Request criteria from orchestrator |
| Circular dependencies | Tasks depend on each other | Report to orchestrator for resolution |
| File not found | Referenced file missing | Clarify if file should be created |
| Component not found | SERENA cannot locate symbol | Search with alternative names or paths |

## Related Operations

- [op-receive-task-assignment.md](op-receive-task-assignment.md) - Previous step
- [op-setup-development-environment.md](op-setup-development-environment.md) - Next step
- [op-validate-acceptance-criteria.md](op-validate-acceptance-criteria.md) - Where criteria are verified
