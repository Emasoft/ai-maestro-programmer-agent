---
name: op-read-handoff-document
description: Parse and process incoming handoff documents
parent-skill: ampa-handoff-management
---

# Read Handoff Document

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Checklist](#checklist)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

This operation explains how to parse and process handoff documents to understand delegated work and resume from checkpoints.

## When to Use

Use this operation when:

1. **Receiving delegation from AMOA**: The AI Maestro Orchestrator Agent has assigned you a task via a handoff document
2. **Resuming a session**: You need to continue work from a previous session that was interrupted
3. **Taking over from another agent**: Another programmer agent has passed work to you
4. **Context was cleared**: The conversation was compacted and you need to restore work state

Do NOT use this operation when:
- Starting fresh work with no prior context
- The task is fully described in the user prompt without a handoff file

## Prerequisites

Before reading a handoff document:

1. **AI Maestro must be running**: The messaging system enables handoff notifications
2. **Handoff directory must exist**: Check `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/`
3. **You must know the task name**: Either from the delegation message or resume instruction

## Procedure

### Step 1: Locate the Handoff Document

The handoff document is stored at a predictable path based on the task name:

```bash
HANDOFF_DIR="$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs"
TASK_NAME="<task-name-from-delegation>"
HANDOFF_FILE="$HANDOFF_DIR/$TASK_NAME/current.md"
```

If you received a delegation via AI Maestro, the message will contain the exact path.

### Step 2: Verify the Document Exists

Before attempting to read:

```bash
if [ -f "$HANDOFF_FILE" ]; then
    echo "Handoff document found"
else
    echo "ERROR: No handoff document at $HANDOFF_FILE"
    # Request clarification from delegating agent
fi
```

### Step 3: Parse the YAML Frontmatter

The handoff document begins with YAML frontmatter containing metadata:

```yaml
---
task: <task-name>
from: <delegating-agent>
to: <receiving-agent>
created: <ISO-timestamp>
priority: <low|normal|high|urgent>
status: <pending|in-progress|blocked|completed>
---
```

Extract these fields to understand the delegation context.

### Step 4: Read the Task Description

After the frontmatter, the document contains:

1. **Task Summary**: One paragraph explaining what needs to be done
2. **Requirements**: Numbered list of specific requirements
3. **Constraints**: Any limitations or rules to follow
4. **Codebase Context**: Relevant paths and file references

### Step 5: Check for Checkpoints

If resuming work, look for the `## Checkpoints` section:

```markdown
## Checkpoints

### Phase Status
- Phase 1 (Tests Written): VALIDATED (15 tests passing)
- Phase 2 (Implementation): IN_PROGRESS (started 2025-12-31T14:00:00Z)
- Phase 3 (Refactoring): PENDING

### Resume Context
- Current focus: Implementing the parse_config function
- Next action: Add validation for empty input
- Blockers: None
```

Resume from the `IN_PROGRESS` phase, not from the beginning.

### Step 6: Verify Validation State

If there is a `### Validation State` section with JSON:

```json
{
  "test_count": 15,
  "tests_passing": 15,
  "last_test_command": "uv run pytest tests/unit/test_feature.py -v",
  "last_test_exit_code": 0
}
```

Re-run the `last_test_command` to verify the checkpoint is still valid before continuing.

### Step 7: Acknowledge Receipt

After successfully reading the handoff, notify the delegating agent using the `agent-messaging` skill:
- **Recipient**: the delegating agent's session name (from the handoff's `from` field)
- **Subject**: "Handoff received: [task-name]"
- **Content**: confirm receipt, state which phase you are resuming from
- **Type**: acknowledgment
- **Priority**: normal

**Verify**: confirm the acknowledgment appears in your sent messages.

## Checklist

Complete these items when reading a handoff document:

