---
name: ampa-project-setup
description: Setup project configuration and tooling. Use when starting work on new project. Trigger with /ampa-project-setup or when initializing a new project.
license: MIT
compatibility: Requires SERENA MCP activated.
metadata:
  author: AI Maestro
  version: 1.0.12
  workflow-instruction: "Step 17 (first task)"
  procedure: "proc-execute-task"
context: fork
agent: ampa-programmer-main-agent
user-invocable: false
---

# AMPA Project Setup Skill

This skill provides procedures for setting up project configuration and tooling when starting work on a new project. It covers language detection, package manager initialization, dependency installation, linting configuration, testing framework setup, and SERENA MCP activation.

## Overview

AMPA is an **implementer** agent. This skill handles project environment setup for code-producing implementers.

The AMPA Project Setup skill equips the AI Maestro Programmer Agent (AMPA) with a complete, repeatable procedure for initializing any new project workspace. When an AMPA agent receives its first task on a project, it must configure the development environment before writing any code. This skill guides that process across eight supported languages (Python, JavaScript/TypeScript, Rust, Go, .NET, C/C++, Objective-C, Swift) by providing six sequential operations: language detection, package manager initialization, dependency installation, linting configuration, testing framework setup, and SERENA MCP activation. Each operation has its own detailed reference file under the `references/` subdirectory. The skill ensures that every AMPA agent starts from a consistent, fully-configured environment regardless of project language or existing state.

## Instructions

Follow these numbered steps in exact order to set up a new project:

1. **Read this entire SKILL.md** to understand the operations and their order before executing anything.
2. **Navigate to the project root directory** and confirm you have write access to the project folder.
3. **Detect the project language** by reading [op-detect-project-language.md](references/op-detect-project-language.md) and executing its procedure. Record the detected language for subsequent steps.
    Sections: When to Use · Prerequisites · Procedure
4. **Initialize the package manager** by reading [op-initialize-package-manager.md](references/op-initialize-package-manager.md) for the detected language and executing its procedure. Verify initialization succeeded by running the package manager's version command.
    Sections: When to Use · Prerequisites · Procedure
5. **Install all dependencies** by reading [op-install-dependencies.md](references/op-install-dependencies.md) and executing its procedure. Confirm zero errors in the installation output.
    Sections: When to Use · Prerequisites · Procedure
6. **Configure linting tools** by reading [op-configure-linting.md](references/op-configure-linting.md) and executing its procedure. For Python projects, also read [ruff-configuration-patterns.md](references/ruff-configuration-patterns.md). Run the linter once to verify it executes without configuration errors.
    Sections (op-configure-linting): When to Use · Prerequisites · Procedure
    Sections (ruff-configuration-patterns): When to configure ruff for a new project · Standard ruff.toml template for AI Maestro Programmer projects · What each rule set does and why it is enabled
7. **Set up the testing framework** by reading [op-setup-testing-framework.md](references/op-setup-testing-framework.md) and executing its procedure. Run the test suite once (even if no tests exist yet) to confirm the framework is properly configured.
    Sections: When to Use · Prerequisites · Procedure
8. **Activate SERENA MCP** by reading [op-activate-serena-mcp.md](references/op-activate-serena-mcp.md) and executing its procedure. Verify SERENA responds to a test command such as `find_symbol`.
    Sections: When to Use · Prerequisites · Procedure
9. **Complete the checklist** at the bottom of this file by marking all items as done.
10. **Report setup status** to the orchestrator agent (AMOA) confirming the environment is ready for task execution.

## Output

After successful execution of this skill, the following artifacts and states are produced:

- **Initialized package manager** — A working package manager configuration file exists (for example `pyproject.toml` for Python, `package.json` for JavaScript/TypeScript, `Cargo.toml` for Rust, `go.mod` for Go).
- **Installed dependency tree** — All project dependencies are installed and resolvable. Virtual environments are created where applicable (for example `.venv/` for Python projects).
- **Linter configuration files** — Language-appropriate linter configuration is in place and verified (for example `ruff.toml` for Python, `.eslintrc` for JavaScript/TypeScript, `clippy.toml` for Rust).
- **Testing framework configuration** — Test runner is configured and can be invoked (for example `pytest.ini` or `pyproject.toml [tool.pytest]` for Python, `jest.config.js` for JavaScript).
- **Active SERENA MCP connection** — SERENA is activated and responding to code navigation commands.
- **Completed setup checklist** — All six checklist items marked as done, confirming environment readiness.

