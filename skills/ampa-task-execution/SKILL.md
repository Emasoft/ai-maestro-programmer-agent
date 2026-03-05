---
name: ampa-task-execution
description: Execute programming tasks per requirements. Use when implementing assigned tasks. Trigger with /ampa-task-execution or when receiving task assignments.
license: MIT
compatibility: Requires SERENA MCP activated.
metadata:
  author: AI Maestro
  version: 1.0.12
  workflow-instruction: "Step 17 - Task Execution"
  procedure: "proc-execute-task"
context: fork
agent: ampa-programmer-main-agent
user-invocable: false
---

# AMPA Task Execution Skill

Execute programming tasks according to requirements and acceptance criteria received from the orchestrator.

## Overview

AMPA is an **implementer** (artifact-producing agent). This skill handles the task execution workflow for the programmer subtype.

The AMPA Task Execution skill is the core operational skill for the AI Maestro Programmer Agent (AMPA). It defines the end-to-end workflow a programmer agent follows when assigned a coding task by an orchestrator agent (AMOA). The workflow covers every phase from receiving the task assignment via AI Maestro messaging, through parsing requirements, setting up the development environment, implementing code, writing tests, and validating acceptance criteria. This skill ensures that every task is completed methodically, with full traceability from requirement to implementation to verification. It depends on SERENA MCP for code navigation and AI Maestro for inter-agent communication.

## Instructions

Follow these numbered steps in order for every assigned task:

1. **Receive the task assignment** -- Read the incoming AI Maestro message from the orchestrator agent, extract the task identifier and metadata, validate all required fields are present, and send an acknowledgment back to the orchestrator.
2. **Parse the task requirements** -- Extract the full list of acceptance criteria, identify any dependencies on other tasks that must be completed first, determine which files and components will be modified, and ask the orchestrator for clarification on anything ambiguous.
3. **Set up the development environment** -- Navigate to the target project directory, activate the correct virtual environment (using `uv venv` or `source .venv/bin/activate` (Windows: `.venv/Scripts/activate.bat` or `.venv/Scripts/Activate.ps1`)), verify all dependencies are installed, and initialize SERENA MCP for code navigation.
4. **Implement the code** -- Use SERENA MCP to analyze the existing code structure, plan the implementation approach in small increments, write code in testable chunks, and add documentation and comments explaining the "why" of each change.
5. **Write tests** -- Identify test scenarios directly from the requirements, write unit tests for all new functions, write integration tests where applicable, run all tests, and fix any failures before proceeding.
6. **Validate acceptance criteria** -- Review each acceptance criterion one by one, verify the implementation satisfies it, document the evidence of validation, and report task completion to the orchestrator via AI Maestro.
7. **Report completion** -- Send a structured completion message to the orchestrator that includes the task identifier, list of files modified, test results summary, and confirmation that all acceptance criteria passed.

## Output

This skill produces the following artifacts upon successful task completion:

- **Implemented code changes** -- New or modified source files in the target project, with inline comments explaining the purpose of each change.
- **Test suite** -- Unit tests and integration tests covering all new functionality, located in the project's `tests/` directory.
- **Validation report** -- A structured message sent to the orchestrator via AI Maestro confirming each acceptance criterion was met, including evidence (test results, code references).
- **Updated checklist** -- The master checklist (defined below) with all items checked, serving as the task completion record.
- **Git commit** -- A commit containing all code and test changes, with a descriptive commit message referencing the task identifier.

## Examples

### Example 1: Implementing a New Utility Function

The orchestrator assigns task `TASK-042: Add a string sanitization function to utils.py`. The programmer agent:
1. Receives the AI Maestro message, extracts task ID `TASK-042` and reads the acceptance criteria: "Function `sanitize_input(text: str) -> str` must strip HTML tags, normalize whitespace, and return a clean string."
2. Uses SERENA MCP to find `utils.py` and understand existing utility patterns.
3. Implements `sanitize_input()` following the existing code style in `utils.py`.
4. Writes 4 unit tests in `tests/test_utils.py`: empty string, normal text, HTML-laden text, and whitespace-heavy text.
5. Runs `uv run pytest tests/test_utils.py -v`, confirms all 4 pass.
6. Sends completion message to orchestrator: "TASK-042 complete. Modified: src/utils.py, tests/test_utils.py. All 4 tests passing. Acceptance criteria met."

