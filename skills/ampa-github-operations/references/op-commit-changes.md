---
name: op-commit-changes
description: Commit changes with meaningful commit messages
parent-skill: ampa-github-operations
---

# Commit Changes

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

Create well-structured commits with meaningful messages following conventional commits specification.

> **Multi-repo rule**: All git commands must use `git -C "$REPO_PATH"` where `REPO_PATH=$AGENT_DIR/repos/<repo-name>`. Never rely on the current working directory.

## When to Use

- Saving incremental progress on a task
- Completing a logical unit of work
- After passing tests
- Before switching branches
- Before pulling changes

## Prerequisites

- Changes exist in working directory
- On the correct feature branch
- Tests pass (if applicable)
- No merge conflicts

## Procedure

### 3.1 Staging Changes Selectively

Review what changed before staging (always use `git -C "$REPO_PATH"`):

```bash
# See all changes
git -C "$REPO_PATH" status

# See detailed diff
git -C "$REPO_PATH" diff

# See diff for specific file
git -C "$REPO_PATH" diff <file>
```

Stage changes:

```bash
# Stage specific file
git -C "$REPO_PATH" add <file>

# Stage multiple specific files
git -C "$REPO_PATH" add <file1> <file2> <file3>

# Stage all changes in a directory
git -C "$REPO_PATH" add <directory>/

# Stage all changes (use with caution)
git -C "$REPO_PATH" add -A

# Stage interactively (review each change)
git -C "$REPO_PATH" add -p
```

**Best Practice:** Stage specific files rather than using `git add -A` to avoid accidentally including sensitive files or unrelated changes.

### 3.2 Commit Message Format

Commit messages have three parts:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Components:**

- **Subject line** (required): Max 72 characters, imperative mood, no period
- **Body** (optional): Explain what and why, wrap at 72 characters
- **Footer** (optional): Reference issues, breaking changes

**Example:**
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with support for Google and GitHub
providers. This replaces the legacy session-based auth system.

- Add OAuth2Strategy class
- Configure passport.js middleware
- Add callback routes for each provider

Closes #123
BREAKING CHANGE: Sessions from v1.x will be invalidated
```

### 3.3 Conventional Commits Syntax

**Types:**

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructure, no feature change |
| `test` | Add or fix tests |
| `chore` | Maintenance, dependencies |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |
| `build` | Build system changes |
| `revert` | Revert previous commit |

**Scope:** Optional, describes the affected component

Examples:
- `feat(api): add user endpoints`
- `fix(ui): correct button alignment`
- `docs(readme): update installation steps`
- `refactor(core): extract validation logic`
- `test(auth): add login unit tests`

**Creating the commit:**

```bash
# Simple commit
git -C "$REPO_PATH" commit -m "feat(auth): add login endpoint"

# Multi-line commit using heredoc
git -C "$REPO_PATH" commit -m "$(cat <<'EOF'
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with support for Google and GitHub
providers.

Closes #123
EOF
)"
```

### 3.4 Amending Commits (When Safe)

**Only amend when:**
- The commit has NOT been pushed
- No one else has based work on the commit

```bash
# Add more changes to last commit
git -C "$REPO_PATH" add <file>
git -C "$REPO_PATH" commit --amend --no-edit

# Change the commit message
git -C "$REPO_PATH" commit --amend -m "new message"

# Amend both changes and message
git -C "$REPO_PATH" add <file>
git -C "$REPO_PATH" commit --amend -m "updated message"
```

**Never amend after pushing** unless you are certain no one else has pulled your changes.

### 3.5 Verifying Commit Success

After committing:

```bash
# See the commit you just made
git -C "$REPO_PATH" log -1

# See commit with diff
git -C "$REPO_PATH" log -1 -p

# Verify working tree is clean
git -C "$REPO_PATH" status

# See commit in one line
git -C "$REPO_PATH" log --oneline -1
```

## Checklist

- [ ] Review changes with `git -C "$REPO_PATH" status` and `git -C "$REPO_PATH" diff`
- [ ] Stage only relevant files
- [ ] Write commit message following conventional format
- [ ] Include issue reference in footer if applicable
- [ ] Verify commit with `git -C "$REPO_PATH" log -1`
- [ ] Ensure working tree is clean after commit

## Examples

### Example 1: Simple Feature Commit

```bash
git -C "$REPO_PATH" status
# Changes not staged for commit:
#   modified:   src/auth.js
#   modified:   src/routes.js

git -C "$REPO_PATH" add src/auth.js src/routes.js
git -C "$REPO_PATH" commit -m "feat(auth): add password reset functionality"

git -C "$REPO_PATH" log -1 --oneline
# a1b2c3d feat(auth): add password reset functionality
```

### Example 2: Bug Fix with Issue Reference

```bash
git -C "$REPO_PATH" add src/utils/validation.js
git -C "$REPO_PATH" commit -m "$(cat <<'EOF'
fix(validation): handle empty string input

Previously, empty strings passed validation incorrectly. Now they are
properly rejected with an appropriate error message.

Fixes #456
EOF
)"
```

### Example 3: Multiple Files with Detailed Message

```bash
git -C "$REPO_PATH" add src/components/Button.jsx src/styles/button.css tests/Button.test.js

git -C "$REPO_PATH" commit -m "$(cat <<'EOF'
feat(ui): add primary button variant

Add new primary button style with hover and active states.
Includes accessibility improvements for keyboard navigation.

- Add Button component with variant prop
- Add corresponding CSS styles
- Add unit tests for all variants

Closes #789
EOF
)"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `nothing to commit` | No staged changes | Stage files first with `git add` |
| `empty commit message` | Forgot message | Message is required |
| `error: pathspec not found` | File path wrong | Check file path spelling |
| `Please tell me who you are` | Git not configured | Set user.name and user.email |
| `Changes not staged` | Forgot to stage | Run `git add` first |

## Recovery Steps

If you committed with wrong message:

```bash
# Amend if not pushed
git -C "$REPO_PATH" commit --amend -m "correct message"
```

If you committed wrong files:

```bash
# If not pushed, reset the commit but keep changes
git -C "$REPO_PATH" reset --soft HEAD~1

# Re-stage correct files and commit again
git -C "$REPO_PATH" add <correct-files>
git -C "$REPO_PATH" commit -m "message"
```

If you need to undo the last commit entirely:

```bash
# Keep changes in working directory
git -C "$REPO_PATH" reset --soft HEAD~1

# Discard changes entirely (DANGEROUS)
git -C "$REPO_PATH" reset --hard HEAD~1
```
