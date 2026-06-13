#!/usr/bin/env python3
"""Real contract tests for the 5 primary AMPA skills + the #17 alignment (no mocks).

The 5 primary skills (task-execution, orchestrator-communication,
github-operations, project-setup, handoff-management) shipped with zero tests
(audit #17 M12). These tests read the ACTUAL skill + reference files on disk and
assert their structural contract and the behaviours the fleet-readiness
alignment (#17) put in place: valid frontmatter, resolvable reference links,
the M5 governance block, the M6 R6-v3 fix, the M7 dialog-loop gates, the M10
G1.1 self-id, the M11 v2 `column:` migration, and the M2/M3/M4 governance
bootstrap. They are anti-drift guards: edit a skill without updating it here
(or vice-versa) and the suite fails.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
AGENT_FILE = REPO_ROOT / "agents" / "ai-maestro-programmer-agent-main-agent.md"

PRIMARY_SKILLS = [
    "ampa-task-execution",
    "ampa-orchestrator-communication",
    "ampa-github-operations",
    "ampa-project-setup",
    "ampa-handoff-management",
]

# Handoff reference files that carry TASK state (must use the v2 `column:`
# field). op-write-bug-report is EXCLUDED — its status field is the bug
# report's own lifecycle (new|confirmed|fixed), not task state.
HANDOFF_TASKSTATE_REFS = [
    "skills/ampa-handoff-management/references/op-create-handoff-document.md",
    "skills/ampa-handoff-management/references/op-read-handoff-document.md",
    "skills/ampa-handoff-management/references/op-document-work-state.md",
]

V2_COLUMNS = {
    "backburner", "todo", "design", "dispatch", "dev", "testing",
    "ai_review", "human_review", "complete", "publish", "published",
    "deploy", "live", "live_auditing", "blocked", "failed", "superseded",
}


def _split_frontmatter(text: str) -> dict:
    """Parse the leading --- YAML frontmatter block of a markdown file."""
    assert text.startswith("---"), "file must open with a YAML frontmatter block"
    parts = text.split("---", 2)
    assert len(parts) >= 3, "frontmatter must be closed with a second ---"
    data = yaml.safe_load(parts[1])
    assert isinstance(data, dict), "frontmatter must parse to a mapping"
    return data


def _resource_links(text: str) -> list[str]:
    """Every (references/<file>.md) link target in a skill's Resources table."""
    return re.findall(r"\(references/([^)]+\.md)\)", text)


