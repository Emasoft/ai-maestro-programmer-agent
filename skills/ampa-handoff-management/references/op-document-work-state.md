---
name: op-document-work-state
description: Save work state for later continuation
parent-skill: ampa-handoff-management
---

# Document Work State

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Checklist](#checklist)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

This operation explains how to save the current work state so that work can be resumed after a session clear or interruption.

## When to Use

Use this operation when:

1. **Context is running low**: The conversation is about to be compacted
2. **Taking a break**: Work will continue in a future session
3. **Reaching a checkpoint**: A natural pause point in the work
4. **Before risky operations**: Saving state before attempting something that might fail
5. **Periodically during long tasks**: Every 30-60 minutes of active work

Do NOT use this operation when:
- Work is complete (use Create Handoff Document instead)
- Handing off to another agent (use Create Handoff Document instead)
- Just reporting a bug (use Write Bug Report instead)
- The work is trivial and easily restartable

## Prerequisites

Before documenting work state:

1. **Tests should be runnable**: Know the command to verify current state
2. **Changes should be saved**: Ensure edited files are written to disk
3. **Handoff directory must exist**: `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/`

## Procedure

### Step 1: Prepare the Handoff Directory

Ensure the task-specific handoff directory exists:

```bash
HANDOFF_DIR="$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs"
TASK_NAME="<current-task-name>"
TASK_DIR="$HANDOFF_DIR/$TASK_NAME"

mkdir -p "$TASK_DIR/archive"
```

### Step 2: Run Current Validation

Execute the test command to capture current state:

```bash
TEST_COMMAND="uv run pytest tests/unit/test_feature.py -v"
TEST_OUTPUT=$($TEST_COMMAND 2>&1)
TEST_EXIT_CODE=$?

# Count passing tests
TESTS_PASSING=$(echo "$TEST_OUTPUT" | grep -c "PASSED")
TESTS_FAILING=$(echo "$TEST_OUTPUT" | grep -c "FAILED")
TESTS_TOTAL=$((TESTS_PASSING + TESTS_FAILING))
```

### Step 3: Capture Modified Files

List files that have been modified:

```bash
# If in a git repository
MODIFIED_FILES=$(git diff --name-only 2>/dev/null || echo "Not in git repo")

# Or track manually
MODIFIED_FILES="src/feature.py, tests/test_feature.py"
```

### Step 4: Archive Previous State (If Exists)

If a `current.md` already exists, archive it:

```bash
if [ -f "$TASK_DIR/current.md" ]; then
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    mv "$TASK_DIR/current.md" "$TASK_DIR/archive/state-$TIMESTAMP.md"
fi
```

### Step 5: Write the Work State Document

Create the work state document with all necessary context:

```markdown
---
task: <task-name>
from: ai-maestro-programmer-agent-main-agent
to: ai-maestro-programmer-agent-main-agent
created: <current-ISO-timestamp>
priority: <current-priority>
status: in-progress
state-type: work-state
---

# <Task Title> - Work State

## Task Summary
<Brief reminder of what this task is about.>

## Current Progress

### Requirements Status
1. [x] <Completed requirement>
2. [x] <Completed requirement>
3. [ ] <In-progress requirement> <- CURRENT
4. [ ] <Pending requirement>

### Phase Status
- Phase 1 (Tests Written): VALIDATED
- Phase 2 (Implementation): IN_PROGRESS
- Phase 3 (Refactoring): PENDING

## Checkpoints

**Last Updated:** <current-ISO-timestamp>

### Validation State
```json
{
  "test_count": <total>,
  "tests_passing": <passing>,
  "tests_failing": <failing>,
  "files_modified": [<list-of-files>],
  "last_test_command": "<test-command>",
  "last_test_exit_code": <exit-code>
}
```

### Resume Context
- **Current focus**: <exact step or function being worked on>
- **Next action**: <specific next thing to do>
- **Blockers**: <any blockers, or "None">

### In-Progress Code

<If there is partially written code, include it here with notes:>

```python
# File: src/feature.py
# Function: parse_config (lines 45-60)
# Status: Partially implemented, missing error handling

def parse_config(path: str) -> Config:
    with open(path) as f:
        data = yaml.safe_load(f)
    # TODO: Add validation
    # TODO: Add error handling for invalid YAML
    return Config(**data)
```

### Mental Context

<Capture your current understanding and thought process:>

1. **Why this approach**: <reason for current implementation approach>
2. **Alternatives considered**: <other approaches and why rejected>
3. **Key insight**: <important realization that should not be forgotten>
4. **Gotcha to remember**: <tricky aspect that might be forgotten>

## Codebase State

### Modified Files
| File | Status | Notes |
|------|--------|-------|
| `src/feature.py` | In progress | Missing error handling |
| `tests/test_feature.py` | Complete | 8 tests defined |
| `src/models.py` | Complete | Added Config dataclass |

### Uncommitted Changes
```
<output of git status or equivalent>
```

## Notes

<Any additional context that would help resume work:>

- <Note 1>
- <Note 2>
```

### Step 6: Save the Work State

Write the complete work state to the file:

```bash
cat > "$TASK_DIR/current.md" << 'EOF'
<complete work state content>
EOF

echo "Work state saved: $TASK_DIR/current.md"
```

### Step 7: Verify the Save

Confirm the file was written correctly:

```bash
if [ -f "$TASK_DIR/current.md" ]; then
    echo "Work state saved successfully"
    head -20 "$TASK_DIR/current.md"
else
    echo "ERROR: Failed to save work state"
fi
```

## Checklist

Complete these items when documenting work state:

- [ ] Ensured all file edits are saved to disk
- [ ] Created task directory if it did not exist
- [ ] Ran current test command and captured results
- [ ] Noted test count, passing, and failing counts
- [ ] Listed all modified files with their status
- [ ] Archived previous work state if one existed
- [ ] Wrote YAML frontmatter with state-type: work-state
- [ ] Documented current requirements progress with checkboxes
- [ ] Documented current phase status
- [ ] Created validation state JSON with test command and exit code
- [ ] Wrote resume context with current focus and next action
- [ ] Included any partially written code with TODO markers
- [ ] Captured mental context (approach reasoning, alternatives, insights)
- [ ] Listed codebase state with modified files table
- [ ] Added any notes that would help resume work
- [ ] Verified the file was saved successfully

## Examples

### Example 1: Mid-Implementation Work State

```markdown
---
task: implement-yaml-parser
from: ai-maestro-programmer-agent-main-agent
to: ai-maestro-programmer-agent-main-agent
created: 2025-02-06T14:45:00Z
priority: high
status: in-progress
state-type: work-state
---

# Implement YAML Parser - Work State

## Task Summary
Implementing a YAML configuration parser with schema validation per AMOA delegation.

## Current Progress

### Requirements Status
1. [x] Parse YAML files using PyYAML library
2. [ ] Validate against JSON schema <- CURRENT
3. [ ] Return typed dataclass objects
4. [ ] Handle parsing errors gracefully

### Phase Status
- Phase 1 (Tests Written): VALIDATED
- Phase 2 (Implementation): IN_PROGRESS (requirement 2)
- Phase 3 (Refactoring): PENDING

## Checkpoints

**Last Updated:** 2025-02-06T14:45:00Z

### Validation State
```json
{
  "test_count": 12,
  "tests_passing": 5,
  "tests_failing": 7,
  "files_modified": ["src/parsers/yaml_parser.py", "tests/unit/test_yaml_parser.py"],
  "last_test_command": "uv run pytest tests/unit/test_yaml_parser.py -v",
  "last_test_exit_code": 1
}
```

### Resume Context
- **Current focus**: Implementing `validate_against_schema()` function
- **Next action**: Add jsonschema validation logic to the function stub
- **Blockers**: None

### In-Progress Code

```python
# File: src/parsers/yaml_parser.py
# Function: validate_against_schema (lines 55-65)
# Status: Stub only, no implementation yet

def validate_against_schema(data: dict, schema_path: str) -> bool:
    """Validate parsed YAML data against a JSON schema.

    Args:
        data: Parsed YAML as a dictionary
        schema_path: Path to JSON schema file

    Returns:
        True if valid, raises SchemaValidationError if not
    """
    # TODO: Load schema from schema_path
    # TODO: Use jsonschema.validate()
    # TODO: Catch jsonschema.ValidationError and wrap in SchemaValidationError
    pass
```

### Mental Context

1. **Why this approach**: Using jsonschema library because it is already a project dependency
2. **Alternatives considered**: Manual validation, but jsonschema is more robust
3. **Key insight**: The schema file uses draft-07, must specify this in validator
4. **Gotcha to remember**: Schema path is relative to project root, not caller location

## Codebase State

### Modified Files
| File | Status | Notes |
|------|--------|-------|
| `src/parsers/yaml_parser.py` | In progress | validate_against_schema is a stub |
| `tests/unit/test_yaml_parser.py` | Complete | 12 tests, 7 waiting for implementation |
| `src/errors.py` | Complete | Added SchemaValidationError |

## Notes

- The existing JSON parser in `src/parsers/json_parser.py` has a similar validation function that can be referenced
- Schema file is at `src/schemas/config_schema.json`
- Remember to handle FileNotFoundError for missing schema files
```

### Example 2: Work State Before Risky Change

```markdown
---
task: refactor-config-loader
from: ai-maestro-programmer-agent-main-agent
to: ai-maestro-programmer-agent-main-agent
created: 2025-02-06T16:30:00Z
priority: normal
status: in-progress
state-type: work-state
---

# Refactor Config Loader - Work State

## Task Summary
Refactoring the config loader to support multiple file formats. About to make a significant architectural change.

## Current Progress

### Requirements Status
1. [x] Abstract base class for loaders
2. [x] YAML loader implementation
3. [x] JSON loader implementation
4. [ ] TOML loader implementation <- NEXT
5. [ ] Factory pattern for loader selection <- ABOUT TO CHANGE

### Phase Status
- Phase 1 (Tests Written): VALIDATED
- Phase 2 (Implementation): VALIDATED (requirements 1-3)
- Phase 3 (Refactoring): IN_PROGRESS

## Checkpoints

**Last Updated:** 2025-02-06T16:30:00Z

### Validation State
```json
{
  "test_count": 24,
  "tests_passing": 24,
  "tests_failing": 0,
  "files_modified": ["src/loaders/base.py", "src/loaders/yaml_loader.py", "src/loaders/json_loader.py"],
  "last_test_command": "uv run pytest tests/unit/test_loaders.py -v",
  "last_test_exit_code": 0
}
```

### Resume Context
- **Current focus**: About to implement loader factory pattern
- **Next action**: Create LoaderFactory class in src/loaders/factory.py
- **Blockers**: None

### IMPORTANT: State Before Change

All 24 tests are currently passing. About to make significant changes to how loaders are instantiated. If this breaks things, revert to this commit:

```
Current HEAD: abc123def (all tests green)
```

### Mental Context

1. **Why this approach**: Factory pattern allows runtime loader selection by file extension
2. **Alternatives considered**: Registry pattern, but factory is simpler for this use case
3. **Key insight**: Loaders should be lazy-loaded to avoid importing all dependencies upfront
4. **Gotcha to remember**: The TOML loader needs tomllib (Python 3.11+) or tomli fallback

## Notes

- SAVING STATE BEFORE RISKY CHANGE
- If the factory implementation breaks things, can restore from current state
- All tests passing, code is in a known good state
```

## Error Handling

### Error: Tests Cannot Be Run

**Symptom**: The test command fails to execute or has missing dependencies.

**Resolution**:
1. Document the last known test state in the work state
2. Note that tests could not be run and why
3. Include the error message from the failed test command
4. The resume session should fix the test environment before continuing

### Error: Cannot Determine Current Focus

**Symptom**: Work was interrupted abruptly and it is unclear what was being worked on.

**Resolution**:
1. Check the most recently modified files to infer current focus
2. Look for TODO comments or incomplete code
3. Check terminal history for recent commands
4. Document best guess with a note that it is uncertain
5. Include more context in the Mental Context section

### Error: Work State Too Large

**Symptom**: The work state document is becoming unwieldy (more than 300 lines).

**Resolution**:
1. Move detailed code snippets to separate files in the task directory
2. Summarize rather than include full code
3. Focus on what is needed to resume, not full history
4. Archive older state versions to keep current.md focused

### Error: Conflicting Work States

**Symptom**: Multiple work state files exist for the same task from different sessions.

**Resolution**:
1. The archive directory should contain older states
2. Only one `current.md` should exist at a time
3. If conflicts exist, merge the most recent information
4. Ensure archiving is happening correctly in future saves
5. Add timestamps to distinguish which is more recent
