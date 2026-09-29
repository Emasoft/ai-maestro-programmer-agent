# AI Maestro Programmer Agent (AMPA)

![version](https://img.shields.io/badge/version-2.0.12-blue)

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
| `ampa-prrd-trdd-kanban`           | The MEMBER (programmer) role POLICY over the granular ama-* pillar skills — op-set, self-mandate rule, missing-derived-TRDD duty |

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

The `scripts/` directory contains 4 project utility scripts. Plugin
validation runs through the **CPV remote launcher**
(`uvx … cpv-remote-validate`), fetched on demand from
`Emasoft/claude-plugins-validation` — the previously vendored CPV validator
scripts were retired (CI and `publish.py` both call the remote validator,
so local copies only drifted behind upstream).

| Script                   | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| `publish.py`             | Strict release pipeline — test, lint, validate, bump, tag (`v{version}` + the `{name}--v{version}` dependency-resolution tag), atomic push |
| `pre-push-hook.py`       | Git pre-push hook — runs cpv-remote-validate before each push |
| `test_order_pipeline.py` | Manual integration test for the order-processing-pipeline example (companion to `op-notify-completion.md`) |
| `smart_exec.py`          | Cross-platform script executor with timeout support           |

### Token-Efficient Reporting

Project scripts support file-based reporting to minimize terminal output:

| Script                   | Flag                              | Description                                                    |
| ------------------------ | --------------------------------- | -------------------------------------------------------------- |
| `test_order_pipeline.py` | `--report-file PATH`              | Write full test report to file; terminal gets concise summary  |
| `pre-push-hook.py`       | `AMPA_REPORT_FILE=PATH` (env var) | Write validation output to file; terminal gets concise summary |

## Workflow

The Programmer Agent owns **Steps 14, 15, 17, 19, 21, 22** from the master
workflow (the implementer's slice; the intervening Steps 16, 18, 20, 23 are
owned by AMOA/AMIA — see `docs/FULL_PROJECT_WORKFLOW.md`):

1. **Step 14**: Request Clarification from Orchestrator
2. **Step 15**: Receive Feedback and Design Updates
3. **Step 17**: Task Execution (code, lint, test)
4. **Step 19**: Pre-PR Gate + PR Creation (after AMOA's green-light)
5. **Step 21**: Respond to PR Review Feedback
6. **Step 22**: Handle Failed PR (fix and resubmit)

## Installation (Production)

Role plugins are installed with `--scope local` inside the specific agent's
working directory (`~/agents/<agent-name>/`). This ensures the plugin is only
available to that agent. Use one of the install commands below, then **restart
Claude Code** — plugin metadata is cached and only picked up on a fresh start.

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

1. Review the linter/formatter errors the fixer reported in its output
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

AMPA is verified against Claude Code v2.1.105–**v2.1.284**. Most items below
describe **new platform capabilities** that AMPA users can opt into without
changing the plugin — but four changes altered how AMPA *executes* and required
fixes: two in the v2.1.184–v2.1.224 range, one in v2.1.232, and one in v2.1.239.
Each is marked **Breaking** in its table.

The v2.1.241–v2.1.248 range added **no** Breaking change — nothing AMPA ships
stopped working — but it did require three substantive updates (two persona
paragraphs, one SERENA diagnostic branch) and three new packaging guards. Those
rows say what was changed and where; every other row in that table is a
verified no-op recorded so the next reader does not have to re-check it.

The one row that might look Breaking is **`--restricted`**, and it is not, by
this section's own test: every existing **Breaking** row is a *silent behavioural
change to a shipped artifact* (skills returned handles; a preload was inert;
spawns backgrounded; BOM'd files never loaded). `--restricted` is a mode the
operator opts into, under which AMPA's bytes behave identically — a constraint on
where AMPA can run, not a change to what it does.

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
- `xhigh` effort level (v2.1.111) is available on the current Opus generation
  (introduced on Opus 4.7, carried forward to Opus 4.8) for the most thorough
  analyses; AMPA does not pin an effort level, so users control it via
  `/effort`.

### New commands and OTel events worth knowing

| Surface                          | What it does                                                  | Added in |
| -------------------------------- | ------------------------------------------------------------- | -------- |
| `/goal`                          | Set a completion condition; Claude keeps working across turns | v2.1.139 |
| `/ultrareview` / `claude ultrareview` | Parallel multi-agent code review; CI-friendly via the CLI subcommand. **Deprecated in v2.1.223** — now an alias for `/code-review ultra` | v2.1.111 / v2.1.120 |
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

### Newer releases (v2.1.144 – v2.1.183)

| Change | Effect on AMPA | Added in |
| ------ | -------------- | -------- |
| **Subagent nesting** | AMPA's spawned sub-agents may spawn their own; sub-agent `disallowedTools` MCP specs (`mcp__server`) are honored. **The depth is no longer 5** — see the v2.1.217–v2.1.224 table below for the current cap | v2.1.172 |
| **`disallowed-tools` skill/command frontmatter** + `/reload-skills` | A skill/command can drop tools while active; skill dirs re-scan without restart | v2.1.152 |
| **Plugins declare `.mcp.json`** + `defaultEnabled: false` | A plugin may ship MCP servers and ship disabled-by-default; AMPA ships neither | v2.1.154 |
| **`Tool(param:value)` permission rules** | e.g. `Agent(model:opus)` / `WebFetch(domain:*.example.com)` — finer allow/deny operators can apply to AMPA's tool use | v2.1.176 / v2.1.178 |
| **Nested-skills loading** | Skills under a nested `.claude/skills/` load when working there; on a name clash they appear as `<dir>:<name>` | v2.1.178 |
| **`post-session` hook** + `disableBundledSkills` | New end-of-session lifecycle hook; a setting to hide bundled skills from the model | v2.1.169 |
| **Dynamic-workflow keyword `workflow` → `ultracode`** | The word "workflow" no longer auto-triggers; AMPA prose is unaffected (it never relied on auto-trigger) | v2.1.161 |
| **`/simplify` → `/code-review`** (`--fix`, `--comment`) | If operators wire AMPA into a review step, use `/code-review` | v2.1.147 / v2.1.152 |
| **Lean system prompt default; Opus 4.8** | AMPA pins no model/effort, so it inherits the session's — no change needed | v2.1.154 |
| **Model-deprecation warning now covers agent frontmatter** | The warning fires (on stderr, incl. `-p`) for a deprecated/auto-updated model pinned in an agent's frontmatter. AMPA's agent pins **no** `model:` (it inherits the session's), so nothing is flagged | v2.1.183 |
| **Auto-mode destructive-git guards** | The classifier blocks `git reset --hard`, `checkout -- .`, `clean -fd`, `stash drop`, non-agent `commit --amend`, and `terraform`/`pulumi`/`cdk destroy` unless asked. AMPA's `publish.py` git ops (`commit`/`tag`/`push`) are NOT in that set, so the publish pipeline is unaffected | v2.1.183 |
| **Scheduled-task / webhook deliveries are task notifications** | In auto mode they can no longer approve a pending action or set the session title — safe for orchestrated/headless AMPA runs | v2.1.183 |
| **Foreground subagents respect the same nesting depth as background ones** | AMPA fan-out stays bounded whichever way a sub-agent is spawned. **The depth is no longer 5** — see below | v2.1.181 |
| **`/config key=value` from the prompt** | Operators can set any setting inline (e.g. `/config effort=high`); no AMPA change — AMPA pins nothing it would override | v2.1.181 |

None of the above required an AMPA code change. The next table did.

### v2.1.184 – v2.1.224 — including two changes AMPA had to act on

| Change | Effect on AMPA | Added in |
| ------ | -------------- | -------- |
| **`context: fork` skills run in the BACKGROUND by default** | **Breaking, and silent.** All six `ampa-*` skills were `context: fork` with no `background:` key, so from v2.1.218 they returned an agent handle instead of their result — the invoking agent got nothing in the turn it asked, with no error. **Fixed by removing `context: fork` entirely** (not by pinning `background: false`): a forked subagent has no AMP identity, so it can neither answer a comprehension handshake nor report a completion. The skills now run inline. **Note the reason, not only the rule** — v2.1.232 gave forks the full conversation, retiring the "a fork cannot see the context" half of the original argument while leaving the AMP-identity half untouched | v2.1.218 |
| **`disable-model-invocation: true` excludes a skill from subagent preload** | **Breaking, and silent.** The agent's `skills:` field listed all six skills, and all six set that key — so the preload was inert and the agent booted without its own procedures. The key was removed from all six; the preload now works | — |
| **Nested subagents: off by default, then default depth 3** | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` sets it. **AMPA's own policy is stricter: single-layer delegation — the sub-agents AMPA spawns do not fan out further** | v2.1.217 / v2.1.219 |
| **Concurrent-subagent cap (default 20)** | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`. AMPA's single-layer policy keeps it far below the cap | v2.1.217 |
| **Per-session 200-subagent spawn cap removed** | Long AMPA sessions no longer refuse new agents; depth and concurrency limits still apply | v2.1.224 (added v2.1.212) |
| **Agent names may not contain `:`** | Reserved for plugin namespacing. AMPA's agent name is compliant; a non-compliant file is not loaded and the error goes only to the debug log | v2.1.218 |
| **`/review` is an alias of `/code-review`; `/ultrareview` is deprecated** | Use `/code-review <level>` or `/code-review ultra`. With no level it reuses the last one you typed | v2.1.223 |
| **Task tool's `mode` parameter deprecated (ignored)** | Subagents inherit the parent session's permission mode. AMPA never passed it | v2.1.212 |
| **Native cross-session `SendMessage` + `ListAgents`** | Claude Code sessions can message each other across machines. **AMPA does not adopt it**: it carries no AI Maestro AID, so a message has no verifiable author, no R6 routing, and no audit entry. AMP remains AMPA's governed channel. Not unsafe — relayed messages have carried no user authority since v2.1.166 and are classifier-evaluated since v2.1.222 — but **ungoverned**, and the transport choice is fleet governance, not a plugin's to make | v2.1.224 |
| **`DirectoryAdded` hook** | Fires on `/add-dir`. AMPA registers no hooks: adding a workspace root does not change `cwd`, and AMPA keys nothing on workspace roots. Deliberate, not an omission | v2.1.219 |
| **Frontmatter booleans accept `yes`/`no`/`on`/`off`/`1`/`0`** | Alongside `true`/`false`. AMPA uses `true`/`false` | v2.1.222 |
| **`archive` plugin source with optional SHA-256 pinning** | Install from a zip over HTTPS, no git or npm. A **marketplace-entry** feature, not a plugin-manifest one — nothing for AMPA to declare | v2.1.224 |
| **Plugins accept `"."` as a `skills` path** | For single-skill plugins whose `SKILL.md` sits at the root. AMPA uses the `skills/` directory layout | v2.1.221 |

### v2.1.225 – v2.1.232 — including one more change AMPA had to act on

| Change | Effect on AMPA | Added in |
| ------ | -------------- | -------- |
| **Non-teammate agent spawns run in the BACKGROUND by default** | **Breaking, and silent** — the v2.1.218 defect class, one layer up. An interactive spawn now returns a *handle*, not the subagent's output; the result arrives later as a task notification. The agent prompt had promised an in-turn return, so it was rewritten to **collect before relaying**: never relay a handle as a finding, never report a delegated task complete on the strength of having spawned it. Confirmed first-hand on v2.1.232 | v2.1.232 |
| **Subagent forking on by default; a fork inherits the full conversation and prompt cache** | Does **not** reopen `context: fork` for the `ampa-*` skills. Three reasons survive, each sufficient on its own: a fork still has no AMP identity; a fork is itself a background spawn; and a fork's state never merges back, while these procedures mutate the main agent's own state. The prompt now records all three, so the constraint cannot be discarded on a reason that has expired | v2.1.232 |
| **`@` mentions another session in the prompt; `SendMessage` delivers to a bare name** | Makes the native cross-session channel far easier to reach by accident. **AMPA's non-adoption stance is unchanged** (see the v2.1.224 row): AMP stays the governed channel because it carries an AI Maestro AID. The `@` affordance is a *user* action in the operator's session, not something the plugin invokes | v2.1.232 |
| **Interactive sessions keep unique names on one machine** | A session claiming a name another live session holds gets a `name-word-word` variant. AMPA keys nothing on session names — its identity is its AID | v2.1.232 |
| **Write tool: newer models may overwrite a file they have not read this session** | Now matches the Edit tool's rules; older models still require the read first. AMPA asserted no read-before-write rule, so nothing broke — and none was added, since overwriting unread files is not a habit worth teaching | v2.1.228 |
| **`/plugin install plugin@marketplace` refreshes the marketplace first** | A newly published AMPA version installs without a manual marketplace refresh. AMPA's documented install uses `--url`, so this reaches marketplace users only | v2.1.232 |
| **`/code-review` at high, xhigh, and max runs in a background agent** | Now matches the other levels. Operators who wire AMPA into a review step get the result as a notification, not inline | v2.1.232 |
| **Marketplace `command` sources; GitLab marketplaces; `additionalMarketplaces` / `allowedMarketplaces` aliases** | All **marketplace-entry** features, not plugin-manifest ones — nothing for AMPA to declare | v2.1.229 / v2.1.232 |

### v2.1.233 – v2.1.240 — including one change AMPA had to act on

| Change | What it means for AMPA | Version |
| ------ | ----------------------- | ------- |
| **UTF-8 BOM in an agent/skill/command `.md` silently ignored (now fixed)** | **Breaking.** Same silent defect class as v2.1.218 and v2.1.232: no error, the artifact simply never loads. AMPA ships none today (verified by byte check over every tracked file, 2026-08-22) and a pytest guard now enforces that | v2.1.239 |
| **Todo/task tools (`TaskCreate`/`TaskGet`/`TaskUpdate`/`TaskList`, `TodoWrite`) removed on Opus 4.8, Sonnet 5, Fable 5, Mythos 5 and newer** | `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` restores them. AMPA's persona and skills reference none of them (verified by grep), so nothing broke and nothing was added | v2.1.233 |
| **Background task notifications between turns now arrive wrapped in `<system-reminder>` tags** | Matching mid-turn delivery — this is how a delegated subagent's result reaches AMPA under the v2.1.232 collect-before-relay rule. The persona now records that the envelope is platform-generated context, never user input and never user approval | v2.1.234 |
| **"Default teammate model" setting removed; agent-team teammates use the leader's model unless the spawn names one** | AMPA pins no `model:` in its frontmatter, so it inherits correctly by default | v2.1.234 |
| **An omitted `subagent_type` now returns an error listing available agents** | Previously the Agent tool advertised a general-purpose default even where unavailable, so an omission failed silently into the wrong agent. Nothing in AMPA depends on that removed default: the persona's only `subagent_type` rule is the prohibition on `"fork"` for AMP-coupled steps (grep, 2026-08-22). The persona asserts no general naming rule, and none was invented here to make the row read better | v2.1.235 |
| **`ANTHROPIC_DEFAULT_MODEL` sets the model new sessions start on** | A `/model` pick still overrides it. An operator preference, not a plugin declaration | v2.1.236 |
| **`notify_when_idle` on cross-session `SendMessage`** | One-shot idle notice, no polling. AMPA's non-adoption stance for the native channel is unchanged (see the v2.1.224 row): AMP stays the governed channel because it carries an AI Maestro AID | v2.1.236 |
| **`ListAgents` reports a session its own name and lists live teammates; Windows gains cross-session messaging** | Makes the native channel easier to reach, which does not make it governed. Stance unchanged | v2.1.239 |
| **Marketplace `headersHelper`; `claude plugin install/update` prompt `[y/N]` (or `-y`)** | The prompt appears only where a catalog entry declares a `headersHelper`. AMPA's documented install is `--url` with none, so scripted installs are unaffected; a marketplace that adds one will need `-y` in CI | v2.1.238 |
| **`claude plugin validate` now checks a bare `.claude/skills` directory; marketplace `metadata.pluginRoot` fixed** | Both marketplace/tooling-side. AMPA uses the `skills/` layout and declares no `pluginRoot` | v2.1.233 / v2.1.239 |

### v2.1.241 – v2.1.248 — three substantive updates, no Breaking change

| Change | What it means for AMPA | Version |
| ------ | ----------------------- | ------- |
| **`--restricted` (or `CLAUDE_CODE_RESTRICTED=1`) removes the built-in tools that run commands or code and `WebFetch` (unless named in `--tools`), keeps file tools inside the working directory, refuses `bypassPermissions`, and ignores user, project and local settings files** | **AMPA cannot run under `--restricted`** unless the operator re-adds the tools via `--tools`. The `ampa-task-execution` loop depends on Bash — step 3 of its workflow is *"activate venv (`uv venv` / `source .venv/bin/activate`), verify dependencies"* (`skills/ampa-task-execution/SKILL.md:41-42`) — and on Edit/Write for the code changes themselves; the skill declares no tool restriction of its own (`allowed-tools`/`tools:` → 0 hits, 2026-08-28). An operator-facing constraint, not a plugin defect — recorded here so nobody debugs it as one | v2.1.248 |
| **`SendMessage` from a subagent to another session: the send goes out under the PARENT session's address and any reply is delivered to the parent session's conversation, not to the subagent** | **Persona updated.** The "Subagent Restriction" section now states it explicitly: a subagent's native `SendMessage` is delivered under AMPA's own address and any reply lands in AMPA's conversation. This *strengthens* the existing non-adoption argument rather than weakening it — the native channel gives a subagent no independent identity either, so it cannot carry an AI Maestro AID any more than a fork can | v2.1.248 |
| **A subagent that stops at its `maxTurns` limit now returns its output marked as partial, with a hint to continue it via `SendMessage`, instead of appearing finished** | **Persona updated.** The v2.1.232 "collect before you relay" rule now also says: check for the `partial` marker before treating truncated subagent output as final, and continue the *same* subagent rather than spawn a new one. Same defect class as v2.1.218/v2.1.232 — output that looks complete and is not | v2.1.246 |
| **Bedrock, Vertex, and Foundry sessions (and any with telemetry disabled): Claude is now told when a configured MCP server failed to connect, instead of concluding its tools don't exist** | **SERENA diagnostic updated.** AMPA hard-depends on SERENA MCP, and `skills/ampa-project-setup/references/op-activate-serena-mcp.md` could not tell "not configured" from "silently unreachable" — both fell into the *assume never installed* branch. An explicit failed-to-connect message now routes straight to server/network troubleshooting | v2.1.247 |
| **Fixed plugin installation failing when `plugin.json` was saved with a UTF-8 byte-order mark (BOM)** | **Guard added.** The v2.1.239 BOM guard globbed `agents/ skills/ commands/` `*.md` only, so a BOM'd manifest — which broke *install* outright, not just loading — could not have been caught. `tests/test_primary_skills.py::test_no_shipped_json_manifest_starts_with_a_utf8_bom` now covers `.claude-plugin/plugin.json` and `hooks/hooks.json`; both ship BOM-free today (byte-verified). Cited by test NAME, not line number — line numbers rot on the next edit, and a stale one is the same silent-drift defect these rows exist to prevent | v2.1.246 |
| **Fixed plugin skills whose frontmatter `name` already includes the `<plugin>:` prefix showing it doubled in the slash menu (e.g. `/plugin:plugin:skill`)** | **Guard added.** All six AMPA skill `name:` values are bare (verified `skills/*/SKILL.md`, 2026-08-28); `tests/test_primary_skills.py::test_no_skill_frontmatter_name_carries_a_plugin_prefix` covers every skill, not only the five the primary-skills test already knew about | v2.1.246 |
| **Improved plugin marketplace hardening: names containing control or invisible characters are rejected** | **Guard added.** AMPA's plugin name and all six skill names carry no control/zero-width/bidi/BOM codepoints (codepoint-verified); `tests/test_primary_skills.py::test_skill_and_plugin_names_carry_no_control_or_invisible_characters` guards both surfaces, so a marketplace rejection cannot be introduced by an invisible paste | v2.1.247 |
| **`experimental.cacheTtl` (`"5m"` or `"1h"`) added to agent frontmatter: a per-agent prompt cache TTL used when no subagent TTL setting is configured** | **Deliberately not adopted.** AMPA's cache-hit pattern is unmeasured, so pinning a TTL would change real cache-retention cost with no evidence it helps. The frontmatter carries no `experimental:` block (grep → 0 hits, 2026-08-28). Adopt it after measuring, not because it is new | v2.1.248 |
| **`promptCacheTtl` and `subagentPromptCacheTtl` settings so API-key and cloud-provider users can keep a 1-hour prompt cache on the main conversation while subagents stay at 5 minutes** | Operator-level `settings.json` knobs, not a plugin declaration — no repo anchor (grep → 0 hits, 2026-08-28). Note the interaction with the row above: `experimental.cacheTtl` applies only *when no subagent TTL setting is configured*, so an operator who sets these takes precedence over any per-agent value AMPA might pin later | v2.1.243 |
| **Cross-session messaging (`SendMessage`/`ListAgents`) now works on Bedrock, Vertex and Foundry and with telemetry disabled; an invalid `crossSessionInbound` value now warns and holds (or refuses) instead of being silently ignored** | Stance unchanged (see the v2.1.224 row): AMP stays AMPA's governed channel because it carries an AI Maestro AID. Wider availability makes the native channel easier to reach, which does not make it governed. `skills/ampa-orchestrator-communication/` invokes only the frozen `amp-*` CLIs (grep for `SendMessage`/`cross-session` → 0 hits, 2026-08-28) | v2.1.248 |
| **New `SendFeedback` tool: Claude can draft a feedback report for the user to send from `/feedback`; the `feedbackDrafts` setting turns it off** | No repo anchor — AMPA declares no tool allowlist this would touch (grep "feedback" → only PR-review-feedback hits, 2026-08-28). A drafted report is queued locally and never sent without the user, so it crosses no AMP boundary | v2.1.247 |
| **Fixed: a hook or background agent that printed megabytes of error output could overflow the conversation and wedge the session on "Prompt is too long"** | Already defended by design, and worth recording as such: all six `ampa-task-execution` reference procedures carry the same Token rule — *"write all command output to a report file; return only a 2-3 line summary + file path"* (e.g. `references/op-implement-code.md:17-18`) — so AMPA never returned raw command output to its caller in the first place | v2.1.247 |
| **Sonnet 5's default auto-compact window is now its full 1M context (auto-compacts at ~967K instead of ~934K)** | No repo anchor — AMPA pins no `model:` and asserts no auto-compact threshold (grep → 0 hits, 2026-08-28), so it inherits the wider window wherever the operator runs it | v2.1.247 |

### v2.1.249 – v2.1.284 — two new model defaults, no Breaking change

| Change | What it means for AMPA | Version |
| ------ | ----------------------- | ------- |
| **Claude Opus 5.5 (`claude-opus-5-5`) is the new default Opus model (v2.1.280); Claude Sonnet 5.5 (`claude-sonnet-5-5`) the new default Sonnet (v2.1.284); both carry 1M context** | No repo anchor — AMPA pins no `model:` and no model ID anywhere (grep `claude-(opus or sonnet or haiku)-5` → 0 hits, 2026-09-29), so it inherits the session default. The §Effort bullet's "carried forward to Opus 4.8" phrasing records when `xhigh` was introduced and stays as written; the current defaults are Opus 5.5 and Sonnet 5.5 | v2.1.280 / v2.1.284 |
| **AGENTS.md is read when a project has no CLAUDE.md (toggle in /config)** | AMPA ships no AGENTS.md and keys no workflow on one; projects AMPA works in gain a fallback instruction file, which changes nothing the plugin declares | v2.1.277 |
| **`"attribution": false` setting hides commit/PR attribution; plugin hook-failure errors name the plugin** | No repo anchor — AMPA sets no attribution default (grep → 1 hit, unrelated prose about review replies, 2026-09-29). Named-plugin hook errors are strictly better diagnostics; AMPA registers no hooks (`hooks/hooks.json` is empty by design) | v2.1.281 |
| **`/doctor` prompt-audit scans CLAUDE.md/skills/agents/commands for outdated prompting patterns; `claude plugin validate` gains MCP-server checks and reserved-name enforcement** | Tooling-side. Running the audit over AMPA's six skills and agent prompt is the cheap drift check; AMPA declares no MCP server in its manifest (verified) and its names pass the existing reserved/invisible-character guards in `tests/test_primary_skills.py` | v2.1.283 |
| **Only official/vouched plugin sources keep `allowed-tools` pre-approval under `allowManagedPermissionRulesOnly`** | Enterprise-mode constraint only: with that setting on, AMPA (a third-party marketplace plugin) loses pre-approval for the one skill declaring an `allowed-tools` frontmatter line (`skills/ampa-prrd-trdd-kanban/SKILL.md` — the only skill-frontmatter declaration repo-wide, agents/ + skills/ grepped, 2026-09-29), so its Bash calls prompt for permission. Outside enterprise mode nothing changes. Recorded so a prompt there is not debugged as a defect | v2.1.284 |

## See Also

> **Related Plugins**: This agent works with the AI Maestro Orchestrator Agent
> (AMOA), AI Maestro Integrator Agent (AMIA), and AI Maestro Architect Agent
> (AMAA). Each agent plugin is installed independently. These plugins are part
> of the AI Maestro ecosystem and are not required for standalone use. AMPA is
> an **implementer** (artifact-producing agent). Future implementer subtypes
> (artist, sfx-expert, etc.) will follow the same patterns.
