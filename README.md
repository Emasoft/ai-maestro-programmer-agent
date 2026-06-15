# AI Maestro Programmer Agent (AMPA)

A general-purpose, multi-language programmer agent for Claude Code that
implements, tests, fixes, and documents code across Python,
JavaScript/TypeScript, Rust, Go, and other toolchains — either standalone or
orchestrated within the AI Maestro ecosystem. The current version is recorded
in `.claude-plugin/plugin.json` (the single source of truth).

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

### Skills (6)

| Skill                             | Description                                           |
| --------------------------------- | ----------------------------------------------------- |
| `ampa-task-execution`             | Execute programming tasks per requirements            |
| `ampa-orchestrator-communication` | Communication with the Orchestrator (AMOA) agent      |
| `ampa-github-operations`          | Git and GitHub operations (clone, branch, commit, PR) |
| `ampa-project-setup`              | Initialize project configuration and install tooling  |
| `ampa-handoff-management`         | Create and receive handoff documents and bug reports  |
| `ampa-prrd-trdd-kanban`           | The MEMBER (programmer) role in the PRRD / TRDD / kanban workflow |

### Memory (global, janitor-hosted)

This plugin uses the **global** AI-Maestro markdown memory system — it ships
**no** per-plugin memory skills or `rules/` mirror. Recall / write / update go
through the global `janitor-memory-recall` / `-write` / `-update` skills; the
protocol + recall law live in `~/.claude/rules/markdown-memory-recall.md`; the
project's memory contract + scope routing live in [`CLAUDE.md`](CLAUDE.md). The
git-tracked PROJECT-scope wiki is `.claude/project/memory/` (stood up once via
`/janitor-memory-bootstrap`). The `memgrep` binary (from `ai-maestro-janitor`)
powers recall and degrades to `grep` when absent — recall degrades, never
breaks.

### Hooks

None. The `hooks/hooks.json` is empty -- AMPA uses globally installed hooks.

### Scripts

The `scripts/` directory contains 5 project utility scripts. Plugin
validation runs through the **CPV remote launcher**
(`uvx … cpv-remote-validate`), fetched on demand from
`Emasoft/claude-plugins-validation` — the previously vendored CPV validator
scripts were retired (CI and `publish.py` both call the remote validator,
so local copies only drifted behind upstream).

| Script                   | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| `publish.py`             | Strict release pipeline — test, lint, validate, bump, push    |
| `pre-push-hook.py`       | Git pre-push hook — runs cpv-remote-validate before each push |
| `test_order_pipeline.py` | OrderPipeline validation test suite                           |
| `smart_exec.py`          | Cross-platform script executor with timeout support           |

### Token-Efficient Reporting

Project scripts support file-based reporting to minimize terminal output:

| Script                   | Flag                              | Description                                                    |
| ------------------------ | --------------------------------- | -------------------------------------------------------------- |
| `test_order_pipeline.py` | `--report-file PATH`              | Write full test report to file; terminal gets concise summary  |
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

## Usage

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

Validation runs through the CPV remote launcher — the exact command CI's
`validate.yml` uses:

```bash
uvx --from git+https://github.com/Emasoft/claude-plugins-validation \
    --with pyyaml \
    cpv-remote-validate plugin . --strict
```

Exit codes: 0 = PASS; 1-4 (CRITICAL/MAJOR/MINOR/NIT) all block in strict
mode. `uvx` ships with [uv](https://docs.astral.sh/uv/).

### CI/CD

- `validate.yml` — Runs plugin validation on push to main and PRs
- `release.yml` — Creates GitHub releases on version tags (`v*`)
- `notify-marketplace.yml` — Dispatches a `plugin-updated` event to the marketplace repo when plugin files change on `main`

## Compatibility with Recent Claude Code Releases

AMPA is verified against Claude Code v2.1.105–v2.1.178. The agent itself
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
  `claude plugin enable` force-enables transitive dependencies. AMPA
  **declares one dependency** (`ai-maestro-plugin`, the 3-pillars scripts),
  so `claude plugin enable ai-maestro-programmer-agent` force-enables it.

### Newer releases (v2.1.144 – v2.1.178)

| Change | Effect on AMPA | Added in |
| ------ | -------------- | -------- |
| **Subagent nesting** (up to 5 levels) | AMPA's spawned sub-agents may now spawn their own — useful for fan-out; sub-agent `disallowedTools` MCP specs (`mcp__server`) are honored | v2.1.172 |
| **`disallowed-tools` skill/command frontmatter** + `/reload-skills` | A skill/command can drop tools while active; skill dirs re-scan without restart | v2.1.152 |
| **Plugins declare `.mcp.json`** + `defaultEnabled: false` | A plugin may ship MCP servers and ship disabled-by-default; AMPA ships neither | v2.1.154 |
| **`Tool(param:value)` permission rules** | e.g. `Agent(model:opus)` / `WebFetch(domain:*.example.com)` — finer allow/deny operators can apply to AMPA's tool use | v2.1.176 / v2.1.178 |
| **Nested-skills loading** | Skills under a nested `.claude/skills/` load when working there; on a name clash they appear as `<dir>:<name>` | v2.1.178 |
| **`post-session` hook** + `disableBundledSkills` | New end-of-session lifecycle hook; a setting to hide bundled skills from the model | v2.1.169 |
| **Dynamic-workflow keyword `workflow` → `ultracode`** | The word "workflow" no longer auto-triggers; AMPA prose is unaffected (it never relied on auto-trigger) | v2.1.161 |
| **`/simplify` → `/code-review`** (`--fix`, `--comment`) | If operators wire AMPA into a review step, use `/code-review` | v2.1.147 / v2.1.152 |
| **Lean system prompt default; Opus 4.8** | AMPA pins no model/effort, so it inherits the session's — no change needed | v2.1.154 |

None of these require an AMPA code change — the plugin stays
backwards-compatible. They are documented so operators know what the latest
platform offers a programmer agent.

## See Also

> **Related Plugins**: This agent works with the AI Maestro Orchestrator Agent
> (AMOA), AI Maestro Integrator Agent (AMIA), and AI Maestro Architect Agent
> (AMAA). Each agent plugin is installed independently. These plugins are part
> of the AI Maestro ecosystem and are not required for standalone use. AMPA is
> an **implementer** (artifact-producing agent). Future implementer subtypes
> (artist, sfx-expert, etc.) will follow the same patterns.
