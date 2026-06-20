---
name: publish-ci-vs-dryrun
description: "publish.py --dry-run (or the local CPV gate) passed but GitHub CI went RED on CPV validation — why local-green is not CI-green for this plugin, and how to not get surprised at tag time"
ocd: 2026-06-21
lmd: 2026-06-21
metadata:
  node_type: memory
  type: project
  tier: component
  functionality: architecture
---
This plugin ships the CPV **`remote-validation` pipeline profile** (CPV TRDD-02e1672b):
`scripts/publish.py`, the auto-generated `cliff.toml`, and `.markdownlint.json` are
**by-design profile-canonical**, and `.github/workflows/release.yml` +
`notify-marketplace.yml` are **ahead-of-canon** (extra hardening). CPV's validator
emits `RC-PIPELINE-DRIFT-001` WARNINGs for these but explicitly **forbids
`--force-templates`** on them — forcing the standard templates would DOWNGRADE the
by-design architecture (e.g. re-vendor the CPV validators this plugin deliberately
removed). The drift WARNINGs are advisory/non-blocking; the plugin validates
`0 CRITICAL / 0 MAJOR / 0 MINOR / 0 NIT` as-is, with 7 non-blocking WARNINGs.

**The trap — local-green is NOT CI-green.** `.github/workflows/validate.yml` runs the gate as:

```
uvx --from git+https://github.com/Emasoft/claude-plugins-validation --with pyyaml \
    cpv-remote-validate plugin . --strict --verbose --report validation-report.md
```

That pulls the **LATEST** CPV from the git default branch — NOT the locally-installed
CPV that `publish.py --dry-run` uses. So a green local dry-run does **not** guarantee
green CI: a CPV release between your install and the CI run can surface new findings.
(CPV#142 documented 4 such CI-only failures for the *standard* `ci.yml` profile — none
affect this plugin, which uses `validate.yml` and has **no** `ci.yml`.)

**The fix — reproduce the EXACT CI command before tagging.** Run the `uvx …
cpv-remote-validate plugin . --strict` line above locally (no `CLAUDE_PRIVATE_USERNAMES`
— this plugin's CI does not set it) and confirm `VALID` / exit 0 BEFORE `publish.py`
tags. Tags are immutable; if CI fails post-tag you roll FORWARD with another patch
bump, you never re-tag. Verified 2026-06-21: v1.4.2 and v1.4.3 were both reproduced
green before tag → CI green.

## Governed by
- [[architecture]] — the publish pipeline is part of the project architecture hub.

## Notes and lessons learned
