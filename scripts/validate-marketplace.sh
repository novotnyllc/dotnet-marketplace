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

# Navigate to repository root (parent of scripts/)
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

PLUGIN_JSON="$REPO_ROOT/.claude-plugin/plugin.json"
MARKETPLACE_JSON="$REPO_ROOT/.claude-plugin/marketplace.json"

errors=0
warnings=0

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

        # Check required top-level fields
        for field in name version description; do
            value=$(jq -r ".$field // empty" "$PLUGIN_JSON")
            if [ -z "$value" ]; then
                echo "ERROR: plugin.json missing required field: $field"
                errors=$((errors + 1))
            else
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
            full_path="$REPO_ROOT/$hooks_path"
            if [ ! -f "$full_path" ]; then
                echo "ERROR: hooks file not found: $hooks_path"
                errors=$((errors + 1))
            else
                echo "OK: $hooks_path exists"
            fi
        fi

        # Validate mcpServers is a string path
        mcp_type=$(jq -r '.mcpServers | type' "$PLUGIN_JSON" 2>/dev/null)
        if [ "$mcp_type" != "string" ]; then
            echo "ERROR: plugin.json.mcpServers must be a string path (got: $mcp_type)"
            errors=$((errors + 1))
        else
            mcp_path=$(jq -r '.mcpServers' "$PLUGIN_JSON")
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

        # Check required fields
        for field in name version description author license; do
            if [ "$field" = "author" ]; then
                # author is an object with name
                author_name=$(jq -r '.author.name // empty' "$MARKETPLACE_JSON")
                if [ -z "$author_name" ]; then
                    echo "ERROR: marketplace.json missing required field: author.name"
                    errors=$((errors + 1))
                else
                    echo "OK: marketplace.json.author.name = \"$author_name\""
                fi
            else
                value=$(jq -r ".$field // empty" "$MARKETPLACE_JSON")
                if [ -z "$value" ]; then
                    echo "ERROR: marketplace.json missing required field: $field"
                    errors=$((errors + 1))
                else
                    echo "OK: marketplace.json.$field = \"$value\""
                fi
            fi
        done

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
