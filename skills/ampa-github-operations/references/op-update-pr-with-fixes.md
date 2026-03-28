---
name: op-update-pr-with-fixes
description: Push fixes to PR after rejection
parent-skill: ampa-github-operations
---

# Update PR with Fixes

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

Push code fixes to an existing PR after rejection from AMIA review. This corresponds to **Step 22** of the AMPA workflow.

> **Multi-repo rule**: All gh commands must use `--repo "$OWNER_REPO"`. All git commands must use `git -C "$REPO_PATH"`.

## When to Use

- After receiving PR review feedback
- After addressing review comments
- When fixes are ready to push
- Before requesting re-review

## Prerequisites

- PR exists with review feedback
- Review comments understood
- Fixes implemented locally
- On the correct PR branch

## Procedure

### 6.1 Making Requested Changes

Ensure you are on the correct branch (always use `--repo` and `git -C`):

```bash
# List PRs and find the branch
gh pr list --repo "$OWNER_REPO" --author "@me"
gh pr view <pr-number> --repo "$OWNER_REPO"

# Check out the PR branch
git -C "$REPO_PATH" checkout <branch-name>

# Or checkout PR directly (from within the repo)
gh pr checkout <pr-number> --repo "$OWNER_REPO"
```

Update branch with latest main (to avoid conflicts):

```bash
git -C "$REPO_PATH" fetch origin main
git -C "$REPO_PATH" merge origin/main
# Resolve conflicts if any
```

Make the requested changes in your editor.

### 6.2 Committing Fixes

Commit each logical fix separately for clear history (always use `git -C "$REPO_PATH"`):

```bash
# Stage specific files for this fix
git -C "$REPO_PATH" add <files>

# Commit with message referencing the review
git -C "$REPO_PATH" commit -m "fix(scope): address review comment about X"
```

**Commit message patterns for fixes:**

```bash
# For a specific review comment
git -C "$REPO_PATH" commit -m "fix(auth): add null check per review feedback"

# For multiple related fixes
git -C "$REPO_PATH" commit -m "fix(api): address security concerns from review

- Add input validation
- Sanitize user input
- Add rate limiting"

# For test additions
git -C "$REPO_PATH" commit -m "test(auth): add unit tests per review request"
```

**Do not squash commits** when pushing fixes. Keep separate commits so reviewer can see what changed since last review.

### 6.3 Pushing Updates to PR Branch

Push changes to update the PR (always use `git -C "$REPO_PATH"`):

```bash
# Push to the same branch (PR updates automatically)
git -C "$REPO_PATH" push origin <branch-name>
```

The PR will automatically update with new commits.

If you rebased and need to force push:

```bash
# Only if you rebased (avoid if possible)
git -C "$REPO_PATH" push --force-with-lease origin <branch-name>
```

**Note:** Prefer merge over rebase to preserve review context. Force pushing can lose review comments.

### 6.4 Updating PR Description

If changes affect the PR scope, update the description (always include `--repo`):

```bash
gh pr edit <pr-number> --repo "$OWNER_REPO" --body "$(cat <<'EOF'
## Summary
<updated summary>

## Changes
- Original change 1
- Original change 2
- **NEW:** Change added per review

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [x] **NEW:** Added tests for edge cases per review

## Review Response
Addressed all review comments:
- Added null check (commit abc123)
- Added unit tests (commit def456)
- Fixed security issue (commit ghi789)

## Related Issues
Closes #123
EOF
)"
```

### 6.5 Notifying Reviewer of Updates

After pushing all fixes, notify the reviewer:

```bash
# Add comment summarizing what was fixed
gh pr comment <pr-number> --repo "$OWNER_REPO" --body "$(cat <<'EOF'
## Updates Pushed

All review comments have been addressed:

| Comment | Resolution | Commit |
|---------|------------|--------|
| Add null check | Fixed | abc123 |
| Add unit tests | Added 5 tests | def456 |
| Security concern | Sanitized input | ghi789 |

Ready for re-review. Thank you for the feedback!
EOF
)"

# Request re-review
gh pr edit <pr-number> --repo "$OWNER_REPO" --add-reviewer "<reviewer-username>"
```

## Checklist

