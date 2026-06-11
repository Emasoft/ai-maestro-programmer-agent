---
name: op-pre-pr-gate
description: Ask AMOA "PR now?" and wait for an explicit green-light before opening a PR
parent-skill: ampa-orchestrator-communication
---

# Pre-PR Gate — "PR now?" request / reply

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

The pre-PR gate is the third dialog loop (loop (c)) of the corrected workflow
model. It exists to protect INTEGRATOR (AMIA) tokens from premature or
incomplete PRs: **a MEMBER never opens a PR on its own judgment.** You believe
the task is done; AMOA confirms it before any PR exists (R6 v3 / #17 M7c).

## When to Use

- You believe an assigned `TRDD-<id>` is implemented and all its completion
  criteria are met — **but you have not opened a PR yet**.
- Immediately before you would otherwise run `op-create-pull-request`.

## Procedure

1. **Self-verify** the completion criteria first (tests green, lint/type clean,
   edge cases handled, no regressions, all EHTs of the TRDD terminal).
2. **Send the "PR now?" request to AMOA** (template below) using the
   `agent-messaging` skill. Include the evidence so AMOA can validate without a
   round-trip.
3. **WAIT** for AMOA's reply. Do **not** open a PR while waiting.
4. **On `GO`** — proceed to `op-create-pull-request`, then send the completion
   notification (`op-notify-completion`). In orchestrated mode AMOA routes the
   PR to AMIA.
5. **On `HOLD` / `BACK`** — return to dev, address AMOA's points, then re-run
   this gate. Never reinterpret a HOLD as a GO.

## Request template (MEMBER → AMOA)

- **Recipient**: your assigned orchestrator agent (AMOA)
- **Subject**: `PR-NOW? <TRDD-id> — <brief description>`
- **Type**: status
- **Priority**: normal
- **Content**:

```text
I believe <TRDD-id> is done — PR now?

Evidence:
- Acceptance criteria: <met — list the criteria and how each is satisfied>
- EHTs: <all terminal — list each EHT TRDD-id + its column>
- Tests: <green — total/passed, coverage%, command used>
- Lint/type: <clean — tools run>
- Branch: <branch-name> (<N commits, files changed, +adds/-dels>)
- Risks/notes: <anything AMOA should weigh before the PR>

Awaiting your GO / HOLD before opening the PR.
```

## Reply semantics (AMOA → MEMBER)

| Reply | Meaning | Your next action |
| ----- | ------- | ---------------- |
| **GO** | AMOA validated acceptance criteria, EHT-terminal, tests green | Run `op-create-pull-request`, then `op-notify-completion` |
| **HOLD: \<reason\>** | A criterion is unmet or a risk is unresolved | Fix the named item, then re-run this gate |
| **BACK-TO-ARCH: \<reason\>** | A design flaw surfaced (not just an impl gap) | AMOA pulls in AMAA; wait for revised TRDD(s) before re-gating |

## Example

- **Subject**: `PR-NOW? TRDD-9a8aba94 — order-pipeline retry logic`
- **Content**: "I believe `TRDD-9a8aba94` is done — PR now? Evidence: acceptance
  criteria met (retry with backoff + idempotency key, both covered by tests);
  EHTs `TRDD-71a2239a` (update callers) and `TRDD-7e80e484` (docs) both in
  `complete`; tests 35/35 green, 94% (`uv run pytest -q`); ruff + mypy clean;
  branch `feat/9a8aba94-order-retry` (4 commits, 6 files, +312/-40). Risk:
  changes the public `process()` signature — flagged for AMIA. Awaiting GO/HOLD."

**Verify**: confirm the request appears in your sent messages; do not proceed
until AMOA replies.

## Error Handling

| Error | Cause | Resolution |
| ----- | ----- | ---------- |
| No AMOA reply within the team's gate timeout | AMOA busy / offline | Re-send once via `agent-messaging`; if still none, escalate the blocker to AMCOS — do **not** self-authorize the PR |
| AMOA reply ambiguous | Unclear GO vs HOLD | Ask one clarifying question; treat anything not an explicit GO as HOLD |
| You already opened the PR before gating | Gate skipped | Convert the PR to draft (`gh pr ready --undo` / open as `--draft`), run the gate, and only mark ready on GO |
