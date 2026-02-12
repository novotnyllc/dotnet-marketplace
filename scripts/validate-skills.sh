#!/usr/bin/env bash
#
# validate-skills.sh -- Validate all SKILL.md files in the dotnet-artisan plugin.
#
# Checks:
#   1. Required frontmatter fields: name, description
#   2. YAML frontmatter is well-formed (parsed via a strict Python parser)
#   3. [skill:name] cross-references point to existing skill directories
#   4. Context budget tracking with stable output keys
#
# Design constraints:
#   - One batched python3 call does all parsing (YAML validation + field extraction + cross-refs)
#   - Bash handles only budget math, reporting, and exit codes
#   - Runs in <5 seconds
#   - Same commands locally and in CI
#   - Exits non-zero on: missing required frontmatter, broken cross-references, BUDGET_STATUS=FAIL
#
# Requirements:
#   - Bash 4+ (uses associative arrays)
#   - python3 (for frontmatter parsing -- no external packages needed)
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

# --- Prerequisites ---

if [ "${BASH_VERSINFO[0]}" -lt 4 ]; then
    echo "ERROR: Bash 4+ required (found ${BASH_VERSION}). Install via Homebrew: brew install bash"
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 required but not found in PATH"
    exit 1
fi

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
# Note: no sort -z (not portable to BSD sort on macOS); order does not matter
skill_files=()
while IFS= read -r -d '' skill_file; do
    skill_files+=("$skill_file")
done < <(find "$REPO_ROOT/skills" -name "SKILL.md" -print0 2>/dev/null)

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

# --- Batched Python3 parsing (single invocation for all files) ---
# Parses frontmatter, extracts fields, and collects cross-references.
# All YAML validation and field extraction happens here for deterministic behavior.
#
# Output format (one JSON object per line, newline-delimited):
#   {"path":"...","valid":true,"name":"...","description":"...","desc_len":N,"refs":["..."]}
#   {"path":"...","valid":false,"error":"..."}
PARSE_SCRIPT=$(mktemp)
trap 'rm -f "$PARSE_SCRIPT"' EXIT
cat > "$PARSE_SCRIPT" << 'PYEOF'
import sys, os, re, json

def parse_yaml_frontmatter(text):
    """Parse simple YAML frontmatter (flat key: value mappings).

    Handles the YAML subset used in SKILL.md files:
    - Simple key: value pairs
    - Quoted string values (single and double)
    - Unquoted scalar values (strings, booleans, numbers)
    - Block scalar indicators (| and >)
    - Comments and blank lines

    Returns a dict of parsed key-value pairs.
    Raises ValueError on malformed input.
    """
    result = {}
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip blank lines and comments
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        # Must be key: value (or key:)
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)', stripped)
        if not m:
            raise ValueError(f"invalid YAML syntax at line {i+2}: {stripped[:60]}")

        key = m.group(1)
        raw_value = m.group(2)

        # Handle block scalars (| and >)
        if raw_value in ("|", ">", "|+", "|-", ">+", ">-"):
            # Collect indented continuation lines
            block_lines = []
            i += 1
            while i < len(lines):
                if lines[i].strip() == "" or (len(lines[i]) > 0 and lines[i][0] in (" ", "\t")):
                    block_lines.append(lines[i])
                    i += 1
                else:
                    break
            # Dedent
            if block_lines:
                indent = len(block_lines[0]) - len(block_lines[0].lstrip())
                value = "\n".join(l[indent:] if len(l) > indent else "" for l in block_lines)
            else:
                value = ""
            if raw_value.startswith(">"):
                value = re.sub(r'(?<!\n)\n(?!\n)', ' ', value)
            result[key] = value.strip()
            continue

        # Handle quoted strings
        if raw_value.startswith('"'):
            if raw_value.endswith('"') and len(raw_value) > 1:
                result[key] = raw_value[1:-1]
            else:
                raise ValueError(f"unclosed double quote at line {i+2}")
            i += 1
            continue

        if raw_value.startswith("'"):
            if raw_value.endswith("'") and len(raw_value) > 1:
                result[key] = raw_value[1:-1]
            else:
                raise ValueError(f"unclosed single quote at line {i+2}")
            i += 1
            continue

        # Handle booleans and other scalars
        if raw_value.lower() in ("true", "yes"):
            result[key] = True
        elif raw_value.lower() in ("false", "no"):
            result[key] = False
        elif raw_value.lower() in ("null", "~", ""):
            result[key] = None
        else:
            result[key] = raw_value

        i += 1

    return result


