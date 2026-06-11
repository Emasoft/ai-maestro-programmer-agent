---
prrd-version: 1.1
updated: 2026-06-12T01:28:38+0200
project: ai-maestro-programmer-agent
project-id: autonomous
canonical-source: design/requirements/PRRD.md
mirrors: []
---

# Project Requirements & Rules — ai-maestro-programmer-agent

MEMBER role plugin (AMPA) — implementation, testing, the dev/testing columns.

## §0. Canonical source + copies

| Path | Role | Update strategy |
|---|---|---|
| `design/requirements/PRRD.md` | **CANONICAL** for this project | Edit first. Bump `prrd-version:`. Update `updated:`. |

## §I. How to read this document

Rule citation form: `PRRD G<n>.<v>` (golden, user-set) or `PRRD S<n>.<v>`
(silver, manager-mutable). Rule numbers are globally unique across G/S;
promote/demote flips the letter without changing the number. The
`get-prrd.py <n>` script returns a rule's text by bare number. Full
spec: `~/.claude/rules/prrd-design-rules.md`.

## 🥇 GOLDEN — set by the USER (immutable to MANAGER)

- **G1.1** — Every agent that writes to GitHub (issue, issue comment, PR, PR comment, PR review, discussion, release note) MUST begin the body with a one-line self-identification of which agent/role/plugin authored it, because all AI Maestro agents share the single human-owner GitHub identity (the owner's gh CLI auth). Recommended leading line: _Posted by the Claude developing **<plugin-or-role>** (via the shared @owner gh auth)._ Commit messages SHOULD carry an `Agent: <role>` trailer.
- **G2.1** — Validation runs ONLY through the CPV plugin invoked remotely (`uvx --from git+https://github.com/Emasoft/claude-plugins-validation … cpv-remote-validate`); vendored copies of validator scripts are forbidden in this repo. CPV false positives and errors are reported as issues on `Emasoft/claude-plugins-validation`; REAL security findings are devitalized or removed — never exempted or suppressed (the exempt-list mechanism was dropped fleet-wide as exploitable).

## 🥈 SILVER — MANAGER-mutable (agents propose via COS)

- **S3.1** — Releases ship exclusively through `scripts/publish.py` (the strict no-skip pipeline: tests → lint → CPV strict → consistency → bump → changelog → tag → push → GitHub release). The pipeline-installed pre-push hook makes `publish.py` the sole sanctioned pusher. A MEMBER never self-approves its own release — USER or MANAGER authorize entering the release pipeline.
- **S4.1** — Every skill, command, hook, and runtime behavior in this plugin ships real tests (no mocks, no conceptual tests); the test runner exits 0 on all-pass and non-zero on any-fail, and `publish.py` runs it as a mandatory gate.
- **S5.1** — Memory notes follow the symptom-indexed protocol in `rules/memory-protocol.md` (index by the QUESTION, not the answer; recall before acting). `memgrep` is a soft dependency: every consumer gates on `command -v memgrep` and falls back to `grep -rliE` — recall degrades, never breaks.
- **S6.1** — Task state lives on the TRDD v2 `column:` pipeline with the 4-zone `design/{proposals,tasks,refused,archived}` folders; the v1 5-column `status:` kanban vocabulary is retired. Docs and templates must not reintroduce it — no parallel legacy versions of documents are kept.
- **S7.1** — The three dialog loops are mandatory for every assigned task: (a) the task-comprehension handshake answered in full before coding (`op-comprehension-handshake`), (b) in-dev issues raised to the ORCHESTRATOR immediately — never silently improvise around a design flaw, (c) the pre-PR gate — no PR is opened without the ORCHESTRATOR's explicit green-light (`op-pre-pr-gate`). The INTEGRATOR owns the `→ completed` flip; the MEMBER never self-marks completed.
- **S8.1** — Agent/skill/tool reports are written under the gitignored `reports/` tree (per-component subfolder, `YYYYMMDD_HHMMSS±HHMM` local-time timestamps); both `/reports/` and `/reports_dev/` stay in `.gitignore`.
