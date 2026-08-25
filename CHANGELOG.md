# Changelog

All notable changes to this project will be documented in this file.
## [2.0.10] - 2026-08-25

### Documentation

- Archive 9 complete cards as themselves (3P-ZON-05)

- Adopt fleet R41 wave + 3-pillars 3.0.0 vocabulary (TRDD-GOE2B4XJ)

## [2.0.9] - 2026-08-25

### Bug Fixes

- The new BOM-dir assertion broke every fresh clone

### Documentation

- Archive the 5 Phase-2 cards as published — shipped in v2.0.8

- Route all inter-agent messaging prose through the frozen amp-* CLIs (TRDD-KCX9O26L)

- Realign AMPA to Claude Code v2.1.240 (TRDD-SL4FJ3M2)

- Close TRDD-SL4FJ3M2 as complete

- Correct an unsourced claim in the v2.1.235 row (TRDD-SL4FJ3M2)

- Record the post-close correction on TRDD-SL4FJ3M2

### Miscellaneous

- V2.0.9

### Tests

- Stop the BOM guard narrowing silently; correct a fabricated timestamp

## [2.0.8] - 2026-08-18

### Documentation

- Add Phase-2 TRDDs MP45ZMAG MYX98XFG LNSZPCKE BYO9XYI0 FLU2C00U 2PJO9IWZ U5ECXGOC — fixes for the 8 confirmed self-audit findings (hub TRDD-BRRJK57P)

- Perform the skipped complete→completed closing edits on 4 archived cards (TRDD-LNSZPCKE)

- Remove dangling PRRD rule-15 citations from 3 cards (TRDD-BYO9XYI0)

- Replace phantom tests/logs/ path with actionable instruction (TRDD-MP45ZMAG)

- Rewrite stale pre-push-hook header to match its code (TRDD-U5ECXGOC)

- Add G1 self-id line to op-respond-to-review Example 1 (TRDD-2PJO9IWZ)

- Add the G1 self-id requirement to op-update-pr-with-fixes (TRDD-FLU2C00U)

- Correct test_order_pipeline.py description (TRDD-MYX98XFG)

- Close the 7 Phase-2 cards — 5 complete (release-via publish), 2 completed+archived (release-via none)

### Miscellaneous

- V2.0.8

## [2.0.7] - 2026-08-16

### Bug Fixes

- Un-archive 8 cards that were mid-pipeline, not terminal

### Documentation

- Mark 9 terminal TRDDs as LANDED — stale STATE prose read as current

- Archive the 14 terminal TRDDs out of the OPEN zone

### Miscellaneous

- V2.0.7

## [2.0.6] - 2026-08-14

### Bug Fixes

