---
name: ampa-github-operations
description: Git and GitHub operations for AMPA. Use when cloning repos, branching, committing, opening PRs, or handling review feedback. Trigger with /ampa-github-operations.
license: MIT
compatibility: Requires gh CLI authenticated.
metadata:
  author: AI Maestro
  version: 1.0.20
  workflow-instruction: "Steps 14 (clone/fork), 17 (branch/commit), 19 (PR creation). Also handles AMPA response portions of Steps 21 (PR review feedback) and 22 (fixing failed PRs)."
  procedure: "proc-complete-task, proc-handle-failed-pr"
context: fork
agent: ai-maestro-programmer-agent-main-agent
user-invocable: false
---

# AMPA GitHub Operations

## Overview

Standardized Git and GitHub operations for AMPA via the gh CLI. Covers the full lifecycle from cloning/forking repositories through branching, committing, PR creation, and responding to review feedback. Used in workflow Steps 14, 17, 19, and AMPA's response portions of Steps 21 and 22.

## Prerequisites

- **gh CLI authenticated**: Verify with `gh auth status`. If not authenticated, run `gh auth login`.
- **Git configured**: User name and email set via `git config`.
- **Repository access**: Project cloned or forked with read/write permissions to the target repository.

## Instructions

Copy this checklist and track your progress:

1. **Clone or fork** the target repository using `gh repo clone <owner>/<repo>` or `gh repo fork <owner>/<repo> --clone`. See [op-clone-repository.md](references/op-clone-repository.md).
2. **Create a feature branch** from the latest main: `git checkout -b <type>/<issue-number>-<short-description> main`. See [op-create-feature-branch.md](references/op-create-feature-branch.md).
3. **Implement changes** and commit incrementally using conventional commit format: `git commit -m "feat(scope): description"`. See [op-commit-changes.md](references/op-commit-changes.md).
4. **Push the branch** to the remote: `git push -u origin <branch-name>`.
5. **Create a pull request** using `gh pr create --title "..." --body "..."` with a description linking to the relevant issue. See [op-create-pull-request.md](references/op-create-pull-request.md).
6. **Respond to review feedback**: Read comments with `gh pr view <number> --comments`, address each comment, commit fixes, and push. See [op-respond-to-review.md](references/op-respond-to-review.md).
7. **Handle failed PRs**: After pushing fixes, update the PR description if needed and request re-review. See [op-update-pr-with-fixes.md](references/op-update-pr-with-fixes.md).
8. **Notify AMOA** of PR creation or update status via ampa-orchestrator-communication skill.

## Output

- **Committed code on feature branch**: One or more commits with conventional messages, pushed to remote.
- **Pull request created**: An open PR on GitHub with descriptive title, body linking to the issue, and reviewers assigned.

## Error Handling

On failure: retry once. If still failing, report to AMOA and wait. Never force-push without AMOA approval.

## Examples

- [ ] Input: Implement task #42 on feature branch
- [x] Output: `gh pr create --title "feat(auth): add JWT validation (#42)" --body "Closes #42"`

## Resources

- **[op-clone-repository.md](references/op-clone-repository.md)** -- Cloning and forking
- **[op-create-feature-branch.md](references/op-create-feature-branch.md)** -- Branch creation
- **[op-commit-changes.md](references/op-commit-changes.md)** -- Staging and committing
- **[op-create-pull-request.md](references/op-create-pull-request.md)** -- PR creation
- **[op-respond-to-review.md](references/op-respond-to-review.md)** -- Handling review feedback
- **[op-update-pr-with-fixes.md](references/op-update-pr-with-fixes.md)** -- Pushing fixes after rejection

## Related

- **ampa-task-execution** -- Implementing code and tests before creating a PR.
- **ampa-orchestrator-communication** -- Messaging AMOA about PR status.
