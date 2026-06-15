---
name: architecture
description: "how does ai-maestro-programmer-agent work — overview, the main parts (main agent, the ampa-* skills + kanban skill, the CPV-direct publish pipeline, the 3-pillars governance under design/), where the PRRD/TRDDs live"
ocd: 2026-06-16
lmd: 2026-06-16
metadata:
  node_type: memory
  type: project
  tier: hub
  functionality: architecture
  globs: ["agents/**", "skills/**", "scripts/**", "design/**", "docs/**"]
---
ai-maestro-programmer-agent (AMPA) is a Claude Code plugin in the AI Maestro fleet.
It implements the MEMBER (programmer) role: a general-purpose, multi-language
implementer that takes an assigned TRDD through `dev → testing → ai_review`,
writes code + real tests, and opens a PR only after the ORCHESTRATOR's pre-PR
gate. It works standalone or orchestrated within the fleet. Distributed via the
`Emasoft/ai-maestro-plugins` marketplace (Layout A hub); depends on
`ai-maestro-plugin` (the 3-pillars scripts: PRRD, TRDD, kanban).

## Parts map
- Main agent: `agents/ai-maestro-programmer-agent-main-agent.md` — MEMBER persona,
  R6 v3 comms (direct edges to AMOA + AMCOS), approval tiers, the three dialog
  loops (comprehension handshake / in-dev raise-immediately / pre-PR gate).
- Skills: `ampa-task-execution`, `ampa-orchestrator-communication`,
  `ampa-github-operations`, `ampa-project-setup`, `ampa-handoff-management`,
  `ampa-prrd-trdd-kanban` (the MEMBER kanban layer).
- Publish: the strict, CPV-direct pipeline `scripts/publish.py` (tests → lint →
  CPV `--strict` → bump → tag → push → release) + the process-ancestry pre-push
  gate. No vendored validators — CI/publish invoke `uvx … cpv-remote-validate`.
- Governance: `design/requirements/PRRD.md` (golden G* / silver S* rules) + the
  4-zone `design/{proposals,tasks,refused,archived}/` TRDD lifecycle.
- Memory: the global janitor 3-scope wiki (this page is the PROJECT hub); the
  contract + scope routing live in `CLAUDE.md`.

## Applies to
- (radiates down to component/aspect pages as they're created; wire the
  reciprocal `## Governed by` on each)

## See also
- (lateral links to other functionality hubs, once they exist)

## Notes and lessons learned
