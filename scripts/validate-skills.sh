#!/usr/bin/env bash
#
# validate-skills.sh -- Validate all SKILL.md files in the dotnet-artisan plugin.
#
# Checks:
#   1. Required frontmatter fields: name, description
#   2. YAML frontmatter is well-formed (delimited by --- with valid key: value syntax)
#   3. [skill:name] cross-references point to existing skill directories
#   4. Context budget tracking with stable output keys
#
# Design constraints:
#   - Single-pass scan per file, one batched python3 call for YAML validation
#   - Runs in <5 seconds
#   - Same commands locally and in CI
#   - Exits non-zero on: missing required frontmatter, broken cross-references, BUDGET_STATUS=FAIL
#
# Environment variables:
#   ALLOW_PLANNED_REFS=1  -- Downgrade unresolved cross-references from errors to warnings.
#                            Use during early development when planned skills have no directories yet.
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

# --- Batched YAML validation (single python3 invocation for all files) ---
# Extracts frontmatter from each SKILL.md, validates it as well-formed YAML.
# Outputs one line per file: "OK:<path>" or "FAIL:<path>:<reason>"
declare -A yaml_valid_map
yaml_output=$(python3 -c '
import sys, os, json, re

results = []
for path in sys.argv[1:]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Normalize CRLF
        content = content.replace("\r\n", "\n").replace("\r", "\n")
        lines = content.split("\n")
        if not lines or lines[0].strip() != "---":
            results.append(f"FAIL:{path}:missing opening ---")
            continue
        # Find closing ---
        fm_lines = []
        found_close = False
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                found_close = True
                break
            fm_lines.append(line)
        if not found_close:
            results.append(f"FAIL:{path}:missing closing ---")
            continue
        # Validate each frontmatter line as valid YAML key: value
        for ln_num, fm_line in enumerate(fm_lines, 2):
            stripped = fm_line.strip()
            if not stripped or stripped.startswith("#"):
                continue  # blank lines and comments are valid YAML
            # Must be key: value pattern (key is unquoted identifier, value follows colon+space)
            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*\s*:", stripped):
                results.append(f"FAIL:{path}:line {ln_num}: invalid YAML syntax: {stripped[:60]}")
                break
            # Check for unclosed quotes in the value portion
            colon_pos = stripped.index(":")
            value = stripped[colon_pos+1:].strip()
            if value.startswith("\"") and not value.endswith("\""):
                results.append(f"FAIL:{path}:line {ln_num}: unclosed double quote")
                break
            if value.startswith("'\''") and not value.endswith("'\''"):
                results.append(f"FAIL:{path}:line {ln_num}: unclosed single quote")
                break
        else:
            results.append(f"OK:{path}")
    except Exception as e:
        results.append(f"FAIL:{path}:{e}")

for r in results:
    print(r)
' "${skill_files[@]}" 2>&1)

while IFS= read -r yaml_line; do
    if [[ "$yaml_line" == OK:* ]]; then
        fpath="${yaml_line#OK:}"
        yaml_valid_map["$fpath"]="ok"
    elif [[ "$yaml_line" == FAIL:* ]]; then
        rest="${yaml_line#FAIL:}"
        # Extract path (everything before second colon-delimited field)
        fpath="${rest%%:*}"
        reason="${rest#*:}"
        yaml_valid_map["$fpath"]="fail"
        rel="${fpath#"$REPO_ROOT/"}"
        echo "ERROR: $rel -- invalid YAML frontmatter: $reason"
        errors=$((errors + 1))
    fi
done <<< "$yaml_output"

echo "=== SKILL.md Validation ==="
echo ""

if [ "${ALLOW_PLANNED_REFS:-0}" = "1" ]; then
    echo "NOTE: ALLOW_PLANNED_REFS=1 -- unresolved cross-references downgraded to warnings"
    echo ""
fi

# Validate each SKILL.md file (single-pass: frontmatter + cross-refs in one read)
for skill_file in "${skill_files[@]}"; do
    skill_dir="$(dirname "$skill_file")"
    skill_dirname="$(basename "$skill_dir")"
    rel_path="${skill_file#"$REPO_ROOT/"}"

    # Skip files that failed YAML validation (already reported above)
    if [ "${yaml_valid_map[$skill_file]:-}" = "fail" ]; then
        continue
    fi

    # Read the file content, normalize CRLF to LF
    content="$(<"$skill_file")"
    content="${content//$'\r'/}"

    # Check for frontmatter delimiters (must start with --- and have closing ---)
    if [[ "$content" != ---* ]]; then
        echo "ERROR: $rel_path -- missing YAML frontmatter (file does not start with ---)"
        errors=$((errors + 1))
        continue
    fi

    # Single-pass: extract frontmatter AND collect cross-references from the body
    in_frontmatter=0
    frontmatter=""
    found_close=0
    line_num=0
    declare -A seen_refs=()
    ref_list=()

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
                in_frontmatter=0
                continue
            fi
            frontmatter+="$line"$'\n'
            continue
        fi

        # Body line: extract [skill:name] cross-references via regex
        rest="$line"
        while [[ "$rest" =~ \[skill:([a-zA-Z0-9_-]+)\] ]]; do
            ref_name="${BASH_REMATCH[1]}"
            if [ -z "${seen_refs[$ref_name]+_}" ]; then
                seen_refs["$ref_name"]=1
                ref_list+=("$ref_name")
            fi
            # Advance past the match to find additional refs on the same line
            rest="${rest#*"[skill:${ref_name}]"}"
        done
    done <<< "$content"

    if [ "$found_close" -eq 0 ]; then
        echo "ERROR: $rel_path -- malformed YAML frontmatter (no closing ---)"
        errors=$((errors + 1))
        unset seen_refs
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

    # Validate collected [skill:name] cross-references
    for ref_name in "${ref_list[@]}"; do
        if [ -z "${valid_skill_dirs[$ref_name]+_}" ]; then
            if [ "${ALLOW_PLANNED_REFS:-0}" = "1" ]; then
                echo "WARN:  $rel_path -- unresolved cross-reference [skill:$ref_name] (planned skill, no directory yet)"
                warnings=$((warnings + 1))
            else
                echo "ERROR: $rel_path -- broken cross-reference [skill:$ref_name] (no skill directory found)"
                errors=$((errors + 1))
            fi
        fi
    done

    unset seen_refs

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
