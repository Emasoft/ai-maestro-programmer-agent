#!/usr/bin/env python3
"""Real contract tests for the 5 primary AMPA skills + the #17 alignment (no mocks).

The 5 primary skills (task-execution, orchestrator-communication,
github-operations, project-setup, handoff-management) shipped with zero tests
(audit #17 M12). These tests read the ACTUAL skill + reference files on disk and
assert their structural contract and the behaviours the fleet-readiness
alignment (#17) put in place: valid frontmatter, resolvable reference links,
the M5 governance block, the M6 R6-v3 fix, the M7 dialog-loop gates, the M10
G1 self-id, the M11 v2 `column:` migration, and the M2/M3/M4 governance
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

# Single source of truth for the core granular pillar skills AMPA wires (verified
# present in installed ai-maestro-plugin >=2.7). The MEMBER-policy skill
# (ampa-prrd-trdd-kanban) must enumerate every one; a typo here or there recreates
# the dead-wiring bug with tests green around the wrong string, so both sides read
# THIS list. (Emasoft/ai-maestro#61 Q1/Q2, TRDD-I8AH88SS.)
GRANULAR_PILLAR_SKILLS = [
    "ama-prrd-get", "ama-prrd-find", "ama-prrd-propose", "ama-prrd-edit",
    "ama-trdd-write", "ama-trdd-update", "ama-trdd-transition", "ama-trdd-find",
    "ama-kanban-render", "ama-proposal-approvals",
]
POLICY_SKILL = "ampa-prrd-trdd-kanban"


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
    """M5: each primary skill's Governance block cites the min-approval-requirement ladder,
    the MEMBER-policy skill, the granular ama-* mechanics, and the never-self-approve line.

    Migrated from the deprecated `approval-tier:` / dead `prrd-trdd-kanban` wiring to the
    granular core skills + min-approval-requirement (Emasoft/ai-maestro#61, TRDD-I8AH88SS).
    """
    body = (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
    assert "## Governance" in body, f"{skill}: missing ## Governance section"
    assert "min-approval-requirement" in body, (
        f"{skill}: must reference the min-approval-requirement ladder (approval-tier is deprecated)"
    )
    assert POLICY_SKILL in body, f"{skill}: must cite the {POLICY_SKILL} MEMBER-policy skill"
    assert "ama-*" in body, f"{skill}: must reference the granular ama-* pillar mechanics"
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


def test_agent_pins_no_model_inherits_session() -> None:
    """Agent frontmatter pins NO `model:` — it inherits the session model.

    The README documents (twice) that AMPA pins no model/effort and inherits
    the session's, and CPV CA-04 (cache warmth) requires it: a frontmatter
    model pin runs the agent on a fixed model regardless of the session,
    breaking prompt-cache warmth and overriding the operator's `/model` choice.
    CC v2.1.183 additionally surfaces a deprecation warning for any model
    pinned in agent frontmatter. A `model: opus` line previously drifted in and
    contradicted all three (fixed in v1.4.1) — this guard stops it recurring.
    The dispatch site may still pass `model:` at Agent() call time when Opus
    power is wanted.
    """
    fm = _split_frontmatter(AGENT_FILE.read_text(encoding="utf-8"))
    assert "model" not in fm, (
        "agent must NOT pin `model:` in frontmatter — it inherits the session "
        "model (README 'pins no model'; CPV CA-04 cache warmth; CC v2.1.183 "
        "flags frontmatter model pins). Pass model at Agent() call time instead."
    )


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


def test_m10_g1_selfid_on_every_github_posting_path() -> None:
    """M10: every GitHub-posting op body carries the G1 self-id line (PR, bug-report, review reply).

    All AI Maestro agents share ONE human-owner GitHub identity, so every body posted to
    GitHub must open with the self-id line naming the authoring agent — otherwise a review
    reply (or any comment) posts under the shared identity with no attribution. TRDD-W5WYY2VF.
    """
    needle = "This is the Claude responsible for the"
    ghops = SKILLS_DIR / "ampa-github-operations" / "references"
    posting_paths = {
        "PR body": ghops / "op-create-pull-request.md",
        "bug-report body": SKILLS_DIR / "ampa-handoff-management" / "references" / "op-write-bug-report.md",
        "PR-review-comment body": ghops / "op-respond-to-review.md",
    }
    for label, path in posting_paths.items():
        assert needle in path.read_text(encoding="utf-8"), f"{label} missing the G1 self-id line"


def test_m10b_agent_trailer_documented_in_commit_convention() -> None:
    """M10b: the commit convention documents the `Agent:` trailer the fleet commits carry.

    commit-discipline.md + PRRD G1 ask every commit to carry `Agent: <plugin-slug>`; the
    agent's own commit manual must document it, not just the PR/issue paths. TRDD-W5WYY2VF.
    """
    commit_doc = (SKILLS_DIR / "ampa-github-operations" / "references" / "op-commit-changes.md").read_text(encoding="utf-8")
    assert "Agent:" in commit_doc, "op-commit-changes must document the `Agent:` commit trailer"


@pytest.mark.parametrize("rel", HANDOFF_TASKSTATE_REFS)
def test_m11_handoff_uses_v2_column(rel: str) -> None:
    """M11: handoff task-state frontmatter uses the v2 `column:` field, not the v1 status enum."""
    body = (REPO_ROOT / rel).read_text(encoding="utf-8")
    assert "column:" in body, f"{rel}: must use the v2 column: field"
    assert not re.search(r"status:\s*<?(backlog|pending|in_progress|review|completed)", body), (
        f"{rel}: stale v1 status enum present"
    )


def test_m4_kanban_skill_present_and_v3() -> None:
    """M4: the MEMBER-policy skill exists, is R6-v3 correct, wires both dialog loops, and carries
    the repurposed policy (self-mandate + min-approval-requirement) — not the dead passthrough.

    Adapted for the granular rewire (TRDD-I8AH88SS): the skill is now the MEMBER-policy layer
    over the core granular ama-* mechanics, so it must state the self-mandate rule and the
    min-approval-requirement vocab, and must NOT still defer to the removed core skill.
    """
    p = SKILLS_DIR / POLICY_SKILL / "SKILL.md"
    assert p.is_file(), "policy skill missing"
    body = p.read_text(encoding="utf-8")
    fm = _split_frontmatter(body)
    assert fm.get("name") == POLICY_SKILL
    assert "op-comprehension-handshake" in body and "op-pre-pr-gate" in body, "must wire both gates"
    assert "R6 v3" in body, "must state the R6 v3 direct-edge model"
    assert "self-mandate" in body.lower(), "must carry the self-mandate rule"
    assert "min-approval-requirement" in body, "must use the min-approval-requirement vocab"
    assert "Requires the universal prrd-trdd-kanban" not in body, (
        "must not still defer to the removed core prrd-trdd-kanban skill (passthrough)"
    )


def test_policy_skill_enumerates_granular_pillars() -> None:
    """The MEMBER-policy skill is the single source that cites EVERY granular ama-* pillar skill.

    The dead-wiring bug (Emasoft/ai-maestro#61) happened because a per-plugin wrapper deferred
    to a core skill that was later renamed. Pinning the policy skill against the canonical
    GRANULAR_PILLAR_SKILLS list means a future core rename or a citation typo fails HERE
    (loudly) instead of silently resolving to nothing again. TRDD-I8AH88SS.
    """
    body = (SKILLS_DIR / POLICY_SKILL / "SKILL.md").read_text(encoding="utf-8")
    missing = [g for g in GRANULAR_PILLAR_SKILLS if g not in body]
    assert not missing, f"{POLICY_SKILL} must cite every granular pillar skill; missing: {missing}"
    assert "op-report-missing-derived-trdd" in body, (
        "policy skill must wire the missing-derived-TRDD duty op"
    )


def test_m2_m3_design_governance_bootstrap() -> None:
    """M2/M3: the 4-zone design/ folders + a real PRRD (project-id + golden & silver rules) exist."""
    for zone in ("proposals", "tasks", "refused", "archived"):
        assert (REPO_ROOT / "design" / zone).is_dir(), f"missing design/{zone}/"
    prrd = (REPO_ROOT / "design" / "requirements" / "PRRD.md").read_text(encoding="utf-8")
    assert "project-id: autonomous" in prrd, "PRRD must declare project-id"
    assert re.search(r"\*\*G\d+\.\d+\*\*", prrd), "PRRD must carry at least one GOLDEN rule"
    assert re.search(r"\*\*S\d+\.\d+\*\*", prrd), "PRRD SILVER must be non-empty (no ungoverned ops)"


def test_memory_is_global_janitor_not_per_plugin() -> None:
    """#18: per-plugin memory skills/rule are removed; CLAUDE.md carries the global janitor contract."""
    assert not (SKILLS_DIR / "programmer-memory-recall").exists(), "per-plugin recall skill must be removed"
    assert not (SKILLS_DIR / "programmer-memory-write").exists(), "per-plugin write skill must be removed"
    assert not (REPO_ROOT / "rules" / "memory-protocol.md").exists(), "per-plugin memory-protocol rule must be removed"
    claude_md = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    assert "janitor-memory-recall" in claude_md, "CLAUDE.md must point at the global recall skill"
    assert "RECALL BEFORE ACTING" in claude_md, "CLAUDE.md must carry the proactive recall contract"
    assert "SCOPE ROUTING" in claude_md, "CLAUDE.md must document the 3-scope routing"
    proj_mem = REPO_ROOT / ".claude" / "project" / "memory"
    assert (proj_mem / "MEMORY.md").is_file(), "PROJECT memory index missing"
    assert (proj_mem / "architecture.md").is_file(), "PROJECT architecture hub missing"


def test_plugin_declares_tooling_dependency() -> None:
    """#17 item 9: plugin.json declares the ai-maestro-plugin dependency (pillar scripts)."""
    import json

    data = json.loads((REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    # dependencies may be plain strings or {name, version} objects — accept both.
    names = [d if isinstance(d, str) else d.get("name") for d in data.get("dependencies", [])]
    assert "ai-maestro-plugin" in names, "must declare ai-maestro-plugin dependency"
    # the dependency must carry a version constraint (CPV: avoid auto-tracking latest)
    versioned = [d for d in data.get("dependencies", []) if isinstance(d, dict) and d.get("name") == "ai-maestro-plugin"]
    assert versioned and versioned[0].get("version"), "ai-maestro-plugin dependency must be version-pinned"


# --------------------------------------------------------------------------
# Claude Code platform-contract guards (TRDD-6QJ4W1MZ).
#
# Two Claude Code changes silently altered how this plugin EXECUTES, with no
# error and no warning. Both were invisible to lint and to every test above,
# because both are frontmatter semantics rather than file structure. These
# guards exist so the NEXT such change fails here instead of in production.
# --------------------------------------------------------------------------

ALL_SKILLS = sorted(p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").is_file())


@pytest.mark.parametrize("skill", ALL_SKILLS)
def test_skill_does_not_fork_amp_coupled_procedure(skill: str) -> None:
    """No ampa-* skill may use `context: fork` — every one is an AMP/session-coupled procedure.

    WHY THIS IS AN ASSERTION AND NOT A COMMENT: Claude Code v2.1.218 flipped
    `context: fork` skills to run in the BACKGROUND by default, so a forked
    skill returns an agent handle and its text arrives later as a task
    notification — the invoking agent gets NOTHING in the turn it asked, with
    no error raised. All six ampa-* skills carried `context: fork` and hit
    exactly that.

    Pinning `background: false` would have papered over a deeper defect: a
    forked subagent has NO AMP identity (stated in the agent definition
    itself), yet every ampa-* skill's procedure requires reading or sending
    AMP messages in the invoking session — receiving the assignment, running
    the comprehension handshake, reporting completion. A fork can therefore
    never COMPLETE one of these procedures, foreground or background. On top
    of that, `agent:` named this same agent, making each invocation a
    self-recursive fork against the depth cap.

    The fix was to remove `context: fork` and `agent:` outright so the
    procedures run inline. Re-adding either re-breaks AMP silently.
    """
    fm = _split_frontmatter((SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8"))
    assert "context" not in fm, (
        f"{skill}: must not set `context:` — ampa-* procedures are AMP/session-coupled and "
        "run inline; a forked subagent has no AMP identity and cannot complete them"
    )
    assert "agent" not in fm, (
        f"{skill}: must not set `agent:` — it is only meaningful with `context: fork`, and it "
        "named this same agent (a self-recursive fork)"
    )


@pytest.mark.parametrize("skill", ALL_SKILLS)
def test_preloaded_skill_is_not_blocked_from_preload(skill: str) -> None:
    """A skill listed in the agent's `skills:` preload must not set `disable-model-invocation`.

    Claude Code excludes `disable-model-invocation: true` skills from subagent
    preloading ("preloading draws from the same set of skills Claude can
    invoke"). All six skills set it while the agent's `skills:` field listed
    all six — so the preload was inert and the role agent booted WITHOUT its
    own operating procedures in context. Silent: no error, no warning, and the
    agent body still instructed itself to use them.
    """
    agent_fm = _split_frontmatter(AGENT_FILE.read_text(encoding="utf-8"))
    preloaded = set(agent_fm.get("skills") or [])
    fm = _split_frontmatter((SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8"))
    if skill in preloaded:
        assert not fm.get("disable-model-invocation"), (
            f"{skill}: is in the agent's `skills:` preload list, so `disable-model-invocation: "
            "true` makes that preload silently inert — drop one or the other"
        )


def test_agent_and_skill_names_carry_no_colon() -> None:
    """`:` is reserved for plugin namespacing; since v2.1.218 a name containing it is REJECTED.

    Claude Code does not load such a file and logs the error only to the debug
    log — so a bad rename would remove the agent from the fleet with no visible
    failure anywhere an operator would look.
    """
    agent_name = str(_split_frontmatter(AGENT_FILE.read_text(encoding="utf-8")).get("name", ""))
    assert ":" not in agent_name, f"agent name {agent_name!r} must not contain ':'"
    for skill in ALL_SKILLS:
        fm = _split_frontmatter((SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8"))
        assert ":" not in str(fm.get("name", "")), f"{skill}: skill name must not contain ':'"


def test_agent_preload_list_matches_shipped_skills() -> None:
    """Every skill the agent preloads must exist on disk — a typo yields a silent no-op.

    The `skills:` field is resolved by name; an entry that matches nothing is
    dropped without an error, which is the same failure mode as the inert
    preload above but caused by a rename instead of a frontmatter key.
    """
    agent_fm = _split_frontmatter(AGENT_FILE.read_text(encoding="utf-8"))
    preloaded = list(agent_fm.get("skills") or [])
    assert preloaded, "agent must declare its operating procedures in `skills:`"
    missing = [s for s in preloaded if s not in ALL_SKILLS]
    assert not missing, f"agent `skills:` names skills that do not exist: {missing}"


# --------------------------------------------------------------------------
# Claude Code v2.1.240 alignment.
#
# v2.1.232 made non-teammate agent spawns run in the BACKGROUND by default in
# interactive sessions, and gave `subagent_type: "fork"` subagents the full
# conversation and prompt cache. v2.1.239 fixed a defect where an agent, skill,
# or command `.md` beginning with a UTF-8 BOM was silently ignored — no error,
# the artifact simply never loaded. None of these error at write time; all
# changed what the persona's prose was *claiming* or what shipped bytes must
# never contain.
#
# The claim guards below are BIDIRECTIONAL on purpose. A guard that only checks
# that a term still appears is greenest exactly when the claim around it has
# been reversed — the term survives the sentence. So each one asserts the claim
# we now believe AND the absence of the claim it replaced.
#
# What they do NOT check: that the platform default is still background, or
# that the platform still ignores a BOM-prefixed file. That is runtime
# behaviour and cannot be observed from disk. They guard prose/byte drift and
# claim nothing more — the alternative would be a test that can never fail.
# --------------------------------------------------------------------------

README_FILE = REPO_ROOT / "README.md"

CLAUDE_CODE_ANCHOR = "v2.1.240"
SUPERSEDED_ANCHOR = "v2.1.232"
LATEST_TABLE_START = "v2.1.233"


def _claim_drift(text: str, *, asserts: list[str], superseded: list[str]) -> list[str]:
    """Bidirectional prose check, taking TEXT so the controls can feed it synthetic input.

    Split out deliberately: a control must be able to prove this reports a defect
    without editing the real README or persona on disk.
    """
    problems = [f"missing claim: {c!r}" for c in asserts if c not in text]
    problems += [f"superseded claim still present: {c!r}" for c in superseded if c in text]
    return problems


def _anchor_claims(anchor: str) -> list[tuple[str, Path, str]]:
    """The three sites that must all name the SAME Claude Code anchor version.

    Parameterised by `anchor` so the superseded spellings are generated from the
    same template as the current ones — the two can never drift apart here.
    """
    return [
        (
            "README 'verified against' line",
            README_FILE,
            f"verified against Claude Code v2.1.105–**{anchor}**",
        ),
        (
            "agent-prompt fan-out heading",
            AGENT_FILE,
            f"**Fan-out limits (Claude Code v2.1.217–{anchor}).**",
        ),
    ]


def test_claude_code_anchor_names_the_same_version_everywhere() -> None:
    """Every site anchoring AMPA to a Claude Code version names the current one.

    This repo has been bitten twice by a bump applied to one site and not its
    siblings — most recently when a `G1.1`→`G1.2` rule bump left fourteen pinned
    citations dangling. The failure is quiet: the un-bumped site keeps claiming a
    verification that was never run against the version it names.

    The superseded direction is checked too, but only for the two ANCHOR
    spellings. A historical table heading legitimately keeps an old version — it
    dates a past range and is correct as written, so asserting its absence would
    fail on correct content.

    The latest table's start version is its own constant (`LATEST_TABLE_START`),
    not derived from the previous range. It used to be hardcoded as the previous
    range's start (e.g. "v2.1.225"), which was only ever true by accident — the
    new range starts one version after wherever the old one ended, and that
    boundary moves independently of the anchor on every bump. Deriving it from
    the old anchor would break on every second bump.
    """
    for label, path, expected in _anchor_claims(CLAUDE_CODE_ANCHOR):
        text = path.read_text(encoding="utf-8")
        assert expected in text, f"{label}: expected to find {expected!r}"

    for label, path, stale in _anchor_claims(SUPERSEDED_ANCHOR):
        text = path.read_text(encoding="utf-8")
        assert stale not in text, (
            f"{label}: still carries the superseded anchor {stale!r} — one site was "
            "bumped and this one was not"
        )

    latest_table = f"### {LATEST_TABLE_START} – {CLAUDE_CODE_ANCHOR} "
    readme = README_FILE.read_text(encoding="utf-8")
    assert latest_table in readme, (
        f"README: expected the latest compatibility table to be headed {latest_table!r}"
    )


def test_agent_prompt_states_the_async_subagent_contract() -> None:
    """The persona describes subagent returns as asynchronous, not in-turn.

    Since v2.1.232 a non-teammate spawn in an interactive session hands back a
    HANDLE, not the subagent's output — the result arrives later as a task
    notification. The persona previously promised an in-turn return ("Subagents
    must return results to you"), which would lead the agent to relay a handle as
    though it were a finding, or report a delegated task complete on the strength
    of having spawned it. Nothing errors when it does; that is the whole hazard.
    """
    problems = _claim_drift(
        AGENT_FILE.read_text(encoding="utf-8"),
        asserts=["Collect before you relay", "background by default"],
        superseded=["Subagents must return results to you"],
    )
    assert not problems, "subagent-return contract drifted: " + "; ".join(problems)


def test_fork_prohibition_rests_on_the_reason_that_survived() -> None:
    """The no-fork rule is justified by AMP identity, not by the retired context argument.

    The original justification was partly "a forked copy could not finish any of
    them" — which leaned on a fork lacking the conversation. v2.1.232 gave forks
    the full conversation and prompt cache, retiring that half.

    The RULE is unchanged (a fork still has no AMP identity, is itself a
    background spawn, and never merges its state back), but a rule defended by a
    reason the changelog contradicts invites the next reader to conclude the
    constraint expired and "optimise" the skills back into forks. Guarding the
    reason is the point; `test_skill_does_not_fork_amp_coupled_procedure` above
    already guards the rule.
    """
    problems = _claim_drift(
        AGENT_FILE.read_text(encoding="utf-8"),
        asserts=["no AMP identity", "inherits the full"],
        superseded=["a forked copy could not finish any of them"],
    )
    assert not problems, "fork rationale drifted: " + "; ".join(problems)


# --- Negative controls for the three guards above -------------------------
# Kept, not run-once-and-deleted: a control that ran during development and was
# not committed is a demo, not a control — the repo cannot tell a working guard
# from a broken one without them.


def test_control_claim_drift_reports_a_missing_claim() -> None:
    """Control: a claim we require but that is absent is reported."""
    problems = _claim_drift("nothing relevant here", asserts=["Collect before you relay"], superseded=[])
    assert problems and "missing claim" in problems[0]


def test_control_claim_drift_reports_a_restored_superseded_claim() -> None:
    """Control: the superseded sentence reappearing is reported.

    This is the direction a one-sided guard misses — the required phrase can sit
    happily in the same file as the claim it was supposed to replace.
    """
    text = "Collect before you relay ... Subagents must return results to you."
    problems = _claim_drift(
        text,
        asserts=["Collect before you relay"],
        superseded=["Subagents must return results to you"],
    )
    assert problems and "superseded claim still present" in problems[0]


def test_control_claim_drift_is_silent_on_correct_text() -> None:
    """Control: correct text produces no findings, so the guard is not trivially red."""
    assert not _claim_drift(
        "Collect before you relay, and wait for the notification.",
        asserts=["Collect before you relay"],
        superseded=["Subagents must return results to you"],
    )


# --------------------------------------------------------------------------
# Claude Code v2.1.239 alignment: no shipped .md may open with a UTF-8 BOM.
#
# Before v2.1.239 an agent/skill/command markdown file starting with a BOM was
# SILENTLY IGNORED by Claude Code — no error, the artifact simply never loaded.
# Same silent-failure class as the v2.1.218 and v2.1.232 issues above.
#
# What this guard does NOT check: whether the platform still ignores such a
# file. It only checks the bytes we ship — runtime behaviour is not observable
# from disk.
# --------------------------------------------------------------------------

BOM_BYTES = b"\xef\xbb\xbf"
SHIPPED_MD_DIRS = ["agents", "skills", "commands"]


def _bom_offenders(files: list[tuple[str, bytes]]) -> list[str]:
    """Return the labels of every (label, raw_bytes) pair that opens with a UTF-8 BOM.

    Split out to take raw bytes directly, so a control can feed it synthetic
    input without writing files to disk.
    """
    return [label for label, raw in files if raw.startswith(BOM_BYTES)]


def test_no_shipped_markdown_starts_with_a_utf8_bom() -> None:
    """No shipped agent/skill/command .md file may open with a UTF-8 BOM.

    Reads raw bytes, not decoded text: `encoding="utf-8"` would surface a BOM as
    a harmless U+FEFF character and `utf-8-sig` would strip it outright, hiding
    the exact defect this guards against. Reports every offender, not just the
    first, since a single-file report would hide a systemic authoring mistake.
    This checks the bytes on disk only — not that the platform still ignores
    such files, which is runtime behaviour unobservable from disk.
    """
    files = []
    for dirname in SHIPPED_MD_DIRS:
        for path in sorted((REPO_ROOT / dirname).rglob("*.md")):
            files.append((str(path.relative_to(REPO_ROOT)), path.read_bytes()))
    offenders = _bom_offenders(files)
    assert not offenders, f"shipped .md files open with a UTF-8 BOM (silently ignored pre-v2.1.239): {offenders}"


def test_control_bom_offenders_detects_synthetic_bom_and_ignores_clean_input() -> None:
    """Control: the BOM predicate flags a synthetic BOM-prefixed file and stays silent on clean input."""
    offenders = _bom_offenders(
        [
            ("clean.md", b"# clean file\n"),
            ("bomful.md", BOM_BYTES + b"# has a bom\n"),
        ]
    )
    assert offenders == ["bomful.md"]

    assert not _bom_offenders([("clean.md", b"# clean file\n")])
