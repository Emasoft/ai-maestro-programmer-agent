# AI Maestro Programmer Agent (AMPA)

**Version**: 1.0.6

## Overview

The AI Maestro Programmer Agent is a **general-purpose programmer** that executes implementation tasks assigned by the Orchestrator. It handles the actual coding work across multiple programming languages and toolchains.

> **Standalone or Orchestrated**: This plugin works in two modes. In **standalone mode**, the agent receives tasks directly from the user and reports back in conversation. In **orchestrated mode** (within the AI Maestro ecosystem), it receives tasks from the Orchestrator (AMOA) via messaging. No additional setup is needed for standalone mode.

### Implementer Agents

In the AI Maestro ecosystem, **implementers** are agents that produce artifacts. The Programmer Agent (AMPA) is one subtype of implementer — it produces code, tests, and pull requests. Other implementer subtypes include artists (visual assets), SFX experts (audio assets), and more. All implementers share the same role (`implementer`) in team registries but use subtype-specific plugins and naming (e.g., `svgbbox-programmer-001`).

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
| `ampa-orchestrator-communication` | Communication with the Orchestrator (AMOA) agent |
| `ampa-github-operations` | Git and GitHub operations (clone, branch, commit, PR) |
| `ampa-project-setup` | Initialize project configuration and install tooling |
| `ampa-handoff-management` | Create and receive handoff documents and bug reports |

### Hooks

None. The `hooks/hooks.json` is empty -- AMPA uses globally installed hooks.

### Scripts

The `scripts/` directory contains the CPV (Claude Plugins Validation) suite — 21 validation scripts covering plugin structure, agents, skills, hooks, security, encoding, documentation, and more. The entry point is `validate_plugin.py`. Scripts are auto-synced from `Emasoft/claude-plugins-validation` via `sync_cpv_scripts.py`.

| Script | Description |
|--------|-------------|
| `validate_plugin.py` | CPV suite entry point — runs all validation checks |

## Workflow

The Programmer Agent follows **Steps 14, 15, 17-19, 21-23** from the master workflow:

1. **Step 14**: Request Clarification from Orchestrator
2. **Step 15**: Receive Feedback and Design Updates
3. **Step 17**: Task Execution (code, lint, test)
4. **Step 19**: Task Completion (create PR, notify)
5. **Step 21**: Respond to PR Review Feedback
6. **Step 22**: Handle Failed PR (fix and resubmit)

## Installation (Production)

Role plugins are installed with `--scope local` inside the specific agent's working directory (`~/agents/<agent-name>/`). This ensures the plugin is only available to that agent.

```bash
# RESTART Claude Code after installing (required!)
```

### Installation (from GitHub)

```bash
claude plugin install ai-maestro-programmer-agent --url https://github.com/Emasoft/ai-maestro-programmer-agent
```

Once installed, start a session with the main agent:

```bash
claude --agent ampa-programmer-main-agent
```

## Getting Started

1. **Install the plugin** using the command from the Installation section above.
2. **Launch the agent** in your project directory:
   ```bash
   cd your-project/
   claude --agent ampa-programmer-main-agent
   ```
3. **In standalone mode** (no orchestrator), describe your task directly in the conversation. The agent will set up the project environment, implement the code, write tests, and commit the changes.
4. **In orchestrated mode** (with AI Maestro running), the agent receives tasks automatically from the AMOA orchestrator via inter-agent messaging. See `docs/FULL_PROJECT_WORKFLOW.md` for the complete multi-agent workflow.

## Development Only (--plugin-dir)

`--plugin-dir` loads a plugin directly from a local directory without marketplace installation. Use only during plugin development.

```bash
claude --plugin-dir .
```

A pre-push git hook (`git-hooks/pre-push`) runs the validation suite before each push. Install it with:

```bash
cp git-hooks/pre-push .git/hooks/pre-push && chmod +x .git/hooks/pre-push
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
| **Go** | `go` | `staticcheck` | `gofmt` | Built-in |
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
uv run python scripts/validate_plugin.py . --verbose
```

### CI/CD

- `validate.yml` — Runs plugin validation on push to main and PRs
- `release.yml` — Creates GitHub releases on version tags (`v*`)
- `notify-marketplace.yml` — Marketplace notification (currently disabled, TBD)

## See Also

> **Related Plugins**: This agent works with the AI Maestro Orchestrator Agent (AMOA), AI Maestro Integrator Agent (AMIA), and AI Maestro Architect Agent (AMAA). Each agent plugin is installed independently. These plugins are part of the AI Maestro ecosystem and are not required for standalone use. AMPA is an **implementer** (artifact-producing agent). Future implementer subtypes (artist, sfx-expert, etc.) will follow the same patterns.

