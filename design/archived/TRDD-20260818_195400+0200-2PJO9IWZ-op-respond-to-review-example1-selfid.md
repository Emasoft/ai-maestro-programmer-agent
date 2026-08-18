---
trdd-id: 2PJO9IWZ
title: op-respond-to-review Example 1 contradicts its own self-id checklist
column: published
created: 2026-08-18T19:54:00+0200
updated: 2026-08-18T20:15:00+0200
release-via: publish
implementation-commits: [7d31c6d]
current-owner: ampa-main-session
task-type: docs
approval-tier: 0
relevant-rules: [1]
---

Phase 2 of the self-audit (hub TRDD-BRRJK57P). Finding axis2-C4, CONFIRMED and
coordinator re-verified by direct read: in
`skills/ampa-github-operations/references/op-respond-to-review.md` the checklist
(~:204) demands every GitHub-posted comment body begin with the G1 self-id line,
Example 2 (~:229) complies, but Example 1's `gh pr comment 123 --body "Fixed SQL
injection..."` (~:219) has no self-id — internally contradictory in a file agents
copy from.

## Fix

Prepend the G1 self-id line to Example 1's comment body, matching Example 2's shape.

## Acceptance

- Every `gh pr comment --body` example in the file begins with the self-id line.

## Approval log

- 2026-08-18T20:05:00+0200 — todo→dev→testing→ai_review→complete by ampa-main-session (hub Phase-2 GO). Fixed in 7d31c6d; Example 1 now matches the checklist and Example 2's shape.
- 2026-08-18T20:15:00+0200 — complete→publish→published by ampa-main-session: shipped in v2.0.8.
