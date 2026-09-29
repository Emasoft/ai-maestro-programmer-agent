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

SCOPE of the citation/text-hash gates (pinned-citation, rule-text hash): a green
run asserts citations and rule VERSIONS only. Container-level stamps
(`prrd-version:`, `updated:`) have no citation pointing at them and are invisible
to these gates by construction — they need their own independent witness
(tracked upstream on ai-maestro#145).
"""

from __future__ import annotations

import hashlib
import json
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


def _prrd_rule_versions() -> dict[str, str]:
    """Map every PRRD rule NUMBER to its current version, from the rule definitions.

    A definition looks like `- **G1.2** — …` or `- **S64.134** — …`. The number is
    globally unique across G/S, and promote/demote flips only the letter, so the
    number alone is the stable key.
    """
    prrd = (REPO_ROOT / "design" / "requirements" / "PRRD.md").read_text(encoding="utf-8")
    return {n: v for n, v in re.findall(r"^- \*\*[GS](\d+)\.(\d+)\*\* —", prrd, re.M)}


# A PINNED citation: letter + number + version, e.g. `G1.2` / `PRRD S64.134`. The
# floating form (`G1`, no version) is deliberately NOT matched — it means
# "whatever rule 1 says now" and cannot dangle.
_PINNED_CITATION = re.compile(r"\b([GS])(\d+)\.(\d+)\b")

# Terminal TRDD columns. A card in one of these is FROZEN and its citations are a
# historical record of the rule as it stood — renumbering them would make them lie.
_TERMINAL_COLUMNS = {"complete", "completed", "failed", "superseded", "published", "live", "cancelled", "refused"}


def _is_frozen_trdd(path: Path) -> bool:
    if path.suffix != ".md" or "design" not in path.parts:
        return False
    m = re.search(r"^column:\s*(\S+)\s*$", path.read_text(encoding="utf-8"), re.M)
    return bool(m and m.group(1) in _TERMINAL_COLUMNS)


# The narration/grammar-example exemption classes from the ratified RP-CITATION
# spec are deliberately UNIMPLEMENTED here, per the spec's own tiebreak: take the
# checker that misses a real dangle over one that reds on a grammar example.


def test_pinned_prrd_citations_resolve_to_a_live_rule_version() -> None:
    """Every version-pinned `PRRD G<n>.<v>` citation in living prose must still resolve.

    Editing a rule's text bumps its version (`G1.1` → `G1.2`), and the number —
    not the version — is what is stable. So every citation that PINS a version
    silently dangles the moment the rule is edited: grep the pinned form in the
    PRRD afterwards and you find nothing, with no hint the two are the same rule.

    That is exactly what happened here. The G1.1 → G1.2 bump left 14 pinned
    citations across skills, docs and tests pointing at a version that no longer
    existed, and the whole suite stayed green — no lint, no test, and no plugin
    validator checks citation integrity. This test is that missing check.

    Frozen TRDDs are exempt by design: a terminal card records the rule as it
    stood when the work was done, so renumbering its citations would make it lie.
    """
    live = _prrd_rule_versions()
    assert live, "parsed no rules from the PRRD — the definition format has drifted"

    # `.py` is scanned too: the first version of this guard globbed *.md only,
    # so a stale citation in a docstring — where several of them actually live —
    # was invisible to it.
    #
    # THIS FILE excludes itself, permanently and by necessity, not by oversight:
    # a detector that documents the defect must quote the defect's own triggers
    # (`G1.1` → `G1.2` appears in the docstrings above), and its negative-control
    # fixtures must contain the thing it detects. Excluding only itself is the
    # smallest exclusion that resolves the self-reference, and a stated hole
    # beats a hidden one. Credit: the ORCHESTRATOR role-plugin hit this in its
    # own implementation and documented it.
    scanned = [
        p
        for d in ("skills", "docs", "agents", "tests", "design")
        for pattern in ("*.md", "*.py")
        for p in (REPO_ROOT / d).rglob(pattern)
        if not _is_frozen_trdd(p) and p.resolve() != Path(__file__).resolve()
    ] + [REPO_ROOT / "README.md", REPO_ROOT / "CLAUDE.md"]
    # Non-vacuity: a silently-empty corpus (glob drift, renamed dirs) must fail
    # here, not pass an empty scan as green.
    assert scanned, f"citation scan found no files to scan ({len(scanned)} scanned) — corpus glob has drifted"

    dangling: list[str] = []
    for path in scanned:
        for i, line in _prose_lines(path.read_text(encoding="utf-8")):
            for letter, number, version in _PINNED_CITATION.findall(line):
                if number not in live:
                    dangling.append(f"{path.relative_to(REPO_ROOT)}:{i}: {letter}{number}.{version} — no rule {number}")
                elif live[number] != version:
                    dangling.append(
                        f"{path.relative_to(REPO_ROOT)}:{i}: {letter}{number}.{version} — rule {number} is now at .{live[number]}"
                    )
    assert not dangling, (
        "version-pinned PRRD citations that no longer resolve — use the floating form "
        "`G<n>` when the claim is not about a specific revision: " + "; ".join(dangling)
    )


def _prrd_rule_bodies() -> dict[str, str]:
    """Map every PRRD rule's full citation (`G1.2`) to its WHOLE rule text, whitespace-normalized.

    Two things here are load-bearing, and the first version of this function got
    both wrong in a way that is worth keeping written down.

    **Capture the whole block, not one line.** `(.*)$` under `re.M` stops at the
    first newline, so a rule wrapped across lines was silently truncated to its
    first line — and an edit to any CONTINUATION line then hashed identically to
    the original. The guard would have passed while the rule's meaning changed,
    which is precisely the defect it exists to catch, reproduced inside the guard
    itself. That is a silent under-coverage: strictly worse than a false alarm,
    because nothing ever tells you it stopped covering.

    **Normalize whitespace before hashing.** A reflow is not a revision. Failing
    on one teaches the author to regenerate the fixture without reading it, which
    is the single move that turns this guard back into decoration. Credit for this
    half: the ORCHESTRATOR role-plugin, which hit it first.
    """
    return _parse_rule_bodies((REPO_ROOT / "design" / "requirements" / "PRRD.md").read_text(encoding="utf-8"))


def _parse_rule_bodies(prrd: str) -> dict[str, str]:
    """The parser, taking TEXT so the controls below can feed it synthetic input.

    Split out deliberately: the controls must not mutate the real PRRD on disk.
    An earlier round of these ran as throwaway scripts that edited the file and
    restored it in a `finally` — which corrupts the repo if the run is
    interrupted, and proves nothing once the script exits.
    """
    out: dict[str, str] = {}
    # A rule runs from its own bullet to the next rule bullet, the next heading, or EOF.
    for m in re.finditer(
        r"^- \*\*([GS])(\d+)\.(\d+)\*\* — (.*?)(?=^- \*\*[GS]\d+\.\d+\*\*|^#|\Z)",
        prrd,
        re.M | re.S,
    ):
        letter, number, version, body = m.groups()
        out[f"{letter}{number}.{version}"] = " ".join(body.split())
    return out


# --- Negative controls for the guards above -------------------------------
#
# A guard that has only ever PASSED is a guard nobody has tested. These prove
# each guard can still FAIL, and they are committed rather than run once by hand
# — a control that ran during development and was not kept is a demo, not a
# control: the repo cannot tell a working guard from a broken one without them.
#
# Control C is the one that keeps A and B honest. A and B pass under the correct
# parser AND under a hypothetical parser that never had the property, if the
# fixture stops exercising it. C asserts the fixture can still TELL THE TWO
# APART, so it fails the moment the fixture drifts to something undiscriminating.
# Credit: the ORCHESTRATOR role-plugin, which found this gap in its own controls.
#
# Control D (naive parser installed end-to-end) was PERFORMED AND OBSERVED, not
# committed: with `_broken_bodies` swapped in as the live parser, A and C went
# red (3 failed) on the committed _FIXTURE_WRAPPED/_FIXTURE_TAIL_EDIT inputs,
# measured at commit 2445f63. It is deliberately not a committed test because
# installing the broken parser makes the suite red by construction.

_BROKEN_PARSER = re.compile(r"^- \*\*([GS])(\d+)\.(\d+)\*\* — (.*)$", re.M)

_FIXTURE_ONE_LINE = "- **S9.1** — Alpha beta gamma delta epsilon zeta.\n"
_FIXTURE_WRAPPED = "- **S9.1** — Alpha beta gamma\n  delta epsilon zeta.\n"
_FIXTURE_TAIL_EDIT = "- **S9.1** — Alpha beta gamma\n  delta epsilon OMEGA.\n"


def _broken_bodies(prrd: str) -> dict[str, str]:
    """The naive parser this guard used to have — kept ONLY as control C's baseline."""
    return {f"{letter}{n}.{v}": " ".join(body.split()) for letter, n, v, body in _BROKEN_PARSER.findall(prrd)}


def test_control_a_edit_on_a_continuation_line_is_detected() -> None:
    """A: a word changed on a rule's SECOND line must change its hash (no silent under-coverage)."""
    assert _parse_rule_bodies(_FIXTURE_WRAPPED)["S9.1"] != _parse_rule_bodies(_FIXTURE_TAIL_EDIT)["S9.1"], (
        "a continuation-line edit hashed identically — the parser is truncating at the first newline, "
        "so the guard passes while a rule's meaning changes"
    )


def test_control_b_a_pure_reflow_is_not_a_revision() -> None:
    """B: rewrapping a rule with no wording change must NOT change its hash (no false positive)."""
    assert _parse_rule_bodies(_FIXTURE_ONE_LINE)["S9.1"] == _parse_rule_bodies(_FIXTURE_WRAPPED)["S9.1"], (
        "a pure reflow changed the hash — that trains authors to regenerate the fixture without "
        "reading it, which turns this guard back into decoration"
    )


def test_control_c_the_fixture_still_discriminates_the_broken_parser() -> None:
    """C: the fixture must still tell the correct parser from the naive one.

    Without this, A and B keep passing even if the fixture is simplified to a
    single line — at which point they prove the parser behaves, not that the
    multi-line property is WHY it behaves. A control that cannot distinguish the
    fixed implementation from the broken one is not a control.
    """
    assert _broken_bodies(_FIXTURE_WRAPPED)["S9.1"] == _broken_bodies(_FIXTURE_TAIL_EDIT)["S9.1"], (
        "the fixture no longer exercises the truncation bug — the naive parser now detects the "
        "continuation-line edit too, so A and B are no longer testing the property they claim to"
    )
    assert _parse_rule_bodies(_FIXTURE_WRAPPED)["S9.1"] != _broken_bodies(_FIXTURE_WRAPPED)["S9.1"], (
        "the correct and naive parsers agree on this fixture — it cannot discriminate them"
    )


def test_control_the_paging_handle_detector_can_still_fire() -> None:
    """The `@handle` guard must catch a handle in prose, and must NOT fire inside code.

    Both halves matter and pull opposite ways: a detector that fires on
    `@eslint/js` in a fence gets suppressed by the next author, and one that
    misses a bare handle in prose is why this repo shipped `@owner` in a template.
    """
    prose = _prose_lines("Posted by the Claude developing X (via the shared @owner gh auth).")
    assert any(_PAGING_HANDLE.search(line) for _, line in prose), "must catch a bare @handle in prose"

    for inert in ("Install `@eslint/js` now.", "```\n@pytest.fixture\n```", "See @types/node here.", "mail x@y.com"):
        assert not any(_PAGING_HANDLE.search(line) for _, line in _prose_lines(inert)), (
            f"false positive on inert text: {inert!r} — a guard that reddens on correct writing gets deleted"
        )


def test_control_prose_lines_keeps_line_numbers_accurate() -> None:
    """Blanking code must preserve line numbers — a guard that misreports the line misdirects.

    The first version of this helper DELETED fenced blocks, which shifted every
    later line number: it reported a real finding at line 160 for a problem on
    line 165, sending the reader to innocent text.
    """
    doc = "prose one\n```\nfenced @handle\n```\nprose @target here\n"
    hits = [i for i, line in _prose_lines(doc) if "@target" in line]
    assert hits == [5], f"expected the finding at line 5, got {hits}"
    assert not any("@handle" in line for _, line in _prose_lines(doc)), "fenced content must be blanked, not scanned"


def test_prrd_rule_text_matches_its_declared_version() -> None:
    """A rule's TEXT may not change without its version moving.

    The inverse of the dangling-citation defect, and strictly worse. A stale
    pointer announces itself the first time someone looks it up and finds
    nothing. A pointer to silently-MUTATED content never announces itself at
    all: edit a rule's text and skip the version bump, and every existing
    `G1.1` citation still resolves perfectly — to text that changed underneath
    it. The version is a machine-readable claim about the text; nothing was
    checking that the claim stayed true.

    Reported by the ORCHESTRATOR role-plugin, which hit exactly this while
    making the same byline fix and shipped the mirror of it.

    On a legitimate edit the fix is TWO steps, and the failure message gives
    both: bump the version in the PRRD, then update this fixture (the printed
    hash is copy-pasteable). The bookkeeping is one line, on a line the author
    is already editing to bump the version.
    """
    fixture_path = REPO_ROOT / "tests" / "prrd-rule-text-hashes.json"
    pinned = json.loads(fixture_path.read_text(encoding="utf-8"))
    live = {k: hashlib.sha256(v.encode()).hexdigest()[:16] for k, v in _prrd_rule_bodies().items()}

    mutated = [
        f"{cite}: text changed but the version did not — bump it in the PRRD, then set this "
        f"fixture entry to {h}"
        for cite, h in live.items()
        if cite in pinned and pinned[cite] != h
    ]
    unpinned = [f'{cite}: new or renumbered — add "{cite}": "{h}" to the fixture' for cite, h in live.items() if cite not in pinned]
    removed = [f"{cite}: in the fixture but no longer in the PRRD — drop it" for cite in pinned if cite not in live]

    assert not (mutated + unpinned + removed), "PRRD rule text / version drift:\n  " + "\n  ".join(
        mutated + unpinned + removed
    )


def _prose_lines(text: str) -> list[tuple[int, str]]:
    """Yield (1-based line number, prose-only line), blanking code rather than deleting it.

    Fenced blocks and inline code spans are blanked IN PLACE instead of stripped,
    because deleting them shifts every following line number and a guard that
    reports the wrong line sends its reader to innocent code — a small version of
    the same silent-misdirection the guards exist to prevent.

    Blanking matters because `@` and rule-shaped tokens are inert inside a code
    span and routine inside a fence (`@eslint/js`, `@pytest.fixture`,
    `--author "@me"`), so only bare prose is ever checked.
    """
    out: list[tuple[int, str]] = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append((i, ""))
            continue
        out.append((i, "" if in_fence else re.sub(r"`[^`\n]*`", "", line)))
    return out


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
        for i, line in _prose_lines(path.read_text(encoding="utf-8")):
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
