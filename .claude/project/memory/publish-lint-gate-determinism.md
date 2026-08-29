---
name: publish-lint-gate-determinism
description: "publish.py suddenly fails the lint gate with dozens of ruff errors after no code change — why, and the fix"
ocd: 2026-07-24
lmd: 2026-07-24
metadata:
  node_type: memory
  type: project
  tier: component
publish-globally: false
---

`scripts/publish.py`'s lint gate runs ruff **UNPINNED** (`uv run --with ruff ruff
check .`). `pyproject.toml`'s `[tool.ruff]` set only `line-length` with **no
`select`**, so the gate used ruff's *default* rule set — which **drifts across ruff
releases**. On 2026-07-24 `--with ruff` resolved to ruff 0.16.0, whose default
expanded to BLE001 / PLW1510 / S110 / EXE001 / SIM / PIE / PLR, surfacing **64
pre-existing tooling lints** (49 in publish.py's own intentional blind-excepts) and
blocking a publish that passed clean under the older ruff v1.4.5/v1.4.6 shipped with.
Under the shipped gate (`ruff check . --select E4,E7,E9,F`) the tree passes.

**Fix (TRDD-1TXG0EON, commit 459032f):** pin the shipped rule set explicitly —
`[tool.ruff.lint] select = ["E4", "E7", "E9", "F"]`. This restores the exact gate every
release met and makes it version-stable. It is NOT a relaxation (E4/E7/E9/F is the
standard v1.4.x passed); adopting ruff's stricter defaults would be a separate opt-in.

## Notes and lessons learned

[^1]: [id:ATOM-RUFF-DRIFT01, status:valid, keywords:"publish_lint_gate_fails_after_no_code_change unpinned_ruff_default_drift ruff_check_dozens_of_errors", ocd:2026-07-24, lmd:2026-07-24]
  DO NOT treat a sudden lint-gate failure (many errors, none in your diff) as YOUR
  regression or "relax the gate", BECAUSE an UNPINNED linter in a publish/CI gate silently
  drifts — a new release with expanded defaults blocks builds that passed before. DO pin
  the intended rule set (or the tool version) so the gate is deterministic; verify with the
  historical default (`ruff check . --select E4,E7,E9,F`) before concluding it's your code.
