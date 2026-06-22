---
trdd-id: e4e12416-9f53-48c9-a32a-40bb1e7eae53
title: smart_exec.py robustness (fail-fast, timeouts, symmetry) + hermetic unit tests
column: complete
created: 2026-06-22T02:40:15+0200
updated: 2026-06-22T03:07:24+0200
current-owner: ampa
assignee: ampa
priority: 3
severity: MEDIUM
effort: M
labels: [smart-exec, fail-fast, timeout, tests, tdd]
task-type: bugfix
parent-trdd: null
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
test-requirements: [unit, lint, typecheck]
review-requirements: []
impacts: []
attempts: 1
last-test-result: pass
implementation-commits: [4809a20]
---

# TRDD-e4e12416 — smart_exec.py robustness + tests

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-06-22

**Origin:** the `go-on-yourself` pass. `scripts/smart_exec.py` (583 LOC, pure argv
builders) has real robustness gaps AND **zero unit tests**. mypy + ruff are already
clean. Source of findings: `reports/ampa-audit/20260622_023521+0200-scripts-tests.md`.

**Current state:** PLANNED. Fix 3 smart_exec issues + 1 pre-push issue, then add
~12-15 hermetic table-driven unit tests (TDD: tests assert the FIXED behavior).

**NEXT ACTION:** apply fixes, write `tests/test_smart_exec.py`, verify mypy/ruff/pytest green.

### Fix 1 — H1: unknown tool leaks a raw traceback instead of clean fail-fast (MEDIUM)
- **Defect (✓ verified by running):** `main()` calls `resolve_tool(ns.tool)`
  (`scripts/smart_exec.py:535`) OUTSIDE the `try/except Exception` block at
  `:551-555`. `resolve_tool` `raise ValueError` for an unknown tool, so
  `smart_exec.py which notatool` dumps a Python traceback (exit code IS 1, but the
  UX is a stack trace, not the clean `Error: ...` the sibling `choose_best` path
  emits). Inconsistent error handling; violates the fail-fast/clean-exit mandate.
- **Fix:** move the `resolve_tool` call + the `--ecosystem` rebuild + the
  `tool_args` strip (lines 535-549) INSIDE the existing `try:` at 551 (whose
  `except Exception as e: print(f"Error: {e}", file=sys.stderr); return 1` already
  does the right thing). One-block move — do not duplicate the handler.

### Fix 2 — M1: get_version subprocess has no timeout (hang risk)
- **Defect (✓ verified):** `get_version` (`scripts/smart_exec.py:182`) runs an
  executor's `--version` with no `timeout=`. A wedged probe (dead docker daemon,
  network-blocking `deno`, `pwsh` cold-start) hangs the whole `executors` command
  forever. Every `subprocess.run` in publish.py/pre-push-hook.py carries a timeout;
  smart_exec is the lone outlier.
- **Fix:** add `timeout=10` to line 182's `subprocess.run`; the existing bare
  `except Exception` already swallows `TimeoutExpired` → returns `None` →
  reported unavailable (correct degradation). Leave line ~578 (the user's actual
  tool invocation) alone — a long-running linter is legitimate.

### Fix 3 — M3: uv version reported only when uvx is ABSENT (cosmetic asymmetry)
- **Defect (✓ verified):** `executor_versions()` (`:193-196`) uses
  `if have("uvx"): ... elif have("uv"): ...`. When both are present (the common
  case) `uv`'s version is silently omitted, unlike every other executor's
  independent `if`. Affects only the `executors` JSON report, not selection.
- **Fix:** split into two independent `if have("uvx"):` / `if have("uv"):` blocks.

### Fix 4 — M2: pre-push-hook.py uvx --version probe has no timeout (consistency)
- **Defect (✓ verified):** `scripts/pre-push-hook.py:170`
  `subprocess.run(["uvx","--version"], ...)` has no `timeout`. Add `timeout=10`.
  **Do NOT change** the warn-and-allow-on-missing-uvx semantics (a documented,
  defensible soft-skip — CI re-runs the strict gate and is the real backstop).

### Tests — new tests/test_smart_exec.py (~12-15 hermetic table-driven cases)
Pure argv-builder assertions (no subprocess; monkeypatch `have()`/`which()` or call
builders directly). Cover, per the audit matrix: `resolve_tool` known→spec /
**unknown→ValueError** (the fail-fast + typosquat guard); `bunx_argv`/`npx_argv`/
`pnpm_dlx_argv`/`yarn_dlx_argv`/`npm_exec_argv` `cmd==pkg` vs `cmd!=pkg`; `uvx_argv`
`pkg==cmd` vs `pkg!=cmd` + `latest=False`; `deno_npm_argv` latest toggle + perms;
`build_argv_for_executor` ecosystem gating (python↛bunx, node↛uvx); `choose_best`
direct-path-wins + priority + `RuntimeError` when nothing applies; **`powershell_module_argv`
injection guard** (accept clean, reject metacharacters — SECURITY); `ps_quote`
`'`→`''`; `main` leading-`--` stripped exactly once.

## Acceptance criteria
- `smart_exec.py which notatool` prints `Error: Unknown tool ...` to stderr, exit 1,
  NO traceback.
- `tests/test_smart_exec.py` passes via `uv run --with pytest pytest tests/ -x -q`.
- mypy + ruff clean; no behavior change to valid invocations.

## Durable artifacts to read before acting
- `reports/ampa-audit/20260622_023521+0200-scripts-tests.md` (H1, M1, M3, M2 + the test matrix)

## Approval log
- 2026-06-22T02:40:15+0200 — Authored under `go-on-yourself`. Tier-0 / planned.
