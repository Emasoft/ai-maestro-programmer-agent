---
trdd-id: K2X9RF7S
title: Migrate the persona and agent.toml to granular ama-* wiring and min-approval-requirement language
column: completed
created: 2026-07-24T13:53:33+0200
updated: 2026-08-18T19:54:00+0200
current-owner: ampa-programmer
task-type: refactor
min-approval-requirement: none
mandate: true
mandated-by: self
relevant-rules: [1]
external-refs: [Emasoft/ai-maestro#61]
blocked-by: []
implementation-commits: [57b35a4]
---

# Migrate the persona and agent.toml to granular ama-* wiring and min-approval-requirement language

## ⏵ STATE — READ THIS FIRST ON RESUME — 2026-07-24

**Why:** persona `agents/ai-maestro-programmer-agent-main-agent.md` (advisor: lines
~448-529, deprecated `approval-tier:` at ~503 + heavy tier-N language) and
`ai-maestro-programmer-agent.agent.toml` (~line 17) reference the dead
`prrd-trdd-kanban` wrapper. This is the LARGEST migration surface — scoped as
"wiring" but really approval-schema migration too.

**DONE (2026-07-24, commit 57b35a4):** persona migrated — `min-approval-requirement:`
field + self-mandate fields, `approval-tier:` documented deprecated/decode-only,
granular `ama-*` mechanics wired + policy-skill pointer, 17-column vocab, missing-
derived duty. **agent.toml unchanged** — its `[skills]` lists AMPA's OWN skills; the
granular `ama-*` come from the `ai-maestro-plugin` dependency (`^2.7.0`), not AMPA's
skill list. Comm-graph left as-is. 93 passed.

**SUPERSEDED — do NOT carry forward:** none yet.

## Scope

- Persona: cite granular `ama-*` pillar skills (mechanics) + the repurposed
  `ampa-prrd-trdd-kanban` (MEMBER policy); migrate `approval-tier:` → `min-approval
  -requirement:` field + prose; adopt 17-column vocab (14 lifecycle + blocked/failed/
  superseded; `failed` retryable, never archived).
- `agent.toml`: ensure the granular `ama-*` skills are enabled/available to the
  agent; drop the dead-wrapper indirection.
- Leave the comm-graph (MEMBER↔ORCHESTRATOR direct edge, COS at team boundary)
  exactly as-is.

## Acceptance criteria

- Persona + agent.toml cite only skills that exist; no `prrd-trdd-kanban` mechanics
  reference; `approval-tier:` not written as a new field (decode-only).
- `uv run pytest tests/ -q` green; CPV gates green.

## Approval log

- 2026-08-18T19:54:00+0200 — COMPLETED by ampa-main-session (TRDD-LNSZPCKE closing edit). The f29e1c2 archival was a pure git mv that skipped the protocol's `complete → completed` column edit; performed here. Work had shipped in 57b35a4.
