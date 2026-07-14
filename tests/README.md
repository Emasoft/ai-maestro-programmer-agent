# AMPA test suite

Real, no-mock contract tests. They read the actual on-disk skills, agent,
persona, and packaging files and assert their structural + governance
contracts, so they act as anti-drift guards: change a skill or the agent
without updating its test (or vice-versa) and the suite fails.

## Files

- `test_primary_skills.py` — the 5 primary skills' frontmatter, resolvable
  `references/` links, and the #17 fleet-readiness alignment (the `## Governance`
  block, the R6-v3 AMCOS direct channel, the comprehension-handshake / pre-PR-gate
  dialog loops, the G1.1 self-id line in the PR and bug-report templates, the v2
  `column:` migration of handoff task-state, the kanban skill, the global janitor
  memory wiring, no `model:` pin on the agent, and the `ai-maestro-plugin`
  dependency).
- `test_governance_compliance.py` — the R23 frozen-CLI decoupling +
  the R6.6 / R37.1 MAESTRO escalation model guards.
- `test_smart_exec.py` — `smart_exec.py`'s cross-platform argv builders
  (interpreter selection, timeout wrapping, report-file flag handling).
- `test_publish_dependency_tag.py` — the release must push the
  `{name}--v{version}` tag Claude Code's dependency resolver reads (derived
  strictly from the manifest, hard-failing on a nameless one), alongside
  `v{version}`, in one `git push --atomic` (`TRDD-UMRQ84S9`).

`scenarios/` holds `governance-scenarios.md` — a Given/When/Then **plan** of the
MEMBER governance *reasoning* behaviors (tier self-classify, propose-don't-edit,
signal-only transitions, the R23 refusal). These are persona behaviors with no
executable to drive; the file is reviewed by reading the persona/skill prose, not
run — its coverage map names the pytest test that enforces each bright-line and
marks the rest `prose-review`. Do NOT fabricate a harness to "run" them.

## Run locally

```bash
uv run --with pytest pytest tests/ -x -q --tb=short
```

This is the exact gate `scripts/publish.py` runs before every release, and the
same gate CI runs in `validate.yml`. A non-zero exit means a skill or persona
has drifted from its test contract — fix the source file, or, if the contract
genuinely changed, update the matching assertion (never weaken or delete a real
assertion to make the suite pass).
