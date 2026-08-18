---
trdd-id: FLU2C00U
title: op-update-pr-with-fixes lacks the G1 self-id requirement
column: published
created: 2026-08-18T19:54:00+0200
updated: 2026-08-18T20:15:00+0200
release-via: publish
implementation-commits: [ba72f17]
current-owner: ampa-main-session
task-type: docs
approval-tier: 0
relevant-rules: [1]
---

Phase 2 of the self-audit (hub TRDD-BRRJK57P). Finding axis2-C3, CONFIRMED and
coordinator re-verified: `skills/ampa-github-operations/references/op-update-pr-with-fixes.md`
never mentions the G1 self-identification requirement (`grep -ci "self-id|G1"` → 0),
while the sibling `op-create-pull-request.md` states it 3 times. Every GitHub-posted
body must begin with the G1 self-id line (shared owner identity); an operation file
agents copy from must carry the requirement.

## Fix

Add the G1 self-id requirement to op-update-pr-with-fixes.md, matching the sibling
file's shape: a statement near the posting instructions plus a checklist item.

## Acceptance

- `grep -c "self-id" skills/ampa-github-operations/references/op-update-pr-with-fixes.md` ≥ 1.

## Approval log

- 2026-08-18T20:05:00+0200 — todo→dev→testing→ai_review→complete by ampa-main-session (hub Phase-2 GO). Fixed in ba72f17; requirement stated, template body carries the self-id line, checklist item added.
- 2026-08-18T20:15:00+0200 — complete→publish→published by ampa-main-session: shipped in v2.0.8.
