---
trdd-id: I8AH88SS
title: Rewire 3-pillars mechanics onto the granular ama-* skills and repurpose the wrapper into a MEMBER-policy skill
column: planned
created: 2026-07-24T13:53:33+0200
updated: 2026-07-24T13:53:33+0200
current-owner: ampa-programmer
task-type: refactor
min-approval-requirement: none
mandate: true
mandated-by: self
relevant-rules: [1, 15]
external-refs: [Emasoft/ai-maestro#61, ai-maestro-programmer-agent#25]
implementation-commits: []
---

# Rewire 3-pillars mechanics onto the granular ama-* skills and repurpose the wrapper into a MEMBER-policy skill

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-24

**Why:** AMPA's 3-pillars wiring defers to a core skill `prrd-trdd-kanban` that no
longer exists in `ai-maestro-plugin` (v2.8.0+ ships GRANULAR skills instead). The
mechanics currently resolve to nothing. Rulings are decided in Emasoft/ai-maestro#61
(Q1/Q2, verified 2026-07-24). This TRDD is the self-mandate Tier-0 fix.

**VERIFIED FACTS (load-bearing):**
- Installed core (`^2.7.0` → 2.8.0..2.10.0) ships all 10 pillar skills:
  `ama-prrd-get`, `ama-prrd-find`, `ama-prrd-propose`, `ama-prrd-edit`,
  `ama-trdd-write`, `ama-trdd-update`, `ama-trdd-transition`, `ama-trdd-find`,
  `ama-kanban-render`, `ama-proposal-approvals`. Names verified against the cache,
  not the issue text. `prrd-trdd-kanban` is confirmed GONE from core.
- The wrapper `skills/ampa-prrd-trdd-kanban/SKILL.md` is ~70% genuine MEMBER
  policy; only lines 5 (`compatibility:`), 6 (`allowed-tools:` core script names),
  28-29, 38-40, 88, 129-135 point at the dead core skill/scripts.
- MEMBER op-set (Q1): MAY author own Tier-0 work directly via `ama-trdd-write` /
  `ama-trdd-update` (self-mandate: `design/tasks/`, `column: planned`,
  `min-approval-requirement: none`, `mandate: true`, `mandated-by: self`, born
  approved). `ama-proposal-approvals` is READ/LIST-only for a MEMBER.
  `ama-trdd-transition` is signal-only for a MEMBER (dev→testing). NON-EXEMPT:
  release, escalation, →failed, force-supersede → via COS/proposal.
- NEW DUTY (Q1-extra): on receiving an assigned TRDD whose derived TRDD is MISSING,
  the MEMBER MUST report it to the sender AND may author it (self-mandate if
  in-slice; proposal if past its authority). No skill exists today — build it (D1).
- Q2 exception applies: KEEP the wrapper file but make it hold genuine role POLICY
  (not a passthrough); wire the granular mechanics directly.

**GREEN-TO-GREEN COUPLING (advisor, Fable 5):** the tests pin MORE than the one
named test. `test_skill_governance_block_present` (line ~80) asserts
`"ampa-prrd-trdd-kanban" in body` for all 5 primary skills; `test_m4_kanban_skill
_present_and_v3` (~206-214) asserts the wrapper's body strings. So T1 (skill
repurpose) + T2 (governance blocks) + T4 (tests) MUST land as ONE commit unit —
sequencing them red-breaks publish.py's test gate mid-way.

**NEXT ACTION:** Read `tests/test_primary_skills.py` fully; enumerate every
assertion that pins the wrapper name or its body strings. Then edit in this order
within ONE unit: (1) repurpose `ampa-prrd-trdd-kanban/SKILL.md`; (2) re-point the 5
primary skills' `## Governance` blocks; (3) add the D1 op-reference; (4) adapt the
tests (single-source `ama-*` name constant; assert granular citations; do NOT add a
repo-wide `approval-tier:` absence assertion). Run `uv run pytest tests/ -q` → must
be green before commit.

**SUPERSEDED — do NOT carry forward:** any plan that DELETES the wrapper (rejected —
Q2 exception + 10+ reference sites); any plan that sequences T1→T2→T3→T4 (red-breaks
the gate).

**Artifacts to read before acting:** this repo's `skills/ampa-prrd-trdd-kanban/
SKILL.md`, `tests/test_primary_skills.py`, and the granular skills under
`~/.claude/plugins/cache/ai-maestro-plugins/ai-maestro-plugin/2.8.0/skills/ama-*`.

## Scope (this TRDD)

One green-to-green unit:
1. **Repurpose the wrapper** `ampa-prrd-trdd-kanban` — drop the dead-core
   `compatibility:` / core-script `allowed-tools:` / Prerequisites / Resources refs;
   cite the granular `ama-*` skills for mechanics; keep+strengthen the MEMBER policy;
   migrate the "Approval tiers" section to `min-approval-requirement:` vocab; add the
   self-mandate rule and the missing-derived-TRDD duty.
2. **Re-point the 5 primary skills' `## Governance` blocks** from
   `ampa-prrd-trdd-kanban` to cite the granular `ama-*` skills directly, and migrate
   `approval-tier` language → `min-approval-requirement` + the 17-column vocab note.
3. **Add the D1 op-reference** `ampa-orchestrator-communication/references/
   op-report-missing-derived-trdd.md` (report-to-sender template + self-mandate
   authoring path) — frontmatter valid per `test_all_op_reference_files_have_valid
   _frontmatter`.
4. **Adapt the tests** — single-source `ama-*` name constant; assert granular
   citations replace the wrapper pin; adapt `test_m4`; NO repo-wide `approval-tier:`
   absence assertion (existing TRDDs migrate on-touch).

Persona/agent.toml wiring is TRDD-K2X9RF7S; docs/scenarios are TRDD-G0768YHK.

## Acceptance criteria

- `grep -rl "prrd-trdd-kanban" skills/ tests/` returns only intentional history
  mentions; every skill's mechanics cite a granular `ama-*` skill that EXISTS in
  installed core.
- `uv run pytest tests/ -q` green; CPV `publish.py` gates green.
- The wrapper skill is no longer a passthrough — it carries the MEMBER op-set, the
  self-mandate rule, escalation floors, and the missing-derived-TRDD duty.
