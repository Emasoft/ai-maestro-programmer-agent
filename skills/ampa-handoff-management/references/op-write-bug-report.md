---
name: op-write-bug-report
description: Document bugs with reproduction steps
parent-skill: ampa-handoff-management
---

# Write Bug Report

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Checklist](#checklist)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

This operation explains how to document bugs discovered during implementation work with proper reproduction steps, expected versus actual behavior, and relevant context.

## When to Use

Use this operation when:

1. **You discover a bug during implementation**: The code does not behave as expected
2. **A test reveals unexpected behavior**: Tests fail for reasons other than your new code
3. **You find issues in existing code**: Pre-existing bugs in the codebase
4. **Edge cases cause failures**: Boundary conditions reveal problems
5. **Integration issues arise**: Components do not work together correctly

Do NOT use this operation when:
- Your own new code fails tests (that is normal TDD, fix it directly)
- You are documenting design decisions (use handoff notes instead)
- The issue is a missing feature (that is a requirement, not a bug)
- You are unsure if it is actually a bug (investigate first)

## Prerequisites

Before writing a bug report:

1. **Reproduce the bug**: You must be able to trigger the bug reliably
2. **Understand the expected behavior**: Know what should happen
3. **Isolate the bug location**: Narrow down to specific file and function
4. **Check if already reported**: Look in the bugs directory for duplicates

## Procedure

### Step 1: Create the Bugs Directory

Ensure the bugs directory exists for the current task:

```bash
HANDOFF_DIR="$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs"
TASK_NAME="<current-task-name>"
BUGS_DIR="$HANDOFF_DIR/$TASK_NAME/bugs"

mkdir -p "$BUGS_DIR"
```

### Step 2: Generate a Bug ID

Create a unique bug identifier:

```bash
BUG_COUNT=$(ls -1 "$BUGS_DIR" 2>/dev/null | wc -l)
BUG_ID=$(printf "bug-%03d" $((BUG_COUNT + 1)))
BUG_FILE="$BUGS_DIR/$BUG_ID.md"
```

### Step 3: Write the Bug Report Header

Begin with YAML frontmatter:

```yaml
---
bug-id: <bug-id>
title: <short-descriptive-title>
severity: <critical|high|medium|low>
status: <new|confirmed|in-progress|fixed|wont-fix>
discovered-by: ai-maestro-programmer-agent-main-agent
discovered-date: <ISO-timestamp>
related-task: <task-name>
affected-files:
  - <file-path-1>
  - <file-path-2>
---
```

Severity levels:
- `critical`: System crash, data loss, security vulnerability
- `high`: Major feature broken, no workaround
- `medium`: Feature partially broken, workaround exists
- `low`: Minor issue, cosmetic, edge case only

### Step 4: Write the Summary

Provide a clear one-paragraph summary:

```markdown
# <Bug Title>

## Summary
<One paragraph describing what the bug is, where it occurs, and its impact. Be specific about the symptoms.>
```

### Step 5: Document Expected vs Actual Behavior

Clearly contrast what should happen versus what does happen:

```markdown
## Expected Behavior
<What the code should do according to requirements, documentation, or reasonable expectations.>

## Actual Behavior
<What the code actually does. Include error messages, incorrect outputs, or unexpected states.>
```

### Step 6: Write Reproduction Steps

Provide exact steps to reproduce the bug:

```markdown
## Reproduction Steps

1. <First step with exact commands or actions>
2. <Second step>
3. <Third step>
4. <Observe the bug>

**Environment:**
- Python version: <version>
- OS: <operating system>
- Relevant dependencies: <list with versions>
```

### Step 7: Include Minimal Reproduction Code

Provide the smallest code sample that triggers the bug:

```markdown
## Minimal Reproduction

```python
# Minimal code to reproduce the bug
from src.parsers.yaml_parser import parse_config

# This input triggers the bug
config = parse_config("invalid: [unclosed bracket")

# Expected: YamlParseError exception
# Actual: IndexError in line 47
```
```

### Step 8: Add Stack Trace or Error Output

Include the actual error message:

```markdown
## Error Output

```
Traceback (most recent call last):
  File "src/parsers/yaml_parser.py", line 47, in parse_config
    return tokens[current_index]
IndexError: list index out of range
```
```

### Step 9: Document Root Cause Analysis (If Known)

If you have identified the cause:

```markdown
## Root Cause Analysis

The bug occurs in `parse_config()` at line 47 of `yaml_parser.py`. The function assumes `tokens` always has at least one element after calling `tokenize()`, but when given malformed input, `tokenize()` returns an empty list.

The missing check is:
```python
if not tokens:
    raise YamlParseError("Empty or invalid YAML input")
```
```

### Step 10: Suggest a Fix (If Known)

Provide a proposed fix:

```markdown
## Proposed Fix

Add input validation before accessing tokens:

```python
def parse_config(yaml_string: str) -> Config:
    tokens = tokenize(yaml_string)
    if not tokens:
        raise YamlParseError("Empty or invalid YAML input")
    # ... rest of function
```

**Impact of fix:**
- Low risk, isolated change
- Requires adding test for empty input case
```

### Step 11: Link Related Items

Connect to related code, tests, and documentation:

```markdown
## Related Items

- **Source file**: `src/parsers/yaml_parser.py` (lines 40-55)
- **Related test**: `tests/unit/test_yaml_parser.py::test_parse_empty_input` (currently missing)
- **Documentation**: `docs/parser-design.md` (section 3.2 error handling)
- **Related bugs**: None found
```

### Step 12: Save the Bug Report

Write the complete bug report to the file:

```bash
cat > "$BUG_FILE" << 'EOF'
<complete bug report content>
EOF

echo "Bug report created: $BUG_FILE"
```

### Step 13: Update the Handoff Document

Add a reference to the bug in the current handoff:

```markdown
## Bugs Discovered
- bug-001: IndexError on empty YAML input (severity: medium) — see `bugs/bug-001.md`
```

The format for each bug entry in the handoff document is:

```
- <bug-id>: <short title> (severity: <level>) — see `bugs/<bug-id>.md`
```

This is a plain-text reference to the bug report file created in Step 12. Do not use Markdown links to the bugs directory -- just reference the filename so the reader knows where to look.

### Step 14: Notify If Critical

For critical or high severity bugs, notify the orchestrator immediately using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: "BUG [severity]: [bug title]"
- **Content**: describe that a critical/high bug was discovered, provide the bug title, and reference the bug report file path for details
- **Type**: bug-report
- **Priority**: urgent

**Verify**: confirm the bug notification was delivered.

Only send this notification for critical or high severity bugs. Medium and low severity bugs are documented in the handoff but do not require immediate notification.

## Checklist

Complete these items when writing a bug report:

- [ ] Verified the bug is reproducible (not a one-time fluke)
- [ ] Checked for duplicate bug reports in the bugs directory
- [ ] Created bugs directory if it did not exist
- [ ] Generated unique bug ID (bug-001, bug-002, etc.)
- [ ] Wrote YAML frontmatter with bug-id, title, severity, status, dates, files
- [ ] Wrote clear one-paragraph summary
- [ ] Documented expected behavior
- [ ] Documented actual behavior with symptoms
- [ ] Wrote step-by-step reproduction instructions
- [ ] Included minimal reproduction code sample
- [ ] Added stack trace or error output
- [ ] Analyzed root cause (if known)
- [ ] Proposed fix (if known)
- [ ] Linked related source files, tests, and documentation
- [ ] Saved bug report to bugs directory
- [ ] Updated handoff document with bug reference
- [ ] Sent notification for critical/high severity bugs

## Examples

### Example 1: Medium Severity Bug Report

```markdown
---
bug-id: bug-001
title: IndexError on empty YAML input
severity: medium
status: new
discovered-by: ai-maestro-programmer-agent-main-agent
discovered-date: 2025-02-06T14:30:00Z
related-task: implement-yaml-parser
affected-files:
  - src/parsers/yaml_parser.py
---

# IndexError on Empty YAML Input

## Summary
The `parse_config()` function raises an `IndexError` instead of a proper `YamlParseError` when given empty or whitespace-only YAML input. This affects error handling and makes debugging harder for users.

## Expected Behavior
When given empty input, the parser should raise a `YamlParseError` with a clear message like "Empty or invalid YAML input".

## Actual Behavior
The parser raises `IndexError: list index out of range` from an internal function, exposing implementation details.

## Reproduction Steps

1. Import the parser: `from src.parsers.yaml_parser import parse_config`
2. Call with empty string: `parse_config("")`
3. Observe IndexError instead of YamlParseError

**Environment:**
- Python version: 3.12.1
- OS: macOS 14.2

## Minimal Reproduction

```python
from src.parsers.yaml_parser import parse_config

parse_config("")  # Raises IndexError
parse_config("   ")  # Also raises IndexError
```

## Error Output

```
Traceback (most recent call last):
  File "src/parsers/yaml_parser.py", line 47, in parse_config
    return tokens[current_index]
IndexError: list index out of range
```

## Root Cause Analysis

The `tokenize()` function returns an empty list for empty input, but `parse_config()` accesses `tokens[0]` without checking if the list is empty.

## Proposed Fix

```python
def parse_config(yaml_string: str) -> Config:
    tokens = tokenize(yaml_string)
    if not tokens:
        raise YamlParseError("Empty or invalid YAML input")
    # ... rest of function
```

## Related Items

- **Source file**: `src/parsers/yaml_parser.py` (line 47)
- **Missing test**: `test_parse_empty_input`
```

### Example 2: Critical Security Bug Report

```markdown
---
bug-id: bug-002
title: Path traversal vulnerability in file loader
severity: critical
status: new
discovered-by: ai-maestro-programmer-agent-main-agent
discovered-date: 2025-02-06T15:00:00Z
related-task: implement-yaml-parser
affected-files:
  - src/parsers/yaml_parser.py
  - src/loaders/file_loader.py
---

# Path Traversal Vulnerability in File Loader

## Summary
The `load_config_file()` function does not sanitize file paths, allowing attackers to read arbitrary files on the system using path traversal sequences like `../../../etc/passwd`.

## Expected Behavior
File paths should be validated to ensure they remain within the allowed configuration directory. Attempts to access files outside this directory should raise a `SecurityError`.

## Actual Behavior
Any file path is accepted and loaded, including paths with `..` sequences that escape the intended directory.

## Reproduction Steps

1. Call `load_config_file("../../../etc/passwd")`
2. Observe that the system passwd file contents are returned
3. This works from any calling directory

**Environment:**
- Python version: 3.12.1
- OS: Any Unix-like system

## Minimal Reproduction

```python
from src.loaders.file_loader import load_config_file

# This should fail but succeeds
content = load_config_file("../../../etc/passwd")
print(content)  # Prints system passwd file!
```

## Root Cause Analysis

The `load_config_file()` function uses `open(path, 'r')` directly without validating that the resolved path is within the allowed directory.

## Proposed Fix

```python
import os

CONFIG_DIR = "/app/configs"

def load_config_file(path: str) -> str:
    # Resolve to absolute path
    abs_path = os.path.abspath(os.path.join(CONFIG_DIR, path))

    # Verify path is within allowed directory
    if not abs_path.startswith(CONFIG_DIR):
        raise SecurityError(f"Access denied: {path}")

    with open(abs_path, 'r') as f:
        return f.read()
```

## Related Items

- **Source file**: `src/loaders/file_loader.py` (lines 10-15)
- **Security documentation**: OWASP Path Traversal
```

## Error Handling

### Error: Cannot Determine Bug Severity

**Symptom**: Unsure whether the bug is critical, high, medium, or low.

**Resolution**:
1. Ask: Does it crash the system or lose data? -> Critical
2. Ask: Does it break a major feature with no workaround? -> High
3. Ask: Does it break a feature but has a workaround? -> Medium
4. Ask: Is it cosmetic or very rare edge case? -> Low
5. When in doubt, choose one level higher than you think

### Error: Cannot Reproduce the Bug

**Symptom**: The bug only happened once and cannot be triggered again.

**Resolution**:
1. Check if the environment changed (dependencies, data, config)
2. Try reproducing in a clean environment
3. Add more logging to capture the state when it occurs
4. If still cannot reproduce after multiple attempts, document as "intermittent" and include all available context
5. Do NOT file a bug report for unreproducible issues unless you have strong evidence

### Error: Bug Is in Third-Party Code

**Symptom**: The bug is in a library or dependency, not in project code.

**Resolution**:
1. Still document it in the bugs directory with a note that it is external
2. Check if the library has a known issue tracker
3. Check if upgrading the library fixes it
4. Consider adding a workaround in project code
5. Link to the upstream bug report if one exists

### Error: Bug Report Too Long

**Symptom**: The bug report exceeds 200 lines.

**Resolution**:
1. Keep reproduction steps minimal (under 10 steps)
2. Use the smallest possible code sample
3. Move lengthy stack traces to a separate file
4. Summarize root cause rather than explaining all attempts
5. Link to related documents instead of inlining content
