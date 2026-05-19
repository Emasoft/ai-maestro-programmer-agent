# AI Maestro Programmer Agent (AMPA)

**Version**: 1.0.26

## Overview

The AI Maestro Programmer Agent is a **general-purpose programmer** that
executes implementation tasks assigned by the Orchestrator. It handles the
actual coding work across multiple programming languages and toolchains.

> **Standalone or Orchestrated**: This plugin works in two modes. In
> **standalone mode**, the agent receives tasks directly from the user and
> reports back in conversation. In **orchestrated mode** (within the AI Maestro
> ecosystem), it receives tasks from the Orchestrator (AMOA) via messaging. No
> additional setup is needed for standalone mode.

### Implementer Agents

In the AI Maestro ecosystem, **implementers** are agents that produce artifacts.
The Programmer Agent (AMPA) is one subtype of implementer — it produces code,
tests, and pull requests. Other implementer subtypes include artists (visual
assets), SFX experts (audio assets), and more. All implementers share the same
role (`implementer`) in team registries but use subtype-specific plugins and
naming (e.g., `svgbbox-programmer-001`).

**Prefix**: `ampa-` = AI Maestro Programmer Agent

## Core Responsibilities

1. **Code Implementation**: Write and modify source code according to
   specifications
2. **Test Writing**: Create comprehensive test suites
3. **Code Fixing**: Resolve bugs and linting/type errors
4. **Documentation**: Write inline documentation and docstrings
5. **Multi-Language Support**: Work across Python, JavaScript, Rust, Go, and
   compiled languages

## Components

### Agent (1)

| Agent                                    | File                                               | Description                           |
| ---------------------------------------- | -------------------------------------------------- | ------------------------------------- |
| `ai-maestro-programmer-agent-main-agent` | `agents/ai-maestro-programmer-agent-main-agent.md` | Main general-purpose programmer agent |

### Skills (5)

| Skill                             | Description                                           |
| --------------------------------- | ----------------------------------------------------- |
| `ampa-task-execution`             | Execute programming tasks per requirements            |
| `ampa-orchestrator-communication` | Communication with the Orchestrator (AMOA) agent      |
| `ampa-github-operations`          | Git and GitHub operations (clone, branch, commit, PR) |
| `ampa-project-setup`              | Initialize project configuration and install tooling  |
| `ampa-handoff-management`         | Create and receive handoff documents and bug reports  |

### Hooks

None. The `hooks/hooks.json` is empty -- AMPA uses globally installed hooks.

### Scripts

The `scripts/` directory contains 24 Python scripts: 18 CPV (Claude Plugins
Validation) scripts covering plugin structure, agents, skills, hooks, security,
encoding, documentation, and more, plus 6 project utility scripts. The entry
point is `validate_plugin.py`. CPV scripts are auto-synced from
`Emasoft/claude-plugins-validation` via `sync_cpv_scripts.py`.

| Script                   | Description                                               |
| ------------------------ | --------------------------------------------------------- |
| `validate_plugin.py`     | CPV suite entry point — runs all validation checks        |
| `pre-push-hook.py`       | Git pre-push hook — runs validation before each push      |
| `sync_cpv_scripts.py`    | Sync CPV validation scripts from upstream GitHub releases |
| `test_order_pipeline.py` | OrderPipeline validation test suite                       |
| `lint_files.py`          | Lint and format Python source files                       |
| `gitignore_filter.py`    | Filter file lists against .gitignore patterns             |
| `smart_exec.py`          | Cross-platform script executor with timeout support       |

### Token-Efficient Reporting

Project scripts support file-based reporting to minimize terminal output:

| Script                   | Flag                              | Description                                                    |
| ------------------------ | --------------------------------- | -------------------------------------------------------------- |
| `test_order_pipeline.py` | `--report-file PATH`              | Write full test report to file; terminal gets concise summary  |
| `sync_cpv_scripts.py`    | `--report-file PATH`              | Write full sync log to file; terminal gets concise summary     |
| `pre-push-hook.py`       | `AMPA_REPORT_FILE=PATH` (env var) | Write validation output to file; terminal gets concise summary |

## Workflow

The Programmer Agent follows **Steps 14, 15, 17-19, 21-23** from the master
workflow:

1. **Step 14**: Request Clarification from Orchestrator
2. **Step 15**: Receive Feedback and Design Updates
3. **Step 17**: Task Execution (code, lint, test)
4. **Step 19**: Task Completion (create PR, notify)
5. **Step 21**: Respond to PR Review Feedback
6. **Step 22**: Handle Failed PR (fix and resubmit)

