# Changelog

All notable changes to the AI Maestro Programmer Agent plugin are documented in this file.

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
