#!/usr/bin/env bash
#
# validate-skills.sh -- Validate all SKILL.md files in the dotnet-artisan plugin.
#
# Thin wrapper that invokes the Python validation script.
# All parsing, validation, and reporting happens in Python for:
#   - Deterministic YAML parsing (strict subset parser, no PyYAML dependency)
#   - No per-file subprocess spawning
#   - Identical behavior across all environments
#
# Requirements:
#   - python3
#
# Environment variables:
#   ALLOW_PLANNED_REFS=1  -- Downgrade unresolved cross-references from errors to warnings.
#
# Output keys (stable, CI-parseable):
#   CURRENT_DESC_CHARS=<N>
#   PROJECTED_DESC_CHARS=<N>
#   BUDGET_STATUS=OK|WARN|FAIL

set -euo pipefail

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 required but not found in PATH"
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

exec python3 "$REPO_ROOT/scripts/_validate_skills.py" \
    --repo-root "$REPO_ROOT" \
    --projected-skills 95 \
    --max-desc-chars 120 \
    --warn-threshold 12000 \
    --fail-threshold 15000 \
    ${ALLOW_PLANNED_REFS:+--allow-planned-refs}
