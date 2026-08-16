---
trdd-id: YK1HL9RH
title: Update the main agent TRDD lifecycle section from the v1 shape to v2 columns and 4 zones
column: complete
created: 2026-07-15T00:17:30+0200
updated: 2026-07-15T00:29:36+0200
current-owner: ai-maestro-programmer-agent
task-type: docs
approval-tier: 0
relevant-rules: [1]
release-via: publish
implementation-commits: [14b1bd2]
last-test-result: pass
---

# TRDD-YK1HL9RH — Main-agent lifecycle: v1 (`status:` + 2 folders) → v2 (`column:` + 4 zones)

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-15

**⚠ LANDED — correction 2026-08-16:** this work SHIPPED in `14b1bd2`
("docs(agent): lifecycle section v1 -> v2 (column + 4 zones)"). Everything below
is AUTHORING-TIME prose that was never refreshed — read it as history, not as
current state.

- **Current state:** `agents/ai-maestro-programmer-agent-main-agent.md:472-483` — section
  "### Two folders (location = authorization)" — describes the **v1** lifecycle: a `status:`
  field and only **two** folders (`proposals/`, `tasks/`).
- **The contradiction:** `design/` on disk has **four** zones — `proposals/ tasks/ archived/
  refused/` (verified) — and every TRDD + `skills/ampa-prrd-trdd-kanban/SKILL.md` uses
  **`column:`**, not `status:`. TRDD v2 has **no `status:` field at all**; `column:` IS the
  state machine. So the persona instructs the agent to set a field that does not exist.
- **NEXT ACTION:** rewrite that section as the 4-zone model keyed on `column:`, name the
  terminal states, and mention `approval-tier:`.
- **Load-bearing facts:**
  - The dividing line between the two terminal zones is **"was it ever approved?"** — a
    never-approved proposal that is declined goes to `refused/`; a once-approved TRDD that
    finishes / is withdrawn / is replaced goes to `archived/`.
  - **`failed` is NOT terminal and is NOT archived** — a failed TRDD stays in `design/tasks/`
    and is retried. Only an explicit decision to give up converts it to `cancelled`.
  - The **tier obligations** section right below (`:485-511`) is already correct v2 —
    do NOT touch it. This TRDD is scoped to the folder/field table only.
- **Reported by:** the MANAGER's fleet-readiness audit, `ai-maestro-programmer-agent#25`
  (section B, MED).

## Problem

The persona is the agent's operating manual. Telling it to set `status: planned` — a field
the v2 schema does not have — means either the agent writes a field nothing reads, or it
notices the contradiction mid-task and has to guess. Documenting 2 of the 4 zones also
leaves the agent with nowhere to put a refused proposal or a completed TRDD.

## Required changes

1. Replace the `status:`/2-folder table with the **4-zone** table keyed on `column:`.
2. State the **lineage rule** (ever-approved → `archived/`; never-approved → `refused/`).
3. State that **`failed` stays in `design/tasks/`** (retryable — never archived as failed).
4. Mention **`approval-tier:`** as the frontmatter field carrying the tier classification.
5. Keep the `git mv` + `## Approval log` + grandfathering guidance (still correct).

## Success criteria

- Zero occurrences of `status: planned` / `status: proposal` in the persona.
- The persona names all 4 zones and matches what `design/` actually contains.
- Full suite green; CPV strict still 0/0/0/0.

## Notes

- `min-approval-requirement:` (the field ai-maestro's `#27` mentions) is deliberately NOT
  introduced here — whether it replaces or coexists with `approval-tier:` is **Q3 of
  `Emasoft/ai-maestro#61`** and unanswered. Writing a guess into the persona is exactly the
  failure this TRDD is fixing. Migrate once the fleet answers.
