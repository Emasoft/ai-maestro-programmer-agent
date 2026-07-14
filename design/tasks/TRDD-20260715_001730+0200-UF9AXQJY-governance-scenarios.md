---
trdd-id: UF9AXQJY
title: Add the MEMBER governance behavior scenarios in the fleet-canonical format
column: dev
created: 2026-07-15T00:17:30+0200
updated: 2026-07-15T00:17:30+0200
current-owner: ai-maestro-programmer-agent
task-type: docs
approval-tier: 0
relevant-rules: [1]
release-via: publish
---

# TRDD-UF9AXQJY — MEMBER governance behavior scenarios

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-15

- **Current state:** `tests/scenarios/` **does not exist** in this repo (the MANAGER's audit
  `#25` said "empty"; it is in fact absent). Governance IS enforced by pytest
  (`tests/test_governance_compliance.py`, 10 tests incl. the R23 bright-line), but the
  scenarios file the fleet audit expects is missing.
- **NEXT ACTION:** author `tests/scenarios/governance-scenarios.md` in the **fleet-canonical
  format**, covering the five behaviors `#25` names: approval-tier self-classify,
  proposal→planned via COS, signal-only column transitions, no golden-PRRD edit, and the R23
  bright-line.
- **Load-bearing facts (from the canonical exemplar — the core plugin's own
  `tests/scenarios/governance-scenarios.md`, read from the installed v2.8.0 cache):**
  - Format is `## SCEN-GNN — <rule>: <title>` + **Verifies:** + Given/When/Then + **PASS:**,
    closing with a `## Coverage map`.
  - These are **persona/prompt behaviors, not script behaviors** — they have **no executable
    to drive**. The core plugin states plainly: *"This file is a scenario PLAN, not a runnable
    harness. Do NOT fabricate a harness to run these."* **Honor that.** Fabricating a fake
    harness would violate both the fleet convention and this project's own no-conceptual-tests
    rule.
  - **SCEN location is an open governance question — `ai-maestro#37`** (per-plugin
    `tests/scenarios/` vs a central AI-Maestro suite). The core plugin's file carries that
    caveat; mine must too, so a "central" ruling turns this file into a pointer rather than
    orphaning it.
  - Canonical per-scenario filename **if** a harness ever lands:
    `tests/scenarios/SCEN-NNN_<slug>.scen.md`.
- **Do NOT** claim the scenarios are "tests that pass". They are reviewed by reading the
  persona/skill prose against each Given/When/Then. Where a scenario **is** mechanically
  enforced, name the pytest test in the coverage map — that is the honest split.

## Problem

The fleet-readiness audit expects each role-plugin to carry behavioral acceptance scenarios
for its TITLE's governance duties. Mine has real pytest enforcement for the *bright-lines* it
can machine-check (R23, escalation prose), but nothing that states the **reasoning behaviors**
a MEMBER must exhibit: when to self-classify a task at Tier 0 versus escalate, that a column
transition is a *signal* and not a self-authorization, and that a golden PRRD rule is
untouchable even when the agent believes it is wrong.

Those behaviors are exactly where a persona silently drifts, because nothing fails when they
are absent.

## Required changes

`tests/scenarios/governance-scenarios.md`, in the canonical format, with scenarios for:
1. **Tier-0 self-classify** — derived NPT/EHT tasks authored straight into `design/tasks/`
   without asking anyone (the anti-over-escalation behavior).
2. **Tier-2 escalate** — a baseline-deviating / release / cross-team task becomes a
   `proposal`, routed via **AMCOS** (never straight to MANAGER).
3. **proposal → planned** — only an approver promotes + `git mv`s; the author never
   self-approves.
4. **Signal-only transitions** — `dev → testing → ai_review` reflect work that HAPPENED; they
   are not permission to enter the release pipeline.
5. **Golden PRRD rule** — the agent proposes, never edits, even when convinced it is right.
6. **R23 bright-line** — the agent reaches the kanban via the frozen CLI, and REFUSES a direct
   `/api/` instruction even when a task explicitly specifies one (the #7 situation).

Plus a **Coverage map** naming, per scenario, the pytest test that mechanically enforces it
(or `prose-review` where none can).

## Success criteria

- The file exists, matches the core plugin's SCEN format, and carries the `ai-maestro#37`
  location caveat.
- **No fabricated harness.** No test claims to "run" a scenario.
- Suite stays green; CPV strict stays 0/0/0/0.

## Notes

- `#25` offered an either/or: add the file **or** document that `test_governance_compliance.py`
  fulfills it. Doing both is strictly better — the file states the behaviors, the coverage map
  points at the mechanical enforcement where it exists and admits where it does not.
