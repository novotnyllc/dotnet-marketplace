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
#   STRICT_REFS=1  -- Treat unresolved cross-references as errors (default: downgrade to warnings).
#
# During early development most skills are planned stubs, so --allow-planned-refs
# is the default. Set STRICT_REFS=1 to enforce strict cross-reference validation.
#
# Output keys (stable, CI-parseable):
#   CURRENT_DESC_CHARS=<N>
#   PROJECTED_DESC_CHARS=<N>
#   BUDGET_STATUS=OK|WARN|FAIL
#   NAME_DIR_MISMATCHES=<N>
#   EXTRA_FIELD_COUNT=<N>
#   FILLER_PHRASE_COUNT=<N>
#   WHEN_PREFIX_COUNT=<N>

set -euo pipefail

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 required but not found in PATH"
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Default to allowing planned refs (most skills are stubs during early development).
# Set STRICT_REFS=1 to treat unresolved cross-references as errors.
ALLOW_PLANNED_FLAG="--allow-planned-refs"
if [ -n "${STRICT_REFS:-}" ]; then
    ALLOW_PLANNED_FLAG=""
fi

exec python3 "$REPO_ROOT/scripts/_validate_skills.py" \
    --repo-root "$REPO_ROOT" \
    --projected-skills 127 \
    --max-desc-chars 120 \
    --warn-threshold 12000 \
    --fail-threshold 15360 \
    $ALLOW_PLANNED_FLAG
