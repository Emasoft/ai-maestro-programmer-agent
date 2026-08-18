---
trdd-id: 1TXG0EON
title: Pin the ruff lint gate to its shipped rule set so ruff-default drift stops blocking publishes
column: completed
created: 2026-07-24T14:25:23+0200
updated: 2026-08-18T19:54:00+0200
current-owner: ampa-programmer
task-type: bugfix
min-approval-requirement: none
mandate: true
mandated-by: self
relevant-rules: [1]
implementation-commits: [459032f]
---

# Pin the ruff lint gate to its shipped rule set so ruff-default drift stops blocking publishes

## ⏵ STATE — READ THIS FIRST ON RESUME — 2026-07-24

**Symptom:** `publish.py --dry-run` fails the LINT gate with 64 ruff errors — 49 in
`scripts/publish.py`, the rest in other scripts/tests. NONE are in the TRDD-I8AH88SS
/ K2X9RF7S / G0768YHK rewire; the rewire's only Python change (`tests/test_primary_
skills.py`) is clean.

**Root cause (verified, not assumed):** `[tool.ruff]` in `pyproject.toml` sets only
`line-length` — no `select` — so the gate used ruff's DEFAULT rule set. `publish.py`
runs `uv run --with ruff ...` with ruff UNPINNED, so it now resolves to **ruff 0.16.0**,
whose default rule set **expanded** to include BLE001 / PLW1510 / S110 / EXE001 / SIM /
PIE / PLR (verified via `ruff check . --statistics`). Under the project's shipped gate
(`ruff check . --select E4,E7,E9,F`) **all checks pass** (verified). v1.4.5/v1.4.6 shipped
clean because `--with ruff` then resolved to an older ruff with the narrower default.
No hidden `ruff.toml` exists anywhere (verified).

**This is a gate-DETERMINISM defect, not a code-quality regression.** The code meets the
E4/E7/E9/F standard every prior release met. The 64 "errors" are rules the project never
adopted, concentrated in intentionally broad-catch tooling (`publish.py`).

**FIX (non-relaxing):** make the shipped rule set explicit under `[tool.ruff.lint]`
`select = ["E4", "E7", "E9", "F"]`. This restores the exact gate v1.4.x shipped under and
makes it version-stable. It does NOT weaken protection below the shipped standard;
adopting ruff 0.16's stricter defaults (and fixing the 64 tooling lints, incl. narrowing
publish.py's blind-excepts) would be RAISING the gate — a separate, opt-in decision, out
of scope for the parity mission.

**FLAGGED FOR USER REVIEW:** this touches the lint gate config. It is one line, fully
reverting to `git revert`, and non-relaxing. If the owner prefers to ADOPT ruff 0.16's
stricter defaults instead, that is a follow-up TRDD (fix 64 lints, mostly in publish.py).

**NEXT ACTION:** none — applied. Optional latent-defect follow-up: `publish.py` uses
`--with ruff`/`--with ruff` UNPINNED for lint (and ruff/pytest generally), so the gate is
non-deterministic across upstream releases; pinning the tool versions in publish.py is a
separate hardening task.

## Acceptance criteria

- `uv run --with ruff ruff check .` passes (0 errors) with the explicit select.
- `uv run --with pytest pytest tests/ -q` still 93 passed.
- `pyproject.toml` change is one `[tool.ruff.lint] select` block; nothing else relaxed.

## Approval log

- 2026-08-18T19:54:00+0200 — COMPLETED by ampa-main-session (TRDD-LNSZPCKE closing edit). The f29e1c2 archival was a pure git mv that skipped the protocol's `complete → completed` column edit; performed here. Work had shipped in 459032f.
