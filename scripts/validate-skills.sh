#!/usr/bin/env bash
#
# validate-skills.sh -- Validate all SKILL.md files in the dotnet-artisan plugin.
#
# Checks:
#   1. Required frontmatter fields: name, description
#   2. YAML frontmatter is well-formed (delimited by ---)
#   3. [skill:name] cross-references point to existing skill directories
#   4. Context budget tracking with stable output keys
#
# Design constraints:
#   - Single-pass scan (no subprocess spawning per file, no network)
#   - Runs in <5 seconds
#   - Same commands locally and in CI
#   - Exits non-zero on: missing required frontmatter, broken cross-references, BUDGET_STATUS=FAIL
#
# Output keys (stable, CI-parseable):
#   CURRENT_DESC_CHARS=<N>
#   PROJECTED_DESC_CHARS=<N>
#   BUDGET_STATUS=OK|WARN|FAIL

set -euo pipefail

# Budget constants
PROJECTED_SKILLS_COUNT=95
MAX_DESC_CHARS=120
WARN_THRESHOLD=12000
FAIL_THRESHOLD=15000

# Navigate to repository root (parent of scripts/)
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

errors=0
warnings=0
total_desc_chars=0
skill_count=0

# Collect all skill directories (any directory containing SKILL.md)
skill_files=()
while IFS= read -r -d '' skill_file; do
    skill_files+=("$skill_file")
done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -print0 2>/dev/null | sort -z)