- [ ] Check out the correct PR branch
- [ ] Sync with main branch
- [ ] Make all requested changes
- [ ] Commit fixes with clear messages
- [ ] Push changes to PR branch
- [ ] Update PR description if needed
- [ ] Add comment summarizing changes
- [ ] Request re-review from original reviewer

## Examples

### Example 1: Single Fix Push

```bash
# Checkout PR branch
git -C "$REPO_PATH" checkout feature/123-auth

# Make fix
# ... edit files ...

# Commit and push
git -C "$REPO_PATH" add src/auth.js
git -C "$REPO_PATH" commit -m "fix(auth): add null check per review"
git -C "$REPO_PATH" push origin feature/123-auth

# Notify
gh pr comment 123 --repo "$OWNER_REPO" --body "Added null check as requested. Ready for re-review."
gh pr edit 123 --repo "$OWNER_REPO" --add-reviewer "amia-reviewer"
```

### Example 2: Multiple Fixes

```bash
git -C "$REPO_PATH" checkout feature/456-api-security

# Fix 1
git -C "$REPO_PATH" add src/validation.js
git -C "$REPO_PATH" commit -m "fix(validation): add input sanitization"

# Fix 2
git -C "$REPO_PATH" add tests/validation.test.js
git -C "$REPO_PATH" commit -m "test(validation): add edge case tests"

# Fix 3
git -C "$REPO_PATH" add src/api.js
git -C "$REPO_PATH" commit -m "fix(api): add rate limiting"

# Push all
git -C "$REPO_PATH" push origin feature/456-api-security

# Summary comment
gh pr comment 456 --repo "$OWNER_REPO" --body "$(cat <<'EOF'
Pushed 3 commits addressing review:
1. Input sanitization (abc123)
2. Edge case tests (def456)
3. Rate limiting (ghi789)

Ready for re-review!
EOF
)"
```

### Example 3: Fix After Rebase

```bash
git -C "$REPO_PATH" checkout feature/789-refactor

# Rebase on main
git -C "$REPO_PATH" fetch origin main
git -C "$REPO_PATH" rebase origin/main

# Make fixes
git -C "$REPO_PATH" add .
git -C "$REPO_PATH" commit -m "fix(core): address all review comments"

# Force push (with lease for safety)
git -C "$REPO_PATH" push --force-with-lease origin feature/789-refactor

# Explain in comment
gh pr comment 789 --repo "$OWNER_REPO" --body "$(cat <<'EOF'
Rebased on main and addressed all review comments.

Note: Force pushed due to rebase. All review comments should still be visible.

Changes:
- Fixed all issues mentioned
- Resolved conflicts with main

Ready for re-review!
EOF
)"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `rejected: non-fast-forward` | Remote has new commits | `git pull origin <branch>` then push |
| `failed to push` | Branch protection | Check if PR is from fork (needs sync) |
| `merge conflict` | Diverged from main | Resolve conflicts locally |
| `PR is closed` | PR was closed | Reopen PR or create new one |
| `force-with-lease rejected` | Someone else pushed | Pull their changes first |

## Recovery Steps

If you pushed broken code:

```bash
# Revert immediately
git -C "$REPO_PATH" revert HEAD
git -C "$REPO_PATH" push origin <branch>

# Comment on PR
gh pr comment <pr-number> --repo "$OWNER_REPO" --body "Reverted broken commit. Investigating issue."
```

If push failed due to conflicts:

```bash
# Pull and merge
git -C "$REPO_PATH" pull origin <branch>

# Or fetch and merge main
git -C "$REPO_PATH" fetch origin main
git -C "$REPO_PATH" merge origin/main

# Resolve conflicts
# ... edit conflicted files ...
git -C "$REPO_PATH" add <resolved-files>
git -C "$REPO_PATH" commit -m "resolve merge conflicts"
git -C "$REPO_PATH" push origin <branch>
```

If you need to completely redo fixes:

```bash
# Reset to state before your fixes
git -C "$REPO_PATH" log --oneline
git -C "$REPO_PATH" reset --hard <commit-before-fixes>

# Make fixes correctly
# ... edit files ...
git -C "$REPO_PATH" add .
git -C "$REPO_PATH" commit -m "fix: corrected implementation"
git -C "$REPO_PATH" push --force-with-lease origin <branch>

# Explain in comment
gh pr comment <pr-number> --repo "$OWNER_REPO" --body "Reset and redid fixes. Previous approach was incorrect."
```
