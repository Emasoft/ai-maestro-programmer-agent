---
name: ampa-handoff-management
description: Create and receive handoff documents for context transfer. Use when transferring work, resuming sessions, or filing bug reports. Trigger with /ampa-handoff.
license: MIT
compatibility: Requires AI Maestro running.
metadata:
  author: AI Maestro
  version: 1.0.0
  workflow-instruction: "support"
  procedure: "proc-handoff-management"
context: fork
agent: ampa-programmer-main-agent
user-invocable: false
---

# AMPA Handoff Management Skill

## Overview

AMPA is an **implementer** agent. This skill handles context transfer between implementer sessions.

This skill enables the AI Maestro Programmer Agent (AMPA) to create and receive handoff documents for seamless context transfer between agents and sessions. Handoff documents are structured Markdown files with YAML frontmatter that capture work state, task context, bug reports, and checkpoint data. The AMPA uses this skill whenever it receives delegated work from the AI Maestro Orchestrator Agent (AMOA), needs to pass completed work to the AI Maestro Integrator Agent (AMIA), discovers bugs during implementation, or must save progress before a session ends. All handoff documents are stored under `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/` in a standardized directory structure that all agents in the ecosystem can read.

## Prerequisites

Before using this skill, ensure the following conditions are met:
1. **AI Maestro must be running** on `localhost:23000` for inter-agent messaging notifications when handoffs are created or received.
2. **The handoff directory must exist** at `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/`. Create it with `mkdir -p "$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/"` if it does not exist.
3. **The AMPA agent must have a valid session name** registered with AI Maestro (format: `ampa-<project>-<instance>`), so that handoff notifications reach the correct recipient.
4. **The `$CLAUDE_PROJECT_DIR` environment variable must be set** to the root of the project directory. This variable is set automatically by Claude Code when a project is loaded.
5. **Read access to the references directory** at `references/` relative to this skill, which contains the detailed operation guides for each handoff operation.

## Instructions

Follow these numbered steps when performing handoff management:

1. **Determine the handoff operation needed.** Consult the Quick Reference table at the bottom of this document to match your current situation to the correct operation (Read, Create, Write Bug Report, or Document Work State).
2. **Read the corresponding operation reference file.** Each operation has a dedicated guide in the `references/` directory. Read the full guide before proceeding.
3. **Verify the handoff directory exists.** Run `mkdir -p "$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/ampa-<task-name>/"` to ensure the task-specific subdirectory is available.
4. **Execute the operation.** Follow the step-by-step procedure in the reference file. All handoff documents must include YAML frontmatter with fields: `type`, `from`, `to`, `task`, `created`, `priority`, and `status`.
5. **Validate the handoff document.** After writing, re-read the document to confirm all required fields are present and the content accurately reflects the current work state.
6. **Send notification via AI Maestro.** After creating or updating a handoff, send a message to the receiving agent using `curl -X POST "http://localhost:23000/api/messages"` with the handoff file path in the message body.
7. **Archive previous versions.** If updating an existing handoff, move the previous `current.md` to the `archive/` subdirectory with a timestamp suffix before writing the new version.

## Purpose

Handoff documents preserve work state across:
- Agent transitions (when AMOA delegates to AMPA)
- Session boundaries (when context is cleared)
- Bug discoveries (structured reporting)
- Work interruptions (save and resume)

## Operations

This skill provides four core operations for handoff management:

### 1. Read Handoff Document
**File**: [op-read-handoff-document.md](references/op-read-handoff-document.md)

**Contents**:
- 1.1 When to read a handoff document
- 1.2 Parsing handoff YAML frontmatter
- 1.3 Extracting task context and requirements
- 1.4 Identifying delegated work items
- 1.5 Resuming from checkpoints

Use this operation when receiving work from AMOA or resuming from a previous session.

### 2. Create Handoff Document
**File**: [op-create-handoff-document.md](references/op-create-handoff-document.md)

**Contents**:
- 2.1 When to create a handoff document
- 2.2 Handoff document structure and format
- 2.3 Capturing current work state
- 2.4 Documenting completed and pending items
- 2.5 Writing to the handoff directory