- Scope the R6 403 claim to the AMP transport (hub#131) + archive TRDD-P9KVMK5A

### Documentation

- Archive TRDD-P9KVMK5A → completed (content edit landed after the rename was staged)

### Miscellaneous

- V2.0.6

## [2.0.5] - 2026-08-14

### Bug Fixes

- Stop promising an in-turn subagent return (TRDD-P9KVMK5A)

### Documentation

- Add TRDD-P9KVMK5A — realign AMPA to Claude Code v2.1.232

### Miscellaneous

- V2.0.5

### Tests

- Guard the v2.1.232 claims in both directions (TRDD-P9KVMK5A)

## [2.0.4] - 2026-08-11

### Miscellaneous

- V2.0.4

### Tests

- Commit the negative controls — mine only ever ran by hand

## [2.0.3] - 2026-08-11

### Bug Fixes

- The rule-text guard was blind to continuation lines

### Miscellaneous

- V2.0.3

## [2.0.2] - 2026-08-11

### Miscellaneous

- V2.0.2

### Tests

- Bind rule TEXT to its version, and cover .py citations

## [2.0.1] - 2026-08-11

### Bug Fixes

- Drop the paging handle from the G1 byline template, bump G1.1 to G1.2

### Documentation

- Close IUJ75HDL — published v2.0.0 (da26fd3)

- Correct the R42.8 claim in IUJ75HDL — it IS ratified

- Unpin the G1 citations my own version bump had just dangled

### Miscellaneous

- V2.0.1

### Tests

- Gate the skill menu against the shipped skill set (RP-SKILL-MENU-01)

- Gate PRRD citation integrity, and fix the one it found

## [2.0.0] - 2026-08-08

### Bug Fixes

- [**breaking**] Run ampa-* skills inline and repair the inert preload (TRDD-IUJ75HDL)

- Drop the dead case pattern and route the preloaded skills (TRDD-IUJ75HDL)

### Documentation

- Record 459032f on 1TXG0EON (ruff-gate pin)

- Capture the ruff-drift publish-lint-gate lesson (TRDD-1TXG0EON)

### Miscellaneous

- V2.0.0

## [1.4.7] - 2026-07-24

### Bug Fixes

- Pin ruff gate to shipped E4/E7/E9/F rule set (TRDD-1TXG0EON)

### Documentation

- Add I8AH88SS/K2X9RF7S/G0768YHK — rewire 3-pillars onto granular ama-* skills

- Mark I8AH88SS complete (58827de)

- Mark K2X9RF7S complete (57b35a4)

- Reflect granular ama-* wiring + add self-mandate/missing-derived/refusal scenarios (TRDD-G0768YHK)

- Mark G0768YHK complete (e3ddf58)

### Miscellaneous

- V1.4.7

### Refactor

- Rewire 3-pillars onto granular ama-* + repurpose wrapper as MEMBER policy (TRDD-I8AH88SS)

- Migrate persona to min-approval-requirement + granular ama-* wiring (TRDD-K2X9RF7S)

## [1.4.6] - 2026-07-14

### Documentation

- Capture the {name}--v{version} dependency-resolution tag (PROJECT wikimem)

- G1.1 self-id on the review-comment path + document the Agent commit trailer (TRDD-W5WYY2VF)

- Mark W5WYY2VF complete (3d93133)

### Miscellaneous

- V1.4.6

## [1.4.5] - 2026-07-14

### Documentation

- Capture the publish CHANGELOG-generation bug lesson (PROJECT wikimem)

- Mark workflow-hardening TRDD-e39a6aa8 complete (8c561b5)

- Lifecycle section v1 -> v2 (column + 4 zones) (TRDD-YK1HL9RH)

- Reflect the dependency-resolution tag + new tests in README/tests (TRDD-UMRQ84S9, UF9AXQJY)

- Mark UMRQ84S9 / YK1HL9RH / UF9AXQJY complete

### Features

- Push the {name}--v{version} dependency-resolution tag atomically (TRDD-UMRQ84S9)

### Miscellaneous

- V1.4.5

### Tests

- Add MEMBER governance behavior scenarios (TRDD-UF9AXQJY)

### Ci

- Least-privilege permissions + job timeouts on all workflows (TRDD-e39a6aa8)

## [1.4.4] - 2026-06-22

### Bug Fixes

- Full-history CHANGELOG + One-Source-of-Truth staging (TRDD-3ff8013f)

- Fail-fast on unknown tool + subprocess timeouts (TRDD-e4e12416)

### Documentation

- TRDD-2f889b66 shipped v1.4.3 — proposal -> tasks, column published

- Capture publish CI-vs-dryrun lesson (PROJECT wikimem)

- Plan go-on-yourself improvement pass — 3 TRDDs

- Correct script count, workflow steps, declare kanban skill (TRDD-ab0d98b0)

- Mark 3 go-on-yourself TRDDs complete (3e245f5, 4809a20, e31a1c6)

### Miscellaneous

- V1.4.4

## [1.4.3] - 2026-06-20

### Features

- Wire #7 progress transitions to the frozen verbs (TRDD-2f889b66)

### Miscellaneous

- V1.4.3

## [1.4.2] - 2026-06-20

### Bug Fixes

- Type git() as CompletedProcess[str] (mypy no-any-return)

### Documentation

- Route programmer #7 kanban integration to the MANAGER (manager#18)

- Record MANAGER decision on TRDD-2f889b66 (manager#18) — approved, build held

### Miscellaneous

- V1.4.2

## [1.4.1] - 2026-06-20

### Bug Fixes

- Inherit the session model (drop model:opus pin) + drop stale version

### Documentation

- Refresh Claude Code compatibility to v2.1.183

### Miscellaneous

- V1.4.1

## [1.4.0] - 2026-06-19

### Bug Fixes

- Decouple 2 live server-/api/ calls to the frozen CLI (R23)

### Features

- Adopt the R37.1 MAESTRO escalation model in the MEMBER persona (R6.6/R37.1)

### Miscellaneous

- V1.4.0

### Tests

- Add R23 + R6.6/R37.1 compliance guards (6 tests)

## [1.3.0] - 2026-06-15

### Features

- Adopt the global janitor 3-scope memory + Claude Code v2.1.178 compat (#18)

### Miscellaneous

- V1.3.0

## [1.2.0] - 2026-06-13

### Bug Fixes

- Clear 7 advisory CPV warnings + 2 doc-accuracy bugs

- Resolve the AMCOS contact contradiction (#17 M6)

- Version-pin the ai-maestro-plugin dependency to ^2.7.0 (CPV warning)

### Documentation

- Modernize the 4 stale docs + handoff enums to v2 (#17 M11)

### Features

- Restore the pre-PR gate (#17 M7c) + ship op-pre-pr-gate template (M13)

- Comprehension-handshake answer replaces bare ACK (#17 M7a) + G1.1 self-id in PR/issue templates (M10)

- Align with the canonical fleet memory system (janitor#20)

- Bootstrap 3-pillars task system — PRRD + 4-zone design/ + MEMBER kanban skill (#17 M2/M3/M4)

- Approval-tier governance in the 5 skills (#17 M5) + real skill-contract tests (#17 M12)

### Miscellaneous

- Keep CPV-direct pipeline; defer canon --force-templates (vendored-script conflict) (#17 / janitor#19)

- V1.2.0

## [1.1.0] - 2026-06-11

### Bug Fixes

- Clear the strict-validation failures blocking every PR (#16)

- Stage uv.lock in the release commit (closes #9) (#13)

- Remove orphaned gitignore_filter.py; delegate .py listing to git

### Documentation

- R6 v2 comms sync + approval-tiers governance section (#14)

- Claude Code v2.1.105-v2.1.143 compatibility notes + v1.0.26 bump (#10)

### Features

- Adopt the markdown memory system (closes #12) (#15)

### Miscellaneous

- Add tldrignore and tldr_session_* to .gitignore

- Update uv.lock

- V1.1.0

## [1.0.25] - 2026-04-13

### Miscellaneous

- Update uv.lock

- V1.0.25

### Ci

- Fix notify-marketplace.yml to use canonical CPV workflow

## [1.0.24] - 2026-04-10

### Bug Fixes

- Correct governance terminology, version sync, and communication rules

- Resolve all CPV validation issues

- Publish.py runs CPV validation remotely + pre-push enforces --strict

- Ruff F541 — remove extraneous f-prefix in publish.py

- Remove CPV_PUBLISH_PIPELINE bypass from pre-push hook — CPV --strict always runs

- Publish.py + pre-push use cpv-remote-validate via uvx

- Embed complete TOC headings in SKILL.md reference tables (CPV strict)

- Restore ## Resources section name + embed all H2 headings (CPV strict)

- Embed exact TOC headings from Contents sections (CPV strict)

- Replace dead example URLs with example.com + add cliff.toml

### Documentation

- Reflow markdown line wrapping to ~80 chars + track uv.lock

### Features

- Add compatible-titles and compatible-clients to agent profile

- Add communication permissions from title-based graph

- Add smart publish pipeline + pre-push hook enforcement

### Miscellaneous

- V1.0.24

### Ci

- Update validate.yml to use cpv-remote-validate --strict

- Strict publish.py + release.yml + .serena in .gitignore

- Add pre-push hook + update publish.py to strict mode with sentinel

- Pre-push hook uses process ancestry instead of env var

## [1.0.22] - 2026-03-26

### Bug Fixes

- Target Emasoft fork for marketplace notifications

- Resolve all CPV MINOR issues (TOC embedding, checklists, examples)

## [1.0.21] - 2026-03-26

### Bug Fixes

- Add missing skill sections to 5 skills + sync CPV scripts

- Remove 2nd person from descriptions, parent traversal refs, absolute paths

- Resolve all MINOR validation issues (TOC, SKILL.md metadata, mypy)

- Resolve remaining validation issues

- Comprehensive audit fixes — all 48 findings addressed

- Cross-platform portability, frontmatter standardization, implementer docs

- Convert shell scripts to Python, embed TOCs, fix CI failures

- Resolve all audit findings — 0 CRITICAL, 0 MAJOR, 0 MINOR

- Resolve all 27 warnings — perfect validation score

- Comprehensive audit — version sync, duplicate sections, stale docs (v1.0.12)

- Script audit — stale bash ref, usage docs, bump to v1.0.13

- Resolve all CPV validation issues, sync scripts, bump to v1.0.15

- Update ROLE_BOUNDARIES.md to current 3-role governance model

- Configure marketplace notification for 23blocks-OS/ai-maestro-plugins

- Add .agent.toml and rename main agent for quad-match rule

- Remove hardcoded localhost:23000 and /api/health from handoff skill

- Update kanban system from 8 columns to AI Maestro's actual 5 statuses

- Resolve LLM-verified compliance issues across 22 files (v1.0.19)

- Allow MINOR issues to pass validation gate (exit 3 = pass)

- Resolve CPV validation issues (MAJOR=1, MINOR=6)

- Resolve CPV validation issues, update quality gate

### Documentation

- Standardize validator references to validate_plugin.py

- Add marketplace installation instructions with --scope local

- Update README with --scope local per-agent installation instructions

- Update for Claude Code 2.1.69 compatibility, bump to v1.0.11

- Update README and AGENT_OPERATIONS, bump to v1.0.16

### Features

- Token budget optimization + sync CPV v1.8.5, bump to v1.0.14

- Add kanban task verification and standardize task ID format

- Add llm-externalizer as recommended MCP for token-efficient analysis

### Miscellaneous

- Sync validation scripts from CPV

- Sync validation scripts from CPV

- Sync validation scripts from CPV

- Bump version to 1.0.2

- Bump version to 1.0.3

- Bump version to 1.0.4

- Sync validation scripts from CPV

- Bump version to 1.0.5

- Sync validation scripts, hooks, and workflows from CPV

- Bump version to 1.0.6

- Replace validation scripts with latest CPV v1.7.3, add auto-sync

- Remove last shell script for full cross-platform Python-only plugin

- Sync CPV validation scripts from v1.7.5

- Sync CPV v1.7.6, bump plugin to v1.0.7

- Sync CPV v1.7.9, bump plugin to v1.0.8

- Sync CPV v1.8.0, bump plugin to v1.0.9

- Sync CPV v1.8.1, bump plugin to v1.0.10

- Bump to v1.0.17 — resolves issues #1, #2, #3

- Bump to v1.0.18 — resolves issues #4, #5, #6

- Bump version to 1.0.20

- Track .serena project config files in git

### Ci

- Replace local validators with CPV uvx remote validation

### Rename

- Emasoft-programmer-agent → ai-maestro-programmer-agent

- Replace all emasoft agent acronyms and references

## [1.0.1] - 2026-02-08

### Bug Fixes

- Resolve all audit issues - broken refs, localhost refs, JSON annotations, verify lines, cross-plugin links

- Fix validate.yml and notify-marketplace.yml for CI

- Fix plugin.json schema for Claude Code compatibility

- Add manifest schema checks for repository type and unknown keys

### Features

- Bump version to 1.0.1

### Refactor

- Convert aimaestro-agent.sh references to skill-based abstractions in AGENT_OPERATIONS.md

### Tests

- Verify push script


