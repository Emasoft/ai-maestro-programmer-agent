---
trdd-id: MYX98XFG
title: README misdescribes test_order_pipeline as publish.py ordering tests
column: published
created: 2026-08-18T19:54:00+0200
updated: 2026-08-18T20:15:00+0200
release-via: publish
implementation-commits: [12e8f27]
current-owner: ampa-main-session
task-type: docs
approval-tier: 0
relevant-rules: [1]
---

Phase 2 of the self-audit (hub TRDD-BRRJK57P). Finding axis3-C2, CONFIRMED and
coordinator re-verified: README.md:90 claims `test_order_pipeline.py` "Tests
publish.py release-step ordering"; the script's own docstring says it is a manual
integration test for an order-processing-pipeline EXAMPLE (companion to
`skills/ampa-orchestrator-communication/references/op-notify-completion.md`), and
`grep -ci publish scripts/test_order_pipeline.py` → 0 while the same instrument
scores README 5 and publish.py 58. `docs/AGENT_OPERATIONS.md:513` describes it
correctly ("OrderPipeline validation test suite").

## Fix

Correct the README.md:90 table cell to match the script's real purpose.

## Acceptance

- README row describes the order-pipeline example test, not publish.py.
- README and docs/AGENT_OPERATIONS.md no longer disagree.

## Approval log

- 2026-08-18T20:05:00+0200 — todo→dev→testing→ai_review→complete by ampa-main-session (hub Phase-2 GO). README row now matches the script docstring and AGENT_OPERATIONS.md; suite 122 passed.
- 2026-08-18T20:15:00+0200 — complete→publish→published by ampa-main-session: shipped in v2.0.8.
