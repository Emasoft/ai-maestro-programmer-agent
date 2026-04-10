---
name: op-create-feature-branch
description: Create a feature branch for task implementation
parent-skill: ampa-github-operations
---

# Create Feature Branch

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

Create a properly named feature branch for implementing a task.

## When to Use

- Starting work on a new task or issue
- Beginning implementation of a feature
- Fixing a bug
- Refactoring code

## Prerequisites

- Repository cloned locally
- On a clean working tree (no uncommitted changes)
- Main branch up to date with remote

## Procedure

### 2.1 Branch Naming Conventions

Use this format for branch names:

```text
<type>/<issue-number>-<short-description>
```

**Types:**

- `feature/` - New functionality
- `fix/` - Bug fixes
- `refactor/` - Code restructuring
- `docs/` - Documentation only
- `test/` - Test additions or fixes
- `chore/` - Maintenance tasks

**Rules:**

- Use lowercase letters only
- Use hyphens to separate words
- Keep description under 50 characters
- Include issue number if applicable

**Examples:**

```text
feature/123-user-authentication
fix/456-memory-leak-on-close
refactor/789-extract-validation-utils
docs/101-api-documentation
test/202-add-integration-tests
chore/303-update-dependencies
```

### 2.2 Creating Branch from Main

Always create feature branches from an up-to-date main:

```bash
# Ensure you are on main
git checkout main

# Pull latest changes
git pull origin main

# Create and switch to new branch
git checkout -b <branch-name>
```

Example:

```bash
git checkout main
git pull origin main
git checkout -b feature/123-add-user-auth
```

Alternative using git switch (Git 2.23+):

```bash
git switch main
git pull origin main
git switch -c feature/123-add-user-auth
```

### 2.3 Switching to Existing Branches

If a branch already exists:

```bash
# List all branches
git branch -a

# Switch to existing local branch
git checkout <branch-name>

# Switch to remote branch (creates local tracking branch)
git checkout -b <branch-name> origin/<branch-name>
```

### 2.4 Pushing New Branch to Remote

After creating and committing on the branch:

```bash
# Push and set upstream tracking
git push -u origin <branch-name>
```

Example:

```bash
git push -u origin feature/123-add-user-auth
```

The `-u` flag sets up tracking so future `git push` and `git pull` work without
specifying the remote.

## Checklist

- [ ] Verify working tree is clean: `git status`
- [ ] Switch to main branch: `git checkout main`
- [ ] Pull latest changes: `git pull origin main`
- [ ] Create branch with proper naming convention
- [ ] Verify you are on the new branch: `git branch`
- [ ] Push branch to remote with tracking: `git push -u origin <branch>`

## Examples

### Example 1: Create Feature Branch

```bash
git status
# On branch main
# nothing to commit, working tree clean

git pull origin main
# Already up to date.

git checkout -b feature/456-add-payment-gateway
# Switched to a new branch 'feature/456-add-payment-gateway'

git branch
# * feature/456-add-payment-gateway
#   main
```

### Example 2: Create Branch and Push Immediately

```bash
git checkout main
git pull origin main
git checkout -b fix/789-null-pointer-exception
# Make initial changes
git add .
git commit -m "fix(core): add null check for user object"
git push -u origin fix/789-null-pointer-exception
```

### Example 3: Create Branch for Forked Repository

```bash
# Sync with upstream first
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Now create feature branch
git checkout -b feature/101-contribute-feature
```

## Error Handling

| Error                                      | Cause                   | Solution                                                        |
| ------------------------------------------ | ----------------------- | --------------------------------------------------------------- |
| `branch already exists`                    | Branch name collision   | Delete old branch: `git branch -d <name>` or use different name |
| `uncommitted changes`                      | Dirty working tree      | Commit or stash changes first                                   |
| `not a git repository`                     | Wrong directory         | `cd` to repository root                                         |
| `cannot update paths and switch to branch` | Branch exists on remote | Use `git checkout -b <name> origin/<name>`                      |
| `Your branch is behind`                    | Local main outdated     | `git pull origin main`                                          |

## Recovery Steps

If you created a branch with wrong name:

```bash
# If no commits yet, just delete and recreate
git checkout main
git branch -d <wrong-name>
git checkout -b <correct-name>

# If commits exist, rename the branch
git branch -m <old-name> <new-name>

# If already pushed, delete remote and push renamed
git push origin --delete <old-name>
git push -u origin <new-name>
```

If you created branch from wrong base:

```bash
# Rebase onto correct base
git checkout <your-branch>
git rebase main
```
