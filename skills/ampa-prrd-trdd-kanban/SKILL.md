---
name: ampa-prrd-trdd-kanban
description: "MEMBER (programmer)'s ROLE POLICY for the PRRD / TRDD / Kanban workflow — the op-set a MEMBER may run, the self-mandate rule for Tier-0 work, the missing-derived-TRDD duty, and which moves need approval. Use when this agent is the assignee of a TRDD in dev or testing, or is authoring its own Tier-0 / derived tasks. Mechanics are the core granular ama-* pillar skills; this skill is the policy layer over them, not a passthrough."
license: MIT
compatibility: Uses the core granular ama-* pillar skills (ai-maestro-plugin >=2.7) for all mechanics.
allowed-tools: "Bash(git:*), Read, Edit, Write, Grep, Glob"
metadata:
  author: "Emasoft"
  version: "1.2.0"
context: fork
agent: ai-maestro-programmer-agent-main-agent
disable-model-invocation: true
---

# AMPA MEMBER role policy (PRRD / TRDD / Kanban)

## Overview

This is the MEMBER (programmer)'s role-**policy** layer over the file-based
3-pillars task system (TRDD task documents, PRRD project rules, the `design/`
kanban). It carries what a MEMBER may DO and when to escalate; the mechanics are
the core **granular `ama-*` pillar skills** (single source of truth — no local
copy to drift). MEMBER is the implementer: when ORCHESTRATOR sets `assignee:` and
moves a TRDD to `dev`, MEMBER owns that TRDD's movement through `dev → testing →
ai_review` (and back to `dev` on test failure, up to the project's
`test-failures` threshold). One MEMBER per session; many MEMBERs may work
different TRDDs in parallel. The INTEGRATOR — never the MEMBER — owns the final
`→ complete` flip after validating the merged PR against the TRDD.

> This file-based kanban (`design/tasks/` + `ama-kanban-render`) is DISTINCT from
> the server-side AI Maestro task API (`/api/teams/{teamId}/tasks`) — that
> integration is tracked separately (issue #7) and is not required for this skill.

## The pillar mechanics — the core granular `ama-*` skills

Invoke these core skills for the mechanics (each carries its own script
allow-list; do not re-implement them here):

| Pillar op | Skill | MEMBER access |
|---|---|---|
| Read / cite a PRRD rule | `ama-prrd-get` | read — every role |
| Search the PRRD by content | `ama-prrd-find` | read — every role |
| Propose a PRRD-rule change | `ama-prrd-propose` | **your** path to request a rule change (non-binding) |
| Edit the PRRD directly | `ama-prrd-edit` | GATED — MANAGER/USER only; **not yours** |
| Author a TRDD | `ama-trdd-write` | **YES**, for your own Tier-0 work (self-mandate, below) |
| Update a TRDD's body / non-column fields | `ama-trdd-update` | **YES**, on a TRDD you own (commits, STATE, post-mortems) |
| Move a TRDD between columns | `ama-trdd-transition` | signal-only for you (`dev → testing`; `testing → dev` on fail) |
| Find TRDDs | `ama-trdd-find` | read — every role |
| Render the kanban board | `ama-kanban-render` | read — every role |
| Approve / refuse / archive proposals | `ama-proposal-approvals` | **read / list ONLY**; never invoke the decision verbs |

## Prerequisites

- The core granular `ama-*` pillar skills above (`ai-maestro-plugin` >=2.7).
- A PRRD at `design/requirements/PRRD.md` and the 4-zone
  `design/{proposals,tasks,refused,archived}/` folders.
- SERENA MCP for code navigation while implementing.
- A TRDD assigned to this session (`assignee: <member-session>`,
  `column: dev`), received via an AMP notification **directly from your
  ORCHESTRATOR** (R6 v3: ORCH ↔ MEMBER is a direct edge; COS guards only
  the team boundary).

## Instructions

1. Read the assigned TRDD frontmatter and body completely (`ama-trdd-find` to
   locate it by id/column).
2. **Answer the task-comprehension handshake (loop a) BEFORE coding:**
   send ORCH all five points (restate / files+domains / ambiguities /
   risks / NPT-EHT) per `op-comprehension-handshake`
   (`ampa-orchestrator-communication`), and WAIT for confirmation.
3. Check `relevant-rules:` and cite each via `ama-prrd-get`; add any missing rule
   numbers to `relevant-rules:` (`ama-trdd-update`).
4. If `delivery: pull-request`, create the feature branch
   `git checkout -b feature/TRDD-<id8>-<slug>`, then set `feature-branch:` in the
   TRDD (`ama-trdd-update`) and bump `updated:`.
5. Implement to the TRDD's acceptance criteria. Author your DERIVED TASKS
   (NPT/EHT) directly via `ama-trdd-write` as a **self-mandate** (see below) —
   Tier-0 self-authority covers your own in-scope subtasks. **In-dev issues
   (loop b): raise any ambiguity, blocker, or suspected design flaw to ORCH
   immediately — NEVER silently improvise around a design flaw** (ORCH pulls in
   ARCH for design, INT for CI/merge).
6. Stage and commit with the TRDD short-ref in the message
   (`git commit -m "feat: <change> (TRDD-<id8>)"`), then append the SHA to
   `implementation-commits:` (`ama-trdd-update`).
7. Set `column: testing` (`ama-trdd-transition`), bump `updated:`, and run the
   union of `test-requirements:` and `audit-requirements:`; pipe output to
   `reports/member/<TS>-tests-<id8>.log`.
8. On pass: set `last-test-result: pass`, `last-test-at: <iso>` (`ama-trdd-update`),
   `column: ai_review` (`ama-trdd-transition`). If `delivery: pull-request`,
   **clear the pre-PR gate (loop c) FIRST**: ask ORCH "I believe TRDD-<id8> is
   done — PR now?" per `op-pre-pr-gate` and open the PR only on the explicit
   green-light. Then notify ORCH directly.
9. On fail: set `last-test-result: fail`, increment `test-failures:`, append a
   `## Test failure post-mortem <N>` section (`ama-trdd-update`), set
   `column: dev` (`ama-trdd-transition`), fix, and re-iterate from step 6.

