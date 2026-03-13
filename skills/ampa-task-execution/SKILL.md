---
name: ampa-task-execution
description: Execute programming tasks. Use when implementing code, writing tests, or validating acceptance criteria. Trigger with /ampa-task-execution or on task assignment.
license: MIT
compatibility: Requires SERENA MCP activated.
metadata:
  author: AI Maestro
  version: 1.0.16
  workflow-instruction: "Step 17 - Task Execution"
  procedure: "proc-execute-task"
context: fork
agent: ai-maestro-programmer-agent-main-agent
user-invocable: false
---

# AMPA Task Execution Skill

## Overview

Core task execution workflow for AMPA. Covers receiving a task assignment through implementing code, writing tests, and validating acceptance criteria. Requires SERENA MCP and AI Maestro.

## Prerequisites

- Task assignment received from orchestrator via AI Maestro with valid requirements and acceptance criteria
- Target project set up (for first-time setup, use **ampa-project-setup** skill)
- SERENA MCP activated for code navigation

## Instructions

Copy this checklist and track your progress:

1. **Receive task assignment** -- Read the AI Maestro message, extract task ID and metadata, validate required fields, acknowledge receipt to the orchestrator.
2. **Parse requirements** -- Extract acceptance criteria, identify dependencies on other tasks, determine target files/components, ask the orchestrator to clarify any ambiguities.
3. **Set up dev environment** -- Navigate to project directory, activate venv (`uv venv` / `source .venv/bin/activate`), verify dependencies, initialize SERENA MCP.
4. **Implement code** -- Use SERENA to analyze existing structure, plan in small increments, write testable code, add comments explaining the "why" of each change.
5. **Write tests** -- Identify scenarios from requirements, write unit and integration tests, run all tests, fix failures before proceeding.
6. **Validate acceptance criteria** -- Review each criterion, verify the implementation satisfies it, document validation evidence.
7. **Report completion** -- Send structured message to orchestrator: task ID, files modified, test results summary, confirmation all acceptance criteria passed.

> **Interruption handling**: If an AI Maestro message arrives during implementation, pause at the nearest safe point (after current commit or test run), process the message using `ampa-orchestrator-communication`, then resume.

## Output

- **Implemented code** -- New/modified source files with inline comments explaining each change
- **Test suite** -- Unit and integration tests in the project's `tests/` directory
- **Completion report** -- Structured AI Maestro message confirming each acceptance criterion was met

## Token Budget

- **Lazy loading**: Only read a reference file when executing that step. Do not pre-read all 6.
- **Test output to file**: Write pytest output to `docs_dev/`. Report only: `[PASS/FAIL] X/Y. Report: <path>`.
- **Completion report**: 3 lines max to AMOA: task ID, pass/fail, path to full report.

## Error Handling

On failure: document it, report to orchestrator, wait for guidance, do not mark complete.

| Condition | Action |
|-----------|--------|
| Missing required fields | Report validation error, request corrected assignment |
| Dependency on incomplete task | Report blocker, do not proceed |
| Tests failing after 3 attempts | Report persistent failure with diagnostics |
| Context running low | Use `ampa-handoff-management` to save progress |

## Examples

- [ ] Input: Task #42 assignment message from AMOA
- [x] Output: 3 modified files, 5 passing tests, completion report sent

## Resources

- **[op-receive-task-assignment.md](references/op-receive-task-assignment.md)** -- Parse and validate incoming task
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-parse-task-requirements.md](references/op-parse-task-requirements.md)** -- Extract criteria, dependencies, target files
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-setup-development-environment.md](references/op-setup-development-environment.md)** -- Configure tooling and verify environment
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-implement-code.md](references/op-implement-code.md)** -- Analyze structure, write implementation
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-write-tests.md](references/op-write-tests.md)** -- Create unit and integration tests
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-validate-acceptance-criteria.md](references/op-validate-acceptance-criteria.md)** -- Verify criteria and document evidence
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling

## Related Skills

- **ampa-orchestrator-communication** -- Status updates, blocker reports, completion notifications.
- **ampa-github-operations** -- Committing, branching, pull requests.
