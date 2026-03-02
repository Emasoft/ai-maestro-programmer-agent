---
name: op-respond-to-review
description: Address AMIA review comments on pull request (Step 21)
parent-skill: ampa-github-operations
operation-type: pr-review-response
workflow-step: 21
---

# Respond to Review

Address review comments from AMIA (AI Maestro Integrator Agent) after PR rejection. This corresponds to **Step 21** of the AMPA workflow.

## Table of Contents

- 5.1 Reading review comments
- 5.2 Understanding rejection reasons
- 5.3 Addressing specific feedback
- 5.4 Replying to review comments
- 5.5 Requesting re-review

## When to Use

- PR has been reviewed and changes requested
- AMIA has rejected the PR with specific feedback
- Need to understand what changes are required
- Ready to address review comments

## Prerequisites

- PR exists and has been reviewed
- Review status is "Changes Requested"
- Access to repository
- gh CLI authenticated

## Procedure

### 5.1 Reading Review Comments

View all review comments on a PR:

```bash
# List all reviews on PR
gh pr view <pr-number> --comments

# View detailed PR information
gh pr view <pr-number>

# View review comments via API for more detail
gh api repos/<owner>/<repo>/pulls/<pr-number>/reviews

# View inline comments
gh api repos/<owner>/<repo>/pulls/<pr-number>/comments
```

Using gh pr checks to see status:
```bash
gh pr checks <pr-number>
```

### 5.2 Understanding Rejection Reasons

Common rejection categories from AMIA:

| Category | Description | How to Address |
|----------|-------------|----------------|
| **Code Quality** | Style issues, complexity | Refactor, format code |
| **Missing Tests** | Insufficient test coverage | Add unit/integration tests |
| **Documentation** | Missing or outdated docs | Update README, docstrings |
| **Security** | Vulnerabilities identified | Fix security issues |
| **Performance** | Performance concerns | Optimize code |
| **Architecture** | Design issues | Refactor approach |
| **Functionality** | Does not meet requirements | Revise implementation |

Parse the review to identify:
1. What specific changes are requested
2. Which files need modification
3. Priority of each comment
4. Whether changes are blocking or suggestions

### 5.3 Addressing Specific Feedback

For each comment, determine the action:

**Blocking comments** (must fix):
- Marked as "Request changes"
- Security vulnerabilities
- Breaking functionality
- Missing required tests

**Non-blocking suggestions** (consider):
- Style preferences
- Alternative approaches
- Nice-to-have improvements

Create a list of changes to make:

```markdown
## Review Response Plan

### Must Fix
- [ ] Add null check in processUser() - security concern
- [ ] Add unit tests for edge cases
- [ ] Fix SQL injection vulnerability in query builder

### Will Address
- [ ] Rename variable per suggestion
- [ ] Add inline comments for complex logic

### Decline (with explanation)
- Performance optimization - will address in separate PR
```

### 5.4 Replying to Review Comments

Reply to individual comments:

```bash
# Reply to a specific review comment
gh api repos/<owner>/<repo>/pulls/<pr-number>/comments/<comment-id>/replies \
  -f body="Fixed in commit abc123. Added null check as suggested."
```

Or reply in the GitHub web interface:
1. Go to PR page
2. Find the comment
3. Click "Reply"
4. Explain what you did or ask for clarification

**Good reply examples:**

For implemented changes:
```
Fixed in commit abc123. Added null check as suggested.
```

For needing clarification:
```
Could you clarify what behavior you expect when the input is empty?
Currently it returns null, should it throw an exception instead?
```

For declining with reason:
```
I considered this approach but chose the current implementation because
it handles X edge case better. Happy to discuss further.
```

### 5.5 Requesting Re-review

After making all changes, request re-review:

```bash
# Add reviewer request
gh pr edit <pr-number> --add-reviewer "<reviewer-username>"
```

Add a comment summarizing changes made:

```bash
gh pr comment <pr-number> --body "$(cat <<'EOF'
## Changes Made in Response to Review

I've addressed all the review comments:

- [x] Added null check in processUser() - commit abc123
- [x] Added unit tests for edge cases - commit def456
- [x] Fixed SQL injection vulnerability - commit ghi789
- [x] Renamed variable per suggestion - commit jkl012

Ready for re-review. Thank you for the thorough feedback!
EOF
)"
```

## Checklist

- [ ] Read all review comments
- [ ] Categorize comments (must fix, will address, decline)
- [ ] Create plan for addressing each comment
- [ ] Make required code changes
- [ ] Reply to each comment explaining resolution
- [ ] Push all changes to PR branch
- [ ] Request re-review from original reviewer
- [ ] Add summary comment listing all changes made

## Examples

### Example 1: Addressing Security Review

```bash
# View the review comments
gh pr view 123 --comments

# Output shows:
# @amia-reviewer: SECURITY: SQL injection vulnerability in query builder.
# Use parameterized queries instead of string concatenation.

# After fixing, reply:
gh pr comment 123 --body "Fixed SQL injection vulnerability in commit abc123. Now using parameterized queries throughout."

# Request re-review
gh pr edit 123 --add-reviewer "amia-reviewer"
```

### Example 2: Handling Multiple Comments

```bash
gh pr comment 456 --body "$(cat <<'EOF'
## Review Response

Addressed all comments from the review:

### Security
- [x] SQL injection fix (commit abc123)
- [x] Added input sanitization (commit def456)

### Tests
- [x] Added unit tests for UserService (commit ghi789)
- [x] Added integration test for API endpoint (commit jkl012)

### Code Quality
- [x] Refactored long method into smaller functions (commit mno345)
- [x] Added inline documentation (commit pqr678)

Ready for re-review!
EOF
)"
```

### Example 3: Declining a Suggestion

```bash
gh pr comment 789 --body "$(cat <<'EOF'
Regarding the suggestion to use async/await instead of Promises:

I've kept the Promise-based approach for this specific case because:
1. We need to run multiple operations in parallel (Promise.all)
2. The error handling is clearer with .catch chains for this use case
3. It matches the existing patterns in this module

Happy to discuss further if you have concerns about specific parts.
EOF
)"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Could not resolve to a PullRequest` | Wrong PR number | Verify PR number with `gh pr list` |
| `Resource not accessible` | No permission | Check repo access |
| `comment not found` | Wrong comment ID | Get correct ID from API |
| `Review not found` | PR has no reviews | Wait for review or check correct PR |

## Recovery Steps

If you pushed a broken fix:
```bash
# Revert the commit
git revert <commit-hash>
git push origin <branch>

# Comment on PR
gh pr comment <pr-number> --body "Reverted broken fix in commit xyz. Working on correct solution."
```

If you addressed wrong comment:
```bash
# Reply to clarify
gh pr comment <pr-number> --body "My previous comment addressed the wrong issue. Working on the correct fix now."
```
