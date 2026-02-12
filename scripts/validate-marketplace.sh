#!/usr/bin/env bash
#
# validate-marketplace.sh -- Validate plugin.json and marketplace.json for dotnet-artisan.
#
# Checks:
#   1. plugin.json exists and is valid JSON
#   2. plugin.json has canonical schema: skills (array), agents (array), hooks (string), mcpServers (string)
#   3. marketplace.json exists and has required fields
#   4. All skill directories referenced in plugin.json contain SKILL.md
#   5. All agent files referenced in plugin.json exist
#   6. hooks and mcpServers paths exist
#
# Design constraints:
#   - Single-pass validation (no subprocess spawning per entry, no network)
#   - Runs in <5 seconds
#   - Same commands locally and in CI
#   - Exits non-zero on validation failures

set -euo pipefail

# Navigate to repository root (parent of scripts/), canonicalized for symlink safety
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"

PLUGIN_JSON="$REPO_ROOT/.claude-plugin/plugin.json"
MARKETPLACE_JSON="$REPO_ROOT/.claude-plugin/marketplace.json"

errors=0
warnings=0

# Reject paths that escape the repository root (traversal, absolute, symlink escape)
validate_path_safe() {
    local path="$1"
    local label="$2"

    # Reject absolute paths
    if [[ "$path" = /* ]]; then
        echo "ERROR: $label contains absolute path: $path"
        return 1
    fi

    # Reject parent traversal
    if [[ "$path" == *".."* ]]; then
        echo "ERROR: $label contains path traversal (..): $path"
        return 1
    fi

    # Resolve canonical path (following symlinks) and verify it stays under REPO_ROOT
    local full_path="$REPO_ROOT/$path"
    if [ -e "$full_path" ]; then
        local resolved
        # Use python3 for portable symlink-resolving realpath (macOS lacks GNU realpath)
        resolved="$(python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$full_path")"
        case "$resolved" in
            "$REPO_ROOT"/*) ;;  # OK - under repo root
            *)
                echo "ERROR: $label resolves outside repository: $path -> $resolved"
                return 1
                ;;
        esac
    fi

    return 0
}

echo "=== Marketplace Validation ==="
echo ""

# --- plugin.json validation ---

echo "--- plugin.json ---"

if [ ! -f "$PLUGIN_JSON" ]; then
    echo "ERROR: plugin.json not found at $PLUGIN_JSON"
    errors=$((errors + 1))
else
    # Validate JSON is well-formed
    if ! jq empty "$PLUGIN_JSON" 2>/dev/null; then
        echo "ERROR: plugin.json is not valid JSON"
        errors=$((errors + 1))
    else
        echo "OK: plugin.json is valid JSON"

        # Check required top-level fields (must be non-empty strings)
        for field in name version description; do
            if ! jq -e ".$field | type == \"string\" and length > 0" "$PLUGIN_JSON" >/dev/null 2>&1; then
                echo "ERROR: plugin.json.$field must be a non-empty string"
                errors=$((errors + 1))
            else
                value=$(jq -r ".$field" "$PLUGIN_JSON")
                echo "OK: plugin.json.$field = \"$value\""
            fi
        done

        # Validate skills is an array of string paths
        skills_valid=$(jq -e '.skills | type == "array" and all(.[]; type == "string")' "$PLUGIN_JSON" 2>/dev/null) || skills_valid="false"
        if [ "$skills_valid" != "true" ]; then
            echo "ERROR: plugin.json.skills must be an array of string paths"
            errors=$((errors + 1))
        else
            skill_count=$(jq -r '.skills | length' "$PLUGIN_JSON")
            echo "OK: plugin.json.skills is an array of strings ($skill_count entries)"

            # Check each skill directory exists and contains SKILL.md
            while IFS= read -r skill_path; do
                if ! validate_path_safe "$skill_path" "skills[]"; then
                    errors=$((errors + 1))
                    continue
                fi
                full_path="$REPO_ROOT/$skill_path"
                if [ ! -d "$full_path" ]; then
                    echo "ERROR: skill directory not found: $skill_path"
                    errors=$((errors + 1))
                elif [ ! -f "$full_path/SKILL.md" ]; then
                    echo "ERROR: SKILL.md not found in skill directory: $skill_path"
                    errors=$((errors + 1))
                else
                    echo "OK: $skill_path/SKILL.md exists"
                fi
            done < <(jq -r '.skills[]' "$PLUGIN_JSON" 2>/dev/null)
        fi

        # Validate agents is an array of string paths
        agents_valid=$(jq -e '.agents | type == "array" and all(.[]; type == "string")' "$PLUGIN_JSON" 2>/dev/null) || agents_valid="false"
        if [ "$agents_valid" != "true" ]; then
            echo "ERROR: plugin.json.agents must be an array of string paths"
            errors=$((errors + 1))
        else
            agent_count=$(jq -r '.agents | length' "$PLUGIN_JSON")
            echo "OK: plugin.json.agents is an array of strings ($agent_count entries)"

            # Check each agent file exists
            while IFS= read -r agent_path; do
                if ! validate_path_safe "$agent_path" "agents[]"; then
                    errors=$((errors + 1))
                    continue
                fi
                full_path="$REPO_ROOT/$agent_path"
                if [ ! -f "$full_path" ]; then
                    echo "ERROR: agent file not found: $agent_path"
                    errors=$((errors + 1))
                else
                    echo "OK: $agent_path exists"
                fi
            done < <(jq -r '.agents[]' "$PLUGIN_JSON" 2>/dev/null)
        fi

        # Validate hooks is a string path
        hooks_type=$(jq -r '.hooks | type' "$PLUGIN_JSON" 2>/dev/null)
        if [ "$hooks_type" != "string" ]; then
            echo "ERROR: plugin.json.hooks must be a string path (got: $hooks_type)"
            errors=$((errors + 1))
        else
            hooks_path=$(jq -r '.hooks' "$PLUGIN_JSON")
            if ! validate_path_safe "$hooks_path" "hooks"; then
                errors=$((errors + 1))
            else
                full_path="$REPO_ROOT/$hooks_path"
                if [ ! -f "$full_path" ]; then
                    echo "ERROR: hooks file not found: $hooks_path"
                    errors=$((errors + 1))
                else
                    echo "OK: $hooks_path exists"
                fi
            fi
        fi

        # Validate mcpServers is a string path
        mcp_type=$(jq -r '.mcpServers | type' "$PLUGIN_JSON" 2>/dev/null)
        if [ "$mcp_type" != "string" ]; then
            echo "ERROR: plugin.json.mcpServers must be a string path (got: $mcp_type)"
            errors=$((errors + 1))
        else
            mcp_path=$(jq -r '.mcpServers' "$PLUGIN_JSON")
            if ! validate_path_safe "$mcp_path" "mcpServers"; then
                errors=$((errors + 1))
            else
                full_path="$REPO_ROOT/$mcp_path"
                if [ ! -f "$full_path" ]; then
                    echo "ERROR: mcpServers file not found: $mcp_path"
                    errors=$((errors + 1))
                else
                    echo "OK: $mcp_path exists"
                fi
            fi
        fi
    fi
fi

echo ""

# --- marketplace.json validation ---

echo "--- marketplace.json ---"

if [ ! -f "$MARKETPLACE_JSON" ]; then
    echo "ERROR: marketplace.json not found at $MARKETPLACE_JSON"
    errors=$((errors + 1))
else
    # Validate JSON is well-formed
    if ! jq empty "$MARKETPLACE_JSON" 2>/dev/null; then
        echo "ERROR: marketplace.json is not valid JSON"
        errors=$((errors + 1))
    else
        echo "OK: marketplace.json is valid JSON"

        # Check required string fields (must be non-empty strings)
        for field in name version description license; do
            if ! jq -e ".$field | type == \"string\" and length > 0" "$MARKETPLACE_JSON" >/dev/null 2>&1; then
                echo "ERROR: marketplace.json.$field must be a non-empty string"
                errors=$((errors + 1))
            else
                value=$(jq -r ".$field" "$MARKETPLACE_JSON")
                echo "OK: marketplace.json.$field = \"$value\""
            fi
        done

        # Check author.name (object with string name field)
        if ! jq -e '.author.name | type == "string" and length > 0' "$MARKETPLACE_JSON" >/dev/null 2>&1; then
            echo "ERROR: marketplace.json.author.name must be a non-empty string"
            errors=$((errors + 1))
        else
            author_name=$(jq -r '.author.name' "$MARKETPLACE_JSON")
            echo "OK: marketplace.json.author.name = \"$author_name\""
        fi

        # Check optional but recommended fields
        for field in repository keywords categories; do
            value=$(jq -r ".$field // empty" "$MARKETPLACE_JSON")
            if [ -z "$value" ] || [ "$value" = "null" ]; then
                echo "WARN: marketplace.json missing recommended field: $field"
                warnings=$((warnings + 1))
            fi
        done

        # Verify version consistency between plugin.json and marketplace.json
        if [ -f "$PLUGIN_JSON" ] && jq empty "$PLUGIN_JSON" 2>/dev/null; then
            plugin_version=$(jq -r '.version // empty' "$PLUGIN_JSON")
            marketplace_version=$(jq -r '.version // empty' "$MARKETPLACE_JSON")
            if [ -n "$plugin_version" ] && [ -n "$marketplace_version" ]; then
                if [ "$plugin_version" != "$marketplace_version" ]; then
                    echo "ERROR: version mismatch -- plugin.json=$plugin_version, marketplace.json=$marketplace_version"
                    errors=$((errors + 1))
                else
                    echo "OK: versions match ($plugin_version)"
                fi
            fi
        fi
    fi
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
