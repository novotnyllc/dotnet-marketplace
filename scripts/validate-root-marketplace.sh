#!/usr/bin/env bash
#
# validate-root-marketplace.sh -- Validate root .claude-plugin/marketplace.json
#
# Checks:
#   Required fields: name, owner.name, plugins array, per-plugin name/source
#   Recommended fields: $schema, metadata, per-plugin version/category/keywords
#   Source path resolution: each plugin source dir exists with plugin.json
#
# Design constraints:
#   - Single-pass validation (no subprocess spawning per entry, no network)
#   - Same commands locally and in CI
#   - Exits non-zero on validation failures

set -euo pipefail

# Navigate to repository root
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
MARKETPLACE_JSON="$REPO_ROOT/.claude-plugin/marketplace.json"

errors=0
warnings=0

echo "=== Root Marketplace Validation ==="
echo ""

if [ ! -f "$MARKETPLACE_JSON" ]; then
    echo "ERROR: marketplace.json not found at $MARKETPLACE_JSON"
    exit 1
fi

# Validate JSON is well-formed
if ! jq empty "$MARKETPLACE_JSON" 2>/dev/null; then
    echo "ERROR: marketplace.json is not valid JSON"
    exit 1
fi

echo "OK: marketplace.json is valid JSON"

# --- Required fields ---

# name (string)
if ! jq -e '.name | type == "string" and length > 0' "$MARKETPLACE_JSON" >/dev/null 2>&1; then
    echo "ERROR: marketplace.json.name must be a non-empty string"
    errors=$((errors + 1))
else
    NAME=$(jq -r '.name' "$MARKETPLACE_JSON")
    echo "OK: marketplace.json.name = \"$NAME\""
fi

# owner.name (string)
if ! jq -e '.owner.name | type == "string" and length > 0' "$MARKETPLACE_JSON" >/dev/null 2>&1; then
    echo "ERROR: marketplace.json.owner.name must be a non-empty string"
    errors=$((errors + 1))
else
    OWNER=$(jq -r '.owner.name' "$MARKETPLACE_JSON")
    echo "OK: marketplace.json.owner.name = \"$OWNER\""
fi

# plugins (array)
if ! jq -e '.plugins | type == "array" and length > 0' "$MARKETPLACE_JSON" >/dev/null 2>&1; then
    echo "ERROR: marketplace.json.plugins must be a non-empty array"
    errors=$((errors + 1))
else
    PLUGIN_COUNT=$(jq '.plugins | length' "$MARKETPLACE_JSON")
    echo "OK: marketplace.json.plugins has $PLUGIN_COUNT plugin(s)"

    # Per-plugin required fields
    for i in $(seq 0 $((PLUGIN_COUNT - 1))); do
        PNAME=$(jq -r ".plugins[$i].name // empty" "$MARKETPLACE_JSON")
        SOURCE=$(jq -r ".plugins[$i].source // empty" "$MARKETPLACE_JSON")

        if [ -z "$PNAME" ]; then
            echo "ERROR: plugins[$i].name is missing or empty"
            errors=$((errors + 1))
        else
            echo "OK: plugins[$i].name = \"$PNAME\""
        fi

        if [ -z "$SOURCE" ]; then
            echo "ERROR: plugins[$i].source is missing or empty"
            errors=$((errors + 1))
        else
            # Resolve source path relative to repo root
            RESOLVED_SOURCE="$REPO_ROOT/$SOURCE"
            if [ ! -d "$RESOLVED_SOURCE" ]; then
                echo "ERROR: plugins[$i].source '$SOURCE' is not a directory"
                errors=$((errors + 1))
            elif [ ! -f "$RESOLVED_SOURCE/.claude-plugin/plugin.json" ]; then
                echo "ERROR: plugins[$i].source '$SOURCE' missing .claude-plugin/plugin.json"
                errors=$((errors + 1))
            else
                echo "OK: plugins[$i].source '$SOURCE' resolves with plugin.json"
            fi
        fi

        # Per-plugin recommended fields
        for field in version category keywords; do
            if ! jq -e ".plugins[$i].$field" "$MARKETPLACE_JSON" >/dev/null 2>&1; then
                echo "WARN: plugins[$i].$field is missing"
                warnings=$((warnings + 1))
            fi
        done
    done
fi

# --- Recommended top-level fields ---

if ! jq -e '."$schema"' "$MARKETPLACE_JSON" >/dev/null 2>&1; then
    echo "WARN: marketplace.json.\$schema is missing"
    warnings=$((warnings + 1))
else
    echo "OK: marketplace.json.\$schema present"
fi

if ! jq -e '.metadata' "$MARKETPLACE_JSON" >/dev/null 2>&1; then
    echo "WARN: marketplace.json.metadata is missing"
    warnings=$((warnings + 1))
else
    echo "OK: marketplace.json.metadata present"
fi

echo ""
echo "=== Summary ==="
echo "Errors: $errors"
echo "Warnings: $warnings"

if [ "$errors" -gt 0 ]; then
    echo ""
    echo "FAILED: $errors error(s) found"
    exit 1
fi

echo ""
echo "PASSED"
exit 0
