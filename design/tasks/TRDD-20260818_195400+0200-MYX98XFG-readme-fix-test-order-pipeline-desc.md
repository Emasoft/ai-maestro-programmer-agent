---
trdd-id: MYX98XFG
title: README misdescribes test_order_pipeline as publish.py ordering tests
column: todo
created: 2026-08-18T19:54:00+0200
updated: 2026-08-18T19:54:00+0200
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