## The self-mandate rule (your Tier-0 work is born approved)

A MEMBER's own Tier-0 work — the NPT/EHT of a task you own, and independent tasks
fully inside your assignment scope — is a **self-mandate**. Author it directly via
`ama-trdd-write` into `design/tasks/` (NEVER `design/proposals/`) carrying:

```yaml
column: planned
min-approval-requirement: none
mandate: true
mandated-by: self
```

It is born approved because sender and receiver are the same agent — do NOT queue
your own derived work for someone's approval; that stalls you. The lifecycle uses
the **17-column** vocabulary (14 lifecycle stages + the exception columns
`blocked` / `failed` / `superseded`). `failed` is **retryable and stays in
`design/tasks/`** — it is never archived.

## The missing-derived-TRDD duty (mandatory)

If you receive an assigned TRDD and judge that a required derived TRDD (an NPT or
EHT) is **missing**, you MUST report it to the sender AND you may author it
yourself — a self-mandate if it is inside your slice, or an `ama-prrd-propose`-style
proposal to the required approver if it reaches past your authority. A MEMBER that
executes a TRDD whose EHTs are absent lands the change and leaves the wound open.
Follow `op-report-missing-derived-trdd` (`ampa-orchestrator-communication`).

## Governance — approval requirements

This skill operates under the AI Maestro **approval requirements** — the
`min-approval-requirement:` ladder `none` (Tier-0 self-authority for in-scope work
+ DERIVED NPT/EHT tasks, authored directly as a self-mandate) → `chief-of-staff` →
`manager` → `user`. (`approval-tier:` is the deprecated, decode-only predecessor:
`0→none, 1→chief-of-staff, 2→manager, 3→user`; never write it on a new TRDD.)
See `~/.claude/rules/trdd-approval-tiers.md` for which transitions need approval.

- **min-approval-requirement `none` (exempt — just do it):** `dev → testing`,
  `testing → ai_review` on pass, `testing → dev` on fail (mechanical bounce via
  `ama-trdd-transition`), recording `implementation-commits:`, appending
  post-mortems, setting `feature-branch:` (`ama-trdd-update`), authoring your own
  NPT/EHT via `ama-trdd-write` as self-mandate, filing PRRD proposals via
  `ama-prrd-propose`.
- **`chief-of-staff` / `manager`:** anything beyond your slice — reprioritizing
  others' work, baseline deviations, cross-team reach, entering the release
  pipeline. File a `proposal` in `design/proposals/` and route via your COS.
- **A MEMBER never self-approves its own releases — USER or MANAGER approve
  entering the release pipeline**, and the INTEGRATOR owns the `→ complete` flip
  (PRRD S3.1 / S7.1). `ama-proposal-approvals` is **read/list only** for you.

## Output

- Commits whose messages carry the TRDD short-ref (and PRRD rule when relevant),
  with SHAs recorded in `implementation-commits:`.
- Test run logs and `last-test-result:` / `last-test-at:` fields.
- Column moves: `dev → testing`, `testing → dev` on failure, `testing → ai_review`
  on pass — gated by the three dialog loops, executed via `ama-trdd-transition`.

## Error Handling

- When `test-failures:` reaches the project threshold (default 5), stop iterating,
  write a `## Escalation note` in the TRDD body (`ama-trdd-update`), and AMP-send
  **ORCH directly** requesting reassignment or re-design. Wait for ORCH to escalate
  to ARCH or reassign before resuming.
- When `ai_review` rejects, treat findings as TRDD updates, implement, re-test, and
  re-submit. NEVER remove a test that surfaces a real bug — the test is the spec.

## Examples

- Assigned a `pull-request` TRDD: read it (`ama-trdd-find`), answer the handshake,
  get ORCH's confirmation, cite PRRD S64.3 (`ama-prrd-get`), branch
  `feature/TRDD-1a2b3c4d-add-cache`, implement, commit
  `feat: add request cache (TRDD-1a2b3c4d, PRRD S64.3)`, record the SHA
  (`ama-trdd-update`), move to `testing` (`ama-trdd-transition`), tests pass, clear
  the pre-PR gate with ORCH, open the PR, move to `ai_review`.
- You spot a missing EHT while implementing: report it to ORCH per
  `op-report-missing-derived-trdd`, then author it via `ama-trdd-write` as a
  self-mandate (`min-approval-requirement: none`, `mandate: true`,
  `mandated-by: self`) if it is inside your slice.

## Resources

The mechanics live in the core granular `ama-*` pillar skills bundled in
`ai-maestro-plugin` (the table above). The exempt-vs-approval authority is
`~/.claude/rules/trdd-approval-tiers.md`. The dialog-loop templates and the
missing-derived-TRDD report template live in `ampa-orchestrator-communication`
(`op-comprehension-handshake`, `op-pre-pr-gate`, `op-report-missing-derived-trdd`).
The MEMBER persona lives in the `ai-maestro-programmer-agent-main-agent` agent
definition.
