---
trdd-id: K2X9RF7S
title: Migrate the persona and agent.toml to granular ama-* wiring and min-approval-requirement language
column: planned
created: 2026-07-24T13:53:33+0200
updated: 2026-07-24T13:53:33+0200
current-owner: ampa-programmer
task-type: refactor
min-approval-requirement: none
mandate: true
mandated-by: self
relevant-rules: [1, 15]
external-refs: [Emasoft/ai-maestro#61]
blocked-by: [I8AH88SS]
implementation-commits: []
---

# Migrate the persona and agent.toml to granular ama-* wiring and min-approval-requirement language

## ⏵ STATE — READ THIS FIRST ON RESUME — 2026-07-24

**Why:** persona `agents/ai-maestro-programmer-agent-main-agent.md` (advisor: lines
~448-529, deprecated `approval-tier:` at ~503 + heavy tier-N language) and
`ai-maestro-programmer-agent.agent.toml` (~line 17) reference the dead
`prrd-trdd-kanban` wrapper. This is the LARGEST migration surface — scoped as
"wiring" but really approval-schema migration too.

**NEXT ACTION:** after I8AH88SS lands, read the persona's governance section and the
agent.toml wiring block; re-point every pillar reference to the granular `ama-*`
skills the repurposed wrapper now cites; migrate the persona's `approval-tier:`
field name + tier-N prose → `min-approval-requirement:` (0→none,1→chief-of-staff,
2→manager,3→user) + the 17-column vocab. Keep the MEMBER→ORCHESTRATOR comm-graph
UNCHANGED (#61: correct as written). Run pytest → green before commit.

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
