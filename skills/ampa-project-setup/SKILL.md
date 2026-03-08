---
name: ampa-project-setup
description: Setup project configuration and tooling. Use when starting work on new project. Trigger with /ampa-project-setup or when initializing a new project.
license: MIT
compatibility: Requires SERENA MCP activated.
metadata:
  author: AI Maestro
  version: 1.0.15
  workflow-instruction: "Step 17 (first task)"
  procedure: "proc-execute-task"
context: fork
agent: ampa-programmer-main-agent
user-invocable: false
---

# AMPA Project Setup Skill

## Overview

Project environment setup for AMPA (see agent definition for role context and supported languages table). Covers language detection, package manager initialization, dependency installation, linting, testing, and SERENA MCP activation.

Use when starting work on a new project or onboarding to a project that lacks tooling. For per-task environment verification, see Step 3 of **ampa-task-execution**.

## Prerequisites

1. Write access to the project directory
2. SERENA MCP available for activation
3. Know the target language (or be ready to detect it)

## Instructions

Copy this checklist and track your progress:

1. **Read this SKILL.md** to understand the operations before executing.
2. **Navigate to the project root** and confirm write access.
3. **Detect language**: Read and execute [op-detect-project-language.md](references/op-detect-project-language.md). Record the result.
4. **Init package manager**: Read and execute [op-initialize-package-manager.md](references/op-initialize-package-manager.md). Verify with version command.
5. **Install dependencies**: Read and execute [op-install-dependencies.md](references/op-install-dependencies.md). Confirm zero errors.
6. **Configure linting**: Read and execute [op-configure-linting.md](references/op-configure-linting.md). For Python, also read [ruff-configuration-patterns.md](references/ruff-configuration-patterns.md). Verify linter runs.
7. **Setup testing**: Read and execute [op-setup-testing-framework.md](references/op-setup-testing-framework.md). Run test suite once.
8. **Activate SERENA**: Read and execute [op-activate-serena-mcp.md](references/op-activate-serena-mcp.md). Verify with `find_symbol`.
9. **Report setup status** to AMOA confirming the environment is ready.

## Output

- Initialized package manager, installed dependencies, linter config, test framework config, active SERENA MCP connection.

## Token Budget

- **Lazy loading**: Only read a reference file when executing that operation. Do not pre-read all 7 references.
- **Tool output capture**: Redirect package manager output to a log file. Report only: `[DONE] <step> (exit 0). Log: <path>`.

## Error Handling

If any setup step fails, do not proceed to the next step. Report the failure to AMOA with the step name, error output, and the log file path. Wait for guidance before retrying.

## Examples

- [ ] Input: New Python 3.12 project directory
- [x] Output: uv init, deps installed, ruff configured, pytest ready, SERENA active

## Resources

- **[op-detect-project-language.md](references/op-detect-project-language.md)** — Identify project language from file patterns
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-initialize-package-manager.md](references/op-initialize-package-manager.md)** — Language-specific package manager initialization
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-install-dependencies.md](references/op-install-dependencies.md)** — Dependency installation and virtual environment setup
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-configure-linting.md](references/op-configure-linting.md)** — Linter configuration for each supported language
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[ruff-configuration-patterns.md](references/ruff-configuration-patterns.md)** — Standard ruff.toml template for Python projects
  Sections: When to Configure Ruff for a New Project · Standard ruff.toml Template for AI Maestro Programmer Projects · What Each Rule Set Does · What Each Ignored Rule Means · Per-File Ignore Patterns · Formatter Settings · How to Run Ruff · Customizing Ruff for Specific Project Types
- **[op-setup-testing-framework.md](references/op-setup-testing-framework.md)** — Test framework config for pytest, jest, vitest, cargo test, etc.
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-activate-serena-mcp.md](references/op-activate-serena-mcp.md)** — SERENA MCP activation, verification, and troubleshooting
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling

## Related Skills

- **ampa-task-execution** — Next skill after project setup, covering task implementation workflow.
