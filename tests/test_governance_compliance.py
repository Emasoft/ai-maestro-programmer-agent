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


def test_r23_c3_start_work_uses_frozen_kanban_move() -> None:
    """R23-C3: op-implement-code reflects start-of-work via amp-kanban-move in_progress, not a curl."""
    body = (SKILLS_DIR / "ampa-task-execution" / "references" / "op-implement-code.md").read_text(encoding="utf-8")
    assert "amp-kanban-move" in body, "must repoint the start transition to the frozen amp-kanban-move CLI"
    assert "in_progress" in body, "the start transition must target the in_progress column"
    assert not _LIVE_API.search(body) and not _ENV_API.search(body), "stale direct /api/ call still present"


def test_r23_c4_submit_for_review_uses_frozen_submit_pr_and_move() -> None:
    """R23-C4: PR submit uses amp-submit-pr; the review move uses amp-kanban-move ai_review — no curl."""
    pr_body = (SKILLS_DIR / "ampa-github-operations" / "references" / "op-create-pull-request.md").read_text(encoding="utf-8")
    notify_body = (SKILLS_DIR / "ampa-orchestrator-communication" / "references" / "op-notify-completion.md").read_text(encoding="utf-8")
    assert "amp-submit-pr" in pr_body, "the PR submit must offer the frozen amp-submit-pr CLI"
    assert "amp-kanban-move" in notify_body, "the review transition must use the frozen amp-kanban-move CLI"
    assert "ai_review" in notify_body, "the review transition must target the ai_review column"
    assert not _LIVE_API.search(pr_body) and not _ENV_API.search(pr_body), "stale direct /api/ call in PR op"
    assert not _LIVE_API.search(notify_body) and not _ENV_API.search(notify_body), "stale direct /api/ call in notify op"


def test_r23_c5_blocked_uses_frozen_task_blocked() -> None:
    """R23-C5: op-report-blocker reflects the block via amp-task-blocked, not a curl …/api/."""
    body = (SKILLS_DIR / "ampa-orchestrator-communication" / "references" / "op-report-blocker.md").read_text(encoding="utf-8")
    assert "amp-task-blocked" in body, "must repoint the blocked transition to the frozen amp-task-blocked CLI"
    assert not _LIVE_API.search(body) and not _ENV_API.search(body), "stale direct /api/ call still present"


def test_r23_c6_done_uses_frozen_task_done() -> None:
    """R23-C6: op-notify-completion records terminal completion via amp-task-done, not a curl …/api/."""
    body = (SKILLS_DIR / "ampa-orchestrator-communication" / "references" / "op-notify-completion.md").read_text(encoding="utf-8")
    assert "amp-task-done" in body, "must repoint the done transition to the frozen amp-task-done CLI"
    assert not _LIVE_API.search(body) and not _ENV_API.search(body), "stale direct /api/ call still present"


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


def _prose_only(text: str) -> str:
    """Strip fenced code blocks and inline code spans, leaving prose an agent would paste.

    `@` is inert inside a code span and routine inside a fence (npm scopes like
    `@eslint/js`, decorators like `@pytest.fixture`, `gh pr list --author "@me"`).
    Only bare prose can page a real account, so only bare prose is checked.
    """
    text = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)  # fenced blocks
    text = re.sub(r"`[^`\n]*`", "", text)  # inline code spans
    return text


# A handle that PAGES: `@name` at a word boundary, not followed by `/`. Measured
# behaviour (gh api markdown): `@foo-bar` and `(@foo)` page; `@types/node` and
# `x@foo` do not. An address does not page its domain, but is PII — also excluded
# here only because the pattern requires a non-word char before the `@`.
_PAGING_HANDLE = re.compile(r"(?<![\w.@-])@[A-Za-z][A-Za-z0-9-]*(?![\w./-])")

# Files whose prose is copied verbatim into GitHub bodies (templates, personas,
# the rule that defines the byline). These are the ones where a bare handle is a
# live hazard rather than incidental text.
_GITHUB_PROSE_FILES = [
    REPO_ROOT / "design" / "requirements" / "PRRD.md",
    AGENT_FILE,
    SKILLS_DIR / "ampa-github-operations" / "references" / "op-create-pull-request.md",
    SKILLS_DIR / "ampa-github-operations" / "references" / "op-respond-to-review.md",
    SKILLS_DIR / "ampa-handoff-management" / "references" / "op-write-bug-report.md",
]


def test_g1_byline_template_carries_no_paging_handle() -> None:
    """PRRD G1.x and every GitHub-body template must carry NO bare `@handle` in prose.

    The self-id byline names the owner in PLAIN WORDS; the `@` only adds a
    notification. A template is the dangerous case precisely because it is COPIED
    OUT of any code span and pasted as finished prose — so backticking is not the
    fix, removing the character is. This repo shipped `@owner` in the G1.1 template
    (reported 2026-08-08), which would page a real organization for any agent that
    used the template as written.

    The guard is scoped to the files whose prose reaches GitHub, and it ignores
    fenced blocks and inline code, where `@` is both inert and routine
    (`@eslint/js`, `@pytest.fixture`, `--author "@me"`).
    """
    offenders: list[str] = []
    for path in _GITHUB_PROSE_FILES:
        assert path.is_file(), f"{path} is missing — the guard's file list has drifted"
        for i, line in enumerate(_prose_only(path.read_text(encoding="utf-8")).splitlines(), 1):
            for m in _PAGING_HANDLE.finditer(line):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{i}: {m.group(0)}")
    assert not offenders, (
        "bare @handle in GitHub-bound prose — it pages a real account when pasted: "
        + "; ".join(offenders)
    )


def test_rp_skill_menu_01_menu_covers_every_shipped_skill() -> None:
    """RP-SKILL-MENU-01: the persona body carries one menu row per shipped skill.

    role-plugins-spec 1.1.0 (TRDD-0FCR6KOW) requires every role-plugin MAIN agent
    whose plugin ships skills to carry a compact skill menu — the skill name plus
    when to reach for it — because skill *descriptions* alone under-trigger for
    role-specific procedures: an agent that cannot SEE its inventory does not reach
    for it.

    THE GUARD IS THE POINT, not the menu. The spec states plainly that a STALE menu
    is worse than none, and asks that a publish gate compare menu entries against the
    shipped SKILL.md count. Without this test, adding a 7th skill leaves a 6-row menu
    that reads as complete and silently hides the new skill from the agent — the same
    silent-omission failure as the preload-exclusion defect that motivated the rule.
    """
    shipped = sorted(p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").is_file())
    assert shipped, "no skills found — check SKILLS_DIR"
    body = AGENT_FILE.read_text(encoding="utf-8")
    # A menu row is a markdown table row that names the skill in backticks. Counting
    # rows (not bare mentions) is deliberate: prose elsewhere in the persona mentions
    # several skills, and those must not be able to satisfy the menu requirement.
    rows = {s: len(re.findall(rf"^\|.*`{re.escape(s)}`", body, re.M)) for s in shipped}
    missing = [s for s, n in rows.items() if n == 0]
    assert not missing, f"RP-SKILL-MENU-01: no menu row for {missing} — the agent cannot see them"
    duplicated = [s for s, n in rows.items() if n > 1]
    assert not duplicated, f"RP-SKILL-MENU-01: {duplicated} appear in more than one menu row (ambiguous)"
