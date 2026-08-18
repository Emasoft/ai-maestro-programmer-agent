---
trdd-id: G0768YHK
title: Update docs and governance scenarios for granular wiring self-mandate and missing-derived duty
column: completed
created: 2026-07-24T13:53:33+0200
updated: 2026-08-18T19:54:00+0200
current-owner: ampa-programmer
task-type: docs
min-approval-requirement: none
mandate: true
mandated-by: self
relevant-rules: [1, 15]
external-refs: [Emasoft/ai-maestro#61, Emasoft/ai-maestro#71]
blocked-by: []
implementation-commits: [e3ddf58]
---

# Update docs and governance scenarios for granular wiring self-mandate and missing-derived duty

## ⏵ STATE — READ THIS FIRST ON RESUME — 2026-07-24

**⚠ LANDED — correction 2026-08-16:** this work SHIPPED in `e3ddf58`
("docs(governance): reflect granular ama-* wiring + add self-mandate/
missing-derived/refusal scenarios"). Everything below is AUTHORING-TIME prose
that was never refreshed — read it as history, not as current state. The NEXT
ACTION below is gated on I8AH88SS + K2X9RF7S, and both landed (`58827de`,
`57b35a4`).

**Why:** docs (`README.md:59`, `docs/FULL_PROJECT_WORKFLOW.md:13`,
`.claude/project/memory/architecture.md:27`) and `tests/scenarios/
governance-scenarios.md` describe the old wrapper wiring + `approval-tier:`
literals. They must reflect the granular `ama-*` wiring, `min-approval-requirement:`,
the 17-column vocab, the self-mandate rule, and the new missing-derived-TRDD duty.

**NEXT ACTION:** after I8AH88SS + K2X9RF7S land, update the three doc files to the
granular wiring; migrate scenario `approval-tier: 0/2` literals →
`min-approval-requirement:`; add Given/When/Then scenarios for (a) the self-mandate
authoring path, (b) the missing-derived-TRDD duty (report-to-sender + author), (c)
the refusal-response proposer corollary (#71). Run pytest → green before commit.

**SUPERSEDED — do NOT carry forward:** none yet.

## Scope

- `README.md`, `docs/FULL_PROJECT_WORKFLOW.md`, `.claude/project/memory/
  architecture.md`: replace wrapper-wiring narrative with granular `ama-*`;
  min-approval-requirement + 17-column vocab.
- `tests/scenarios/governance-scenarios.md`: migrate `approval-tier:` literals; add
  self-mandate, missing-derived-TRDD, and refusal-response scenarios in the core
  SCEN format.

## Acceptance criteria

- Docs cite only skills that exist; no stale `prrd-trdd-kanban` / `approval-tier:`
  narrative presented as current.
- New scenarios present and consistent with the repurposed skill (I8AH88SS).
- `uv run pytest tests/ -q` green; CPV gates green.

## Approval log

- 2026-08-18T19:54:00+0200 — COMPLETED by ampa-main-session (TRDD-LNSZPCKE closing edit). The f29e1c2 archival was a pure git mv that skipped the protocol's `complete → completed` column edit; performed here. Work had shipped in e3ddf58.
