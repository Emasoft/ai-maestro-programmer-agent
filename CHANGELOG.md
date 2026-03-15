# Changelog

All notable changes to the AI Maestro Programmer Agent plugin are documented in this file.

## [1.0.20] - 2026-03-15

### Added
- **LLM Externalizer integration**: Added `llm-externalizer` as recommended MCP in `.agent.toml` and agent frontmatter
- New "LLM Externalizer (Token Saver)" section in main agent definition with tool table and usage rules
- LLM Externalizer guidance in Token Budget sections (agent definition + task-execution SKILL)
- "Recommended Companion Plugins" section in README with install instructions
- Updated "Remember" list: item #5 "Use LLM Externalizer to save tokens"

## [1.0.19] - 2026-03-15

### Fixed
- **R2 kanban dashes**: Replaced all `in-progress` status values with `in_progress` (underscore) in 5 reference files across handoff-management, orchestrator-communication, and task-execution skills
- **R2 kanban statuses**: Updated handoff document status lists from `pending|in-progress|blocked|completed` to the correct 5-status system `backlog|pending|in_progress|review|completed`
- **R7 task ID format**: Replaced all legacy `TASK-xxx` and `AMPA-xxx` task IDs with UUID format across 9 reference files in orchestrator-communication and task-execution skills
- **R1 governance**: Fixed COS role in TEAM_REGISTRY_SPECIFICATION.md Role Types table from "0 (org-wide)" to "1 (per closed team)"
- **R11 TOC**: Removed extra "Checklist" entry from op-read-handoff-document.md TOC to match standard 5-entry format

### Verified
- Full-repo prefix scan: no wrong e-prefixes (EAMA/ECOS/EOA/EIA/EPA/EAA) or emasoft-role patterns found — all "Emasoft" occurrences are legitimate (author name, GitHub URLs, historical changelog)

## [1.0.18] - 2026-03-13

### Fixed
- **Issue #4**: Removed hardcoded `localhost:23000` and `/api/health` from handoff skill; uses `$AIMAESTRO_API` env var and correct `/api/sessions` endpoint
- **Issue #5**: Updated kanban system from 8 columns to AI Maestro's actual 5 statuses (`backlog`/`pending`/`in_progress`/`review`/`completed`) across all 4 docs + PR reference

### Added
- **Issue #6**: Task verification step in receive-task-assignment (optional kanban read-back via `$AIMAESTRO_API`); standardized task ID format (UUID + optional `externalRef` for GitHub issue numbers)

## [1.0.17] - 2026-03-13

### Fixed
- **Issue #3**: Updated ROLE_BOUNDARIES.md to current 3-role governance model (manager/chief-of-staff/member), synced from upstream
- **Issue #2**: Created `ai-maestro-programmer-agent.agent.toml` for quad-match rule compliance; renamed main agent from `ampa-programmer-main-agent` to `ai-maestro-programmer-agent-main-agent`; updated all 13 referencing files
- **Issue #1**: Configured marketplace notification workflow for `23blocks-OS/ai-maestro-plugins` with correct secret name, event-type, and client-payload (remains disabled until secret is configured)

## [1.0.16] - 2026-03-08

### Changed
- Updated README: fixed script counts (18 CPV + 6 project), added missing project scripts to table
- Updated AGENT_OPERATIONS.md: added v1.0.15 Recent Changes entry, expanded Scripts Reference to all 6 project scripts, bumped doc version to 1.4.0
- Verified docs/ROLE_BOUNDARIES.md, docs/FULL_PROJECT_WORKFLOW.md, docs/TEAM_REGISTRY_SPECIFICATION.md are current and accurate

## [1.0.15] - 2026-03-08

### Fixed
- Fixed all MAJOR validation issues: added missing `## Error Handling` and `## Examples` sections to all 5 SKILL.md files
- Fixed all WARNING issues: embedded complete TOC headings from reference files into SKILL.md Resources sections
- Fixed all MINOR issues: standardized reference file frontmatter, moved TOC within 200-char threshold, added checklist patterns
- Standardized all 29 reference file TOC format to 5-entry standard (`When to Use · Prerequisites · Procedure · Examples · Error Handling`)
- Removed unnecessary frontmatter fields (`workflow-step`, `operation-type`, `message-type`, `priority`) from all reference files
- Added "Use when ..." phrase to task-execution skill description (Nixtla strict mode)
- Added "Copy this checklist and track your progress" phrase to all 5 SKILL.md Instructions sections
- Standardized Sections separator character to `·` across all SKILL.md files

### Changed
- Trimmed SKILL.md Token Budget sections from 4 to 3 bullets where needed to stay under 5000 char limit
- Shortened reference file frontmatter descriptions to keep TOC within 200-char position limit

