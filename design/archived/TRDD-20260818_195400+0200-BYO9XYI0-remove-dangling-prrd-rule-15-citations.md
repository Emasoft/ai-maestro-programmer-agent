---
trdd-id: BYO9XYI0
title: Three cards cite PRRD rule 15 which does not exist
column: completed
created: 2026-08-18T19:54:00+0200
updated: 2026-08-18T20:05:00+0200
release-via: none
implementation-commits: [8214ee5]
current-owner: ampa-main-session
task-type: docs
approval-tier: 0
relevant-rules: [1]
---

Phase 2 of the self-audit (hub TRDD-BRRJK57P). Finding axis2-C2, CONFIRMED and
coordinator re-verified: 3 archived cards from the 2026-07-24 authoring batch carry
`relevant-rules: [1, 15]` (G0768YHK, I8AH88SS, K2X9RF7S, each line 12); the PRRD
defines rules 1–8 only — `grep -n '\*\*[GS]15' design/requirements/PRRD.md` exits 1,
while the same-shape regex finds all 8 real rules (instrument proven).

## Fix

Remove the dangling `15` from each card's `relevant-rules:` (→ `[1]`). A
machine-verifiably false citation on a terminal card falls under the terminal-freeze
false-claim exception.

## Acceptance

- `grep -rn "relevant-rules:.*15" design/` returns nothing.

## Approval log

- 2026-08-18T20:05:00+0200 — todo→dev→testing→ai_review→complete by ampa-main-session (hub Phase-2 GO). Fixed in 8214ee5. Acceptance note: the grep in this card's body still matches ITSELF (the finding record quotes the defect); all live frontmatter citations are clean.
