# Changelog

All notable changes to this project will be documented in this file.
## [Unreleased]

### Documentation

- TRDD-2f889b66 shipped v1.4.3 — proposal -> tasks, column published

- Capture publish CI-vs-dryrun lesson (PROJECT wikimem)

- Plan go-on-yourself improvement pass — 3 TRDDs

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


