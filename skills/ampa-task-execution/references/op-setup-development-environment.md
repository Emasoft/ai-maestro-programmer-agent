---
name: op-setup-development-environment
description: Set up the development environment for the assigned task
workflow-step: "Step 17.3 - Setup Development Environment"
parent-skill: ampa-task-execution
---

# Operation: Setup Development Environment

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.



## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 3.1: Navigate to Target Project Directory](#step-31-navigate-to-target-project-directory)
  - [Step 3.2: Activate Required Virtual Environment](#step-32-activate-required-virtual-environment)
  - [Step 3.3: Verify Dependencies Are Installed](#step-33-verify-dependencies-are-installed)
  - [Step 3.4: Initialize SERENA MCP for Code Navigation](#step-34-initialize-serena-mcp-for-code-navigation)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: Python Project Setup](#example-1-python-project-setup)
  - [Example 2: New Python Project (No venv)](#example-2-new-python-project-no-venv)
  - [Example 3: Node.js Project Setup](#example-3-nodejs-project-setup)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

Configure the development tooling required for the specific task.

## When to Use

> **First-time project setup?** If this is your first time working on this project, use the `ampa-project-setup` skill instead — it provides comprehensive environment initialization including language detection, linting, and testing framework setup. This operation is for subsequent tasks where the environment is already configured.

Use this operation when:
- You have parsed task requirements and are ready to implement
- You need to switch to a different project context
- The task requires specific tooling or dependencies

## Prerequisites

Before executing this operation:
1. Task requirements must be parsed (op-parse-task-requirements completed)
2. Target project directory must exist
3. Required tools (uv, git, SERENA) must be available

## Procedure

### Step 3.1: Navigate to Target Project Directory

Identify the project path from task context or project configuration:

```bash
# Verify project directory exists
ls -la /path/to/target/project

# Set as working directory for subsequent commands
cd /path/to/target/project
```

Verify project structure is valid:
- Contains expected source directories
- Has pyproject.toml or package.json as appropriate
- Is a git repository (has .git folder)

### Step 3.2: Activate Required Virtual Environment

For Python projects:

```bash
# Check if virtual environment exists
ls -la .venv/

# If not, create it
uv venv --python 3.12

# Activate the environment
source .venv/bin/activate
# Windows: .venv\Scripts\activate.bat (cmd) or .venv\Scripts\Activate.ps1 (PowerShell)

# Verify activation
which python
# Should show: /path/to/project/.venv/bin/python
```

For Node.js projects:

```bash
# Verify Node version
node --version

# Verify package manager
bun --version  # or npm/pnpm as appropriate
```

### Step 3.3: Verify Dependencies Are Installed

For Python projects:

```bash
# Sync dependencies from pyproject.toml
uv sync

# Verify key dependencies
uv run python -c "import <key_package>; print('OK')"
```

For Node.js projects:

```bash
# Install dependencies
bun install

# Verify installation
bun run --silent echo "Dependencies OK"
```

Check for task-specific dependencies:

| Dependency Type | Check Command | Install Command |
|-----------------|---------------|-----------------|
| Python package | `uv run python -c "import pkg"` | `uv add pkg` |
| Node package | `bun pm ls pkg` | `bun add pkg` |
| System tool | `which tool` | Platform-specific |

### Step 3.4: Initialize SERENA MCP for Code Navigation

Verify SERENA is accessible:

```
mcp__serena__get_codebase_structure()
```

If SERENA fails to initialize:
1. Check if the project has been indexed
2. Verify the project path is correct
3. Report environment setup failure to orchestrator

Common SERENA initialization commands:

| Command | Purpose |
|---------|---------|
| `get_codebase_structure()` | Get project overview |
| `find_symbol("name")` | Locate functions, classes |
| `get_symbol_details("name")` | Get full implementation |

## Checklist

- [ ] Project directory verified and accessible
- [ ] Virtual environment exists or created
- [ ] Virtual environment activated
- [ ] Dependencies synced (uv sync or bun install)
- [ ] Key dependencies verified importable
- [ ] Git repository status checked
- [ ] SERENA MCP responding correctly
- [ ] Code structure can be queried

## Examples

### Example 1: Python Project Setup

Task requires working on `~/projects/my-api`:

```bash
# Navigate to project
cd ~/projects/my-api

# Check for existing venv
ls -la .venv/
# .venv exists

# Activate
source .venv/bin/activate
# Windows: .venv\Scripts\activate.bat (cmd) or .venv\Scripts\Activate.ps1 (PowerShell)

# Sync dependencies
uv sync
# Resolved 45 packages in 1.2s

# Verify key packages
uv run python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"
# FastAPI 0.109.0

# Check git status
git status
# On branch main, working tree clean

# Initialize SERENA
mcp__serena__get_codebase_structure()
# Returns project structure with src/, tests/, etc.
```

Environment ready for development.

### Example 2: New Python Project (No venv)

Task requires working on a freshly cloned project:

```bash
# Navigate
cd ~/projects/new-project

# No venv exists
ls -la .venv/
# ls: .venv/: No such file or directory

# Create venv
uv venv --python 3.12
# Creating virtual environment at: .venv

# Activate
source .venv/bin/activate
# Windows: .venv\Scripts\activate.bat (cmd) or .venv\Scripts\Activate.ps1 (PowerShell)

# Sync dependencies
uv sync
# Resolved 23 packages in 0.8s
```

### Example 3: Node.js Project Setup

Task requires working on a TypeScript frontend:

```bash
# Navigate
cd ~/projects/frontend

# Check Node version
node --version
# v20.10.0

# Install dependencies
bun install
# Installed 156 packages

# Verify key package
bun run tsc --version
# Version 5.3.3
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Directory not found | Invalid project path | Verify path with orchestrator |
| uv: command not found | uv not installed | Install: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Python version mismatch | Wrong Python specified | Use `uv venv --python X.Y` with correct version |
| Dependency conflict | Package version issues | Report to orchestrator, may need manual resolution |
| SERENA not responding | MCP not configured | Verify SERENA MCP is in settings |
| Git not clean | Uncommitted changes | Report to orchestrator, may need to stash |

## Related Operations

- [op-parse-task-requirements.md](op-parse-task-requirements.md) - Previous step
- [op-implement-code.md](op-implement-code.md) - Next step
- [op-write-tests.md](op-write-tests.md) - Tests require same environment
