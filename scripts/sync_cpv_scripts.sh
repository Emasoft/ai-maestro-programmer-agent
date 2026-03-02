#!/usr/bin/env bash
# sync_cpv_scripts.sh - Sync validation scripts from claude-plugins-validation
#
# Downloads the latest validation scripts from the official CPV repository
# (Emasoft/claude-plugins-validation) and replaces the local copies.
#
# Usage:
#   ./scripts/sync_cpv_scripts.sh           # Sync from GitHub (default branch)
#   ./scripts/sync_cpv_scripts.sh v1.7.3    # Sync from a specific tag
#
# Requirements: gh (GitHub CLI), authenticated

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

REPO="Emasoft/claude-plugins-validation"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REF="${1:-}"  # Optional: tag or branch to sync from

# Validation scripts to sync (all validate_*.py + utilities)
SCRIPTS=(
    cpv_validation_common.py
    gitignore_filter.py
    lint_files.py
    smart_exec.py
    validate_agent.py
    validate_command.py
    validate_documentation.py
    validate_encoding.py
    validate_enterprise.py
    validate_hook.py
    validate_lsp.py
    validate_marketplace_pipeline.py
    validate_marketplace.py
    validate_mcp.py
    validate_plugin.py
    validate_rules.py
    validate_scoring.py
    validate_security.py
    validate_skill_comprehensive.py
    validate_skill.py
    validate_xref.py
)

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  CPV Validation Scripts Sync${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check gh is available
if ! command -v gh &> /dev/null; then
    echo -e "${RED}ERROR: gh (GitHub CLI) is required but not installed.${NC}"
    echo "Install with: brew install gh"
    exit 1
fi

# Determine the ref to sync from
if [ -z "$REF" ]; then
    # Get the latest release tag
    REF=$(gh api "repos/${REPO}/releases/latest" --jq '.tag_name' 2>/dev/null || echo "")
    if [ -z "$REF" ]; then
        # Fallback to default branch
        REF=$(gh api "repos/${REPO}" --jq '.default_branch' 2>/dev/null || echo "master")
        echo -e "${YELLOW}No releases found. Using branch: ${REF}${NC}"
    else
        echo -e "${GREEN}Latest release: ${REF}${NC}"
    fi
else
    echo -e "${BLUE}Syncing from ref: ${REF}${NC}"
fi

echo -e "${BLUE}Source: ${REPO}@${REF}${NC}"
echo ""

# Track results
SYNCED=0
FAILED=0
UNCHANGED=0

for script in "${SCRIPTS[@]}"; do
    # Download from GitHub raw content
    CONTENT=$(gh api "repos/${REPO}/contents/scripts/${script}?ref=${REF}" --jq '.content' 2>/dev/null || echo "")

    if [ -z "$CONTENT" ]; then
        echo -e "${YELLOW}  SKIP: ${script} (not found in CPV@${REF})${NC}"
        FAILED=$((FAILED + 1))
        continue
    fi

    # Decode base64 content
    DECODED=$(echo "$CONTENT" | base64 --decode 2>/dev/null)

    if [ -z "$DECODED" ]; then
        echo -e "${RED}  FAIL: ${script} (decode error)${NC}"
        FAILED=$((FAILED + 1))
        continue
    fi

    # Check if content is different from current
    if [ -f "${SCRIPT_DIR}/${script}" ]; then
        CURRENT_HASH=$(shasum -a 256 "${SCRIPT_DIR}/${script}" | cut -d' ' -f1)
        NEW_HASH=$(echo "$DECODED" | shasum -a 256 | cut -d' ' -f1)
        if [ "$CURRENT_HASH" = "$NEW_HASH" ]; then
            UNCHANGED=$((UNCHANGED + 1))
            continue
        fi
    fi

    # Write the file
    echo "$DECODED" > "${SCRIPT_DIR}/${script}"
    chmod +x "${SCRIPT_DIR}/${script}"
    echo -e "${GREEN}  UPDATED: ${script}${NC}"
    SYNCED=$((SYNCED + 1))
done

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  Synced: ${SYNCED}  ${NC}Unchanged: ${UNCHANGED}  ${YELLOW}Skipped: ${FAILED}${NC}"
echo -e "${BLUE}========================================${NC}"

if [ $SYNCED -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}NOTE: ${SYNCED} script(s) updated. Stage and commit before pushing:${NC}"
    echo "  git add scripts/"
    echo "  git commit -m 'chore: sync CPV validation scripts from ${REF}'"
fi

exit 0
