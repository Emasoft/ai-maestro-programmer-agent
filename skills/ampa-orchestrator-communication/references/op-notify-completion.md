---
name: op-notify-completion
description: Notify AMOA when task is complete
parent-skill: ampa-orchestrator-communication
---

# Notify Completion

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

This operation describes how to inform the AI Maestro Orchestrator Agent (AMOA)
when your task implementation is complete and ready for review.

## 5.1 Completion Criteria

Before notifying AMOA of completion, verify ALL of these criteria are met:

### Mandatory Criteria

| Criterion              | Verification                        |
| ---------------------- | ----------------------------------- |
| **All tests pass**     | Run full test suite, 100% pass rate |
| **Code implemented**   | All specified functionality works   |
| **Edge cases handled** | Error conditions covered            |
| **No regressions**     | Existing tests still pass           |
| **Code formatted**     | Linter passes, style consistent     |
| **Type checks pass**   | No type errors (if applicable)      |

### Quality Criteria

| Criterion                 | Verification                 |
| ------------------------- | ---------------------------- |
| **Code reviewed**         | Self-reviewed for issues     |
| **Documentation updated** | Docstrings, comments current |
| **Commits organized**     | Logical commit history       |
| **Branch ready**          | Clean, mergeable state       |

### Deliverables Ready

| Deliverable        | Status               |
| ------------------ | -------------------- |
| Source code        | Committed and pushed |
| Tests              | Written and passing  |
| Documentation      | Updated if required  |
| PR (if applicable) | Created and ready    |

## Prerequisites

Before sending completion notification:

1. **All tests pass**: Run complete test suite
2. **Code formatted**: Run linter and formatter
3. **Type checks pass**: Run type checker (if applicable)
4. **Self-reviewed**: Review your own changes
5. **Commits pushed**: All changes committed and pushed
6. **PR created (if applicable)**: Pull request ready for review

## 5.2 Completion Notification Format

Structure your completion notification with these components:

> **Note**: The structure below shows the conceptual message content. Use the
> `agent-messaging` skill to send messages - it handles the exact API format
> automatically.

```json
{
  "to": "orchestrator-master",
  "subject": "COMPLETE: [Task ID] - [Brief Description]",
  "priority": "high",
  "content": {
    "type": "completion-notification",
    "message": "[Brief completion summary]",
    "task_id": "[TASK-ID]",
    "status": "completed",
    "deliverables": {
      "code": {
        "branch": "[branch-name]",
        "commits": [number],
        "files_changed": [number],
        "lines_added": [number],
        "lines_removed": [number]
      },
      "tests": {
        "total": [number],
        "passed": [number],
        "coverage_percent": [number]
      },
      "documentation": {
        "updated": [true/false],
        "files": ["[file1]", "[file2]"]
      },
      "pr": {
        "created": [true/false],
        "url": "[PR-URL]",
        "title": "[PR-Title]"
      }
    },
    "implementation_notes": "[Any important notes about the implementation]",
    "known_limitations": ["[Limitation 1]", "[Limitation 2]"],
    "testing_notes": "[How to test the implementation]",
    "ready_for_review": true
  }
}
```

### Message Components

| Field                        | Description                          | Required      |
| ---------------------------- | ------------------------------------ | ------------- |
| `task_id`                    | The identifier of the completed task | Yes           |
| `status`                     | Must be "completed"                  | Yes           |
| `deliverables`               | Summary of all deliverables          | Yes           |
| `deliverables.code`          | Code change statistics               | Yes           |
| `deliverables.tests`         | Test results                         | Yes           |
| `deliverables.documentation` | Documentation changes                | Yes           |
| `deliverables.pr`            | Pull request information             | If applicable |
| `implementation_notes`       | Important implementation details     | No            |
| `known_limitations`          | Any limitations or caveats           | No            |
| `testing_notes`              | How to verify the implementation     | No            |
| `ready_for_review`           | Confirmation ready for review        | Yes           |

## 5.3 Deliverables Summary

### Code Deliverables

Include these statistics:

```json
"code": {
  "branch": "feature/a1b2c3d4-e5f6-7890-abcd-ef1234567890-user-auth",
  "commits": 5,
  "files_changed": 8,
  "lines_added": 342,
  "lines_removed": 45
}
```

Get these values with:

```bash
# Branch name
git branch --show-current

# Commit count (from branch point)
git rev-list --count main..HEAD

# Files changed
git diff --stat main..HEAD | tail -1

# Lines added/removed
git diff --stat main..HEAD | tail -1
```

### Test Deliverables

Include test results:

```json
"tests": {
  "total": 24,
  "passed": 24,
  "coverage_percent": 92
}
```

Get these values with:

```bash
# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing -v

# Parse output for totals
```

### Documentation Deliverables

Include documentation changes:

```json
"documentation": {
  "updated": true,
  "files": [
    "docs/api/auth.md",
    "README.md"
  ]
}
```

### Pull Request Deliverables

If PR was created:

```json
"pr": {
  "created": true,
  "url": "https://github.com/org/repo/pull/123",
  "title": "feat(auth): Add user authentication module"
}
```

## Procedure

Follow these steps to notify completion:

1. **Verify all tests pass**: Run complete test suite
2. **Verify code quality**: Run linter, formatter, type checker
3. **Gather statistics**: Collect code and test metrics
4. **Create PR (if applicable)**: Open pull request
5. **Self-review**: Review your own changes one more time
6. **Compose notification**: Use the format from section 5.2
7. **Send to AMOA**: Send the completion notification using the
   `agent-messaging` skill
