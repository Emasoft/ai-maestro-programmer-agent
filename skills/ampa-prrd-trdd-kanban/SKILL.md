---
name: ampa-prrd-trdd-kanban
description: "MEMBER (programmer)'s role in the PRRD / TRDD / Kanban workflow. Use when this agent is the assignee of a TRDD in dev or testing — implementing code, running tests, recording commit SHAs, bouncing back from test failures, signalling completion through the pre-PR gate."
license: MIT
compatibility: Requires the universal prrd-trdd-kanban skill (ai-maestro-plugin) for shared mechanics.
allowed-tools: "Bash(python3:*), Bash(get-prrd.py:*), Bash(findprrd.py:*), Bash(findtrdd.py:*), Bash(kanban.py:*), Bash(git:*), Read, Edit, Write, Grep, Glob"
metadata:
  author: "Emasoft"
  version: "1.1.0"
context: fork
agent: ai-maestro-programmer-agent-main-agent
disable-model-invocation: true
---

# AMPA PRRD / TRDD / Kanban Skill

## Overview

This is the MEMBER (programmer)'s role-specific layer of the PRRD /
TRDD / Kanban model — the file-based 3-pillars task system (TRDD task
documents, PRRD project rules, the `design/` kanban). MEMBER is the
implementer: when ORCHESTRATOR sets `assignee:` and moves a TRDD to
`dev`, MEMBER owns that TRDD's movement through `dev → testing →
ai_review` (and back to `dev` on test failure, up to the project's
`test-failures` threshold). One MEMBER per session; many MEMBERs may
work different TRDDs in parallel. The INTEGRATOR — never the MEMBER —
owns the final `→ completed` flip after validating the merged PR against
the TRDD. For universal mechanics, see the `prrd-trdd-kanban` skill in
`ai-maestro-plugin`.

> This file-based kanban (`design/tasks/` + `kanban.py`) is DISTINCT from
> the server-side AI Maestro task API (`/api/teams/{teamId}/tasks`) —
> that integration is tracked separately (issue #7) and is not required
> for this skill.

## Prerequisites

- The universal `prrd-trdd-kanban` skill (`ai-maestro-plugin` — also home
  of `get-prrd.py` / `prrd-edit.py` / `findtrdd.py` / `kanban.py`) for
  shared mechanics and the exempt-operations reference.
- A PRRD at `design/requirements/PRRD.md` and the 4-zone
  `design/{proposals,tasks,refused,archived}/` folders.
- SERENA MCP for code navigation while implementing.
- A TRDD assigned to this session (`assignee: <member-session>`,
  `column: dev`), received via an AMP notification **directly from your
  ORCHESTRATOR** (R6 v3: ORCH ↔ MEMBER is a direct edge; COS guards only
  the team boundary).

## Instructions

1. Read the assigned TRDD frontmatter and body completely.
2. **Answer the task-comprehension handshake (loop a) BEFORE coding:**
   send ORCH all five points (restate / files+domains / ambiguities /
   risks / NPT-EHT) per `op-comprehension-handshake`
   (`ampa-orchestrator-communication`), and WAIT for confirmation.
3. Check `relevant-rules:` and cite each with `get-prrd.py --cite <N>`;
   add any missing rule numbers to `relevant-rules:`.
4. If `delivery: pull-request`, create the feature branch
   `git checkout -b feature/TRDD-<id8>-<slug>`, then set
   `feature-branch:` in the TRDD and bump `updated:`.
5. Implement to the TRDD's acceptance criteria. Author your DERIVED
   TASKS (NPT/EHT) directly in `design/tasks/` as `planned` — Tier-0
   self-authority covers your own in-scope implementation subtasks.
   **In-dev issues (loop b): raise any ambiguity, blocker, or suspected
   design flaw to ORCH immediately — NEVER silently improvise around a
   design flaw** (ORCH pulls in ARCH for design, INT for CI/merge).
6. Stage and commit with the TRDD short-ref in the message
   (`git commit -m "feat: <change> (TRDD-<id8>)"`), then append the SHA
   to `implementation-commits:`.
7. Set `column: testing`, bump `updated:`, and run the union of
   `test-requirements:` and `audit-requirements:`; pipe output to
   `reports/member/<TS>-tests-<id8>.log`.
8. On pass: set `last-test-result: pass`, `last-test-at: <iso>`,
   `column: ai_review`. If `delivery: pull-request`, **clear the pre-PR
   gate (loop c) FIRST**: ask ORCH "I believe TRDD-<id8> is done — PR
   now?" per `op-pre-pr-gate` and open the PR only on the explicit
   green-light. Then notify ORCH directly.
9. On fail: set `last-test-result: fail`, increment `test-failures:`,
   append a `## Test failure post-mortem <N>` section, set
   `column: dev`, fix, and re-iterate from step 6.

### Approval tiers (what you may do alone)

- **Tier 0 (exempt — just do it):** `dev → testing`, `testing →
  ai_review` on pass, `testing → dev` on fail (mechanical bounce),
  recording `implementation-commits:`, appending post-mortems, setting
  `feature-branch:`, authoring NPT/EHT in `design/tasks/`, filing PRRD
  proposals via `prrd-edit.py propose`.
- **Tier 1 (via COS) / Tier 2 (MANAGER via COS):** anything beyond your
  slice — reprioritizing others' work, baseline deviations, cross-team
  reach, entering the release pipeline. File a `proposal` in
  `design/proposals/` and route per the approval-tiers rule.
- **A MEMBER never self-approves its own releases — USER or MANAGER
  approve entering the release pipeline**, and the INTEGRATOR owns the
  `→ completed` flip (PRRD S3.1 / S7.1).

## Output

- Commits whose messages carry the TRDD short-ref (and PRRD rule when
  relevant), with SHAs recorded in `implementation-commits:`.
- Test run logs and `last-test-result:` / `last-test-at:` fields.
- Column moves: `dev → testing`, `testing → dev` on failure,
  `testing → ai_review` on pass — gated by the three dialog loops.

## Error Handling

- When `test-failures:` reaches the project threshold (default 5), stop
  iterating, write a `## Escalation note` in the TRDD body, and AMP-send
  **ORCH directly** requesting reassignment or re-design. Wait for ORCH
  to escalate to ARCH or reassign before resuming.
- When `ai_review` rejects, treat findings as TRDD updates, implement,
  re-test, and re-submit. NEVER remove a test that surfaces a real bug —
  the test is the spec.

## Examples

- Assigned a `pull-request` TRDD: read it, answer the handshake, get
  ORCH's confirmation, cite PRRD S64.3, branch
  `feature/TRDD-1a2b3c4d-add-cache`, implement, commit
  `feat: add request cache (TRDD-1a2b3c4d, PRRD S64.3)`, record the SHA,
  move to `testing`, tests pass, clear the pre-PR gate with ORCH, open
  the PR, move to `ai_review`.
- Tests fail at attempt 2: set `last-test-result: fail`, bump
  `test-failures:` to 2, append `## Test failure post-mortem 2`, move
  back to `dev`, fix the defect, re-commit, re-run.

## Resources

For the shared workflow mechanics and the exempt-operations reference,
consult the universal `prrd-trdd-kanban` skill bundled in
`ai-maestro-plugin`; its exempt-operations reference is the authority on
which transitions need MANAGER approval. The dialog-loop templates live
in `ampa-orchestrator-communication` (`op-comprehension-handshake`,
`op-pre-pr-gate`). The MEMBER persona lives in the
`ai-maestro-programmer-agent-main-agent` agent definition.