## Installation (Production)

Role plugins are installed with `--scope local` inside the specific agent's
working directory (`~/agents/<agent-name>/`). This ensures the plugin is only
available to that agent.

```bash
# RESTART Claude Code after installing (required!)
```

### Installation (from GitHub)

```bash
claude plugin install ai-maestro-programmer-agent --url https://github.com/Emasoft/ai-maestro-programmer-agent
```

### Installation (from git subdirectory)

If this plugin lives inside a parent repository, use the `git-subdir` source
type:

```bash
claude plugin install ai-maestro-programmer-agent --url https://github.com/Emasoft/EMASOFT-PROGRAMMER-AGENT --subdir ai-maestro-programmer-agent
```

Once installed, start a session with the main agent:

```bash
claude --agent ai-maestro-programmer-agent-main-agent
```

## Recommended Companion Plugins

| Plugin             | Purpose                                                                                                          | Install                                  |
| ------------------ | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `llm-externalizer` | Offload file analysis, scanning, and comparison to cheaper local/remote LLMs — saves orchestrator context tokens | `claude plugin install llm-externalizer` |

When `llm-externalizer` is installed alongside this plugin, the agent
automatically uses it for code analysis (`code_task`), codebase scanning
(`scan_folder`), per-file independent audits (`code_task` with
`answer_mode: 0` and `max_retries: 3`), and post-refactoring validation
(`check_references`, `check_imports`).

## Getting Started

1. **Install the plugin** using the command from the Installation section above.
2. **Launch the agent** in your project directory:
   ```bash
   cd your-project/
   claude --agent ai-maestro-programmer-agent-main-agent
   ```
3. **In standalone mode** (no orchestrator), describe your task directly in the
   conversation. The agent will set up the project environment, implement the
   code, write tests, and commit the changes.
4. **In orchestrated mode** (with AI Maestro running), the agent receives tasks
   automatically from the AMOA orchestrator via inter-agent messaging. See
   `docs/FULL_PROJECT_WORKFLOW.md` for the complete multi-agent workflow.

## Development Only (--plugin-dir)

`--plugin-dir` loads a plugin directly from a local directory without
marketplace installation. Use only during plugin development.

```bash
claude --plugin-dir .
```

After modifying plugin files, use `/reload-plugins` in your Claude Code session
to activate changes without restarting.

A pre-push git hook (`scripts/pre-push-hook.py`) runs the validation suite
before each push. Install it with:

```bash
cp scripts/pre-push-hook.py .git/hooks/pre-push && chmod +x .git/hooks/pre-push
```

### Proxy / TLS Note

If you are behind a corporate proxy (MITM) and `gh` CLI fails with TLS errors,
enable weaker network isolation in your Claude Code settings:

```json
{ "sandbox": { "enableWeakerNetworkIsolation": true } }
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

| Language                  | Toolchain     | Linter        | Formatter      | Type Checker |
| ------------------------- | ------------- | ------------- | -------------- | ------------ |
| **Python**                | `uv`          | `ruff check`  | `ruff format`  | `mypy`       |
| **JavaScript/TypeScript** | `bun`         | `eslint`      | `prettier`     | `tsc`        |
| **Rust**                  | `cargo`       | `clippy`      | `rustfmt`      | Built-in     |
| **Go**                    | `go`          | `staticcheck` | `gofmt`        | Built-in     |
| **.NET (C#/F#)**          | `dotnet`      | Built-in      | Built-in       | Built-in     |
| **C/C++**                 | `gcc`/`clang` | `clang-tidy`  | `clang-format` | Built-in     |
| **Objective-C**           | `clang`       | `clang-tidy`  | `clang-format` | Built-in     |
| **Swift**                 | `swift`       | `swiftlint`   | `swift-format` | Built-in     |

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
uv run --with pyyaml python scripts/validate_plugin.py . --verbose
```

If `uv` is not available, use `python3 scripts/validate_plugin.py . --verbose`
with PyYAML installed.

### CI/CD

- `validate.yml` — Runs plugin validation on push to main and PRs
- `release.yml` — Creates GitHub releases on version tags (`v*`)
- `notify-marketplace.yml` — Marketplace notification (currently disabled, TBD)

## Compatibility with Recent Claude Code Releases

