#!/usr/bin/env python3
"""Real governance-compliance tests — R23 frozen-CLI + R6.6/R37.1 MAESTRO model (no mocks).

These guard the two governance rules the MANAGER's verified audit (programmer-agent#20,
the R23 comment on #19, and the R6.6/R37.1 sweep on #21) applied to the MEMBER
persona + skills. They read the ACTUAL on-disk source — edit a skill/persona back
into a breach and the suite fails.

- **R23 (IRON, frozen-CLI decoupling).** No plugin element may call the ai-maestro
  SERVER API (`/api/*`) directly, nor instruct an agent to. Server access goes
  through the installed frozen CLI (`amp-*`, `aimaestro-*.sh`). The bright-line
  (R23.6) is an EXECUTABLE fetch (`curl/wget/… /api/`) or a `$AIMAESTRO_API/api/`
  shell expansion. Inert mentions of `/api/` — doc paths (`docs/api/auth.md`),
  example PR bodies (`GET /api/users/:id`), and the prohibition notes this very
  decoupling added — are allowed and must NOT trip the guard.
- **R6.6 / R37.1 (the MAESTRO model).** A MEMBER's escalation/approval chain tops
  out at the MAESTRO reached via AMCOS → MANAGER — never a generic "user" named as
  the authority. The PRRD Tier-3 `USER` label is a fixed contract token (governed
  by ~/.claude/rules/trdd-approval-tiers.md) and is intentionally EXEMPT — the
  last test guards that we did not over-zealously rename it.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DOCS_DIR = REPO_ROOT / "docs"
AGENT_FILE = REPO_ROOT / "agents" / "ai-maestro-programmer-agent-main-agent.md"

# An EXECUTABLE server-API call: a real fetch tool/library on the same line as a
# `/api/` path. Bare `http(s)://…/api/` prose URLs are deliberately NOT in the
# verb set, so inert example URLs/doc-paths don't false-positive (R23.6's line is
# "no direct call/instruction", not "no mention").
_LIVE_API = re.compile(
    r"\b(?:curl|wget|fetch|requests\.(?:get|post|put|patch|delete)|urllib|http\.client|axios|XMLHttpRequest)\b[^\n`]*?/api/"
)
# The exact shape both real violations used: the server base URL env var + /api/.
# Matches `$AIMAESTRO_API/api/…` and `${AIMAESTRO_API}/api/…`.
_ENV_API = re.compile(r"AIMAESTRO_API\}?/api/")

# Forbidden user-as-authority escalation phrases (R6.6/R37.1). Each was present
# before the #20/#21 sweep and is now repointed to "the MAESTRO (via AMCOS →
# MANAGER)" or to AMCOS directly. NOT a blanket ban on the word "user" — the
# standalone-mode operator prompts, AMAMA's user-interface function, and the
# persona's correct "never contact user directly in orchestrated mode" constraint
# are legitimate and stay.
_FORBIDDEN_USER_AUTHORITY = [
    "Request AMOA to escalate to user",
    "Send direct notification to user",
    "Escalate to user directly",
    "notify user directly",
    "report the messaging failure to the user",
    "ask the user for task details",
    "escalates to USER on crisis",
]


def _agent_facing_md() -> list[Path]:
    """Every markdown file on the agent-facing surface: skills/ + docs/ + the persona."""
    files = list(SKILLS_DIR.rglob("*.md")) + list(DOCS_DIR.rglob("*.md")) + [AGENT_FILE]
    return [p for p in files if p.is_file()]


def test_r23_no_live_api_calls_on_agent_surface() -> None:
    """R23.6 bright-line: zero executable `/api/` calls anywhere in skills/docs/persona."""
    offenders = []
    for p in _agent_facing_md():
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if _LIVE_API.search(line) or _ENV_API.search(line):
                offenders.append(f"{p.relative_to(REPO_ROOT)}:{i}: {line.strip()}")
    assert not offenders, "live server-/api/ calls violate R23:\n" + "\n".join(offenders)


def test_r23_c1_receive_task_uses_frozen_kanban_cli() -> None:
    """R23-C1: op-receive-task-assignment verifies the kanban via amp-kanban-list, not a curl."""
    body = (SKILLS_DIR / "ampa-task-execution" / "references" / "op-receive-task-assignment.md").read_text(encoding="utf-8")
    assert "amp-kanban-list" in body, "must repoint to the frozen amp-kanban-list CLI"
    assert not _LIVE_API.search(body) and not _ENV_API.search(body), "stale direct /api/ call still present"
    assert "if AI Maestro running" in body, "the checklist line must drop the '(if API available)' wording"


def test_r23_c2_handoff_uses_frozen_status_cli() -> None:
    """R23-C2: ampa-handoff-management resolves liveness via amp-status, not curl …/api/sessions."""
    body = (SKILLS_DIR / "ampa-handoff-management" / "SKILL.md").read_text(encoding="utf-8")
    assert "amp-status" in body, "must repoint the liveness check to the frozen amp-status CLI"
    assert "/api/sessions" not in body, "stale /api/sessions reference still present"


def test_r6_r37_no_user_as_authority_prose() -> None:
    """R6.6/R37.1: no MEMBER escalation/approval prose names the user as the top authority."""
    offenders = []
    for p in _agent_facing_md():
        text = p.read_text(encoding="utf-8")
        for phrase in _FORBIDDEN_USER_AUTHORITY:
            if phrase in text:
                offenders.append(f"{p.relative_to(REPO_ROOT)}: {phrase!r}")
    assert not offenders, "user-as-authority prose violates R6.6/R37.1:\n" + "\n".join(offenders)


def test_r37_escalation_chain_names_maestro() -> None:
    """R37.1: the swept escalation surfaces now name the MAESTRO as the top-of-chain authority."""
    must_carry_maestro = [
        AGENT_FILE,
        SKILLS_DIR / "ampa-orchestrator-communication" / "references" / "op-report-blocker.md",
        DOCS_DIR / "FULL_PROJECT_WORKFLOW.md",
        DOCS_DIR / "ROLE_BOUNDARIES.md",
    ]
    for p in must_carry_maestro:
        assert "MAESTRO" in p.read_text(encoding="utf-8"), f"{p.name}: must name the MAESTRO authority"


def test_r37_tier3_user_label_is_preserved() -> None:
    """M8 exempt: the PRRD Tier-3 `USER` contract label must survive the MAESTRO sweep untouched."""
    body = AGENT_FILE.read_text(encoding="utf-8")
    assert "Tier 3 — USER" in body, "the fixed PRRD Tier-3 USER label must NOT be renamed (ruling-2 exemption)"
