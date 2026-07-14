---
trdd-id: W5WYY2VF
title: Extend the G1.1 self-id to the PR-review-comment path and add the Agent commit trailer
column: complete
created: 2026-07-15T00:34:50+0200
updated: 2026-07-15T00:38:00+0200
current-owner: ai-maestro-programmer-agent
task-type: docs
approval-tier: 0
relevant-rules: [1]
release-via: publish
implementation-commits: [3d93133]
last-test-result: pass
---

# TRDD-W5WYY2VF — G1.1 self-id on the review-comment path + `Agent:` commit trailer

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-15

- **Current state (verified):**
  - `op-create-pull-request.md` ✅ has the G1.1 self-id line; `op-write-bug-report.md` ✅ has
    it too (the audit called it missing — it is present at :106). `test_m10` guards both.
  - `op-respond-to-review.md` ❌ — the `gh pr comment … ## Changes Made in Response to Review`
    body (:173+) is posted to GitHub with **no** self-id line. This is a real gap.
  - `op-commit-changes.md` ❌ — the commit convention (§3.2) documents type/scope/subject/
    body/footer but **no `Agent:` trailer**, so the fleet's commit self-id convention
    (`commit-discipline.md`, `PRRD G1.1`) is undocumented in the agent's own manual.
- **NEXT ACTION:** (1) extend `test_m10` to also require the self-id needle in
  `op-respond-to-review.md`, plus a new assertion that `op-commit-changes.md` documents the
  `Agent:` trailer — RED first. (2) add the self-id line to the review-comment body. (3) add
  the `Agent: <plugin-slug>` trailer to the commit convention (footer components + example).
- **Load-bearing facts:**
  - Canonical self-id wording (mirror it exactly):
    `_This is the Claude responsible for the <project> project (AMPA programmer, via the
    shared owner gh auth)._`
  - The needle `test_m10` matches is `"This is the Claude responsible for the"`.
  - Only the **GitHub-posted** review comment needs the line — a local `gh pr comment` that
    summarizes changes IS a GitHub post, so it qualifies.
- **Reported by:** the MANAGER's fleet-readiness audit `#25` (section B, MED). The audit's
  claim that op-write-bug-report lacks the line is stale — note that in the closure report.

## Problem

All AI Maestro agents share ONE human-owner GitHub identity, so G1.1 requires every
GitHub-posted body to open with a one-line self-id naming the authoring agent. The PR and
bug-report paths carry it; the **PR-review-comment** path does not — a review reply posts
under the shared identity with no attribution. And the agent's commit-convention doc never
mentions the `Agent:` trailer, even though `commit-discipline.md` asks every commit to carry
it (and this session's commits do).

## Required changes

1. `op-respond-to-review.md` — the review-comment body begins with the G1.1 self-id line;
   add a one-line note that any GitHub-posted comment must carry it (cite G1.1).
2. `op-commit-changes.md` — document the `Agent: <plugin-slug>` trailer in §3.2 (footer
   components + the worked example), so the manual matches the convention the commits follow.
3. `tests/test_primary_skills.py::test_m10` — extend to require the self-id needle in
   `op-respond-to-review.md`; add a small assertion that `op-commit-changes.md` documents the
   `Agent:` trailer. (TDD: assertions RED before the doc edits.)

## Success criteria

- `test_m10` (extended) green; full suite green; CPV strict 0/0/0/0.
- Every GitHub-posting op file on the agent surface carries the self-id line.

## Notes

- Scoped to the two real gaps only. NOT touching the 3-pillars wiring (blocked on
  `ai-maestro#61` Q1/Q2) or `min-approval-requirement:` (blocked on Q3).