def extract_refs(body_text):
    """Extract unique [skill:name] cross-references from body text."""
    return list(dict.fromkeys(re.findall(r'\[skill:([a-zA-Z0-9_-]+)\]', body_text)))


def process_file(path):
    """Process a single SKILL.md file. Returns a dict with results."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"path": path, "valid": False, "error": str(e)}

    # Normalize CRLF to LF
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    lines = content.split("\n")

    # Check for opening delimiter
    if not lines or lines[0].strip() != "---":
        return {"path": path, "valid": False, "error": "missing opening ---"}

    # Find closing delimiter and extract frontmatter
    fm_lines = []
    body_start = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            body_start = i + 1
            break
        fm_lines.append(line)

    if body_start is None:
        return {"path": path, "valid": False, "error": "missing closing ---"}

    fm_text = "\n".join(fm_lines)

    # Parse YAML frontmatter
    try:
        parsed = parse_yaml_frontmatter(fm_text)
    except ValueError as e:
        return {"path": path, "valid": False, "error": str(e)}

    if not isinstance(parsed, dict):
        return {"path": path, "valid": False, "error": "frontmatter is not a mapping"}

    # Extract fields from parsed YAML (not regex)
    name = parsed.get("name", "")
    description = parsed.get("description", "")

    if isinstance(name, bool):
        name = str(name).lower()
    if isinstance(description, bool):
        description = str(description).lower()

    name = str(name) if name else ""
    description = str(description) if description else ""

    # Extract cross-references from body
    body_text = "\n".join(lines[body_start:])
    refs = extract_refs(body_text)

    return {
        "path": path,
        "valid": True,
        "name": name,
        "description": description,
        "desc_len": len(description),
        "refs": refs,
    }


# Process all files passed as arguments
skill_paths = sys.argv[1:]
for path in skill_paths:
    result = process_file(path)
    print(json.dumps(result))
PYEOF
python_output=$(python3 "$PARSE_SCRIPT" "${skill_files[@]}")

echo "=== SKILL.md Validation ==="
echo ""

if [ "${ALLOW_PLANNED_REFS:-0}" = "1" ]; then
    echo "NOTE: ALLOW_PLANNED_REFS=1 -- unresolved cross-references downgraded to warnings"
    echo ""
fi

# Process Python output (one JSON object per line)
while IFS= read -r json_line; do
    if [ -z "$json_line" ]; then
        continue
    fi

    # Parse JSON fields using jq (already a dependency from validate-marketplace.sh)
    valid=$(echo "$json_line" | jq -r '.valid')
    fpath=$(echo "$json_line" | jq -r '.path')
    rel_path="${fpath#"$REPO_ROOT/"}"

    if [ "$valid" = "false" ]; then
        err_msg=$(echo "$json_line" | jq -r '.error')
        echo "ERROR: $rel_path -- invalid YAML frontmatter: $err_msg"
        errors=$((errors + 1))
        continue
    fi

    # Extract parsed fields
    name=$(echo "$json_line" | jq -r '.name')
    description=$(echo "$json_line" | jq -r '.description')
    desc_len=$(echo "$json_line" | jq -r '.desc_len')

    # Validate required field: name
    if [ -z "$name" ]; then
        echo "ERROR: $rel_path -- missing required frontmatter field: name"
        errors=$((errors + 1))
    fi

    # Validate required field: description
    if [ -z "$description" ]; then
        echo "ERROR: $rel_path -- missing required frontmatter field: description"
        errors=$((errors + 1))
    else
        total_desc_chars=$((total_desc_chars + desc_len))
        skill_count=$((skill_count + 1))

        if [ "$desc_len" -gt "$MAX_DESC_CHARS" ]; then
            echo "WARN:  $rel_path -- description is $desc_len chars (target: <=$MAX_DESC_CHARS)"
            warnings=$((warnings + 1))
        fi
    fi

    # Validate cross-references
    while IFS= read -r ref_name; do
        if [ -z "$ref_name" ]; then
            continue
        fi
        if [ -z "${valid_skill_dirs[$ref_name]+_}" ]; then
            if [ "${ALLOW_PLANNED_REFS:-0}" = "1" ]; then
                echo "WARN:  $rel_path -- unresolved cross-reference [skill:$ref_name] (planned skill, no directory yet)"
                warnings=$((warnings + 1))
            else
                echo "ERROR: $rel_path -- broken cross-reference [skill:$ref_name] (no skill directory found)"
                errors=$((errors + 1))
            fi
        fi
    done < <(echo "$json_line" | jq -r '.refs[]' 2>/dev/null)

done <<< "$python_output"

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
