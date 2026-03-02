---
name: ampa-github-operations
description: Git and GitHub operations for AMPA. Use when cloning repos, branching, committing, opening PRs, or handling review feedback. Trigger with /ampa-github-operations.
license: MIT
compatibility: Requires gh CLI authenticated.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ampa-programmer-main-agent
user-invocable: false
workflow-instruction: "Steps 19, 21, 22"
procedure: "proc-complete-task, proc-handle-failed-pr"
---

# AMPA GitHub Operations

## Overview

This skill provides the AI Maestro Programmer Agent (AMPA) with standardized procedures for all Git and GitHub operations. It covers the full lifecycle from cloning a repository, creating feature branches, committing code changes with conventional commit messages, opening pull requests via the gh CLI, and responding to EIA code review feedback. All operations use the gh CLI tool and follow the AI Maestro ecosystem conventions for branch naming, commit formatting, and PR descriptions. This skill is used during workflow Steps 19 (create PR), 21 (respond to review), and 22 (push fixes after rejection).

This skill provides procedures for Git and GitHub operations within the AI Maestro Programmer Agent workflow. Use these operations for repository management, branching, commits, and pull request lifecycle.

## When to Use This Skill

- **Cloning/forking**: When starting work on a new project or task
- **Branching**: When beginning implementation of a task
- **Committing**: When saving incremental progress or completing work
- **Pull Requests**: When submitting completed work for review (Step 19)
- **Review Response**: When addressing EIA review comments (Step 21)
- **PR Updates**: When pushing fixes after PR rejection (Step 22)

## Prerequisites

1. **gh CLI installed and authenticated**: Run `gh auth status` to verify
2. **Git configured**: User name and email set
3. **Repository access**: Read/write permissions to target repository

## Instructions

1. Verify that the gh CLI is installed and authenticated by running `gh auth status`. If not authenticated, run `gh auth login` and follow the prompts.
2. Clone or fork the target repository using `gh repo clone <owner>/<repo>` or `gh repo fork <owner>/<repo> --clone`. See [op-clone-repository.md](references/op-clone-repository.md) for details.
3. Create a feature branch from the latest main branch using the naming convention `<type>/<issue-number>-<short-description>`. Example: `git checkout -b feature/123-add-user-auth main`. See [op-create-feature-branch.md](references/op-create-feature-branch.md).
4. Make code changes and commit incrementally using conventional commit format: `git commit -m "feat(scope): description"`. See [op-commit-changes.md](references/op-commit-changes.md).
5. Push the feature branch to the remote: `git push -u origin <branch-name>`.
6. Create a pull request using `gh pr create --title "<type>(scope): description" --body "..."` with a clear description linking to the relevant issue. See [op-create-pull-request.md](references/op-create-pull-request.md).
7. If the PR receives review feedback from EIA, read the comments with `gh pr view <number> --comments`, address each comment, commit fixes, and push updates. See [op-respond-to-review.md](references/op-respond-to-review.md).
8. After pushing fixes, update the PR description if needed and request re-review with `gh pr edit <number> --add-reviewer <reviewer>`. See [op-update-pr-with-fixes.md](references/op-update-pr-with-fixes.md).

## Operations Reference

### Repository Setup

| Operation | File | When to Use |
|-----------|------|-------------|
| Clone Repository | [op-clone-repository.md](references/op-clone-repository.md) | Initial project setup, forking upstream repos |
| Create Feature Branch | [op-create-feature-branch.md](references/op-create-feature-branch.md) | Starting work on a new task |

**Table of Contents - op-clone-repository.md:**
- 1.1 When to clone vs fork
- 1.2 Cloning with gh CLI
- 1.3 Forking upstream repositories
- 1.4 Setting up remotes for forks
- 1.5 Verifying clone success

**Table of Contents - op-create-feature-branch.md:**
- 2.1 Branch naming conventions
- 2.2 Creating branch from main
- 2.3 Switching to existing branches
- 2.4 Pushing new branch to remote

### Commit Operations

| Operation | File | When to Use |
|-----------|------|-------------|
| Commit Changes | [op-commit-changes.md](references/op-commit-changes.md) | Saving progress with meaningful messages |

**Table of Contents - op-commit-changes.md:**
- 3.1 Staging changes selectively
- 3.2 Commit message format
- 3.3 Conventional commits syntax
- 3.4 Amending commits (when safe)
- 3.5 Verifying commit success

### Pull Request Lifecycle

| Operation | File | When to Use |
|-----------|------|-------------|
| Create Pull Request | [op-create-pull-request.md](references/op-create-pull-request.md) | Submitting completed task for review (Step 19) |
| Respond to Review | [op-respond-to-review.md](references/op-respond-to-review.md) | Addressing EIA review comments (Step 21) |
| Update PR with Fixes | [op-update-pr-with-fixes.md](references/op-update-pr-with-fixes.md) | Pushing fixes after rejection (Step 22) |

**Table of Contents - op-create-pull-request.md:**
- 4.1 Preparing branch for PR
- 4.2 Writing PR title and description
- 4.3 Creating PR with gh CLI
- 4.4 Setting reviewers and labels
- 4.5 Linking to issues

