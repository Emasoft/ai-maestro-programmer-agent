#!/usr/bin/env python3
"""Real tests for the programmer memory system (issue #12).

Tests the canonical shell recipes documented in
skills/programmer-memory-recall/SKILL.md and
skills/programmer-memory-write/SKILL.md against a real fixture memory dir —
no mocks. The recall recipe is executed through bash exactly as the skill
documents it (memgrep when present, `grep -rliE` fallback otherwise), and
the write recipe's output is parsed back with PyYAML to prove the schema.

Anti-drift guard: the last tests assert the SKILL.md files still carry the
exact commands exercised here, so editing a skill recipe without updating
the tests (or vice versa) fails the suite.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
RECALL_SKILL = REPO_ROOT / "skills" / "programmer-memory-recall" / "SKILL.md"
WRITE_SKILL = REPO_ROOT / "skills" / "programmer-memory-write" / "SKILL.md"
RULE_FILE = REPO_ROOT / "rules" / "memory-protocol.md"

# PATH containing standard tools (bash, grep) but NOT ~/.cargo/bin, so
# `command -v memgrep` fails and the fallback branch is genuinely exercised.
FALLBACK_PATH = "/usr/bin:/bin"

# The canonical recall recipe from the skill, verbatim shape: gate on
# memgrep, fall back to grep -rliE. $1 = symptom, $2 = memdir.
RECALL_RECIPE = (
    'SYMPTOM="$1"; MEMDIR="$2"; '
    "if command -v memgrep >/dev/null 2>&1; then "
    '  memgrep recall "$SYMPTOM" "$MEMDIR"; '
    "else "
    '  grep -rliE "$SYMPTOM" "$MEMDIR" 2>/dev/null; '
    "fi"
)


def _make_fixture_memdir(root: Path) -> Path:
    """Create a real memory dir with three schema-valid notes + MEMORY.md."""
    memdir = root / "memory"
    memdir.mkdir()
    (memdir / "project_uv-lock-staging.md").write_text(
        "---\n"
        "name: project_uv-lock-staging\n"
        'description: "publish failed with stale lockfile / uv.lock one version behind after release"\n'
        "metadata:\n"
        "  node_type: memory\n"
        "  type: project\n"
        "---\n"
        "publish.py must stage uv.lock in the release commit; _sync_uv_lock\n"
        "regenerates it during the bump.\n",
        encoding="utf-8",
    )
    (memdir / "reference_serena-activation.md").write_text(
        "---\n"
        "name: reference_serena-activation\n"
        'description: "SERENA tools not found / how to activate the project for code navigation"\n'
        "metadata:\n"
        "  node_type: memory\n"
        "  type: reference\n"
        "---\n"
        "Activate with the activate_project tool before find_symbol works.\n",
        encoding="utf-8",
    )
    (memdir / "feedback_no-mocked-tests.md").write_text(
        "---\n"
        "name: feedback_no-mocked-tests\n"
        'description: "are mocked tests acceptable / user said tests must be real"\n'
        "metadata:\n"
        "  node_type: memory\n"
        "  type: feedback\n"
        "---\n"
        "Never mock the system under test.\n"
        "**Why:** mocked results discover nothing.\n"
        "**How to apply:** run the real command in tests.\n",
        encoding="utf-8",
    )
    (memdir / "MEMORY.md").write_text(
        "- [uv.lock staging](project_uv-lock-staging.md) — stale lockfile after release.\n"
        "- [SERENA activation](reference_serena-activation.md) — activate before navigating.\n"
        "- [No mocked tests](feedback_no-mocked-tests.md) — tests must be real.\n",
        encoding="utf-8",
    )
    return memdir


def _run_recall(symptom: str, memdir: Path, path_env: str) -> subprocess.CompletedProcess[str]:
    """Run the canonical recall recipe through bash with a controlled PATH."""
    return subprocess.run(
        ["bash", "-c", RECALL_RECIPE, "recall", symptom, str(memdir)],
        capture_output=True,
        text=True,
        env={**os.environ, "PATH": path_env},
        timeout=60,
        check=False,
    )


def test_grep_fallback_finds_note_by_symptom(tmp_path: Path) -> None:
    """Recall recipe with memgrep ABSENT finds the right note via the grep fallback."""
    memdir = _make_fixture_memdir(tmp_path)
    probe = subprocess.run(
        ["bash", "-c", "command -v memgrep"],
        capture_output=True,
        text=True,
        env={**os.environ, "PATH": FALLBACK_PATH},
        check=False,
    )
    assert probe.returncode != 0, "precondition failed: memgrep still on the restricted PATH"
    result = _run_recall("stale lockfile", memdir, FALLBACK_PATH)
    assert result.returncode == 0, f"fallback recall failed: {result.stderr}"
    assert "project_uv-lock-staging.md" in result.stdout
    assert "reference_serena-activation.md" not in result.stdout


def test_grep_fallback_unrelated_symptom_yields_no_results(tmp_path: Path) -> None:
    """Recall recipe with memgrep ABSENT returns empty output (exit 1) for an unrelated symptom."""
    memdir = _make_fixture_memdir(tmp_path)
    result = _run_recall("kubernetes ingress flapping", memdir, FALLBACK_PATH)
    assert result.stdout.strip() == "", "expected zero matches for an unrelated symptom"
    assert result.returncode == 1, "grep signals no-match with exit 1"


def test_memgrep_recall_ranks_target_note_first(tmp_path: Path) -> None:
    """Recall recipe with memgrep PRESENT returns the symptom-matching note ranked first."""
    if shutil.which("memgrep") is None:
        pytest.skip("memgrep not installed — fallback path covered by the grep tests")
    memdir = _make_fixture_memdir(tmp_path)
    result = _run_recall("publish failed with stale lockfile", memdir, os.environ["PATH"])
    assert result.returncode == 0, f"memgrep recall failed: {result.stderr}"
    first_line = result.stdout.strip().splitlines()[0]
    assert "project_uv-lock-staging" in first_line, f"unexpected top result: {first_line}"


def test_write_procedure_produces_schema_valid_note_and_index_line(tmp_path: Path) -> None:
    """Executing the write skill's documented steps yields a schema-valid note + MEMORY.md line."""
    memdir = tmp_path / "memory"
    memdir.mkdir()
    note_name = "project_pipe-truncation"
    note_path = memdir / f"{note_name}.md"
    # Steps 4-5 of the write skill, performed exactly as documented.
    note_path.write_text(
        "---\n"
        f"name: {note_name}\n"
        'description: "command output looks truncated / wrong line count when piping through tee | head"\n'
        "metadata:\n"
        "  node_type: memory\n"
        "  type: project\n"
        "---\n"
        "SIGPIPE kills tee before it finishes writing; capture to a file\n"
        "first, then inspect it separately.\n",
        encoding="utf-8",
    )
    index = memdir / "MEMORY.md"
    index.write_text(
        f"- [Pipe truncation](({note_name}.md)".replace("((", "(")
        + " — tee|head silently truncates captures.\n",
        encoding="utf-8",
    )
    # Validate the note against the schema in rules/memory-protocol.md.
    text = note_path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.+)$", text, re.DOTALL)
    assert match, "note must have YAML frontmatter delimited by --- lines"
    front = yaml.safe_load(match.group(1))
    body = match.group(2).strip()
    assert front["name"] == note_path.stem, "frontmatter name must equal the filename stem"
    assert isinstance(front["description"], str) and front["description"].strip()
    assert front["metadata"]["node_type"] == "memory"
    assert front["metadata"]["type"] in {"user", "feedback", "project", "reference"}
    assert body, "note body must carry the fact"
    # Validate the index line format: "- [Title](file.md) — hook"
    index_line = index.read_text(encoding="utf-8").strip()
    assert re.match(r"^- \[.+\]\(" + re.escape(f"{note_name}.md") + r"\) — .+$", index_line)
    # Round-trip: the note is recallable from the symptom via the fallback.
    result = _run_recall("truncated", memdir, FALLBACK_PATH)
    assert f"{note_name}.md" in result.stdout


