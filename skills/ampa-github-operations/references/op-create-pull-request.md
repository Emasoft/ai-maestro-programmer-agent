---
name: op-create-pull-request
description: Create a pull request with proper description
parent-skill: ampa-github-operations
---

# Create Pull Request

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

Create a pull request to submit completed work for review. This corresponds to
**Step 19** of the AMPA workflow.

## When to Use

- Task implementation is complete
- All tests pass locally
- Code is ready for review
- **AMOA has green-lit the PR via the pre-PR gate** (never open a PR before this)
- Submitting work for AMIA review (Step 19)

## Prerequisites

- **ORCHESTRATOR (AMOA) green-light received — the pre-PR gate (R6 v3 / #17 M7c).**
  Before opening any PR you MUST have asked AMOA "I believe `<TRDD-id>` is done —
  PR now?" and received an explicit go-ahead *after* AMOA validated the acceptance
  criteria, confirmed all EHTs are terminal, and confirmed tests are green.
  **Never open a PR without it** — use the "PR now?" request/reply template
  (`op-pre-pr-gate`) in the `ampa-orchestrator-communication` skill.
- Feature branch pushed to remote
- All changes committed
- Tests passing
- gh CLI authenticated

## Procedure

### 4.1 Preparing Branch for PR

Before creating PR, ensure branch is ready:

```bash
# Ensure all changes are committed
git status
# Should show: nothing to commit, working tree clean

# Ensure branch is pushed
git push origin <branch-name>

# Sync with main to check for conflicts
git fetch origin main
git merge origin/main
# Resolve any conflicts if needed

# Run tests one final time
# (command depends on project)
```

### 4.2 Writing PR Title and Description

**Title format** (same as commit message):

```text
<type>(<scope>): <short description>
```

Keep under 72 characters. Use imperative mood.

**Description template:**

Every PR body MUST begin with the G1.1 self-identification line — all AI
Maestro agents share the single human-owner GitHub identity, so the body
itself must say which agent authored it:

```markdown
_This is the Claude responsible for the <project> project (AMPA programmer,
via the shared owner gh auth)._

## Summary

Brief description of what this PR does.

## Changes

- Change 1
- Change 2
- Change 3

## Testing

How was this tested?

## Related Issues

Closes #123
```

### 4.3 Creating PR with gh CLI

Create PR using heredoc for proper formatting:

```bash
gh pr create --title "<type>(<scope>): <description>" --body "$(cat <<'EOF'
_This is the Claude responsible for the <project> project (AMPA programmer,
via the shared owner gh auth)._

## Summary
<1-3 sentences describing the change>

## Changes
- <specific change 1>
- <specific change 2>
- <specific change 3>

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Related Issues
Closes #<issue-number>
EOF
)"
```

**Full example:**

```bash
gh pr create --title "feat(auth): add OAuth2 login support" --body "$(cat <<'EOF'
_This is the Claude responsible for the acme-webshop project (AMPA programmer,
via the shared owner gh auth)._

## Summary
Implements OAuth2 authentication flow with support for Google and GitHub providers.

## Changes
- Add OAuth2Strategy class for handling OAuth flows
- Configure passport.js middleware for each provider
- Add callback routes and token handling
- Add user profile sync on first login

## Testing
- [ ] Unit tests pass
- [ ] Integration tests with mock OAuth server pass
- [ ] Manual testing with real Google account

## Related Issues
Closes #123
EOF
)"
```

### 4.4 Setting Reviewers and Labels

Add reviewers and labels at creation time:

```bash
gh pr create \
  --title "feat(auth): add OAuth2 login" \
  --body "..." \
  --reviewer "username1,username2" \
  --label "enhancement,status:review"
```

Or add after creation:

```bash
# Add reviewer
gh pr edit <pr-number> --add-reviewer "username"

# Add label
gh pr edit <pr-number> --add-label "enhancement"

# Add assignee
gh pr edit <pr-number> --add-assignee "@me"
```

### 4.5 Linking to Issues

Link PR to issues to auto-close them on merge:

In PR description, use keywords:

- `Closes #123` - Closes issue when PR merges
- `Fixes #123` - Same as Closes
- `Resolves #123` - Same as Closes
- `Related to #123` - Links without closing

Multiple issues:

```markdown
Closes #123, Closes #124 Fixes #125 Related to #126
```

### 4.6 Creating the PR via the Frozen `amp-submit-pr` CLI (Optional, Orchestrated Mode)

In orchestrated mode, prefer the frozen `amp-submit-pr` CLI to open the PR and
register it on the kanban in one step — never the server `/api/` directly
(R23 frozen-CLI decoupling). The CLI resolves your team and identity from your
registration:

```bash
amp-submit-pr <repo-path> "<type>(<scope>): <description>" --body "$(cat <<'EOF'
_This is the Claude responsible for the <project> project (AMPA programmer,
via the shared owner gh auth)._

## Summary
<1-3 sentences describing the change>

## Changes
- <specific change 1>
- <specific change 2>

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass

## Related Issues
Closes #<issue-number>
EOF
)" --base main
```

The PR body still MUST begin with the G1.1 self-identification line (section
4.2). The `--base` flag defaults to `main`; pass it explicitly only when
targeting a different base branch.

> **Note**: This path is optional and non-fatal. If AI Maestro is not running,
> the programmer has no AID, or the `amp-submit-pr` CLI is unavailable, fall
> back to the `gh pr create` form (section 4.3) — never block the PR on a
> kanban call. After `amp-submit-pr` succeeds, record the returned PR URL so the
> `amp-kanban-move … ai_review` step in `op-notify-completion` can reference it.

## Checklist

- [ ] AMOA pre-PR green-light received ("PR now?" → explicit go-ahead)
- [ ] PR body begins with the G1.1 self-identification line
- [ ] All changes committed and pushed
- [ ] Tests pass locally
- [ ] Branch is up to date with main
- [ ] PR title follows conventional format
- [ ] PR description includes Summary, Changes, Testing sections
- [ ] Issue number linked in description
- [ ] Reviewer assigned (if required)
- [ ] Appropriate labels added

## Examples

### Example 1: Simple Feature PR

```bash
gh pr create \
  --title "feat(api): add user profile endpoint" \
  --body "$(cat <<'EOF'
## Summary
Adds GET /api/users/:id endpoint to retrieve user profiles.

## Changes
- Add UserController.getProfile method
- Add route handler in routes/users.js
- Add input validation middleware

## Testing
- [ ] Unit tests for controller
- [ ] Integration tests for endpoint

## Related Issues
Closes #234
EOF
)"
```

### Example 2: Bug Fix PR with Reviewer

```bash
gh pr create \
  --title "fix(ui): correct date picker timezone handling" \
  --body "$(cat <<'EOF'
## Summary
Fixes timezone conversion bug where dates were displayed in UTC instead of local time.

## Changes
- Update DatePicker component to use local timezone
- Add timezone offset calculation
- Update date formatting utilities

## Testing
- [ ] Manual testing across timezones
- [ ] Unit tests for date utilities

## Related Issues
Fixes #567
EOF
)" \
  --reviewer "senior-dev" \
  --label "bug,high-priority"
```

### Example 3: Draft PR for Early Feedback

```bash
gh pr create \
  --title "feat(payments): integrate Stripe API" \
  --body "WIP: Initial Stripe integration. Looking for early feedback on approach." \
  --draft
```

Convert draft to ready for review:

```bash
gh pr ready <pr-number>
```

## Error Handling

| Error                                | Cause                     | Solution                            |
| ------------------------------------ | ------------------------- | ----------------------------------- |
| `no commits between main and branch` | Branch not diverged       | Make commits on feature branch      |
| `pull request already exists`        | PR exists for this branch | Use existing PR or close it first   |
| `branch not found on remote`         | Not pushed                | `git push -u origin <branch>`       |
| `validation failed`                  | Missing required fields   | Check repo PR template requirements |
| `user not found`                     | Wrong reviewer username   | Verify username spelling            |

## Recovery Steps

If PR was created with wrong title:

```bash
gh pr edit <pr-number> --title "correct title"
```

If PR was created with wrong description:

```bash
gh pr edit <pr-number> --body "$(cat <<'EOF'
new description
EOF
)"
```

If PR was created against wrong base branch:

```bash
gh pr edit <pr-number> --base correct-branch
```

If you need to completely redo:

```bash
# Close the PR
gh pr close <pr-number>

# Create new PR
gh pr create ...
```
