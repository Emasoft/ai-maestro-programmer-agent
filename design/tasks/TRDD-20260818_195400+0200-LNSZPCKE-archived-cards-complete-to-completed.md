---
trdd-id: LNSZPCKE
title: Four archived cards skipped the archival protocol column edit
column: todo
created: 2026-08-18T19:54:00+0200
updated: 2026-08-18T19:54:00+0200
current-owner: ampa-main-session
task-type: docs
approval-tier: 0
relevant-rules: [1]
---

Phase 2 of the self-audit (hub TRDD-BRRJK57P). Finding axis2-C1, CONFIRMED and
coordinator re-verified with the full column × release-via pair table: the archive
SET is substantively correct (no mis-archive), but 4 cards in `design/archived/`
carry `column: complete` + release-via none — the f29e1c2 archival was a pure
`git mv` (0 insertions/0 deletions) that skipped the Archival protocol's
`complete → completed` frontmatter edit:

- TRDD-G0768YHK, TRDD-I8AH88SS, TRDD-K2X9RF7S, TRDD-1TXG0EON

## Fix

Perform the skipped closing edit on each: `column: complete` → `column: completed`,
bump `updated:`, append the Approval-log COMPLETED line. This is the terminal-freeze
exception "the closing edit itself".

## Acceptance

- `grep -H "^column:" design/archived/*.md` shows only completed/published values.

## Approval log
