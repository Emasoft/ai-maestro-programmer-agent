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

import os
import subprocess
import sys
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


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a git command and return the CompletedProcess result.

    The return type is parameterized as ``CompletedProcess[str]`` because
    ``text=True`` is always set, so ``.stdout``/``.stderr`` are ``str`` (not
    ``bytes``). Without the ``[str]`` parameter mypy infers ``Any`` for the
    streams, which then leaks ``Any`` out of typed callers like
    ``get_base_branch()`` (the ``[no-any-return]`` error at the
    ``.split("/")[-1]`` site).
    """
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=check,
    )


def get_repo_root() -> Path:
    """Return the absolute path to the git repository root."""
    result = git("rev-parse", "--show-toplevel")
    return Path(result.stdout.strip())


def get_base_branch() -> str:
    """Return the name of the default remote branch (e.g. 'main')."""
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
    """Print a colored banner with separator lines above and below."""
    sep = f"{color}{'=' * 40}{NC}"
    print(sep)
    for line in lines:
        print(f"{color}  {line}{NC}")
    print(sep)


def main() -> int:
    """Run plugin validation before push; block on CRITICAL/MAJOR issues."""
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
        _local_ref, local_sha, _remote_ref, remote_sha = parts

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
    os.chdir(repo_root)

    # Local CPV validator scripts were retired in bc1c306 — validation runs
    # through the CPV remote launcher (the same command CI's validate.yml
    # uses), fetched on demand via uvx. Without uvx there is no validator to
    # run, so warn-and-allow rather than blocking every push on a tooling gap.
    uvx_check = subprocess.run(["uvx", "--version"], capture_output=True, text=True)
    if uvx_check.returncode != 0:
        print(f"{YELLOW}WARNING: uvx not found — cannot run cpv-remote-validate{NC}")
        print(f"{YELLOW}Cannot validate plugin. Allowing push.{NC}")
        return 0

    print(f"{BLUE}Running plugin validation (cpv-remote-validate --strict)...{NC}")
    print()

    # Determine report file path for concise output when invoked by agents
    report_file = os.environ.get("AMPA_REPORT_FILE")

    cmd = [
        "uvx",
        "--from", "git+https://github.com/Emasoft/claude-plugins-validation",
        "--with", "pyyaml",
        "cpv-remote-validate", "plugin", ".", "--strict",
    ]

    if report_file:
        # Capture validator output to file, show only concise summary
        result = subprocess.run(cmd, capture_output=True, text=True)
        Path(report_file).write_text(
            result.stdout + ("\n" + result.stderr if result.stderr else ""),
            encoding="utf-8",
        )
    else:
        # Default: stream validator output directly to terminal (text=True for type consistency)
        result = subprocess.run(cmd, text=True)

    exit_code = result.returncode

    print()

    # cpv-remote-validate --strict exit codes mirror CI's quality gate:
    # 0=PASS; 1=CRITICAL, 2=MAJOR, 3=MINOR, 4=NIT all BLOCK (only exit 0
    # passes in CI's validate.yml, so the hook must block the same set or
    # pushes land that CI then rejects).
    severity_names = {1: "CRITICAL", 2: "MAJOR", 3: "MINOR", 4: "NIT"}

    if report_file:
        # Concise summary for agent consumption
        if exit_code == 0:
            print(f"[PASS] All validation checks passed. Push allowed. Report: {report_file}")
            return 0
        name = severity_names.get(exit_code, f"exit {exit_code}")
        print(f"[BLOCKED] {name} issues found. Push blocked. Report: {report_file}")
        return 1

    if exit_code == 0:
        banner(GREEN, [
            "PASSED: All validation checks passed",
            "Push allowed.",
        ])
        return 0
    name = severity_names.get(exit_code, f"exit code {exit_code}")
    banner(RED, [
        f"BLOCKED: {name} issues found (CI's strict gate blocks the same)",
        "Fix ALL issues before pushing.",
    ])
    return 1


if __name__ == "__main__":
    sys.exit(main())