- [ ] Located handoff file at `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/<task>/current.md`
- [ ] Verified file exists before reading
- [ ] Parsed YAML frontmatter for metadata (task, from, to, priority, status)
- [ ] Read task description, requirements, and constraints
- [ ] Identified codebase context and relevant file paths
- [ ] Checked for checkpoint section if resuming work
- [ ] Found last validated phase and current in-progress phase
- [ ] Re-ran validation command to verify checkpoint integrity
- [ ] Sent acknowledgment message to delegating agent via AI Maestro

## Examples

### Example 1: Reading a Fresh Delegation

The handoff document at `thoughts/shared/handoffs/implement-parser/current.md`:

```markdown
---
task: implement-parser
from: amoa-orchestrator-main-agent
to: ai-maestro-programmer-agent-main-agent
created: 2025-02-06T10:00:00Z
priority: high
status: pending
---

# Implement Config Parser

## Task Summary
Implement a configuration file parser that reads YAML files and validates them against a schema.

## Requirements
1. Parse YAML files using PyYAML library
2. Validate against JSON schema
3. Return typed dataclass objects
4. Handle parsing errors gracefully

## Constraints
- Must use existing error handling patterns in src/errors.py
- Must follow TDD approach (tests first)
- Maximum file size: 10MB

## Codebase Context
- Schema location: src/schemas/config_schema.json
- Output types: src/models/config.py
- Existing parser reference: src/parsers/json_parser.py
```

After reading this, you would:
1. Note this is a fresh task (status: pending, no checkpoints)
2. Understand the four requirements
3. Check the codebase paths mentioned
4. Begin with writing tests (TDD approach per constraints)

### Example 2: Resuming from Checkpoint

The handoff document contains a checkpoint section:

```markdown
## Checkpoints

### Phase Status
- Phase 1 (Tests Written): VALIDATED
- Phase 2 (Implementation): IN_PROGRESS
- Phase 3 (Refactoring): PENDING

### Validation State
```json
{
  "test_count": 8,
  "tests_passing": 5,
  "last_test_command": "uv run pytest tests/unit/test_parser.py -v",
  "last_test_exit_code": 1
}
```

### Resume Context
- Current focus: parse_yaml function
- Next action: Fix handling of nested dictionaries
- Blockers: None
```

After reading this, you would:
1. Skip Phase 1 (already validated)
2. Resume Phase 2 implementation
3. Run the test command to see current state
4. Focus on the nested dictionary handling issue
5. NOT re-implement already passing tests

## Error Handling

### Error: Handoff File Not Found

**Symptom**: The expected handoff file does not exist at the specified path.

**Cause**: The delegating agent may not have created the handoff yet, or the path is incorrect.

**Resolution**:
1. Check if the handoffs directory exists: `ls -la $CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/`
2. Look for similarly named task directories
3. Send a message to the delegating agent requesting the handoff location
4. If delegating agent is unavailable, ask the user for task details

### Error: Invalid YAML Frontmatter

**Symptom**: The YAML parser fails when reading the frontmatter.

**Cause**: Malformed YAML syntax in the handoff document.

**Resolution**:
1. Read the raw file content to inspect the frontmatter
2. Look for common issues: missing colons, incorrect indentation, unquoted special characters
3. If possible, fix the syntax and continue
4. If the document is severely corrupted, request a new handoff from the delegating agent

### Error: Checkpoint Validation Fails

**Symptom**: Re-running the `last_test_command` produces different results than recorded.

**Cause**: The codebase changed since the checkpoint was created, or the checkpoint data is stale.

**Resolution**:
1. Compare current test output with the recorded `tests_passing` count
2. If more tests are failing now, investigate what changed
3. If tests are now passing that were previously failing, update the checkpoint
4. Consider starting the current phase from scratch if the state is too divergent
5. Document the discrepancy in the handoff before continuing

### Error: Missing Required Sections

**Symptom**: The handoff document is missing the task description, requirements, or constraints.

**Cause**: The delegating agent created an incomplete handoff.

**Resolution**:
1. Send a message to the delegating agent requesting the missing information
2. Check if there is an archived version with more complete information
3. If the task is clear from context, proceed and document assumptions
4. Update the handoff document with the missing sections once clarified
