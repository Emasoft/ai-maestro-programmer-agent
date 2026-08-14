---
trdd-id: P9KVMK5A
title: Realign AMPA to Claude Code v2.1.232
column: dev
created: 2026-08-14T12:50:46+0200
updated: 2026-08-14T12:50:46+0200
current-owner: ai-maestro-programmer-agent-main-agent
task-type: docs
approval-tier: 0
scope: project
project-id: ai-maestro-programmer-agent
relevant-rules: [1]
parent-trdd:
npt: []
eht: []
implementation-commits: []
---

# Realign AMPA to Claude Code v2.1.232

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-14

- **Baseline**: v2.0.4 / `808a64f`, realigned to Claude Code v2.1.224 by
  [[TRDD-IUJ75HDL]]. Working tree clean at start.
- **Trigger**: the v2.1.225 → v2.1.232 changelog.
- **NEXT ACTION**: see the work items below; all are docs/prompt/test — no
  runtime code changes.
- **Surface, swept and verified**: `README.md`, `agents/…main-agent.md`,
  `tests/`. `docs/`, `commands/` and `hooks/` carry **no** Claude Code
  version claims (grep, 2026-08-14) — nothing to update there.

## The one change that alters how AMPA executes

**v2.1.232: "non-teammate agent spawns in interactive sessions now run in the
background by default."**

This is the same defect class as v2.1.218 was for skills, one layer up: the
platform changed a default, nothing errors, and an artifact keeps asserting a
property it no longer has. The agent prompt's **Subagent Restriction** block
says subagents "must return results to you". By default that is now false *in
the turn that asked* — an interactive spawn returns a handle and the result
arrives later as a task notification.

The correction is to the stated contract, not the architecture: AMPA's
single-layer delegation policy is unchanged, and nothing needs to be spawned
differently. What changes is that the prompt must stop promising an in-turn
return it no longer gets by default.

## The rationale that quietly went stale

The same v2.1.232 line says a `subagent_type: "fork"` subagent now **inherits
the full conversation and prompt cache**.

[[TRDD-IUJ75HDL]] removed `context: fork` from all six skills and justified it
in the agent prompt as "a forked copy could not finish any of them". Half of
that reason was contextual — a fork lacked the conversation the procedure
depends on — and v2.1.232 falsifies that half.

**The decision does not change; the reason must.** A fork still has no AMP
identity, which is an AI Maestro property no Claude Code release can grant. So
the rationale is re-grounded on that alone. Left as written, a future reader
would find a justification the changelog contradicts, conclude the constraint
was obsolete, and "optimize" the skills back into forks — losing the actual
reason in the process.

This is the recorded lesson from the prior round applied to itself: *an
artifact that asserts a property it no longer has*. A stale rationale is worse
than a missing one, because it forecloses the check.

## Work items

- **W1 — agent prompt, Subagent Restriction.** State the v2.1.232 default
  (interactive spawns run in the background; the result arrives as a task
  notification, not in-turn) and what AMPA does about it.
- **W2 — agent prompt, fork rationale.** Re-ground on no-AMP-identity alone.
  Record that inheriting the conversation does **not** confer AMP identity, so
  a future reader has the reason and not just the rule.
- **W3 — agent prompt, fan-out limits.** Re-anchor the version range; depth 3
  / concurrency 20 / no per-session cap are unchanged.
- **W4 — README.** Re-anchor the verified-through version and add rows for the
  v2.1.225–v2.1.232 items that bear on a role agent.
- **W5 — guard.** Only if an honest one exists. A guard that cannot fail is
  worse than none: it forecloses the check it appears to perform.

## Verification

1. `uv run --with pytest pytest tests/ -x -q`
2. `uv run --with ruff ruff check .` (gate pinned to `E4,E7,E9,F` per
   [[TRDD-1TXG0EON]])
3. `uv run scripts/publish.py --dry-run` — CPV lint + `--strict` validate

## Acceptance criteria

- [ ] The agent prompt no longer promises an in-turn subagent return.
- [ ] The fork rationale rests only on no-AMP-identity, and says so explicitly.
- [ ] README is anchored to v2.1.232 with the new items recorded.
- [ ] Every guard added can actually fail, and its docstring claims only what
      it checks.
- [ ] Tests, ruff, and `publish.py --dry-run` all green.

## Approval log

- 2026-08-14T12:50:46+0200 — Tier 0 (own scope, docs + own agent prompt + own
  tests; no baseline deviation, no cross-project reach). Self-mandated.
