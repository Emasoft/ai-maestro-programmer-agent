---
name: ampa-github-operations
description:
  Git and GitHub operations for AMPA. Use when cloning repos, branching,
  committing, opening PRs, or handling review feedback. Trigger with
  /ampa-github-operations. Loaded by ai-maestro-programmer-agent-main-agent.
license: MIT
compatibility: Requires gh CLI authenticated.
metadata:
  author: AI Maestro
  version: 1.0.20
  workflow-instruction:
    "Steps 14 (clone/fork), 17 (branch/commit), 19 (PR creation). Also handles
    AMPA response portions of Steps 21 (PR review feedback) and 22 (fixing
    failed PRs)."
  procedure: "proc-complete-task, proc-handle-failed-pr"
context: fork
agent: ai-maestro-programmer-agent-main-agent
user-invocable: false
---

# AMPA GitHub Operations

## Overview

Standardized Git and GitHub operations for AMPA via the gh CLI. Covers the full
lifecycle from cloning/forking repositories through branching, committing, PR
creation, and responding to review feedback. Used in workflow Steps 14, 17, 19,
and AMPA's response portions of Steps 21 and 22.

## Prerequisites

- **gh CLI authenticated**: Verify with `gh auth status`. If not authenticated,
  run `gh auth login`.
- **Git configured**: User name and email set via `git config`.
- **Repository access**: Project cloned or forked with read/write permissions to
  the target repository.

## Instructions

Copy this checklist and track your progress:

1. **Clone or fork** the repository — see Resources table.
2. **Create a feature branch** from latest main — see Resources table.
3. **Implement changes** and commit with conventional format — see Resources table.
4. **Push the branch** to remote: `git push -u origin <branch-name>`.
5. **Create a pull request** with gh CLI — see Resources table.
6. **Respond to review feedback** — see Resources table.
7. **Handle failed PRs** — see Resources table.
8. **Notify AMOA** of PR creation or update status via
   ampa-orchestrator-communication skill.

## Output

- **Committed code on feature branch**: One or more commits with conventional
  messages, pushed to remote.
- **Pull request created**: An open PR on GitHub with descriptive title, body
  linking to the issue, and reviewers assigned.

## Error Handling

On failure: retry once. If still failing, report to AMOA and wait. Never
force-push without AMOA approval.

## Examples

- [ ] Input: Implement task #42 on feature branch
- [x] Output:
      `gh pr create --title "feat(auth): add JWT validation (#42)" --body "Closes #42"`

## Resources

| Document | Description |
|----------|-------------|
| [op-clone-repository.md](references/op-clone-repository.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-create-feature-branch.md](references/op-create-feature-branch.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-commit-changes.md](references/op-commit-changes.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-create-pull-request.md](references/op-create-pull-request.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-respond-to-review.md](references/op-respond-to-review.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |
| [op-update-pr-with-fixes.md](references/op-update-pr-with-fixes.md) | When to Use, Prerequisites, Procedure, Examples, Error Handling |

## Related

- **ampa-task-execution** -- Implementing code and tests before creating a PR.
- **ampa-orchestrator-communication** -- Messaging AMOA about PR status.