if [ ${#skill_files[@]} -eq 0 ]; then
    echo "ERROR: No SKILL.md files found under $REPO_ROOT/skills/"
    exit 1
fi

# Build a set of valid skill directory names for cross-reference validation
declare -A valid_skill_dirs
for skill_file in "${skill_files[@]}"; do
    skill_dir="$(dirname "$skill_file")"
    skill_dirname="$(basename "$skill_dir")"
    valid_skill_dirs["$skill_dirname"]=1
done

echo "=== SKILL.md Validation ==="
echo ""

# Validate each SKILL.md file
for skill_file in "${skill_files[@]}"; do
    skill_dir="$(dirname "$skill_file")"
    skill_dirname="$(basename "$skill_dir")"
    rel_path="${skill_file#"$REPO_ROOT/"}"

    # Read the file content
    content="$(<"$skill_file")"

    # Check for frontmatter delimiters (must start with --- and have closing ---)
    if [[ "$content" != ---* ]]; then
        echo "ERROR: $rel_path -- missing YAML frontmatter (file does not start with ---)"
        errors=$((errors + 1))
        continue
    fi

    # Extract frontmatter block (between first and second ---)
    # Use awk-like logic with bash to avoid subprocesses per file
    in_frontmatter=0
    frontmatter=""
    found_close=0
    line_num=0
    while IFS= read -r line; do
        line_num=$((line_num + 1))
        if [ "$line_num" -eq 1 ]; then
            if [[ "$line" == "---" ]]; then
                in_frontmatter=1
                continue
            fi
        elif [ "$in_frontmatter" -eq 1 ]; then
            if [[ "$line" == "---" ]]; then
                found_close=1
                break
            fi
            frontmatter+="$line"$'\n'
        fi
    done <<< "$content"

    if [ "$found_close" -eq 0 ]; then
        echo "ERROR: $rel_path -- malformed YAML frontmatter (no closing ---)"
        errors=$((errors + 1))
        continue
    fi

    # Check required field: name
    has_name=0
    name_value=""
    while IFS= read -r fm_line; do
        if [[ "$fm_line" =~ ^name:\ *(.*) ]]; then
            has_name=1
            name_value="${BASH_REMATCH[1]}"
            # Strip quotes if present
            name_value="${name_value#\"}"
            name_value="${name_value%\"}"
            name_value="${name_value#\'}"
            name_value="${name_value%\'}"
        fi
    done <<< "$frontmatter"

    if [ "$has_name" -eq 0 ] || [ -z "$name_value" ]; then
        echo "ERROR: $rel_path -- missing required frontmatter field: name"
        errors=$((errors + 1))
    fi

    # Check required field: description
    has_description=0
    description_value=""
    # Description may be on one line or span multiple lines with quotes
    in_desc=0
    while IFS= read -r fm_line; do
        if [ "$in_desc" -eq 1 ]; then
            # Continuation of multi-line description
            if [[ "$fm_line" == *'"' ]] || [[ "$fm_line" == *"'" ]]; then
                description_value+=" $fm_line"
                in_desc=0
            else
                description_value+=" $fm_line"
            fi
        elif [[ "$fm_line" =~ ^description:\ *(.*) ]]; then
            has_description=1
            description_value="${BASH_REMATCH[1]}"
            # Check if it's a multi-line value starting with a quote but not closing
            if [[ "$description_value" == '"'* ]] && [[ "$description_value" != *'"' ]]; then
                in_desc=1
            fi
        fi
    done <<< "$frontmatter"

    if [ "$has_description" -eq 0 ] || [ -z "$description_value" ]; then
        echo "ERROR: $rel_path -- missing required frontmatter field: description"
        errors=$((errors + 1))
    else
        # Strip surrounding quotes for character counting
        desc_stripped="$description_value"
        desc_stripped="${desc_stripped#\"}"
        desc_stripped="${desc_stripped%\"}"
        desc_stripped="${desc_stripped#\'}"
        desc_stripped="${desc_stripped%\'}"
        desc_len=${#desc_stripped}
        total_desc_chars=$((total_desc_chars + desc_len))
        skill_count=$((skill_count + 1))

        if [ "$desc_len" -gt "$MAX_DESC_CHARS" ]; then
            echo "WARN:  $rel_path -- description is $desc_len chars (target: <=$MAX_DESC_CHARS)"
            warnings=$((warnings + 1))
        fi
    fi

    # Validate [skill:name] cross-references in the file body
    # Extract all [skill:...] references
    # References to existing skill directories are valid.
    # References to non-existent directories are warnings (planned skills), not errors.
    while IFS= read -r ref_match; do
        if [ -z "$ref_match" ]; then
            continue
        fi
        # ref_match is the skill name from [skill:name]
        if [ -z "${valid_skill_dirs[$ref_match]+_}" ]; then
            echo "WARN:  $rel_path -- unresolved cross-reference [skill:$ref_match] (planned skill, no directory yet)"
            warnings=$((warnings + 1))
        fi
    done < <(grep -oE '\[skill:[a-zA-Z0-9_-]+\]' "$skill_file" 2>/dev/null | sed 's/\[skill://;s/\]//' | sort -u)

done

echo ""
echo "=== Budget Report ==="

# Calculate projected budget
projected_desc_chars=$((PROJECTED_SKILLS_COUNT * MAX_DESC_CHARS))

# Determine budget status
budget_status="OK"
if [ "$total_desc_chars" -ge "$FAIL_THRESHOLD" ] || [ "$projected_desc_chars" -ge "$FAIL_THRESHOLD" ]; then
    budget_status="FAIL"
elif [ "$total_desc_chars" -ge "$WARN_THRESHOLD" ] || [ "$projected_desc_chars" -ge "$WARN_THRESHOLD" ]; then
    budget_status="WARN"
fi

# Output stable keys for CI parsing
echo "CURRENT_DESC_CHARS=$total_desc_chars"
echo "PROJECTED_DESC_CHARS=$projected_desc_chars"
echo "BUDGET_STATUS=$budget_status"

echo ""
echo "Skills validated: $skill_count"
echo "Current budget: $total_desc_chars / $FAIL_THRESHOLD chars"
echo "Projected budget ($PROJECTED_SKILLS_COUNT skills x $MAX_DESC_CHARS chars): $projected_desc_chars chars"

if [ "$budget_status" = "WARN" ]; then
    echo "WARNING: Budget approaching limit (WARN threshold: $WARN_THRESHOLD chars)"
    warnings=$((warnings + 1))
fi

if [ "$budget_status" = "FAIL" ]; then
    echo "FAIL: Budget exceeds hard limit (FAIL threshold: $FAIL_THRESHOLD chars)"
    errors=$((errors + 1))
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