## Supported Languages

| Language | Package Manager | Linter | Testing |
|----------|-----------------|--------|---------|
| Python | uv | ruff, mypy | pytest |
| JavaScript/TypeScript | bun, pnpm | eslint | jest, vitest |
| Rust | cargo | clippy | cargo test |
| Go | go mod | staticcheck | go test |
| .NET | dotnet | - | dotnet test |
| C/C++ | cmake, make | clang-tidy | gtest |
| Objective-C | xcodebuild | - | XCTest |
| Swift | swift, xcodebuild | swiftlint | XCTest |

## When to Use This Skill

Use this skill when:
- Starting work on a new project for the first time
- The project lacks proper tooling configuration
- You need to set up a consistent development environment
- Onboarding to an existing project that needs tooling verification

> **Note**: For per-task development environment verification (virtual env activation, dependency check), see Step 3 of the **ampa-task-execution** skill. This skill covers one-time project initialization only.

## Prerequisites

Before using this skill:
1. Have access to the project directory
2. Have SERENA MCP available for activation
3. Know the target programming language (or be ready to detect it)

## Operations Reference

This skill provides the following operations. Read each operation file before executing its procedure.

### 1. Detect Project Language
**File**: [op-detect-project-language.md](references/op-detect-project-language.md)

Contents:
- 1.1 When to detect project language
- 1.2 File-based language detection patterns
- 1.3 Configuration file indicators
- 1.4 Fallback detection strategies
- 1.5 Multi-language project handling

### 2. Initialize Package Manager
**File**: [op-initialize-package-manager.md](references/op-initialize-package-manager.md)

Contents:
- 2.1 When to initialize package manager
- 2.2 Python: uv initialization
- 2.3 JavaScript/TypeScript: bun or pnpm initialization
- 2.4 Rust: cargo initialization
- 2.5 Go: go mod initialization
- 2.6 Other languages: initialization procedures

### 3. Install Dependencies
**File**: [op-install-dependencies.md](references/op-install-dependencies.md)

Contents:
- 3.1 When to install dependencies
- 3.2 Reading dependency files
- 3.3 Package manager specific install commands
- 3.4 Handling missing or outdated dependencies
- 3.5 Virtual environment management

### 4. Configure Linting
**File**: [op-configure-linting.md](references/op-configure-linting.md)

Contents:
- 4.1 When to configure linting
- 4.2 Python: ruff and mypy configuration
- 4.3 JavaScript/TypeScript: eslint configuration
- 4.4 Rust: clippy configuration
- 4.5 Other languages: linter setup

For ruff linter and formatter configuration, see [ruff-configuration-patterns.md](references/ruff-configuration-patterns.md):
- When to configure ruff for a new project
- Standard ruff.toml template for AI Maestro Programmer projects
- What each rule set does and why it is enabled
- What each ignored rule means and why it is ignored
- Per-file ignore patterns and when to use them
- Formatter settings (quote style, indent, line endings)
- How to run ruff check and ruff format
- Customizing ruff for specific project types

### 5. Setup Testing Framework
**File**: [op-setup-testing-framework.md](references/op-setup-testing-framework.md)

Contents:
- 5.1 When to setup testing framework
- 5.2 Python: pytest configuration
- 5.3 JavaScript/TypeScript: jest or vitest configuration
- 5.4 Rust: cargo test configuration
- 5.5 Other languages: test framework setup

### 6. Activate SERENA MCP
**File**: [op-activate-serena-mcp.md](references/op-activate-serena-mcp.md)

Contents:
- 6.1 When to activate SERENA MCP
- 6.2 SERENA activation procedure
- 6.3 Verifying SERENA connection
- 6.4 SERENA tool availability check
- 6.5 Troubleshooting SERENA activation

## Standard Setup Procedure

Execute these operations in order for a complete project setup:

1. **Detect Language** - Run op-detect-project-language to identify the project language
2. **Initialize Package Manager** - Run op-initialize-package-manager for the detected language
3. **Install Dependencies** - Run op-install-dependencies to get all required packages
4. **Configure Linting** - Run op-configure-linting to enable code quality checks
5. **Setup Testing** - Run op-setup-testing-framework to enable test execution
6. **Activate SERENA** - Run op-activate-serena-mcp for code navigation

