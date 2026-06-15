# ai-maestro-programmer-agent — plugin guidance

## Memory: the janitor-hosted global 3-scope wiki

This plugin uses the **global** AI-Maestro markdown memory system — not a
per-plugin one. The protocol, the recall law ("index by the QUESTION, not the
answer"), the note schema, the 2-step non-destructive correction protocol, and
the three scopes all live in `~/.claude/rules/markdown-memory-recall.md`. The
operations are the global skills: `janitor-memory-recall` (find by symptom),
`janitor-memory-write` (capture a fact), `janitor-memory-update` (revise). The
PROJECT scope for this repo is `.claude/project/memory/` (git-tracked, stood up
once via `/janitor-memory-bootstrap`).

Do **NOT** re-create per-plugin `*-memory-recall` / `*-memory-write` skills or a
`rules/memory-protocol.md` mirror — those were removed in favor of the global
system (issue #18). The agent prompts (the main agent + every sub-agent the
main agent spawns) carry the proactive-use contract directly, since sub-agents
inherit nothing.

Use the FIXED zsh-portable array form when composing a multi-scope recall (the
old space-joined `$ROOTS` string silently returns 0 hits on zsh/macOS):

```bash
ROOTS=(); for d in "$LOCAL_MEM" "$PROJECT_MEM" "$USER_MEM"; do [ -d "$d" ] && ROOTS+=("$d"); done
memgrep recall "$SYMPTOM" "${ROOTS[@]}"
```

### The proactive contract (main agent AND every spawned sub-agent)

- **RECALL BEFORE ACTING** — before debugging a recurring problem, making a
  design decision, or acting on a recurring alert, recall first (symptom-indexed,
  across all 3 scopes) via `/janitor-memory-recall`.
- **WRITE / UPDATE AFTER SOLVING** — after a non-trivial fix or decision, write
  or update the owning wikimem page (clean-the-fact + demote-the-error-to-a
  `[^N]`-lesson) via `/janitor-memory-write` / `/janitor-memory-update`.
- **MAINTAIN THE PROJECT WIKIMEM** — keep `.claude/project/memory/` current
  (architecture hub, key-solution pages), git-tracked + shared.
- **SCOPE ROUTING** — machine-private (paths, hostnames, secrets) → LOCAL
  (`~/.claude/projects/<slug>/memory/`); project-shared, no secrets → PROJECT
  (`.claude/project/memory/`); cross-project → USER; **UNSURE → LOCAL**.

### PROGRAMMER-specific recall/write moments (the role flavoring)

**Recall BEFORE:**
- debugging a bug, a failing test, or a recurring error — the diagnosis (and the
  guardrail) is often already written down, found from the error text;
- choosing an approach for an assigned task — prior constraints and confirmed
  user/project preferences may already be recorded;
- a refactor or migration that smells familiar — read the prior decision first.

**Write / update AFTER:**
- a non-trivial fix (Bug Autopsy): capture WHY it happened with the SYMPTOM in
  the `description:` so the next session finds the guardrail from the error text;
- learning a durable project constraint not derivable from code/git history;
- a confirmed user/MANAGER preference about how to build in this project.

### Sub-agent propagation

Sub-agents spawned via the Agent tool inherit none of this. When a spawned
sub-agent will debug, design, or solve something durable, include in its prompt:
"Before acting, recall via `/janitor-memory-recall` with the symptom; after a
non-trivial fix/decision, write/update via `/janitor-memory-write` /
`/janitor-memory-update` (scope: private→LOCAL, project-shared→PROJECT,
cross-project→USER; unsure→LOCAL)."