AMPA is verified against Claude Code v2.1.105–v2.1.143. The agent itself
remains backwards-compatible with earlier Claude Code builds; the items
below describe **new platform capabilities** that AMPA users can opt into
without changing the plugin.

### Main-thread agent capabilities (v2.1.116 / v2.1.117 / v2.1.119)

When AMPA is launched with `claude --agent ai-maestro-programmer-agent-main-agent`,
Claude Code now reads three additional fields from the agent frontmatter:

| Field            | Effect                                                                                   | Added in |
| ---------------- | ---------------------------------------------------------------------------------------- | -------- |
| `mcpServers`     | MCP servers are pre-loaded for the main-thread session — useful for declaring SERENA/LLM-Externalizer requirements at agent invocation time | v2.1.117 |
| `hooks:`         | Agent-level hooks fire on the main-thread session (previously subagent-only)             | v2.1.116 |
| `permissionMode` | `--agent` honors the agent's declared permission mode                                    | v2.1.119 |

AMPA does **not** ship hard-coded `mcpServers` entries because SERENA MCP and
LLM Externalizer are typically configured globally via the user's
`.mcp.json` or via the `llm-externalizer` plugin's own server registration.
Operators who want SERENA pre-loaded at `--agent` startup can extend the
agent frontmatter in their own fork.

### Hook authoring (v2.1.139)

When extending AMPA with hooks (project- or plugin-scope), prefer the
exec-form `args: string[]` field over the shell-form `command:` string:

```json
{
  "type": "command",
  "args": ["uv", "run", "scripts/pre-push-hook.py", "$CLAUDE_PROJECT_DIR"]
}
```

Exec form spawns the command directly without a shell, so path placeholders
never need quoting and there is no shell-injection surface.

`PreCompact` hooks (v2.1.105) can block compaction — exit code 2 or
`{"decision":"block"}` from a `PreCompact` hook keeps the current
conversation intact. Useful for long task-execution flows where compaction
mid-task would lose state.

### Effort and caching (v2.1.108 / v2.1.120 / v2.1.133)

- `ENABLE_PROMPT_CACHING_1H=1` extends the prompt-cache TTL to 1 hour for
  API-key / Bedrock / Vertex / Foundry users. Recommended for long
  programmer sessions where AMPA re-reads the same project files turn after
  turn.
- Skills and hooks now see the active effort level via `${CLAUDE_EFFORT}`
  (skills) and `$CLAUDE_EFFORT` (Bash tool / hook env). AMPA skills can
  dial scan depth up/down based on this value when relevant.
- `xhigh` effort level (v2.1.111) is available on Opus 4.7 for the most
  thorough analyses; AMPA does not pin an effort level, so users control it
  via `/effort`.

### New commands and OTel events worth knowing

| Surface                          | What it does                                                  | Added in |
| -------------------------------- | ------------------------------------------------------------- | -------- |
| `/goal`                          | Set a completion condition; Claude keeps working across turns | v2.1.139 |
| `/ultrareview` / `claude ultrareview` | Parallel multi-agent code review; CI-friendly via the CLI subcommand | v2.1.111 / v2.1.120 |
| `/less-permission-prompts`       | Scans transcripts for read-only Bash/MCP calls and proposes an allowlist | v2.1.111 |
| `claude project purge`           | Wipe all Claude Code state for a project                      | v2.1.126 |
| `claude_code.skill_activated`    | OpenTelemetry event with `invocation_trigger` attribute       | v2.1.126 |
| `worktree.bgIsolation: "none"`   | Lets background sessions edit the working copy directly       | v2.1.143 |

### Plugin manifest changes (v2.1.129 / v2.1.143)

- `themes` and `monitors` should now live under `"experimental": { ... }`
  in `plugin.json`. AMPA ships neither, so no migration is required.
- `claude plugin disable` now refuses to disable a plugin that another
  enabled plugin depends on (with a copy-pasteable disable-chain hint).
  `claude plugin enable` force-enables transitive dependencies. AMPA has no
  declared dependencies on other plugins, so this only matters for
  operators bundling AMPA inside a meta-plugin.

## See Also

> **Related Plugins**: This agent works with the AI Maestro Orchestrator Agent
> (AMOA), AI Maestro Integrator Agent (AMIA), and AI Maestro Architect Agent
> (AMAA). Each agent plugin is installed independently. These plugins are part
> of the AI Maestro ecosystem and are not required for standalone use. AMPA is
> an **implementer** (artifact-producing agent). Future implementer subtypes
> (artist, sfx-expert, etc.) will follow the same patterns.
