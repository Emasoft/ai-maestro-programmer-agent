---
name: ampa-project-setup
description:
  Setup project configuration and tooling. Use when starting work on new
  project. Trigger with /ampa-project-setup or when initializing a new project.
  Loaded by ai-maestro-programmer-agent-main-agent.
license: MIT
compatibility: Requires SERENA MCP activated.
metadata:
  author: AI Maestro
  version: 1.0.20
  workflow-instruction: "Step 17 (first task)"
  procedure: "proc-execute-task"
context: fork
agent: ai-maestro-programmer-agent-main-agent
user-invocable: false
---

# AMPA Project Setup Skill

## Overview

Project environment setup for AMPA (see agent definition for role context and
supported languages table). Covers language detection, package manager
initialization, dependency installation, linting, testing, and SERENA MCP
activation.

Use when starting work on a new project or onboarding to a project that lacks
tooling. For per-task environment verification, see Step 3 of
**ampa-task-execution**.

## Prerequisites

1. Write access to the project directory
2. SERENA MCP available for activation
3. Know the target language (or be ready to detect it)

## Instructions

Copy this checklist and track your progress:

1. **Read this SKILL.md** to understand the operations before executing.
2. **Navigate to the project root** and confirm write access.
3. **Detect language**: Read and execute
   [op-detect-project-language.md](references/op-detect-project-language.md):
   When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling.
   Record the result.
4. **Init package manager**: Read and execute
   [op-initialize-package-manager.md](references/op-initialize-package-manager.md):
   When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling.
   Verify with version command.
5. **Install dependencies**: Read and execute
   [op-install-dependencies.md](references/op-install-dependencies.md):
   When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling.
   Confirm zero errors.
6. **Configure linting**: Read and execute
   [op-configure-linting.md](references/op-configure-linting.md):
   When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling.
   For Python, also read
   [ruff-configuration-patterns.md](references/ruff-configuration-patterns.md):
   When to Configure Ruff for a New Project, Standard ruff.toml Template for AI Maestro Programmer Projects, What Each Rule Set Does, What Each Ignored Rule Means, Per-File Ignore Patterns, Formatter Settings, How to Run Ruff, Customizing Ruff for Specific Project Types.
   Verify linter runs.
7. **Setup testing**: Read and execute
   [op-setup-testing-framework.md](references/op-setup-testing-framework.md):
   When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling.
   Run test suite once.
8. **Activate SERENA**: Read and execute
   [op-activate-serena-mcp.md](references/op-activate-serena-mcp.md):
   When to Use, Prerequisites, Procedure, SERENA Tool Reference, Checklist, Examples, Error Handling.
   Verify with `find_symbol`.
9. **Report setup status** to AMOA confirming the environment is ready.

## Output

- Initialized package manager, installed dependencies, linter config, test
  framework config, active SERENA MCP connection.

## Error Handling

If any setup step fails, do not proceed to the next step. Report the failure to
AMOA with the step name, error output, and the log file path. Wait for guidance
before retrying.

## Examples

- [ ] Input: New Python 3.12 project directory
- [x] Output: uv init, deps installed, ruff configured, pytest ready, SERENA
      active

## Reference Documents

| Document | Description |
|----------|-------------|
| [op-detect-project-language.md](references/op-detect-project-language.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling |
| [op-initialize-package-manager.md](references/op-initialize-package-manager.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling |
| [op-install-dependencies.md](references/op-install-dependencies.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling |
| [op-configure-linting.md](references/op-configure-linting.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling |
| [ruff-configuration-patterns.md](references/ruff-configuration-patterns.md) | When to Configure Ruff for a New Project, Standard ruff.toml Template for AI Maestro Programmer Projects, What Each Rule Set Does, What Each Ignored Rule Means, Per-File Ignore Patterns, Formatter Settings, How to Run Ruff, Customizing Ruff for Specific Project Types |
| [op-setup-testing-framework.md](references/op-setup-testing-framework.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling |
| [op-activate-serena-mcp.md](references/op-activate-serena-mcp.md) | When to Use, Prerequisites, Procedure, SERENA Tool Reference, Checklist, Examples, Error Handling |

## Related

- **ampa-task-execution** — Next skill after project setup.
