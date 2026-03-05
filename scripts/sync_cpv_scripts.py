#!/usr/bin/env python3
# sync_cpv_scripts.py - Sync validation scripts from claude-plugins-validation
#
# Downloads the latest validation scripts from the official CPV repository
# (Emasoft/claude-plugins-validation) and replaces the local copies.
#
# Usage:
#   python scripts/sync_cpv_scripts.py           # Sync from GitHub (latest release)
#   python scripts/sync_cpv_scripts.py v1.7.3    # Sync from a specific tag
#
# Requirements: gh (GitHub CLI), authenticated

import base64
import hashlib
import os
import platform
import subprocess
import sys
from pathlib import Path

# ANSI color codes
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
NC = "\033[0m"

REPO = "Emasoft/claude-plugins-validation"

# Validation scripts to sync (all validate_*.py + utilities)
SCRIPTS = [
    "cpv_validation_common.py",
    "gitignore_filter.py",
    "lint_files.py",
    "smart_exec.py",
    "validate_agent.py",
    "validate_command.py",
    "validate_documentation.py",
    "validate_encoding.py",
    "validate_enterprise.py",
    "validate_hook.py",
    "validate_lsp.py",
    "validate_marketplace_pipeline.py",
    "validate_marketplace.py",
    "validate_mcp.py",
    "validate_plugin.py",
    "validate_rules.py",
    "validate_scoring.py",
    "validate_security.py",
    "validate_skill_comprehensive.py",
    "validate_skill.py",
    "validate_xref.py",
]


def cprint(color: str, message: str) -> None:
    """Print a colored message to stdout."""
    print(f"{color}{message}{NC}")


def gh_api(endpoint: str, jq_filter: str) -> str:
    """Call gh api with a jq filter and return the stripped output string.

    Returns empty string on any failure rather than raising, so callers
    can treat an empty result as 'not found / unavailable'.
    """
    result = subprocess.run(
        ["gh", "api", endpoint, "--jq", jq_filter],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def resolve_ref(repo: str, requested_ref: str) -> str:
    """Resolve the git ref to sync from.

    If requested_ref is provided use it directly.  Otherwise try the latest
    release tag and fall back to the repository default branch.
    """
    if requested_ref:
        cprint(BLUE, f"Syncing from ref: {requested_ref}")
        return requested_ref

    # Try latest release
    tag = gh_api(f"repos/{repo}/releases/latest", ".tag_name")
    if tag:
        cprint(GREEN, f"Latest release: {tag}")
        return tag

    # Fall back to default branch
    branch = gh_api(f"repos/{repo}", ".default_branch") or "master"
    cprint(YELLOW, f"No releases found. Using branch: {branch}")
    return branch


def fetch_script_bytes(repo: str, ref: str, script_name: str) -> bytes | None:
    """Download a script from the GitHub API and return its decoded bytes.

    The GitHub Contents API returns base64-encoded content with embedded
    newlines (every 60 chars).  We strip those newlines before decoding —
    this is the fix for the bash trailing-newline stripping bug that was
    causing CI failures.

    Returns None on network failure or decode error.
    """
    endpoint = f"repos/{repo}/contents/scripts/{script_name}?ref={ref}"
    raw_content = gh_api(endpoint, ".content")

    if not raw_content:
        return None

    # Strip embedded newlines that GitHub inserts into the base64 payload
    cleaned = raw_content.replace("\n", "").replace("\r", "")

    try:
        return base64.b64decode(cleaned)
    except Exception:
        return None


def sha256_of_bytes(data: bytes) -> str:
    """Return the hex SHA-256 digest of the given bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_of_file(path: Path) -> str:
    """Return the hex SHA-256 digest of the file at *path*."""
    return sha256_of_bytes(path.read_bytes())


def make_executable(path: Path) -> None:
    """Set the executable bit on *path* (no-op on Windows)."""
    if platform.system() == "Windows":
        return
    current_mode = path.stat().st_mode
    # Add owner/group/other execute bits that mirror existing read bits
    exec_bits = (current_mode & 0o444) >> 2  # r→x
    os.chmod(path, current_mode | exec_bits | 0o111)


def check_gh_available() -> None:
    """Exit with a helpful message if the gh CLI is not installed."""
    result = subprocess.run(
        ["gh", "--version"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        cprint(RED, "ERROR: gh (GitHub CLI) is required but not installed.")
        print("Install gh CLI: https://cli.github.com/ (macOS: brew install gh)")
        sys.exit(1)


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    requested_ref = sys.argv[1] if len(sys.argv) > 1 else ""

    cprint(BLUE, "========================================")
    cprint(BLUE, "  CPV Validation Scripts Sync")
    cprint(BLUE, "========================================")
    print()

    check_gh_available()

    ref = resolve_ref(REPO, requested_ref)

    cprint(BLUE, f"Source: {REPO}@{ref}")
    print()

    synced = 0
    failed = 0
    unchanged = 0

    for script in SCRIPTS:
        new_bytes = fetch_script_bytes(REPO, ref, script)

        if new_bytes is None:
            cprint(YELLOW, f"  SKIP: {script} (not found in CPV@{ref})")
            failed += 1
            continue

        dest = script_dir / script

        # Skip write if the file content is identical
        if dest.exists():
            if sha256_of_file(dest) == sha256_of_bytes(new_bytes):
                unchanged += 1
                continue

        # Write decoded bytes directly — no string conversion, no newline issues
        dest.write_bytes(new_bytes)
        make_executable(dest)
        cprint(GREEN, f"  UPDATED: {script}")
        synced += 1

    print()
    cprint(BLUE, "========================================")
    print(
        f"{GREEN}  Synced: {synced}  {NC}"
        f"Unchanged: {unchanged}  "
        f"{YELLOW}Skipped: {failed}{NC}"
    )
    cprint(BLUE, "========================================")

    if synced > 0:
        print()
        cprint(YELLOW, f"NOTE: {synced} script(s) updated. Stage and commit before pushing:")
        print("  git add scripts/")
        print(f"  git commit -m 'chore: sync CPV validation scripts from {ref}'")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