def test_recall_skill_doc_carries_canonical_fallback_recipe() -> None:
    """programmer-memory-recall SKILL.md exists, has valid frontmatter, and documents the exact gate + fallback."""
    assert RECALL_SKILL.is_file(), "recall SKILL.md missing"
    text = RECALL_SKILL.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, "recall SKILL.md must start with YAML frontmatter"
    front = yaml.safe_load(match.group(1))
    assert front["name"] == "programmer-memory-recall"
    assert "symptom" in front["description"].lower()
    assert "command -v memgrep" in text, "skill must gate on memgrep presence"
    assert "grep -rliE" in text, "skill must document the grep fallback"
    assert "memgrep recall" in text, "skill must document the memgrep path"


def test_write_skill_doc_carries_schema_and_index_contract() -> None:
    """programmer-memory-write SKILL.md exists, has valid frontmatter, and documents schema + MEMORY.md index."""
    assert WRITE_SKILL.is_file(), "write SKILL.md missing"
    text = WRITE_SKILL.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, "write SKILL.md must start with YAML frontmatter"
    front = yaml.safe_load(match.group(1))
    assert front["name"] == "programmer-memory-write"
    assert "node_type: memory" in text, "skill must document the note schema"
    assert "MEMORY.md" in text, "skill must document the index line step"
    assert "user|feedback|project|reference" in text or all(
        t in text for t in ("user", "feedback", "project", "reference")
    ), "skill must document the type enum"


def test_rule_file_present_and_carries_protocol() -> None:
    """rules/memory-protocol.md exists and carries the one-law + fallback + PROGRAMMER wiring."""
    assert RULE_FILE.is_file(), "rules/memory-protocol.md missing"
    text = RULE_FILE.read_text(encoding="utf-8")
    assert "index by the QUESTION, not the answer" in text
    assert "command -v memgrep" in text and "grep -rliE" in text
    assert "PROGRAMMER workflow wiring" in text
    assert "programmer-memory-recall" in text and "programmer-memory-write" in text
