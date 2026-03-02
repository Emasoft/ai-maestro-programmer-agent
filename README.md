# AI Maestro Programmer Agent (AMPA)

**Version**: 1.0.0

## Overview

The AI Maestro Programmer Agent is a **general-purpose programmer** that executes implementation tasks assigned by the Orchestrator. It handles the actual coding work across multiple programming languages and toolchains.

**Prefix**: `ampa-` = AI Maestro Programmer Agent

## Core Responsibilities

1. **Code Implementation**: Write and modify source code according to specifications
2. **Test Writing**: Create comprehensive test suites
3. **Code Fixing**: Resolve bugs and linting/type errors
4. **Documentation**: Write inline documentation and docstrings
5. **Multi-Language Support**: Work across Python, JavaScript, Rust, Go, and compiled languages

## Components

### Agent (1)

| Agent | File | Description |
|-------|------|-------------|
| `ampa-programmer-main-agent` | `agents/ampa-programmer-main-agent.md` | Main general-purpose programmer agent |

### Skills (5)

| Skill | Description |
|-------|-------------|
| `ampa-task-execution` | Execute programming tasks per requirements |
| `ampa-orchestrator-communication` | Communication with the Orchestrator (EOA) agent |
| `ampa-github-operations` | Git and GitHub operations (clone, branch, commit, PR) |
| `ampa-project-setup` | Initialize project configuration and install tooling |
| `ampa-handoff-management` | Create and receive handoff documents and bug reports |

### Hooks

None. The `hooks/hooks.json` is empty -- AMPA uses globally installed hooks.

### Scripts (1)

| Script | Description |
|--------|-------------|
| `validate_plugin.py` | Plugin structure validator |

## Workflow

The Programmer Agent follows **Steps 14, 15, 17-19, 21-23** from the master workflow:

1. **Step 14**: Receive task from Orchestrator via AI Maestro
2. **Step 15**: Investigate code context using SERENA MCP
3. **Step 17**: Implement changes using Edit tool (NOT scripts)
4. **Step 18**: Run language-specific linter/formatter/type checker
5. **Step 19**: Write/update tests for changed code
6. **Step 21**: Run tests and capture results to timestamped log
7. **Step 22**: If tests fail, delegate to code fixer and repeat
8. **Step 23**: Report completion to Orchestrator with file paths

## Installation (Production)

Role plugins are installed with `--scope local` inside the specific agent's working directory (`~/agents/<agent-name>/`). This ensures the plugin is only available to that agent.

```bash
# NOTE: Marketplace install is TBD
# claude plugin marketplace add emasoft-plugins --url https://github.com/Emasoft/emasoft-plugins
# claude plugin install ai-maestro-programmer-agent@emasoft-plugins --scope local

# RESTART Claude Code after installing (required!)
```

Once installed, start a session with the main agent:

```bash
claude --agent ampa-programmer-main-agent
```

## Development Only (--plugin-dir)

`--plugin-dir` loads a plugin directly from a local directory without marketplace installation. Use only during plugin development.

```bash
claude --plugin-dir ./OUTPUT_SKILLS/ai-maestro-programmer-agent
```

## Requirements

### SERENA MCP (REQUIRED)

The Programmer Agent relies on SERENA MCP for code investigation:
- Symbol search
- Function/class lookup
- Call graph analysis
- Import/dependency tracking

**SERENA must be available before starting work.**

## Supported Languages

| Language | Toolchain | Linter | Formatter | Type Checker |
|----------|-----------|--------|-----------|--------------|
| **Python** | `uv` | `ruff check` | `ruff format` | `mypy` |
| **JavaScript/TypeScript** | `bun` | `eslint` | `prettier` | `tsc` |
| **Rust** | `cargo` | `clippy` | `rustfmt` | Built-in |
| **Go** | `go` | `golint` | `gofmt` | Built-in |
| **.NET (C#/F#)** | `dotnet` | Built-in | Built-in | Built-in |
| **C/C++** | `gcc`/`clang` | `clang-tidy` | `clang-format` | Built-in |
| **Objective-C** | `clang` | `clang-tidy` | `clang-format` | Built-in |
| **Swift** | `swift` | `swiftlint` | `swift-format` | Built-in |

## Troubleshooting

### Plugin Not Loading

**Symptom**: Commands/agents not available after installation

**Cause**: Claude Code caches plugin metadata

**Solution**: Restart Claude Code after installation/updates

### SERENA MCP Not Available

**Symptom**: Code investigation fails with "SERENA not available"

**Cause**: SERENA MCP server not configured or not running

**Solution**:
1. Verify SERENA MCP is configured in Claude Code settings
2. Check MCP server is running: `curl http://localhost:PORT/health`
3. Restart Claude Code to reconnect to MCP servers

### Tests Not Running

**Symptom**: Tests fail with "command not found"

**Cause**: Language toolchain not installed or not in PATH

**Solution**:
1. Install required toolchain (see Supported Languages table)
2. Verify toolchain is in PATH: `which uv` / `which bun` / etc.
3. Restart terminal/Claude Code to pick up PATH changes

### Code Fixer Agent Failing

**Symptom**: Code fixer reports "Unable to fix errors"

**Cause**: Linter/formatter errors require manual intervention

**Solution**:
1. Review error logs in `tests/logs/`
2. Manual fix may be required for complex issues
3. Report blocking issues to Orchestrator

## Validation

```bash
cd OUTPUT_SKILLS/ai-maestro-programmer-agent
uv run python scripts/validate_plugin.py . --verbose
```

## See Also

> **Related Plugins**: This agent works with the AI Maestro Orchestrator Agent (EOA), AI Maestro Integrator Agent (EIA), and AI Maestro Architect Agent (EAA). Each agent plugin is installed independently.