@pytest.mark.parametrize("skill", PRIMARY_SKILLS)
def test_skill_frontmatter_valid(skill: str) -> None:
    """Each primary skill's SKILL.md has valid frontmatter with name==dir + description."""
    fm = _split_frontmatter((SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8"))
    assert fm.get("name") == skill, f"{skill}: frontmatter name must equal the directory"
    assert str(fm.get("description", "")).strip(), f"{skill}: description must be non-empty"


@pytest.mark.parametrize("skill", PRIMARY_SKILLS)
def test_skill_governance_block_present(skill: str) -> None:
    """M5: each primary skill carries the approval-tiers reference + never-self-approve line."""
    body = (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
    assert "## Governance" in body, f"{skill}: missing ## Governance section"
    assert "approval tiers" in body.lower(), f"{skill}: must reference the approval tiers"
    assert "ampa-prrd-trdd-kanban" in body, f"{skill}: must point at the kanban skill"
    assert "never self-approves its own releases" in body, (
        f"{skill}: must carry the never-self-approve line"
    )


@pytest.mark.parametrize("skill", PRIMARY_SKILLS)
def test_skill_resource_links_resolve(skill: str) -> None:
    """Every reference file a primary skill lists in its Resources table exists on disk."""
    skill_dir = SKILLS_DIR / skill
    links = _resource_links((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    assert links, f"{skill}: expected at least one references/ link"
    for target in links:
        assert (skill_dir / "references" / target).is_file(), (
            f"{skill}: broken Resources link references/{target}"
        )


def test_all_op_reference_files_have_valid_frontmatter() -> None:
    """Every op-*.md reference under the 5 skills parses + declares name + parent-skill."""
    op_files = [p for s in PRIMARY_SKILLS for p in (SKILLS_DIR / s / "references").glob("op-*.md")]
    assert op_files, "expected op-*.md reference files"
    for p in op_files:
        fm = _split_frontmatter(p.read_text(encoding="utf-8"))
        assert fm.get("name") == p.stem, f"{p.name}: name must equal the file stem"
        assert fm.get("parent-skill"), f"{p.name}: must declare parent-skill"


def test_m6_amcos_contradiction_resolved() -> None:
    """M6: the main agent treats AMCOS as a direct channel, not a 'never contact' title."""
    body = AGENT_FILE.read_text(encoding="utf-8")
    assert "Never contact**: AMAMA, AMCOS" not in body, "stale R6-v2 'never contact AMCOS' line present"
    assert "Direct channels" in body and "AMCOS" in body, "AMCOS must be a documented direct channel"


def test_m7c_pre_pr_gate_in_completion_flow() -> None:
    """M7c: op-notify-completion gates PR creation behind AMOA's green-light, no inline PR."""
    body = (SKILLS_DIR / "ampa-orchestrator-communication" / "references" / "op-notify-completion.md").read_text(encoding="utf-8")
    assert "Pre-PR gate" in body, "completion flow must contain the pre-PR gate step"
    assert "Only on green-light" in body, "PR creation must be gated on the green-light"
    assert "Create PR (if applicable)**: Open pull request" not in body, "stale inline-PR step still present"


def test_m7c_pr_creation_requires_greenlight() -> None:
    """M7c: op-create-pull-request requires the AMOA pre-PR green-light as a prerequisite."""
    body = (SKILLS_DIR / "ampa-github-operations" / "references" / "op-create-pull-request.md").read_text(encoding="utf-8")
    assert "green-light" in body.lower() and "pre-PR gate" in body, "PR op must require the green-light"


def test_m7a_handshake_replaces_bare_ack() -> None:
    """M7a: op-receive-task-assignment answers the comprehension handshake, not a bare ACK."""
    body = (SKILLS_DIR / "ampa-task-execution" / "references" / "op-receive-task-assignment.md").read_text(encoding="utf-8")
    assert "comprehension handshake" in body.lower(), "must reference the comprehension handshake"
    assert "HANDSHAKE:" in body, "must use the HANDSHAKE subject form"
    assert "Task received and validated. Beginning work." not in body, "bare ACK string still present"


def test_m13_dialog_loop_templates_exist() -> None:
    """M13: the comprehension-handshake and pre-PR-gate templates exist with valid frontmatter."""
    refs = SKILLS_DIR / "ampa-orchestrator-communication" / "references"
    for name in ("op-comprehension-handshake.md", "op-pre-pr-gate.md"):
        p = refs / name
        assert p.is_file(), f"missing template {name}"
        fm = _split_frontmatter(p.read_text(encoding="utf-8"))
        assert fm.get("name") == p.stem


def test_m10_g1_selfid_in_pr_and_bug_templates() -> None:
    """M10: the PR body and bug-report body templates begin with the G1.1 self-id line."""
    pr = (SKILLS_DIR / "ampa-github-operations" / "references" / "op-create-pull-request.md").read_text(encoding="utf-8")
    bug = (SKILLS_DIR / "ampa-handoff-management" / "references" / "op-write-bug-report.md").read_text(encoding="utf-8")
    needle = "This is the Claude responsible for the"
    assert needle in pr, "PR template missing the G1.1 self-id line"
    assert needle in bug, "bug-report template missing the G1.1 self-id line"


@pytest.mark.parametrize("rel", HANDOFF_TASKSTATE_REFS)
def test_m11_handoff_uses_v2_column(rel: str) -> None:
    """M11: handoff task-state frontmatter uses the v2 `column:` field, not the v1 status enum."""
    body = (REPO_ROOT / rel).read_text(encoding="utf-8")
    assert "column:" in body, f"{rel}: must use the v2 column: field"
    assert not re.search(r"status:\s*<?(backlog|pending|in_progress|review|completed)", body), (
        f"{rel}: stale v1 status enum present"
    )


def test_m4_kanban_skill_present_and_v3() -> None:
    """M4: the ampa-prrd-trdd-kanban skill exists, is R6-v3 correct, and wires the dialog loops."""
    p = SKILLS_DIR / "ampa-prrd-trdd-kanban" / "SKILL.md"
    assert p.is_file(), "kanban skill missing"
    body = p.read_text(encoding="utf-8")
    fm = _split_frontmatter(body)
    assert fm.get("name") == "ampa-prrd-trdd-kanban"
    assert "op-comprehension-handshake" in body and "op-pre-pr-gate" in body, "must wire both gates"
    assert "R6 v3" in body, "must state the R6 v3 direct-edge model"


def test_m2_m3_design_governance_bootstrap() -> None:
    """M2/M3: the 4-zone design/ folders + a real PRRD (project-id + golden & silver rules) exist."""
    for zone in ("proposals", "tasks", "refused", "archived"):
        assert (REPO_ROOT / "design" / zone).is_dir(), f"missing design/{zone}/"
    prrd = (REPO_ROOT / "design" / "requirements" / "PRRD.md").read_text(encoding="utf-8")
    assert "project-id: autonomous" in prrd, "PRRD must declare project-id"
    assert re.search(r"\*\*G\d+\.\d+\*\*", prrd), "PRRD must carry at least one GOLDEN rule"
    assert re.search(r"\*\*S\d+\.\d+\*\*", prrd), "PRRD SILVER must be non-empty (no ungoverned ops)"


def test_memory_protocol_path_is_scripts_memgrep() -> None:
    """Phase 3: the memory docs point at scripts/memgrep (janitor v0.7.0), not the old tools/ path."""
    proto = (REPO_ROOT / "rules" / "memory-protocol.md").read_text(encoding="utf-8")
    recall = (SKILLS_DIR / "programmer-memory-recall" / "SKILL.md").read_text(encoding="utf-8")
    assert "scripts/memgrep" in proto, "protocol must reference scripts/memgrep"
    assert "command -v memgrep" in proto, "protocol must keep the grep-fallback gate"
    assert "scripts/memgrep" in recall, "recall skill must reference scripts/memgrep"


def test_plugin_declares_tooling_dependency() -> None:
    """#17 item 9: plugin.json declares the ai-maestro-plugin dependency (pillar scripts)."""
    import json

    data = json.loads((REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert "ai-maestro-plugin" in data.get("dependencies", []), "must declare ai-maestro-plugin dependency"
