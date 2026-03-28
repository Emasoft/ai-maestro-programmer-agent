---
name: op-clone-repository
description: Clone or fork a repository to local machine
parent-skill: ampa-github-operations
---

# Clone Repository

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

Clone or fork the project repository to your local agent folder for development.

> **Multi-repo rule**: Always clone into `$AGENT_DIR/repos/<repo-name>`. Use `amp-clone-repo.sh <repo-url>` (preferred) which clones to the correct location automatically. All subsequent git commands must use `git -C "$REPO_PATH"` to target the correct repo.

## When to Use

- Starting work on a new project
- Setting up a local development environment
- Contributing to an upstream open source project
- Creating a personal copy of a repository

## Prerequisites

- gh CLI installed (see https://cli.github.com/)
  - macOS: `brew install gh`
  - Linux: `sudo apt install gh` or see https://github.com/cli/cli/blob/trunk/docs/install_linux.md
  - Windows: `winget install --id GitHub.cli`
- gh CLI authenticated: `gh auth login`
- Git configured with user name and email
- Network access to GitHub

## Procedure

### 1.1 When to Clone vs Fork

**Clone directly** when:
- You have write access to the repository
- It is your own repository
- You are part of the organization that owns the repo

**Fork first** when:
- You do not have write access
- Contributing to an open source project
- You want to make changes without affecting the original

### 1.2 Cloning with amp-clone-repo.sh (Preferred)

Use the amp script which clones to the correct agent folder automatically:

```bash
# Preferred: clones to $AGENT_DIR/repos/<repo-name>
amp-clone-repo.sh <repo-url>
```

### 1.3 Cloning with gh CLI (Manual)

Clone a repository you have access to, always specifying the target directory inside the agent folder:

```bash
# Clone to agent repos directory (ALWAYS specify destination)
REPO_PATH="$AGENT_DIR/repos/<repo-name>"
gh repo clone <owner>/<repo> "$REPO_PATH"

# Clone with SSH (if configured)
gh repo clone <owner>/<repo> "$REPO_PATH" -- --config core.sshCommand="ssh -i ~/.ssh/id_rsa"
```

Example:
```bash
REPO_PATH="$AGENT_DIR/repos/<project>"
gh repo clone <owner>/<project> "$REPO_PATH"
```

### 1.4 Forking Upstream Repositories

Fork and clone in one command, always specifying the clone destination:

```bash
REPO_PATH="$AGENT_DIR/repos/<repo-name>"

# Fork to your account and clone locally
gh repo fork <owner>/<repo> --clone=true -- "$REPO_PATH"

# Fork without cloning
gh repo fork <owner>/<repo> --clone=false

# Fork to an organization
gh repo fork <owner>/<repo> --org=<org-name> --clone=true
```

Example:
```bash
REPO_PATH="$AGENT_DIR/repos/kubernetes"
gh repo fork kubernetes/kubernetes --clone=true -- "$REPO_PATH"
```

### 1.5 Setting Up Remotes for Forks

After forking, verify remotes are configured correctly (always use `git -C` to target the repo):

```bash
# List remotes
git -C "$REPO_PATH" remote -v
```

Expected output for a fork:
```
origin    https://github.com/<your-username>/<repo>.git (fetch)
origin    https://github.com/<your-username>/<repo>.git (push)
upstream  https://github.com/<original-owner>/<repo>.git (fetch)
upstream  https://github.com/<original-owner>/<repo>.git (push)
```

If upstream is missing, add it:
```bash
git -C "$REPO_PATH" remote add upstream https://github.com/<original-owner>/<repo>.git
```

Sync fork with upstream:
```bash
git -C "$REPO_PATH" fetch upstream
git -C "$REPO_PATH" checkout main
git -C "$REPO_PATH" merge upstream/main
git -C "$REPO_PATH" push origin main
```

### 1.6 Verifying Clone Success

After cloning, verify the setup (always use `git -C` to target the repo):

```bash
# Verify repo directory exists
[ -d "$REPO_PATH/.git" ] || { echo "Repo not found at $REPO_PATH"; exit 1; }

# Verify git status
git -C "$REPO_PATH" status

# Check remote configuration
git -C "$REPO_PATH" remote -v

# Verify branch
git -C "$REPO_PATH" branch -a

# Check recent commits
git -C "$REPO_PATH" log --oneline -5
```

## Checklist

- [ ] Determine if clone or fork is needed
- [ ] Run gh repo clone or gh repo fork command
- [ ] Change into repository directory
- [ ] Verify remotes are configured
- [ ] Add upstream remote if forked
- [ ] Verify main branch is up to date

## Examples

### Example 1: Clone Own Repository (amp script)

```bash
amp-clone-repo.sh https://github.com/<owner>/<project>
REPO_PATH="$AGENT_DIR/repos/<project>"
git -C "$REPO_PATH" status
# On branch main
# Your branch is up to date with 'origin/main'.
```

### Example 2: Fork and Clone Open Source Project

```bash
REPO_PATH="$AGENT_DIR/repos/react"
gh repo fork facebook/react --clone=true -- "$REPO_PATH"
git -C "$REPO_PATH" remote -v
# origin    https://github.com/<owner>/react.git (fetch)
# origin    https://github.com/<owner>/react.git (push)
# upstream  https://github.com/facebook/react.git (fetch)
# upstream  https://github.com/facebook/react.git (push)
```

### Example 3: Clone to Agent Repos Directory

```bash
REPO_PATH="$AGENT_DIR/repos/<project>"
gh repo clone <owner>/<project> "$REPO_PATH"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `repository not found` | Wrong repo name or private repo without access | Verify repo name, check access permissions |
| `could not read Username` | Not authenticated | Run `gh auth login` |
| `Permission denied (publickey)` | SSH key issue | Use HTTPS or configure SSH key |
| `destination path already exists` | Directory exists | Remove directory or use different name |
| `fatal: not a git repository` | Not in repo directory | `cd` into cloned directory |

## Recovery Steps

If clone fails:

1. Delete partial clone if exists: `rm -rf "$REPO_PATH"`
2. Verify authentication: `gh auth status`
3. Verify repository exists: `gh repo view <owner>/<repo>`
4. Try with HTTPS explicitly: `git clone https://github.com/<owner>/<repo>.git "$REPO_PATH"`
