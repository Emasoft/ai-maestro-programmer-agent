---
trdd-id: U5ECXGOC
title: pre-push-hook header documents a validator and install path that do not exist
column: published
created: 2026-08-18T19:54:00+0200
updated: 2026-08-18T20:15:00+0200
release-via: publish
implementation-commits: [c494626]
current-owner: ampa-main-session
task-type: docs
approval-tier: 0
relevant-rules: [1]
---

Phase 2 of the self-audit (hub TRDD-BRRJK57P). Findings axis3-C1 + axis3-C3 (same
stale header block), CONFIRMED and coordinator re-verified:

- `scripts/pre-push-hook.py:2-11` documents `validate_plugin.py` with "MINOR (exit 3)
  = warning only, push allowed". Reality: no `validate_plugin.py` exists anywhere
  (`find -iname` → nothing); the hook runs `cpv-remote-validate --strict` (:193) and
  blocks on ANY non-zero exit including 3 (:217-224) — matching CI's gate, as the
  in-code comment at ~:208 correctly states. The header contradicts the code it heads.
- `:14` instructs `cp git-hooks/pre-push .git/hooks/pre-push`; no `git-hooks/` exists
  in the tree (only a rejected artifact under gitignored reports_dev). The live
  mechanism is `.githooks/` + `git config core.hooksPath .githooks`, enforced by
  `publish.py:144-167`.

## Fix

Rewrite the header block (lines 2-16) to describe reality: cpv-remote-validate
--strict, all non-zero exits block, install via `git config core.hooksPath .githooks`
(auto-enforced by publish.py).

## Acceptance

- Header mentions neither `validate_plugin.py` nor `git-hooks/` nor "warning only".
- Header's exit-code table matches the blocking behavior at :217-224.

## Approval log

- 2026-08-18T20:05:00+0200 — todo→dev→testing→ai_review→complete by ampa-main-session (hub Phase-2 GO). Fixed in c494626; header now names cpv-remote-validate --strict, all-non-zero-block semantics, and the .githooks/core.hooksPath install.
- 2026-08-18T20:15:00+0200 — complete→publish→published by ampa-main-session: shipped in v2.0.8.
