---
trdd-id: e39a6aa8-f12d-47fd-b24d-bb3e1f7d7ade
title: CI workflow hardening — least-privilege permissions + job timeouts
column: complete
created: 2026-06-22T10:50:55+0200
updated: 2026-06-22T10:54:13+0200
current-owner: ampa
assignee: ampa
priority: 4
severity: LOW
effort: S
labels: [ci, github-actions, security, hardening]
task-type: security
parent-trdd: null
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
test-requirements: [lint]
review-requirements: []
impacts: [ci-pipeline]
attempts: 1
last-test-result: pass
implementation-commits: [8c561b5]
---

# TRDD-e39a6aa8 — CI workflow hardening

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-06-22

**Origin:** the `go-on-yourself` pass — the one project area not yet audited
(`.github/workflows/`). Applies the USER's standing `~/.claude/rules/gh-actions.md`
standard (least-privilege `permissions`, job `timeout-minutes`). Security-POSITIVE
(tightens, never relaxes); CI is currently green + CPV VALID.

**Confirmed gaps (read all 3 workflows):**
- `validate.yml` — no `permissions:` (job only checks out + CPV-validates + uploads an
  artifact → needs only `contents: read`; `upload-artifact` uses the runtime token, not
  a GITHUB_TOKEN scope) and no `timeout-minutes`.
- `release.yml` — no `permissions:` (checkout + CPV-validate → `contents: read`) and no
  `timeout-minutes`.
- `notify-marketplace.yml` — already `permissions: contents: read` ✓; missing
  `timeout-minutes`.

**Changes (minimal, safe):**
1. Add `permissions:\n  contents: read` (top-level) to `validate.yml` + `release.yml`.
2. Add `timeout-minutes: 15` to the `validate` and `validate-tag` jobs (CPV via uvx
   fetch takes <5 min; 15 is a generous bound preventing a hung-job minute-burn) and
   `timeout-minutes: 10` to `notify-marketplace`'s `notify` job.

**Explicitly NOT done (recommended to USER):** bump `actions/checkout@v6 → @v7` (latest
is the fresh `v7.0.0`; a brand-new major on the release gate deserves a deliberate
opt-in + a CI run to confirm). `setup-python@v6` and `upload-artifact@v7` are already
current majors — no change. Third-party actions are already SHA-pinned.

## Acceptance criteria
- All 3 workflows parse as valid YAML (local `yaml.safe_load`).
- `validate.yml` + `release.yml` carry top-level `permissions: contents: read`; all 3
  jobs carry `timeout-minutes`.
- CPV strict re-run stays **VALID** (0 CRITICAL/MAJOR/MINOR/NIT) after the edits.
- No functional change to what the workflows do (read-only validation / dispatch).

## Durable artifacts to read before acting
- `~/.claude/rules/gh-actions.md` — the standard being applied.
- `.claude/project/memory/publish-ci-vs-dryrun.md` — release.yml/notify-marketplace.yml
  are ahead-of-canon (CPV `--force-templates` forbidden); more hardening stays
  ahead-of-canon + non-blocking.

## Approval log
- 2026-06-22T10:50:55+0200 — Authored under `go-on-yourself`, applying the user's own
  gh-actions standard (security-positive). Tier-0 / planned.
