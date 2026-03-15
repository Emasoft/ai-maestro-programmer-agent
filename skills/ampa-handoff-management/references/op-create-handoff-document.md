---
name: op-create-handoff-document
description: Create handoff documents for context transfer
parent-skill: ampa-handoff-management
---

# Create Handoff Document

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Checklist](#checklist)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

This operation explains how to create handoff documents that transfer work context to other agents or preserve state for future sessions.

## When to Use

Use this operation when:

1. **Completing a delegated task**: You finished the work and need to return results to AMOA
2. **Passing work to another agent**: Another agent will continue your work
3. **Session is ending**: Context will be cleared and work must be resumable
4. **Reaching a milestone**: A significant checkpoint that should be preserved
5. **Blocked and escalating**: You cannot proceed and need to hand off to a different agent

Do NOT use this operation when:
- You are in the middle of active implementation (use Document Work State instead)
- You just want to report a bug (use Write Bug Report instead)
- The work is trivial and fully self-contained

## Prerequisites

Before creating a handoff document:

1. **Know the recipient**: Either a specific agent name or "future self" for session resume
2. **Have a clear task name**: Consistent naming enables document retrieval
3. **Understand current state**: What is done, what remains, what is blocked
4. **Handoff directory must be writable**: `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/`

## Procedure

### Step 1: Prepare the Handoff Directory

Ensure the task-specific handoff directory exists:

```bash
HANDOFF_DIR="$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs"
TASK_NAME="<your-task-name>"
TASK_DIR="$HANDOFF_DIR/$TASK_NAME"

mkdir -p "$TASK_DIR/archive"
mkdir -p "$TASK_DIR/bugs"
```

### Step 2: Archive Previous Handoff (If Exists)

If a `current.md` already exists, archive it before creating a new one:

```bash
if [ -f "$TASK_DIR/current.md" ]; then
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    mv "$TASK_DIR/current.md" "$TASK_DIR/archive/handoff-$TIMESTAMP.md"
fi
```

### Step 3: Write the YAML Frontmatter

The handoff document must begin with metadata:

```yaml
---
task: <task-name>
from: ai-maestro-programmer-agent-main-agent
to: <receiving-agent-or-future-self>
created: <current-ISO-timestamp>
priority: <low|normal|high|urgent>
status: <backlog|pending|in_progress|review|completed>
---
```

Status values:
- `backlog`: Work is queued but not yet scheduled
- `pending`: Work has not started yet
- `in_progress`: Work is partially complete
- `review`: Work is done, awaiting review
- `completed`: All work is finished

### Step 4: Write the Task Summary

Provide a concise summary of the task:

```markdown
# <Task Title>

## Task Summary
<One paragraph describing what the task is about, what was accomplished, and what remains.>
```

### Step 5: Document Requirements and Progress

List all requirements with their completion status:

```markdown
## Requirements
1. [x] Parse YAML files using PyYAML library
2. [x] Validate against JSON schema
3. [ ] Return typed dataclass objects
4. [ ] Handle parsing errors gracefully

**Completed**: 2 of 4 requirements
**Remaining**: Requirements 3 and 4
```

### Step 6: Document Constraints

List any constraints that apply to the remaining work:

```markdown
## Constraints
- Must use existing error handling patterns in src/errors.py
- Must follow TDD approach (tests first)
- Maximum file size: 10MB
```

### Step 7: Provide Codebase Context

List relevant files and their purposes:

```markdown
## Codebase Context
- `src/parsers/yaml_parser.py` - Main implementation file (created)
- `tests/unit/test_yaml_parser.py` - Test file (8 tests, 5 passing)
- `src/schemas/config_schema.json` - Validation schema (existing)
- `src/models/config.py` - Output types (needs update)
```

### Step 8: Create the Checkpoints Section

Document the phase-based progress:

```markdown
## Checkpoints

**Task:** <task-name>
**Started:** <ISO-timestamp-when-work-began>
**Last Updated:** <current-ISO-timestamp>

### Phase Status
- Phase 1 (Tests Written): VALIDATED (8 tests defined)
- Phase 2 (Implementation): IN_PROGRESS (started <timestamp>)
- Phase 3 (Refactoring): PENDING
- Phase 4 (Documentation): PENDING

### Validation State
```json
{
  "test_count": 8,
  "tests_passing": 5,
  "files_modified": ["src/parsers/yaml_parser.py", "tests/unit/test_yaml_parser.py"],
  "last_test_command": "uv run pytest tests/unit/test_yaml_parser.py -v",
  "last_test_exit_code": 1
}
```

### Resume Context
- Current focus: <exact step within current phase>
- Next action: <what should be done next>
- Blockers: <any blockers, or "None">
```

### Step 9: Add Notes and Decisions

Document any important decisions or observations:

```markdown
## Notes

### Decisions Made
1. Used `ruamel.yaml` instead of `PyYAML` for better comment preservation
2. Chose to validate lazily rather than eagerly for performance

### Observations
- The existing JSON parser has a bug in error handling (see bugs/bug-001.md)
- The schema file is missing documentation for the `metadata` field

### Open Questions
- Should we support YAML 1.2 or stick with 1.1?
- How should we handle circular references?
```

### Step 10: Write the File

Save the complete handoff document:

```bash
cat > "$TASK_DIR/current.md" << 'EOF'
<complete handoff document content>
EOF
```

### Step 11: Notify the Receiving Agent

Send a notification to the receiving agent using the `agent-messaging` skill:
- **Recipient**: the receiving agent's session name
- **Subject**: "Handoff ready: [task-name]"
- **Content**: include the handoff document file path, the current status, and a brief summary of the work state
- **Type**: handoff
- **Priority**: match the priority from the handoff document frontmatter

**Verify**: confirm the handoff notification appears in your sent messages.

## Checklist

Complete these items when creating a handoff document:

- [ ] Created task directory at `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/<task>/`
- [ ] Archived previous handoff if one existed
- [ ] Wrote YAML frontmatter with task, from, to, created, priority, status
- [ ] Wrote task summary paragraph
- [ ] Listed all requirements with completion checkboxes
- [ ] Documented constraints for remaining work
- [ ] Listed codebase context with file purposes
- [ ] Created checkpoints section with phase status
- [ ] Included validation state JSON with test counts and commands
- [ ] Wrote resume context with current focus, next action, blockers
- [ ] Added notes section with decisions, observations, open questions
- [ ] Saved file to `<task-dir>/current.md`
- [ ] Sent notification to receiving agent via AI Maestro

## Examples

### Example 1: Handoff for Completed Work

```markdown
---
task: implement-yaml-parser
from: ai-maestro-programmer-agent-main-agent
to: amoa-orchestrator-main-agent
created: 2025-02-06T15:30:00Z
priority: high
status: completed
---

# Implement YAML Parser

## Task Summary
Implemented a YAML configuration parser with schema validation. All requirements met, all tests passing, code reviewed and documented.

## Requirements
1. [x] Parse YAML files using PyYAML library
2. [x] Validate against JSON schema
3. [x] Return typed dataclass objects
4. [x] Handle parsing errors gracefully

**Completed**: 4 of 4 requirements

## Codebase Context
- `src/parsers/yaml_parser.py` - Main implementation (247 lines)
- `tests/unit/test_yaml_parser.py` - Test file (15 tests, all passing)
- `src/models/config.py` - Updated with new dataclasses

## Checkpoints

### Phase Status
- Phase 1 (Tests Written): VALIDATED
- Phase 2 (Implementation): VALIDATED
- Phase 3 (Refactoring): VALIDATED
- Phase 4 (Documentation): VALIDATED

### Validation State
```json
{
  "test_count": 15,
  "tests_passing": 15,
  "last_test_command": "uv run pytest tests/unit/test_yaml_parser.py -v",
  "last_test_exit_code": 0
}
```

## Notes

### Decisions Made
1. Used jsonschema library for validation (already a project dependency)
2. Created custom exceptions YamlParseError and SchemaValidationError
```

### Example 2: Handoff for Blocked Work

```markdown
---
task: integrate-external-api
from: ai-maestro-programmer-agent-main-agent
to: amoa-orchestrator-main-agent
created: 2025-02-06T16:00:00Z
priority: urgent
status: blocked
---

# Integrate External API

## Task Summary
Attempted to integrate the payment processing API. Implementation is blocked waiting for API credentials and endpoint documentation.

## Requirements
1. [x] Create API client class structure
2. [ ] Implement authentication flow
3. [ ] Add payment processing methods
4. [ ] Write integration tests

**Completed**: 1 of 4 requirements
**Blocked on**: Requirements 2, 3, 4

## Blockers

### BLOCKER-1: Missing API Credentials
- **Description**: No API key or secret available for the payment provider
- **Impact**: Cannot test authentication or any API calls
- **Resolution needed**: Obtain credentials from payment provider dashboard

### BLOCKER-2: Missing Endpoint Documentation
- **Description**: The API documentation link in the requirements returns 404
- **Impact**: Cannot implement payment processing methods
- **Resolution needed**: Get updated documentation URL or PDF

## Checkpoints

### Phase Status
- Phase 1 (Tests Written): PARTIAL (structure only, no assertions)
- Phase 2 (Implementation): BLOCKED

### Resume Context
- Current focus: Waiting for blockers to be resolved
- Next action: Once credentials available, implement auth flow
- Blockers: See BLOCKER-1 and BLOCKER-2 above
```

## Error Handling

### Error: Cannot Write to Handoff Directory

**Symptom**: File write operations fail with permission denied.

**Cause**: The handoff directory does not exist or lacks write permissions.

**Resolution**:
1. Check if parent directory exists: `ls -la $CLAUDE_PROJECT_DIR/thoughts/shared/`
2. Create the directory structure: `mkdir -p $CLAUDE_PROJECT_DIR/thoughts/shared/handoffs`
3. Verify write permissions
4. If running in a sandboxed environment, request the user to create the directory

### Error: AI Maestro Not Responding

**Symptom**: The messaging send operation fails or times out.

**Cause**: AI Maestro service is not running or the messaging is not configured.

**Resolution**:
1. Use the `agent-messaging` skill's status check operation to verify the messaging service is running
2. Verify your messaging identity is initialized following the `agent-messaging` skill's instructions
3. If AI Maestro is down, document in the handoff that notification was not sent
4. The receiving agent can poll the handoff directory instead of waiting for notification

### Error: Conflicting Handoff Already Exists

**Symptom**: Another agent is actively working on the same task.

**Cause**: Two agents were assigned the same task, or the previous handoff was not properly archived.

**Resolution**:
1. Check the existing handoff's `from` field to identify the other agent
2. Send a message to that agent to coordinate
3. If the other agent is no longer active, archive their handoff and create yours
4. Ensure task names are unique to prevent future conflicts

### Error: Large Handoff Document

**Symptom**: The handoff document exceeds reasonable size (more than 500 lines).

**Cause**: Too much detail is being included in the handoff.

**Resolution**:
1. Move detailed technical notes to separate reference files
2. Keep the handoff focused on status, requirements, and resume context
3. Link to external documents for deep technical details
4. Consider if some content belongs in bug reports or documentation instead