### Example 2: Fixing a Bug in an Existing Module

The orchestrator assigns task `BUG-017: Fix off-by-one error in pagination logic`. The programmer agent:
1. Reads the task requirements: "The `paginate()` function in `src/api/pagination.py` returns one fewer item than expected on the last page."
2. Uses SERENA MCP to locate `paginate()`, reads the function body, and traces the logic to find the off-by-one error at the boundary calculation.
3. Fixes the boundary calculation, adds a comment explaining why `<=` is correct instead of `<`.
4. Adds a regression test specifically for the last-page edge case.
5. Runs the full test suite to confirm no regressions.
6. Reports completion with the fix description and test evidence.

### Example 3: Handling a Blocked Task

The orchestrator assigns task `TASK-055: Add caching layer to data fetcher`. The programmer agent:
1. Parses requirements and discovers dependency on `TASK-054: Implement Redis client wrapper`, which is not yet complete.
2. Does NOT proceed with implementation. Instead, sends a blocker report to the orchestrator: "TASK-055 blocked by TASK-054 (Redis client wrapper not yet available). Awaiting guidance."
3. Waits for orchestrator response before taking any action.

### Example Input/Output

**Input:** Task assignment message from orchestrator:

```
Subject: "Task TASK-042: Add string sanitization to utils"
Content: {
  "type": "task-assignment",
  "task_id": "TASK-042",
  "requirements": "Add sanitize_input(text: str) -> str that strips HTML tags and normalizes whitespace.",
  "acceptance_criteria": ["Function exists in src/utils.py", "All HTML tags removed", "Whitespace normalized", "Unit tests pass"],
  "priority": "normal"
}
```

**Output:** Completed implementation report sent back to orchestrator:

```
Subject: "Task TASK-042 complete: string sanitization added"
Content: {
  "type": "completion-notification",
  "task_id": "TASK-042",
  "files_modified": ["src/utils.py", "tests/test_utils.py"],
  "tests": "4 passed, 0 failed",
  "acceptance_criteria_met": ["Function exists in src/utils.py: YES", "All HTML tags removed: YES", "Whitespace normalized: YES", "Unit tests pass: YES"],
  "branch": "feature/task-042-sanitize-input",
  "commit": "feat(utils): add sanitize_input function"
}
```

## Purpose

This skill provides the complete workflow for receiving, understanding, implementing, testing, and validating programming tasks. It ensures all acceptance criteria are met before marking a task as complete.

## When to Use

Use this skill when:
- You receive a task assignment via AI Maestro message
- You need to implement code changes according to specifications
- You must validate your implementation against acceptance criteria

## Prerequisites

Before using this skill:
1. SERENA MCP must be activated for code navigation
2. Development environment must be configured for the target project
3. You must have received a valid task assignment with requirements

## Task Execution Workflow

The task execution process follows these ordered steps:

### Step 1: Receive Task Assignment
Parse and validate the incoming task from AI Maestro.

**Reference**: [op-receive-task-assignment.md](references/op-receive-task-assignment.md)

**Sections in op-receive-task-assignment.md:** When to Use · Prerequisites · Procedure · Step 1.1: Read Incoming AI Maestro Message · Step 1.2: Extract Task Identifier and Metadata · Step 1.3: Validate Message Format and Required Fields · Step 1.4: Acknowledge Receipt to Orchestrator · Checklist · Examples · Error Handling · Related Operations

**Contents**:
- 1.1 Read Incoming AI Maestro Message
- 1.2 Extract Task Identifier and Metadata
- 1.3 Validate Message Format and Required Fields
- 1.4 Acknowledge Receipt to Orchestrator

### Step 2: Parse Task Requirements
Understand what needs to be implemented.

**Reference**: [op-parse-task-requirements.md](references/op-parse-task-requirements.md)

