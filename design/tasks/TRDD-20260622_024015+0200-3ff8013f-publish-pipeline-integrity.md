---
trdd-id: 3ff8013f-3ee8-496a-bc6f-383d911ecac5
title: publish.py release-pipeline integrity — full-history CHANGELOG + Step-11 staging One-Source-of-Truth
column: planned
created: 2026-06-22T02:40:15+0200
updated: 2026-06-22T02:40:15+0200
current-owner: ampa
assignee: ampa
priority: 2
severity: HIGH
effort: M
labels: [publish, changelog, bugfix, one-source-of-truth]
task-type: bugfix
parent-trdd: null
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
test-requirements: [unit, lint, typecheck]
review-requirements: []
impacts: [ci-pipeline]
attempts: 0
last-test-result: not-run
implementation-commits: []
---

# TRDD-3ff8013f — publish.py release-pipeline integrity

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-06-22

**Origin:** the `go-on-yourself` autonomous-improvement pass (2026-06-22). Two
verified defects in the canonical release pipeline `scripts/publish.py`, found by
the docs-meta + scripts-tests audits (reports under
`reports/ampa-audit/20260622_02*`).

**Current state:** PLANNED. Two independent fixes in `scripts/publish.py`, one
content regen of `CHANGELOG.md`, plus 3-4 added branch tests in
`scripts/test_order_pipeline.py`.

**NEXT ACTION:** apply the two fixes, regenerate the full CHANGELOG, add the
tests, verify (git-cliff both forms + `publish.py --patch --dry-run` green), commit.

### Fix 1 — CHANGELOG collapsed to a single version (HIGH)
- **Defect (✓ verified):** `run_git_cliff` (`scripts/publish.py:830-861`) calls
  `git-cliff --bump --unreleased --tag vX.Y.Z -o CHANGELOG.md`. `--unreleased`
  restricts output to commits **since the last tag**, and `-o` OVERWRITES — so the
  committed `CHANGELOG.md` holds only the newest version (currently just `[1.4.3]`,
  11 lines). The docstring FALSELY claims it "walks the full tag history ... and
  produces the complete CHANGELOG.md". v1.3.0→v1.4.3 all shipped a single-version
  changelog. Running `git-cliff -o CHANGELOG.md` (no `--unreleased`) yields the
  correct **274-line / 13-section** full history (10 non-conventional commits
  correctly skipped by `filter_unconventional = true`).
- **Fix:** drop `--unreleased` from the **CHANGELOG-generation** call so it
  regenerates the complete file every release exactly as the docstring promises
  (`git-cliff --bump --tag vX.Y.Z -o CHANGELOG.md`). **Keep the SECOND call** (the
  release-notes extraction, ~lines 866-880) latest-only — it legitimately wants the
  newest section. Correct the docstring to match. Then regenerate `CHANGELOG.md`
  once to restore the lost history.

### Fix 2 — Step-11 staging diverges from `_list_py_files` (One-Source-of-Truth, latent)
- **Defect (✓ verified):** version bump (`update_python_versions`) and the
  consistency check both find `__version__` markers via `_list_py_files()`
  (gitignore-aware, `git ls-files`). But the Step-11 staging loop
  (`scripts/publish.py:1432-1441`) re-discovers the just-bumped files with a
  bespoke `plugin_root.rglob("*.py")` walk whose skip list does NOT honor
  `.gitignore` / `*_dev/`. Two code paths that must agree on "which .py files carry
  the version" are implemented twice with different rules. LATENT today (no real
  `^__version__` markers exist in-repo) — it activates the day a module gains a real
  `__version__ = "x.y.z"`.
- **Fix:** replace the bespoke `rglob` loop with `for py_path in _list_py_files(plugin_root):`
  keeping the `re.search(... new_version ...)` filter. One selector for version-bearing files.

### Fix 3 — add the 3-4 missing branch tests to scripts/test_order_pipeline.py
Per the scripts-tests audit coverage gap: (a) `validate_order` missing-`order_id`
rejection; (b) a retry-then-**recover** stage asserting `status==COMPLETED and
retry_count>0` (the RETRYING→success transition is currently unreachable/untested);
(c) an exact-batch-size boundary test (`len == batch_size`). Keep all 14 existing
tests passing.

## Acceptance criteria
- `git-cliff -o /tmp/cl.md` (no `--unreleased`) and the committed `CHANGELOG.md`
  agree (full 13-section history); the release-notes extraction still returns only
  the latest section.
- Step-11 staging uses `_list_py_files`; `test_order_pipeline.py --json` still passes
  (now with the added cases); `publish.py --patch --dry-run` is green.
- mypy + ruff clean; the docstring matches the actual behavior.

## Durable artifacts to read before acting
- `reports/ampa-audit/20260622_023429+0200-docs-meta.md` (H1/H2, exact lines + fix)
- `reports/ampa-audit/20260622_023521+0200-scripts-tests.md` (H2 staging, test gaps)

## Approval log
- 2026-06-22T02:40:15+0200 — Authored under the user's `go-on-yourself` directive
  (autonomous in-scope improvement of this plugin). Tier-0 / planned.
