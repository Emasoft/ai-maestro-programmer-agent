---
trdd-id: MP45ZMAG
title: README fixer troubleshooting cites nonexistent tests-logs directory
column: published
created: 2026-08-18T19:54:00+0200
updated: 2026-08-18T20:15:00+0200
release-via: publish
implementation-commits: [d1b7f8e]
current-owner: ampa-main-session
task-type: docs
approval-tier: 0
relevant-rules: [1]
---

Phase 2 of the self-audit (hub TRDD-BRRJK57P). Finding axis1-C1, CONFIRMED and
coordinator re-verified at f29e1c2 and again at 8e9264b.

## Defect

`README.md:266` instructs "Review error logs in `tests/logs/`". No `tests/logs/`
directory exists and nothing in the tree writes it — the only occurrence of the
path in the whole repo is the line telling you to read it (`grep -rn "tests/logs" .`
→ README.md:266 only). The instruction is unactionable.

## Fix

Replace the phantom path with an actionable instruction: review the fixer's own
reported linter/formatter output (the errors it prints when it says "Unable to
fix errors").

## Acceptance

- `grep -rn "tests/logs" .` (excluding .git/reports) returns nothing.
- The troubleshooting step tells the reader where the errors actually appear.

## Approval log

- 2026-08-18T20:05:00+0200 — todo→dev→testing→ai_review→complete by ampa-main-session (hub Phase-2 GO). Fixed in d1b7f8e; acceptance verified: `grep -rn "tests/logs" README.md` → exit 1; suite 122 passed.
- 2026-08-18T20:15:00+0200 — complete→publish→published by ampa-main-session: shipped in v2.0.8 (release created, tags pushed atomically).
