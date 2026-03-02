---
name: op-clone-repository
description: Clone or fork a repository to local machine
parent-skill: ampa-github-operations
operation-type: setup
---

# Clone Repository

Clone or fork the project repository to your local machine for development.

## Table of Contents

- 1.1 When to clone vs fork
- 1.2 Cloning with gh CLI
- 1.3 Forking upstream repositories
- 1.4 Setting up remotes for forks
- 1.5 Verifying clone success

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

### 1.2 Cloning with gh CLI

Clone a repository you have access to:

```bash
# Clone to current directory
gh repo clone <owner>/<repo>

# Clone to specific directory
gh repo clone <owner>/<repo> <directory>

# Clone with SSH (if configured)
gh repo clone <owner>/<repo> -- --config core.sshCommand="ssh -i ~/.ssh/id_rsa"
```

Example:
```bash
gh repo clone <owner>/<project>
cd <project>
```

### 1.3 Forking Upstream Repositories

Fork and clone in one command:

```bash
# Fork to your account and clone locally
gh repo fork <owner>/<repo> --clone=true

# Fork without cloning
gh repo fork <owner>/<repo> --clone=false

# Fork to an organization
gh repo fork <owner>/<repo> --org=<org-name> --clone=true
```

Example:
```bash
gh repo fork kubernetes/kubernetes --clone=true
cd kubernetes
```

### 1.4 Setting Up Remotes for Forks

After forking, verify remotes are configured correctly:

```bash
# List remotes
git remote -v
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
git remote add upstream https://github.com/<original-owner>/<repo>.git
```

Sync fork with upstream:
```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 1.5 Verifying Clone Success

After cloning, verify the setup:

```bash
# Check you are in the repo directory
pwd

# Verify git status
git status

# Check remote configuration
git remote -v

# Verify branch
git branch -a

# Check recent commits
git log --oneline -5
```

## Checklist

- [ ] Determine if clone or fork is needed
- [ ] Run gh repo clone or gh repo fork command
- [ ] Change into repository directory
- [ ] Verify remotes are configured
- [ ] Add upstream remote if forked
- [ ] Verify main branch is up to date

## Examples

### Example 1: Clone Own Repository

```bash
gh repo clone <owner>/<project>
cd <project>
git status
# On branch main
# Your branch is up to date with 'origin/main'.
```

### Example 2: Fork and Clone Open Source Project

```bash
gh repo fork facebook/react --clone=true
cd react
git remote -v
# origin    https://github.com/<owner>/react.git (fetch)
# origin    https://github.com/<owner>/react.git (push)
# upstream  https://github.com/facebook/react.git (fetch)
# upstream  https://github.com/facebook/react.git (push)
```

### Example 3: Clone to Specific Directory

```bash
gh repo clone <owner>/<project> ~/projects/<project>
cd ~/projects/<project>
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

1. Delete partial clone if exists: `rm -rf <repo-name>`
2. Verify authentication: `gh auth status`
3. Verify repository exists: `gh repo view <owner>/<repo>`
4. Try with HTTPS explicitly: `git clone https://github.com/<owner>/<repo>.git`