**Table of Contents - op-respond-to-review.md:**
- 5.1 Reading review comments
- 5.2 Understanding rejection reasons
- 5.3 Addressing specific feedback
- 5.4 Replying to review comments
- 5.5 Requesting re-review

**Table of Contents - op-update-pr-with-fixes.md:**
- 6.1 Making requested changes
- 6.2 Committing fixes
- 6.3 Pushing updates to PR branch
- 6.4 Updating PR description
- 6.5 Notifying reviewer of updates

## Quick Reference

### Branch Naming Convention

```
<type>/<issue-number>-<short-description>
```

Examples:
- `feature/123-add-user-auth`
- `fix/456-resolve-memory-leak`
- `refactor/789-extract-utils`

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### PR Title Format

```
<type>(<scope>): <short description>
```

Example: `feat(auth): add OAuth2 login support`

## Output

When this skill is applied correctly, the following artifacts are produced:

- **Cloned repository**: A local working copy of the target repository with remotes configured for upstream and origin.
- **Feature branch**: A properly named branch following the `<type>/<issue-number>-<short-description>` convention, pushed to the remote.
- **Commit history**: One or more commits with conventional commit messages that clearly describe each change.
- **Pull request**: An open PR on GitHub with a descriptive title, body linking to the relevant issue, and appropriate reviewers assigned.
- **Review responses**: If review feedback is received, updated commits addressing each comment, with reply comments acknowledging the feedback.
- **AI Maestro notification**: A message sent to EOA (Orchestrator) confirming PR creation or update status.

## Examples

### Example 1: Creating a Feature Branch and PR for a New Feature

```bash
# Clone the repository
gh repo clone Emasoft/svgbbox

# Create feature branch
git checkout -b feature/42-add-viewbox-parser main

# Make changes, commit with conventional format
git add src/parser.py
git commit -m "feat(parser): add viewBox attribute parsing"

# Push and create PR
git push -u origin feature/42-add-viewbox-parser
gh pr create --title "feat(parser): add viewBox attribute parsing" --body "Closes #42. Adds parsing support for the viewBox SVG attribute."
```

### Example 2: Responding to EIA Review Comments

```bash
# Read the review comments on PR #15
gh pr view 15 --comments

# Address the feedback by fixing the code
git add src/parser.py tests/test_parser.py
git commit -m "fix(parser): handle missing viewBox gracefully per review"

# Push the fix and notify reviewer
git push origin feature/42-add-viewbox-parser
gh pr comment 15 --body "Addressed review feedback: added null check for missing viewBox. Ready for re-review."
```

### Example 3: Handling a Rejected PR

```bash
# Read rejection reason
gh pr view 15 --comments

# Fix the issues identified in the review
git add src/parser.py
git commit -m "fix(parser): validate viewBox dimensions are positive numbers"

# Push fixes and update PR description
git push origin feature/42-add-viewbox-parser
gh pr edit 15 --body "Updated: Added dimension validation per reviewer feedback. Closes #42."
gh pr edit 15 --add-reviewer eia-feature-reviewer
```

## Checklist - Full GitHub Workflow

Copy this checklist and track your progress:

- [ ] Clone or fork repository
- [ ] Create feature branch with proper naming
- [ ] Make changes and commit incrementally
- [ ] Push branch to remote
- [ ] Create pull request with description
- [ ] Address review comments if rejected
- [ ] Push fixes and request re-review

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `gh: command not found` | gh CLI not installed | Install with `brew install gh` |
| `gh auth login` required | Not authenticated | Run `gh auth login` |
| `Permission denied` | No write access | Request access or fork repository |
| `Branch already exists` | Branch name collision | Delete old branch or use different name |
| `Merge conflicts` | Diverged from main | Rebase or merge main into branch |

## Related Skills

- **ampa-orchestrator-communication**: For messaging EIA about PR status
- **ampa-task-execution**: For implementing code changes, writing tests, and validating acceptance criteria before creating a PR

## Resources

- **Related Skills**:
  - **ampa-task-execution** skill -- For implementing code changes, writing tests, and validating acceptance criteria before creating a PR
  - **ampa-orchestrator-communication** skill -- For messaging EOA and EIA about PR status and task progress
- **Reference Documents** (in this skill's references directory):
  - [op-clone-repository.md](references/op-clone-repository.md) - Cloning and forking procedures
  - [op-create-feature-branch.md](references/op-create-feature-branch.md) - Branch creation and naming
  - [op-commit-changes.md](references/op-commit-changes.md) - Staging and committing changes
  - [op-create-pull-request.md](references/op-create-pull-request.md) - PR creation procedures
  - [op-respond-to-review.md](references/op-respond-to-review.md) - Handling review feedback
  - [op-update-pr-with-fixes.md](references/op-update-pr-with-fixes.md) - Pushing fixes after rejection
- **External Documentation**:
  - [GitHub CLI Manual](https://cli.github.com/manual/) - Full gh CLI reference
  - [Conventional Commits](https://www.conventionalcommits.org/) - Commit message specification

## See Also

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Conventional Commits](https://www.conventionalcommits.org/)