Use this operation when transferring work to another agent or ending a session.

### 3. Write Bug Report
**File**: [op-write-bug-report.md](references/op-write-bug-report.md)

**Contents**:
- 3.1 When to write a bug report
- 3.2 Bug report structure and required fields
- 3.3 Capturing reproduction steps
- 3.4 Documenting expected versus actual behavior
- 3.5 Linking to related code and tests

Use this operation when discovering bugs during implementation work.

### 4. Document Work State
**File**: [op-document-work-state.md](references/op-document-work-state.md)

**Contents**:
- 4.1 When to document work state
- 4.2 Work state document structure
- 4.3 Capturing in-progress changes
- 4.4 Recording decision context
- 4.5 Enabling session resume

Use this operation to save current work for later continuation.

## Handoff Directory Structure

All handoff documents are stored in a standardized location:

```
$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/
├── ampa-<task-name>/
│   ├── current.md           # Active handoff document
│   ├── archive/             # Previous handoff versions
│   └── bugs/                # Bug reports for this task
```

## Integration with AI Maestro

This skill integrates with AI Maestro for inter-agent messaging:
- Handoff creation triggers notification to receiving agent
- Bug reports can be escalated to AMOA for triage
- Work state documents enable checkpoint-based resume

## Quick Reference

| Situation | Operation to Use |
|-----------|------------------|
| Received delegation from AMOA | Read Handoff Document |
| Completing work, passing to next agent | Create Handoff Document |
| Found a bug during implementation | Write Bug Report |
| Need to pause work for later | Document Work State |
| Resuming after context clear | Read Handoff Document |

## Output

This skill produces the following artifacts:
- **Handoff documents** (`current.md`): Markdown files with YAML frontmatter stored at `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/ampa-<task-name>/current.md`. Contains task context, completed items, pending items, checkpoint state, and file references.
- **Bug reports** (`bugs/<bug-id>.md`): Structured bug reports stored in the `bugs/` subdirectory of the task handoff folder. Each report includes reproduction steps, expected versus actual behavior, code references, and severity classification.
- **Archived handoffs** (`archive/<timestamp>-current.md`): Previous versions of handoff documents preserved with timestamp prefixes for audit trail and rollback capability.
- **AI Maestro notifications**: JSON messages sent to the receiving agent via the AI Maestro API confirming that a handoff document has been created or updated.

## Checklist

Copy this checklist and track your progress:

- [ ] Determine handoff operation needed (Read, Create, Bug Report, or Document Work State)
- [ ] Read the corresponding operation reference file
- [ ] Verify handoff directory exists
- [ ] Execute the handoff operation
- [ ] Validate the handoff document (all required YAML fields present)
- [ ] Send notification via AI Maestro to receiving agent
- [ ] Archive previous version if updating an existing handoff

## Error Handling

Common errors encountered during handoff management and their resolutions:

| Error | Cause | Resolution |
|-------|-------|------------|
| Handoff directory does not exist | `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/` was never created | Run `mkdir -p "$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/ampa-<task-name>/"` to create it |
| AI Maestro notification fails | AI Maestro is not running on `localhost:23000` | Verify AI Maestro is running with `curl -s "http://localhost:23000/api/health"`. If it returns an error, start AI Maestro before retrying |
| YAML frontmatter parse error | Missing `---` delimiters or invalid YAML syntax in the handoff document | Re-read the handoff document and ensure the frontmatter starts and ends with `---` on its own line, and all values are properly quoted if they contain special characters |
| Receiving agent not found | The `to` field in the handoff references an agent session name that is not registered with AI Maestro | Check the team registry at `.ai-maestro/team-registry.json` for valid agent session names, or ask AMOA for the correct recipient |
| Handoff document is stale | A `current.md` already exists from a previous task iteration | Archive the existing document by moving it to `archive/` with a timestamp suffix, then create the new handoff as `current.md` |

## Examples

### Example 1: Creating a handoff after completing implementation

The AMPA has finished implementing a feature and needs to pass it to AMIA for code review:

```markdown
---
type: handoff
from: ampa-svgbbox-programmer-001
to: amia-svgbbox-reviewer
task: implement-bbox-calculation
timestamp: 2026-02-14T10:30:00Z
status: implementation-complete
---

# Handoff: implement-bbox-calculation

## Completed Items
- Implemented `calculate_bbox()` function in `src/bbox/calculator.py`
- Added unit tests in `tests/unit/test_calculator.py` (12 tests, all passing)
- Updated type annotations and docstrings

## Files Modified
- `src/bbox/calculator.py` (new file, 145 lines)
- `tests/unit/test_calculator.py` (new file, 210 lines)

## Pending Items
- Code review by AMIA
- Integration test with SVG parser module

## Notes
- Used numpy for matrix operations as specified in architecture doc
- Edge case: zero-dimension bounding boxes return empty BBox object (see test_empty_bbox)
```

After writing this to `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/ampa-implement-bbox-calculation/current.md`, send a notification:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to": "amia-svgbbox-reviewer", "subject": "Handoff ready: implement-bbox-calculation", "priority": "normal", "content": {"type": "handoff", "message": "Implementation complete. Handoff at thoughts/shared/handoffs/ampa-implement-bbox-calculation/current.md"}}'
```

### Example 2: Receiving a delegation handoff from AMOA

The AMPA receives a message from AMOA with a task delegation. The first step is to read the handoff:

```bash
# 1. Read the handoff document
cat "$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/amoa-refactor-parser/current.md"

# 2. Extract key fields from YAML frontmatter
# Look for: task, requirements, deadline, dependencies, checkpoint (if resuming)

# 3. Acknowledge receipt via AI Maestro
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to": "amoa-svgbbox-orchestrator", "subject": "Handoff received: refactor-parser", "priority": "normal", "content": {"type": "acknowledgment", "message": "AMPA received handoff for refactor-parser. Starting work."}}'
```

### Example 3: Writing a bug report discovered during implementation

While working on a feature, the AMPA discovers a bug in an existing module:

```markdown
---
type: bug-report
from: ampa-svgbbox-programmer-001
task: implement-bbox-calculation
bug-id: BUG-2026-0214-001
severity: high
timestamp: 2026-02-14T11:15:00Z
---

# Bug Report: SVG path parser returns incorrect coordinates for arc commands

## Reproduction Steps
1. Load `tests/fixtures/arc-path.svg`
2. Call `parse_path(svg_content)` from `src/parser/path_parser.py`
3. Inspect the returned coordinate list for arc (`A`) commands

## Expected Behavior
Arc command coordinates should be absolute after conversion from relative coordinates.

## Actual Behavior
Arc commands retain relative coordinates, causing bbox calculation to be offset by the current pen position.

## Affected Code
- `src/parser/path_parser.py`, function `_parse_arc_command()`, line 87-102

## Related Tests
- `tests/unit/test_path_parser.py::test_arc_absolute_coords` (currently failing)
```

Save this to `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/ampa-implement-bbox-calculation/bugs/BUG-2026-0214-001.md` and escalate to AMOA for triage.

## Resources

Related skills, documents, and tools for handoff management:

- **[op-read-handoff-document.md](references/op-read-handoff-document.md)** -- Detailed guide for parsing and processing incoming handoff documents
- **[op-create-handoff-document.md](references/op-create-handoff-document.md)** -- Detailed guide for creating outgoing handoff documents with proper structure
- **[op-write-bug-report.md](references/op-write-bug-report.md)** -- Detailed guide for structured bug reporting during implementation
- **[op-document-work-state.md](references/op-document-work-state.md)** -- Detailed guide for capturing in-progress work state for session resume
- **AI Maestro messaging API** -- Used for sending handoff notifications between agents (`http://localhost:23000/api/messages`)
- **Team Registry** (`.ai-maestro/team-registry.json`) -- Contains valid agent session names needed for the `to` field in handoff documents
- **AMOA Orchestrator Agent** -- The primary source of task delegations and the escalation target for bug reports
- **AMIA Integrator Agent** -- The primary recipient of implementation-complete handoffs for code review
