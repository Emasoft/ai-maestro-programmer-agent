---
name: op-commit-changes
description: Commit changes with meaningful commit messages
parent-skill: ampa-github-operations
operation-type: commit
---

# Commit Changes

Create well-structured commits with meaningful messages following conventional commits specification.

## Table of Contents

- 3.1 Staging changes selectively
- 3.2 Commit message format
- 3.3 Conventional commits syntax
- 3.4 Amending commits (when safe)
- 3.5 Verifying commit success

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

Review what changed before staging:

```bash
# See all changes
git status

# See detailed diff
git diff

# See diff for specific file
git diff <file>
```

Stage changes:

```bash
# Stage specific file
git add <file>

# Stage multiple specific files
git add <file1> <file2> <file3>

# Stage all changes in a directory
git add <directory>/

# Stage all changes (use with caution)
git add -A

# Stage interactively (review each change)
git add -p
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
git commit -m "feat(auth): add login endpoint"

# Multi-line commit using heredoc
git commit -m "$(cat <<'EOF'
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
git add <file>
git commit --amend --no-edit

# Change the commit message
git commit --amend -m "new message"

# Amend both changes and message
git add <file>
git commit --amend -m "updated message"
```

**Never amend after pushing** unless you are certain no one else has pulled your changes.

### 3.5 Verifying Commit Success

After committing:

```bash
# See the commit you just made
git log -1

# See commit with diff
git log -1 -p

# Verify working tree is clean
git status

# See commit in one line
git log --oneline -1
```

## Checklist

- [ ] Review changes with `git status` and `git diff`
- [ ] Stage only relevant files
- [ ] Write commit message following conventional format
- [ ] Include issue reference in footer if applicable
- [ ] Verify commit with `git log -1`
- [ ] Ensure working tree is clean after commit

## Examples

### Example 1: Simple Feature Commit

```bash
git status
# Changes not staged for commit:
#   modified:   src/auth.js
#   modified:   src/routes.js

git add src/auth.js src/routes.js
git commit -m "feat(auth): add password reset functionality"

git log -1 --oneline
# a1b2c3d feat(auth): add password reset functionality
```

### Example 2: Bug Fix with Issue Reference

```bash
git add src/utils/validation.js
git commit -m "$(cat <<'EOF'
fix(validation): handle empty string input

Previously, empty strings passed validation incorrectly. Now they are
properly rejected with an appropriate error message.

Fixes #456
EOF
)"
```

### Example 3: Multiple Files with Detailed Message

```bash
git add src/components/Button.jsx src/styles/button.css tests/Button.test.js

git commit -m "$(cat <<'EOF'
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
git commit --amend -m "correct message"
```

If you committed wrong files:

```bash
# If not pushed, reset the commit but keep changes
git reset --soft HEAD~1

# Re-stage correct files and commit again
git add <correct-files>
git commit -m "message"
```

If you need to undo the last commit entirely:

```bash
# Keep changes in working directory
git reset --soft HEAD~1

# Discard changes entirely (DANGEROUS)
git reset --hard HEAD~1
```