**Sections in op-parse-task-requirements.md:** When to Use · Prerequisites · Procedure · Step 2.1: Extract Acceptance Criteria List · Step 2.2: Identify Dependencies on Other Tasks · Step 2.3: Determine Target Files and Components · Step 2.4: Clarify Ambiguities with Orchestrator · Checklist · Examples · Error Handling · Related Operations

**Contents**:
- 2.1 Extract Acceptance Criteria List
- 2.2 Identify Dependencies on Other Tasks
- 2.3 Determine Target Files and Components
- 2.4 Clarify Ambiguities with Orchestrator

### Step 3: Setup Development Environment
Configure tooling for the specific task.

**Reference**: [op-setup-development-environment.md](references/op-setup-development-environment.md)

**Sections in op-setup-development-environment.md:** When to Use · Prerequisites · Procedure · Step 3.1: Navigate to Target Project Directory · Step 3.2: Activate Required Virtual Environment · Step 3.3: Verify Dependencies Are Installed · Step 3.4: Initialize SERENA MCP for Code Navigation · Checklist · Examples · Error Handling · Related Operations

**Contents**:
- 3.1 Navigate to Target Project Directory
- 3.2 Activate Required Virtual Environment
- 3.3 Verify Dependencies Are Installed
- 3.4 Initialize SERENA MCP for Code Navigation

> **Note**: For first-time project setup (language detection, package manager, dependencies, linting), see the **ampa-project-setup** skill. This step covers per-task environment verification only.

### Step 4: Implement Code
Write the code following requirements.

**Reference**: [op-implement-code.md](references/op-implement-code.md)

**Contents**:
- 4.1 Analyze Existing Code Structure with SERENA
- 4.2 Plan Implementation Approach
- 4.3 Write Code in Small, Testable Increments
- 4.4 Add Documentation and Comments

### Step 5: Write Tests
Create tests for the implementation.

**Reference**: [op-write-tests.md](references/op-write-tests.md)

**Contents**:
- 5.1 Identify Test Scenarios from Requirements
- 5.2 Write Unit Tests for New Functions
- 5.3 Write Integration Tests if Applicable
- 5.4 Run Tests and Fix Failures

### Step 6: Validate Acceptance Criteria
Verify all criteria are met before completion.

**Reference**: [op-validate-acceptance-criteria.md](references/op-validate-acceptance-criteria.md)

**Contents**:
- 6.1 Review Each Acceptance Criterion
- 6.2 Verify Implementation Satisfies Criterion
- 6.3 Document Validation Evidence
- 6.4 Report Completion to Orchestrator

## Master Checklist

Copy this checklist and track your progress:

- [ ] Task assignment received and acknowledged
- [ ] Requirements parsed and understood
- [ ] Development environment ready
- [ ] Code implementation complete
- [ ] Tests written and passing
- [ ] All acceptance criteria validated
- [ ] Completion reported to orchestrator

## Error Handling

If any step fails:
1. Document the failure reason
2. Report the blocker to orchestrator via AI Maestro
3. Wait for guidance before proceeding
4. Do not mark task complete with failing criteria

## Related Skills

- **ampa-orchestrator-communication** skill -- For messaging the orchestrator agent, sending status updates, blocker reports, and completion notifications via AI Maestro.
- **ampa-handoff-management** skill -- For managing task handoffs between agents, including structured handoff documents and context transfer.
- **ampa-github-operations** skill -- For committing code changes, creating branches, opening pull requests, and other GitHub operations.

## Resources

- **SERENA MCP documentation** -- Required for code navigation operations used in Steps 3 and 4 of the workflow. SERENA provides symbol search, function body reading, and code structure analysis.
- **AI Maestro messaging guide** -- Covers the message format and API used for all inter-agent communication in Steps 1, 2 (clarification), 6, and 7 (completion reporting). See the `agent-messaging` skill installed globally by AI Maestro.
- **uv documentation** -- The Python package manager used for virtual environment setup and dependency management in Step 3. Use `uv venv --python 3.12` to create environments and `uv run pytest` to execute tests.
- **pytest documentation** -- The test framework used in Step 5 for writing and running unit and integration tests. Use `uv run pytest -v` for verbose output.
- **GitHub CLI (gh) documentation** -- Used by the ampa-github-operations skill for creating branches, commits, and pull requests after task completion.