## Checklist

Copy this checklist and track your progress:

- [ ] Project language detected and confirmed
- [ ] Package manager initialized and verified
- [ ] All dependencies installed successfully
- [ ] Linting tools configured and tested
- [ ] Testing framework configured and verified
- [ ] SERENA MCP activated and responding

## Troubleshooting

### Package Manager Not Found

**Problem**: The expected package manager is not installed on the system.

**Solution**: Install the package manager first. See the specific operation file for installation instructions for each package manager.

### Dependency Installation Fails

**Problem**: Dependencies fail to install due to version conflicts or missing packages.

**Solution**: Check the op-install-dependencies.md file for troubleshooting steps specific to each package manager.

### Linter Configuration Errors

**Problem**: Linter fails to run or produces incorrect configuration errors.

**Solution**: Verify the linter configuration file format. See op-configure-linting.md for correct configuration templates.

### SERENA MCP Not Responding

**Problem**: SERENA MCP fails to activate or does not respond to commands.

**Solution**: See op-activate-serena-mcp.md for SERENA-specific troubleshooting steps.

### Multi-Language Project Setup

**Problem**: Project uses multiple languages and needs multiple toolchains.

**Solution**: Run the setup procedure for each language independently. Start with the primary language (usually the one with the entry point), then set up secondary languages.

## Error Handling

When errors occur during project setup, follow these resolution steps:

1. **Language detection returns "unknown"** — If no recognizable project files are found, check that you are in the correct project root directory. Look for hidden configuration files (for example `.python-version`, `.nvmrc`). If the project is truly empty, ask the orchestrator (AMOA) for the intended language before proceeding.
2. **Package manager command exits with non-zero code** — Do not attempt fallback package managers. Read the exact error message, check whether the package manager binary is installed and on PATH, and verify the correct version is available. Report the exact error to AMOA if the binary is missing.
3. **Dependency version conflict during installation** — Read the conflict message to identify which packages have incompatible version requirements. Do not downgrade or remove packages without orchestrator approval. Report the specific conflicting packages and versions to AMOA.
4. **Linter produces configuration parse errors** — Verify the configuration file syntax matches the linter version installed. Common cause: using configuration keys from a newer version of the linter than what is installed. Check the installed linter version with its `--version` flag.
5. **Test framework import errors on first run** — This usually means the testing library was not included in the dependency installation step. Verify the test dependency is listed in the project manifest (for example `[tool.pytest]` in `pyproject.toml`) and re-run dependency installation.
6. **SERENA MCP activation timeout** — Verify the SERENA MCP server process is running. Check the MCP configuration in `.claude/settings.json`. If the server is not configured, follow the full activation procedure in [op-activate-serena-mcp.md](references/op-activate-serena-mcp.md).
    Sections: When to Use · Prerequisites · Procedure
7. **Permission denied errors on any step** — Do not use `sudo` or change file ownership. Report the permission issue and the exact file path to AMOA for resolution.

## Examples

### Example 1: Setting Up a Python Project

Scenario: You receive a task to work on a Python library project that has a `pyproject.toml` but no virtual environment or linting configuration.

```
Step 1: Read this SKILL.md (done).
Step 2: Navigate to {baseDir}/my-python-lib and confirm write access.
Step 3: Run language detection. Found pyproject.toml and src/*.py files. Detected language: Python.
Step 4: Run "uv venv --python 3.12" to create virtual environment, then "source .venv/bin/activate" (Windows: .venv\Scripts\activate.bat or .venv\Scripts\Activate.ps1).
        Verify with "uv --version". Output: "uv 0.7.12". Success.
Step 5: Run "uv sync" to install all dependencies from pyproject.toml.
        Output shows 47 packages installed, 0 errors. Success.
Step 6: Create ruff.toml using the AI Maestro Programmer standard template from ruff-configuration-patterns.md.
        Run "uv run ruff check src/" to verify. Output: "All checks passed". Success.
Step 7: Verify [tool.pytest.ini_options] exists in pyproject.toml.
        Run "uv run pytest --co" (collect-only) to verify framework. Output: "no tests ran". Success (framework works, no tests yet).
Step 8: Activate SERENA MCP. Run find_symbol(name="main") to verify. SERENA responds with results. Success.
Step 9: Mark all checklist items as done.
Step 10: Report to AMOA: "Project setup complete. Python 3.12, uv, ruff, pytest, SERENA all configured."
```

