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

## Multi-Repo Rule

**All git/gh commands MUST specify the target repo.** Use `git -C "$REPO_PATH"` for git commands and `--repo "$OWNER/$REPO"` for gh commands. Set `REPO_PATH=$AGENT_DIR/repos/<repo-name>` before any operation. See the multi-repo rules in the main agent definition.

## Instructions

Copy this checklist and track your progress:

1. **Identify target repo** -- Run `amp-project-repos.sh` to list repos. Set `REPO_PATH=$AGENT_DIR/repos/<repo-name>` and `OWNER_REPO=<owner>/<repo>`.
2. **Clone or fork** the target repository using `amp-clone-repo.sh <repo-url>` (preferred) or `gh repo clone <owner>/<repo> "$REPO_PATH"`. See [op-clone-repository.md](references/op-clone-repository.md).
3. **Create a feature branch** from the latest main: `git -C "$REPO_PATH" checkout -b <type>/<issue-number>-<short-description> main`. See [op-create-feature-branch.md](references/op-create-feature-branch.md).
4. **Implement changes** and commit incrementally using conventional commit format: `git -C "$REPO_PATH" commit -m "feat(scope): description"`. See [op-commit-changes.md](references/op-commit-changes.md).
5. **Push the branch** to the remote: `git -C "$REPO_PATH" push -u origin <branch-name>`.
6. **Create a pull request** using `amp-submit-pr.sh "$REPO_PATH" "<title>"` (preferred) or `gh pr create --repo "$OWNER_REPO" --title "..." --body "..."` with a description linking to the relevant issue. See [op-create-pull-request.md](references/op-create-pull-request.md).
7. **Respond to review feedback**: Read comments with `gh pr view <number> --repo "$OWNER_REPO" --comments`, address each comment, commit fixes, and push. See [op-respond-to-review.md](references/op-respond-to-review.md).
8. **Handle failed PRs**: After pushing fixes, update the PR description if needed and request re-review. See [op-update-pr-with-fixes.md](references/op-update-pr-with-fixes.md).
9. **Notify AMOA** of PR creation or update status via ampa-orchestrator-communication skill.

## Output

- **Committed code on feature branch**: One or more commits with conventional messages, pushed to remote.
- **Pull request created**: An open PR on GitHub with descriptive title, body linking to the issue, and reviewers assigned.

## Token Budget

- **Lazy loading**: Only read a reference file when executing that operation. Do not pre-read all.
- **PR descriptions**: Inline (required by GitHub), but build/test logs to file.
- **Reports**: 3 lines max to AMOA. Diffs >50 lines go to file.

## Error Handling

On failure: retry once. If still failing, report to AMOA and wait. Never force-push without AMOA approval.

## Examples

- [ ] Input: Implement task #42 on feature branch
- [x] Output: `gh pr create --repo "$OWNER_REPO" --title "feat(auth): add JWT validation (#42)" --body "Closes #42"`

## Resources

- **[op-clone-repository.md](references/op-clone-repository.md)** -- Cloning and forking procedures
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-create-feature-branch.md](references/op-create-feature-branch.md)** -- Branch creation and naming
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-commit-changes.md](references/op-commit-changes.md)** -- Staging and committing changes
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-create-pull-request.md](references/op-create-pull-request.md)** -- PR creation procedures
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-respond-to-review.md](references/op-respond-to-review.md)** -- Handling review feedback
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling
- **[op-update-pr-with-fixes.md](references/op-update-pr-with-fixes.md)** -- Pushing fixes after rejection
  Sections: When to Use · Prerequisites · Procedure · Examples · Error Handling

## Related Skills

- **ampa-task-execution** -- For implementing code changes, writing tests, and validating acceptance criteria before creating a PR.
- **ampa-orchestrator-communication** -- For messaging AMOA and AMIA about PR status and task progress.