## [1.0.14] - 2026-03-07

### Added
- Token Budget section in agent definition — file-based reporting, lazy reference loading, stdout capture
- Token Budget section in all 5 SKILL.md files with per-skill guidance
- Token rule blockquote in all 29 reference files
- `--report-file` flag to `test_order_pipeline.py` — writes full report to file, prints concise summary
- `--report-file` flag to `sync_cpv_scripts.py` — writes sync details to file, prints concise summary
- `AMPA_REPORT_FILE` env var support in `pre-push-hook.py` — captures validator output to file
- `uv` fallback to `python3` in `pre-push-hook.py` for local dev without uv installed

### Changed
- Trimmed redundant boilerplate from all 5 SKILL.md overview sections (role context already in agent def)
- Fixed mypy type error in `pre-push-hook.py` (CompletedProcess[bytes] vs [str])

## [1.0.13] - 2026-03-06

### Fixed
- Fixed stale `sync_cpv_scripts.sh` reference in pre-push-hook.py comment (now `.py`)
- Fixed `uv run python` usage in test_order_pipeline.py docstring (now `python3`)

### Changed
- Bumped plugin version to 1.0.13

## [1.0.12] - 2026-03-05

### Fixed
- Removed duplicate `## Instructions` section in orchestrator-communication SKILL.md
- Removed duplicate "Related Skills" and "See Also" sections in github-operations SKILL.md
- Fixed README validation command: `python3` instead of `uv run python` (no pyproject.toml)
- Bumped all skill and agent versions from 1.0.6 to 1.0.12 (were out of sync with plugin)
- Updated AGENT_OPERATIONS.md "Recent Changes" section (was stale since 2026-02-07)
- Made sync_cpv_scripts.py executable

### Changed
- Bumped plugin version to 1.0.12

## [1.0.11] - 2026-03-05

### Added
- Documented `${CLAUDE_SKILL_DIR}` variable in AGENT_OPERATIONS.md (new in Claude Code 2.1.69)
- Added `git-subdir` installation method in README for parent-repo installs
- Added `/reload-plugins` workflow note for plugin development
- Added proxy/TLS troubleshooting note for `gh` CLI behind corporate proxies

### Changed
- Bumped plugin version to 1.0.11
- Updated documentation for Claude Code 2.1.69 compatibility

## [1.0.10] - 2026-03-03

### Changed
- Updated CPV validation scripts to v1.8.1 (bug fix: cpv_validation_common.py, validate_security.py)
- Bumped plugin version to 1.0.10

## [1.0.9] - 2026-03-03

### Changed
- Updated CPV validation scripts to v1.8.0 (14 scripts updated)
- Bumped plugin version to 1.0.9

## [1.0.8] - 2026-03-03

### Changed
- Updated CPV validation scripts to v1.7.9 (10 scripts updated)
- Bumped plugin version to 1.0.8

## [1.0.7] - 2026-03-03

### Fixed
- Resolved all 27 remaining validation warnings (perfect score: 0 issues)
- Embedded TOC sections after all list-item reference links for progressive discovery
- Moved pre-push hook from non-standard git-hooks/ to scripts/pre-push-hook.py

### Changed
- Updated CPV validation scripts to v1.7.6
- Bumped plugin version to 1.0.7

## [1.0.6] - 2026-03-02

### Fixed
- Rewrote shell scripts (sync_cpv_scripts, pre-push hook) in Python for cross-platform compatibility
- Fixed CI workflow treating MINOR validation issues as failures
- Fixed notify-marketplace.yml YAML parse error from empty env block
- Fixed all TOC embedding issues for progressive discovery in SKILL.md files
- Replaced deprecated golint references with staticcheck
- Fixed macOS-only gh CLI install instructions to be cross-platform

### Changed
- Renamed plugin from emasoft-programmer-agent to ai-maestro-programmer-agent
- Renamed all agent acronyms (EOA→AMOA, EIA→AMIA, EPA→AMPA, etc.)
- Standardized frontmatter across all reference files
- Bumped all skill versions to 1.0.6 to match plugin version
- Added .editorconfig for consistent line endings and encoding
- Added standalone mode documentation for use without orchestrator

### Added
- Python sync script (sync_cpv_scripts.py) as cross-platform replacement
- Python pre-push hook for cross-platform git hook execution
- Windows virtual environment activation instructions
- Cross-reference notes between overlapping skills
- Getting Started section in README

## [1.0.0] - 2026-02-28

### Added
- Initial release of the AI Maestro Programmer Agent plugin
- 5 skills: task-execution, orchestrator-communication, github-operations, project-setup, handoff-management
- 29 reference operation files
- CPV validation suite integration (21 scripts)
- Pre-push validation hook
- GitHub Actions CI/CD workflows
