#!/usr/bin/env python3
# pre-push hook - Validate plugin before allowing push
#
# Runs validate_plugin.py in strict mode: CRITICAL and MAJOR severity levels
# block the push. MINOR issues are warnings only (push allowed).
#
# Exit codes from validate_plugin.py:
#   0 - All checks passed
#   1 - CRITICAL issues found (blocks push)
#   2 - MAJOR issues found (blocks push)
#   3 - MINOR issues found (warning only, push allowed)
#
# To install:
#   mkdir -p .git/hooks && cp git-hooks/pre-push .git/hooks/pre-push && chmod +x .git/hooks/pre-push
#
# To bypass (NOT RECOMMENDED):
#   git push --no-verify

import sys
import subprocess
from pathlib import Path

# ANSI colors
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
NC = "\033[0m"

# Plugin file patterns (same as shell version)
PLUGIN_PATTERNS = (
    ".claude-plugin/",
    "agents/",
    "commands/",
    "skills/",
    "hooks/",
    "scripts/",
    ".mcp.json",
)

NULL_SHA = "0000000000000000000000000000000000000000"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command and return the CompletedProcess result."""
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=check,
    )


def get_repo_root() -> Path:
    result = git("rev-parse", "--show-toplevel")
    return Path(result.stdout.strip())


def get_base_branch() -> str:
    result = git("symbolic-ref", "refs/remotes/origin/HEAD", check=False)
    if result.returncode == 0:
        # e.g. refs/remotes/origin/main -> main
        return result.stdout.strip().split("/")[-1]
    return "main"


def get_changed_files(local_sha: str, remote_sha: str) -> list[str]:
    """Return list of changed file paths for the push range."""
    if remote_sha == NULL_SHA:
        # New branch: compare against merge-base with default branch
        base_branch = get_base_branch()
        merge_base_result = git("merge-base", local_sha, f"origin/{base_branch}", check=False)
        if merge_base_result.returncode == 0:
            merge_base = merge_base_result.stdout.strip()
            result = git("diff", "--name-only", merge_base, local_sha, check=False)
            return result.stdout.splitlines() if result.returncode == 0 else []
        else:
            # No common ancestor; list all files in the commit tree
            result = git("ls-tree", "-r", "--name-only", local_sha, check=False)
            return result.stdout.splitlines() if result.returncode == 0 else []
    else:
        result = git("diff", "--name-only", f"{remote_sha}..{local_sha}", check=False)
        return result.stdout.splitlines() if result.returncode == 0 else []


def is_plugin_file(path: str) -> bool:
    """Check whether path matches any plugin file pattern."""
    for pattern in PLUGIN_PATTERNS:
        if pattern.endswith("/"):
            if path.startswith(pattern) or f"/{pattern[:-1]}/" in path:
                return True
        else:
            if path.endswith(pattern):
                return True
    return False


def banner(color: str, lines: list[str]) -> None:
    sep = f"{color}{'=' * 40}{NC}"
    print(sep)
    for line in lines:
        print(f"{color}  {line}{NC}")
    print(sep)


def main() -> int:
    # git passes remote name and URL as argv[1] and argv[2]
    remote = sys.argv[1] if len(sys.argv) > 1 else "origin"
    url = sys.argv[2] if len(sys.argv) > 2 else ""

    print(f"{BLUE}{'=' * 40}{NC}")
    print(f"{BLUE}  Pre-push Plugin Validation{NC}")
    print(f"{BLUE}{'=' * 40}{NC}")
    print()
    print(f"{BLUE}Pushing to:{NC} {remote} ({url})")
    print()

    repo_root = get_repo_root()

    plugin_files_changed = False

    # Read push refs from stdin (one line per ref being pushed)
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split()
        if len(parts) != 4:
            continue
        local_ref, local_sha, remote_ref, remote_sha = parts

        if local_sha == NULL_SHA:
            # Branch deletion — no validation needed
            print(f"{GREEN}Branch deletion detected. No validation needed.{NC}")
            continue

        changed_files = get_changed_files(local_sha, remote_sha)
        for f in changed_files:
            if is_plugin_file(f):
                plugin_files_changed = True
                break

        if plugin_files_changed:
            break

    if not plugin_files_changed:
        print(f"{GREEN}No plugin files changed. Skipping validation.{NC}")
        return 0

    # Change to repo root before running the validator
    import os
    os.chdir(repo_root)

    validator = repo_root / "scripts" / "validate_plugin.py"
    if not validator.is_file():
        print(f"{YELLOW}WARNING: scripts/validate_plugin.py not found{NC}")
        print(f"{YELLOW}Cannot validate plugin. Allowing push.{NC}")
        return 0

    print(f"{BLUE}Running plugin validation...{NC}")
    print()

    # NOTE: CPV scripts are synced in CI (validate.yml), not during pre-push.
    # To manually update local validation scripts, run: python3 scripts/sync_cpv_scripts.py
    result = subprocess.run(
        ["uv", "run", "--with", "pyyaml", "python", "scripts/validate_plugin.py", ".", "--verbose"],
        # No shell=True — executable list only
    )
    exit_code = result.returncode

    print()

    if exit_code == 0:
        banner(GREEN, [
            "PASSED: All validation checks passed",
            "Push allowed.",
        ])
        return 0
    elif exit_code == 1:
        banner(RED, [
            "BLOCKED: CRITICAL issues found",
            "Fix ALL issues before pushing.",
        ])
        return 1
    elif exit_code == 2:
        banner(RED, [
            "BLOCKED: MAJOR issues found",
            "Fix ALL issues before pushing.",
        ])
        return 1
    elif exit_code == 3:
        banner(YELLOW, [
            "WARNING: MINOR issues found",
            "Push allowed. Fix when convenient.",
        ])
        return 0
    else:
        banner(YELLOW, [
            f"Validation returned exit code {exit_code}",
            "Please check the validation script. Push allowed.",
        ])
        return 0


if __name__ == "__main__":
    sys.exit(main())