8. **Wait for feedback**: Check your inbox using the `agent-messaging` skill for
   AMOA response

## Checklist

Use this checklist before sending completion notification:

- [ ] All unit tests pass (100% pass rate)
- [ ] All integration tests pass (if applicable)
- [ ] Linter passes with no errors
- [ ] Type checker passes with no errors (if applicable)
- [ ] Code has been self-reviewed
- [ ] Commits are organized and have good messages
- [ ] All changes are committed and pushed
- [ ] Branch is up to date with main/base branch
- [ ] Documentation is updated (if required)
- [ ] PR is created and ready (if applicable)
- [ ] I have gathered all code and test statistics
- [ ] Known limitations are documented
- [ ] Testing notes are prepared
- [ ] The message follows the required format

## 5.4 Sending Notification

Send the completion notification to the orchestrator using the `agent-messaging`
skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "COMPLETE: [TASK_ID] - [Brief Description]"
- **Content**: include the completion summary following the format from section
  5.2 (branch, commits, files changed, test results, coverage, documentation
  updated, PR URL, implementation notes, known limitations, testing notes)
- **Type**: notification
- **Priority**: high

**Verify**: confirm the completion notification appears in your sent messages.

## 5.5 Examples

### Example 1: Feature Implementation Complete

**Situation**: New feature fully implemented with tests.

Send a completion notification to the orchestrator using the `agent-messaging`
skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "COMPLETE: b2c3d4e5-f6a7-8901-bcde-f23456789012 - Order
  Processing Pipeline"
- **Content**: "Order processing pipeline implementation complete with full test
  coverage. Branch: feature/b2c3d4e5-f6a7-8901-bcde-f23456789012-order-pipeline
  (8 commits, 12 files changed, +567/-23 lines). Tests: 35/35 passing, 94%
  coverage. Docs updated: docs/architecture/order-pipeline.md,
  docs/api/orders.md. PR: https://github.com/org/repo/pull/789 - feat(orders):
  Add order processing pipeline. Implementation notes: Implemented async
  pipeline with retry logic, orders processed in batches of 100 for efficiency.
  Testing: uv run pytest tests/ -v or manually: uv run python
  scripts/test_order_pipeline.py"
- **Type**: notification
- **Priority**: high

**Verify**: confirm the completion notification was delivered.

### Example 2: Bug Fix Complete

**Situation**: Bug fix implemented and verified.

Send a completion notification to the orchestrator using the `agent-messaging`
skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "COMPLETE: c3d4e5f6-a7b8-9012-cdef-345678901234 - Fix Race
  Condition in Cache Update"
- **Content**: "Race condition in cache update fixed. Added mutex lock and
  regression tests. Branch:
  fix/c3d4e5f6-a7b8-9012-cdef-345678901234-cache-race-condition (3 commits, 2
  files changed, +45/-12 lines). Tests: 8/8 passing, 100% coverage. PR:
  https://github.com/org/repo/pull/101 - fix(cache): Add mutex lock to prevent
  race condition. Implementation notes: Added threading.Lock() around cache
  write operations, verified fix under concurrent load testing. Testing: uv run
  pytest tests/unit/test_cache.py::test_concurrent_updates -v --count=100"
- **Type**: notification
- **Priority**: high

**Verify**: confirm the completion notification was delivered.

### Example 3: Refactoring Complete

**Situation**: Refactoring task completed.

Send a completion notification to the orchestrator using the `agent-messaging`
skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "COMPLETE: d4e5f6a7-b8c9-0123-defa-456789012345 - Refactor
  Payment Module"
- **Content**: "Payment module refactored. Reduced complexity, improved
  testability. Branch:
  refactor/d4e5f6a7-b8c9-0123-defa-456789012345-payment-module (6 commits, 5
  files changed, +234/-312 lines). Tests: 28/28 passing, 96% coverage. Docs
  updated: docs/architecture/payment-module.md. PR:
  https://github.com/org/repo/pull/202 - refactor(payment): Simplify payment
  processing module. Implementation notes: Split monolithic PaymentProcessor
  into PaymentValidator, PaymentExecutor, and PaymentNotifier. Reduced
  cyclomatic complexity from 32 to 8. Testing: All existing tests pass, new unit
  tests added for each extracted class."
- **Type**: notification
- **Priority**: high

**Verify**: confirm the completion notification was delivered.

## Error Handling

| Error                              | Cause                         | Resolution                                                               |
| ---------------------------------- | ----------------------------- | ------------------------------------------------------------------------ |
| Messaging service offline          | Messaging service not running | Use the `agent-messaging` skill's status check, start AI Maestro service |
| Message delivery failed            | Network issue                 | Retry the send operation up to 3 times using the `agent-messaging` skill |
| `Tests failing after notification` | Regression introduced         | Send correction notification                                             |

### Post-Notification Issues

If you discover an issue after sending completion notification, send a
correction to the orchestrator using the `agent-messaging` skill:

- **Recipient**: your assigned orchestrator agent
- **Subject**: "CORRECTION: [TASK_ID] - Issue Found After Completion"
- **Content**: describe the issue found, explain what you are doing to fix it,
  and provide a revised completion estimate
- **Type**: status
- **Priority**: high

**Verify**: confirm the correction message was delivered.
