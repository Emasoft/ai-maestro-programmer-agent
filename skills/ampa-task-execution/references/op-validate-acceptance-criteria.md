---
name: op-validate-acceptance-criteria
description: Validate that implementation meets all acceptance criteria
workflow-step: "Step 17.6 - Validate Acceptance Criteria"
parent-skill: ampa-task-execution
---

# Operation: Validate Acceptance Criteria

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.



## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 6.1: Review Each Acceptance Criterion](#step-61-review-each-acceptance-criterion)
  - [Step 6.2: Verify Implementation Satisfies Criterion](#step-62-verify-implementation-satisfies-criterion)
  - [Step 6.3: Document Validation Evidence](#step-63-document-validation-evidence)
- [Validation Record: TASK-001](#validation-record-task-001)
  - [AC-001: Email format is validated on submit](#ac-001-email-format-is-validated-on-submit)
  - [AC-002: Invalid email shows error message](#ac-002-invalid-email-shows-error-message)
  - [AC-003: Valid email allows form submission](#ac-003-valid-email-allows-form-submission)
  - [Step 6.4: Report Completion to Orchestrator](#step-64-report-completion-to-orchestrator)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: All Criteria Passed](#example-1-all-criteria-passed)
  - [Example 2: Criterion Failed](#example-2-criterion-failed)
  - [Example 3: Partial Evidence](#example-3-partial-evidence)
  - [AC-001: Error message visible](#ac-001-error-message-visible)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

Verify all acceptance criteria are met before marking the task complete.

## When to Use

Use this operation when:
- Implementation is complete
- Tests are written and passing
- You are ready to mark the task as done

## Prerequisites

Before executing this operation:
1. Code implementation must be complete (op-implement-code completed)
2. Tests must be written and passing (op-write-tests completed)
3. All acceptance criteria must be documented with IDs
4. Evidence must be available for each criterion

## Procedure

### Step 6.1: Review Each Acceptance Criterion

Go through each criterion from the task assignment:

| Criterion ID | Description | Evidence Type |
|--------------|-------------|---------------|
| AC-001 | Email format is validated | Test passes |
| AC-002 | Error message shown for invalid | UI screenshot/test |
| AC-003 | Valid email allows submission | Test passes |

For each criterion, identify what constitutes valid evidence:

| Evidence Type | Description | Example |
|---------------|-------------|---------|
| Test Pass | Automated test verifies behavior | `test_email_validation PASSED` |
| Manual Test | Hand-verified in running system | Screenshot of error message |
| Code Review | Code inspection confirms logic | Function contains validation |
| Log Output | System logs show expected behavior | Captured log entries |

### Step 6.2: Verify Implementation Satisfies Criterion

For each criterion, perform verification:

**For Test-Verified Criteria:**
```bash
# Run the specific test(s) that verify this criterion
uv run pytest tests/unit/test_validators.py::TestValidateEmail -v

# Capture the output
# PASSED = criterion satisfied
# FAILED = criterion NOT satisfied
```

**For Code-Verified Criteria:**
```
# Use SERENA to verify the code contains expected logic
mcp__serena__get_symbol_details("validate_email")

# Manually verify the implementation matches the criterion
```

**For Manual-Verified Criteria:**
1. Start the application in development mode
2. Perform the action described in the criterion
3. Observe and document the result
4. Capture evidence (screenshot, log, output)

### Step 6.3: Document Validation Evidence

Create a validation record for each criterion:

```markdown
## Validation Record: TASK-001

### AC-001: Email format is validated on submit
- **Status**: PASSED
- **Evidence Type**: Test
- **Evidence**: `tests/unit/test_validators.py::TestValidateEmail` - 9 tests passed
- **Verified At**: 2024-01-15T10:30:00Z

### AC-002: Invalid email shows error message
- **Status**: PASSED
- **Evidence Type**: Test + Code Review
- **Evidence**:
  - Test: `test_invalid_email_shows_error PASSED`
  - Code: Error message defined in `src/validators/messages.py:42`
- **Verified At**: 2024-01-15T10:35:00Z

### AC-003: Valid email allows form submission
- **Status**: PASSED
- **Evidence Type**: Test
- **Evidence**: `test_valid_email_submits_form PASSED`
- **Verified At**: 2024-01-15T10:40:00Z
```

If ANY criterion is NOT PASSED:
- Do NOT proceed to completion
- Fix the implementation
- Re-run verification

### Step 6.4: Report Completion to Orchestrator

Send a completion message with validation summary to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent session
- **Subject**: "COMPLETE: [TASK_ID]"
- **Content**: "Task completed. All acceptance criteria validated." Include the validation summary with total criteria, passed count, and failed count.
- **Type**: completion
- **Priority**: normal

**Verify**: confirm the completion message appears in your sent messages.

## Checklist

- [ ] All acceptance criteria listed and numbered
- [ ] Each criterion reviewed individually
- [ ] Evidence collected for each criterion
- [ ] All criteria show PASSED status
- [ ] Validation record documented
- [ ] Completion message sent to orchestrator
- [ ] Task status updated to complete
- [ ] Changed files committed to git

## Examples

### Example 1: All Criteria Passed

Task: "Add email validation to user form"

| ID | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| AC-001 | Email format validated | PASSED | 9 unit tests passed |
| AC-002 | Error message shown | PASSED | Test + code review |
| AC-003 | Form submits with valid email | PASSED | Integration test passed |

Completion message sent:

> **Note**: The structure below shows the conceptual message content. Use the `agent-messaging` skill to send messages - it handles the exact API format automatically.

```json
{
  "to": "orchestrator-master",
  "subject": "COMPLETE: AMPA-001",
  "content": {
    "type": "completion",
    "task_id": "AMPA-001",
    "status": "complete",
    "validation_summary": {
      "total_criteria": 3,
      "passed": 3,
      "failed": 0
    }
  }
}
```

### Example 2: Criterion Failed

Task: "Add password complexity validation"

| ID | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| AC-001 | Min 8 characters | PASSED | Test passed |
| AC-002 | Requires uppercase | FAILED | Test failed - no uppercase check |
| AC-003 | Requires number | PASSED | Test passed |

Action required:
1. Do NOT report completion
2. Fix the implementation for AC-002
3. Re-run all tests
4. Re-validate all criteria
5. Only then report completion

### Example 3: Partial Evidence

When a criterion cannot be fully automated:

| ID | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| AC-001 | Error message visible | NEEDS MANUAL | Requires visual inspection |

For manual criteria:
1. Start dev server: `uv run uvicorn src.main:app`
2. Navigate to form
3. Enter invalid email
4. Observe error message
5. Capture screenshot
6. Document as evidence

```markdown
### AC-001: Error message visible
- **Status**: PASSED (Manual)
- **Evidence**: Screenshot saved to docs_dev/validation/error-message.png
- **Verified By**: AMPA Agent
- **Verified At**: 2024-01-15T10:45:00Z
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Criterion unclear | Ambiguous requirement | Request clarification before marking |
| Test flaky | Intermittent failure | Fix flakiness, must pass consistently |
| Evidence lost | Screenshot/log deleted | Re-capture evidence before completion |
| Partial pass | Only some cases work | Not passed - fix implementation |
| Cannot verify | Missing tooling | Report blocker, request guidance |

## Related Operations

- [op-write-tests.md](op-write-tests.md) - Previous step
- [op-receive-task-assignment.md](op-receive-task-assignment.md) - For next task
- [../ampa-orchestrator-communication](../ampa-orchestrator-communication/SKILL.md) - For messaging patterns