### Example 2: Setting Up a TypeScript Project

Scenario: You receive a task to work on a TypeScript web application that has a `package.json` but dependencies are not installed.

```
Step 1: Read this SKILL.md (done).
Step 2: Navigate to {baseDir}/my-ts-app and confirm write access.
Step 3: Run language detection. Found package.json with "typescript" in devDependencies and src/*.ts files.
        Detected language: TypeScript.
Step 4: Check for bun.lockb or pnpm-lock.yaml. Found bun.lockb. Package manager: bun.
        Run "bun --version". Output: "1.2.5". Success.
Step 5: Run "bun install" to install all dependencies.
        Output shows 312 packages installed, 0 errors. Success.
Step 6: Check for existing .eslintrc or eslint.config.js. Found eslint.config.js already present.
        Run "bun run eslint src/" to verify. Output: "0 errors, 2 warnings". Success (configuration works).
Step 7: Check package.json scripts for test command. Found "test": "vitest".
        Run "bun run vitest --run" to verify framework. Output: "Test Files: 3 passed". Success.
Step 8: Activate SERENA MCP. Run find_symbol(name="App") to verify. SERENA responds. Success.
Step 9: Mark all checklist items as done.
Step 10: Report to AMOA: "Project setup complete. TypeScript, bun, eslint, vitest, SERENA all configured."
```

### Example 3: Setting Up a Rust Project

Scenario: You receive a task to work on a Rust command-line tool project with an existing `Cargo.toml`.

```
Step 1: Read this SKILL.md (done).
Step 2: Navigate to {baseDir}/my-rust-cli and confirm write access.
Step 3: Run language detection. Found Cargo.toml and src/main.rs. Detected language: Rust.
Step 4: Cargo is the default package manager for Rust. Run "cargo --version".
        Output: "cargo 1.82.0". Success.
Step 5: Run "cargo build" to fetch and install all dependencies.
        Output: "Compiling 23 crates, Finished dev target". Success.
Step 6: Clippy is the standard Rust linter. Run "cargo clippy -- -D warnings" to verify.
        Output: "Checking my-rust-cli... Finished". Success.
Step 7: Run "cargo test" to verify the test framework.
        Output: "running 5 tests... test result: ok. 5 passed". Success.
Step 8: Activate SERENA MCP. Run find_symbol(name="main") to verify. SERENA responds. Success.
Step 9: Mark all checklist items as done.
Step 10: Report to AMOA: "Project setup complete. Rust 1.82, cargo, clippy, cargo test, SERENA all configured."
```

## Resources

Related skills and documentation for the AMPA programmer agent:

- **[op-detect-project-language.md](references/op-detect-project-language.md)** — Detailed procedure for identifying the programming language of a project based on file patterns and configuration files.
  Sections: When to Use · Prerequisites · Procedure
- **[op-initialize-package-manager.md](references/op-initialize-package-manager.md)** — Language-specific package manager initialization procedures for all eight supported languages.
  Sections: When to Use · Prerequisites · Procedure
- **[op-install-dependencies.md](references/op-install-dependencies.md)** — Dependency installation procedures, virtual environment management, and conflict resolution.
  Sections: When to Use · Prerequisites · Procedure
- **[op-configure-linting.md](references/op-configure-linting.md)** — Linter configuration templates and verification procedures for each supported language.
  Sections: When to Use · Prerequisites · Procedure
- **[ruff-configuration-patterns.md](references/ruff-configuration-patterns.md)** — Standard ruff.toml template for Python projects, including rule explanations and customization guidance.
  Sections: When to configure ruff for a new project · Standard ruff.toml template for AI Maestro Programmer projects · What each rule set does and why it is enabled
- **[op-setup-testing-framework.md](references/op-setup-testing-framework.md)** — Testing framework configuration for pytest, jest, vitest, cargo test, go test, and others.
  Sections: When to Use · Prerequisites · Procedure
- **[op-activate-serena-mcp.md](references/op-activate-serena-mcp.md)** — SERENA MCP activation procedure, verification, and troubleshooting.
  Sections: When to Use · Prerequisites · Procedure
- **Coding Standards** — See the project's own coding standards or linting configuration (configured via `op-configure-linting`).
- **AMPA Task Execution skill** (`ampa-task-execution`) — The next skill to use after project setup, covering how to execute assigned implementation tasks.
