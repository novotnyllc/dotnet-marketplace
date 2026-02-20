#!/usr/bin/env bash
#
# generate-changelog.sh -- Generate changelog entries from conventional commits.
#
# Usage:
#   ./scripts/generate-changelog.sh [--dry-run] [--since TAG] [--changelog FILE]
#
# Options:
#   --dry-run       Print generated entries to stdout without modifying CHANGELOG.md
#   --since TAG     Override the starting point (default: derived from plugin.json version)
#   --changelog FILE  Path to CHANGELOG.md (default: CHANGELOG.md in repo root)
#
# When run without --dry-run, inserts generated entries into the [Unreleased]
# section of CHANGELOG.md, preserving any existing manual entries.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$REPO_ROOT"

DRY_RUN=false
SINCE_TAG=""
CHANGELOG="$REPO_ROOT/CHANGELOG.md"
TAG_PREFIX="dotnet-artisan/v"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)     DRY_RUN=true; shift ;;
        --since)       SINCE_TAG="$2"; shift 2 ;;
        --changelog)   CHANGELOG="$2"; shift 2 ;;
        -h|--help)
            sed -n '2,/^$/{ s/^# //; s/^#//; p; }' "$0"
            exit 0
            ;;
        *) echo "ERROR: Unknown option: $1"; exit 1 ;;
    esac
done

# --- Determine commit range ---

if [ -z "$SINCE_TAG" ]; then
    # Derive the since tag from the version in plugin.json (source of truth),
    # not from git tags. Tags are created by auto-tag.yml after merge, so they
    # may not exist locally when running on a branch.
    PLUGIN_JSON="$REPO_ROOT/.claude-plugin/plugin.json"
    if [ -f "$PLUGIN_JSON" ] && command -v jq &>/dev/null; then
        CURRENT_VERSION=$(jq -r '.version' "$PLUGIN_JSON")
        if [ -n "$CURRENT_VERSION" ] && [ "$CURRENT_VERSION" != "null" ]; then
            SINCE_TAG="${TAG_PREFIX}${CURRENT_VERSION}"
        fi
    fi

    # Fall back to tag scan if plugin.json read failed
    if [ -z "$SINCE_TAG" ]; then
        SINCE_TAG=$(git tag --list "${TAG_PREFIX}*" --sort=-version:refname | head -1)
    fi
fi

if [ -n "$SINCE_TAG" ]; then
    # Verify the tag actually exists as a git ref
    if git rev-parse "$SINCE_TAG" &>/dev/null; then
        RANGE="${SINCE_TAG}..HEAD"
        echo "Generating changelog from $SINCE_TAG to HEAD"
    else
        echo "WARN: Tag $SINCE_TAG not found locally -- generating changelog from all commits"
        RANGE=""
    fi
else
    RANGE=""
    echo "No previous tag found -- generating changelog from all commits"
fi

COMMIT_COUNT=$(git log --no-merges --format='%s' $RANGE -- | wc -l | tr -d ' ')
if [ "$COMMIT_COUNT" -eq 0 ]; then
    echo "No commits found in range -- nothing to generate"
    exit 0
fi

echo "  $COMMIT_COUNT commits in range"

# --- Parse and categorize commits ---

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

# One file per Keep-a-Changelog category
for cat in breaking added changed fixed documentation; do
    > "$TMP_DIR/$cat"
done
> "$TMP_DIR/seen"

SKIPPED=0
NONCONVENTIONAL=0

# Process each commit (subject only -- body inspection for BREAKING CHANGE uses a second pass)
while IFS= read -r subject; do
    [ -z "$subject" ] && continue

    # Parse conventional commit: type(scope)!: description
    # Regex stored in variable for bash 3.2 compatibility
    CC_RE='^([a-z]+)(\(([^)]+)\))?(!)?: *(.+)$'
    if [[ "$subject" =~ $CC_RE ]]; then
        TYPE="${BASH_REMATCH[1]}"
        SCOPE="${BASH_REMATCH[3]:-}"
        BANG="${BASH_REMATCH[4]:-}"
        DESC="${BASH_REMATCH[5]}"
    else
        NONCONVENTIONAL=$((NONCONVENTIONAL + 1))
        echo "  SKIP (non-conventional): $subject" >&2
        continue
    fi

    # Filter noise
    if [[ "$TYPE" == "chore" && "$SCOPE" == "release" ]] || [[ "$TYPE" == "chore" && "$SCOPE" == "flow" ]]; then
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    # Capitalize first letter
    DESC="$(echo "${DESC:0:1}" | tr '[:lower:]' '[:upper:]')${DESC:1}"

    # Format bullet
    if [ -n "$SCOPE" ]; then
        LINE="- **${SCOPE}**: ${DESC}"
    else
        LINE="- ${DESC}"
    fi

    # Deduplicate by lowercase description
    DEDUP_KEY=$(echo "$DESC" | tr '[:upper:]' '[:lower:]')
    if grep -qxF "$DEDUP_KEY" "$TMP_DIR/seen" 2>/dev/null; then
        continue
    fi
    echo "$DEDUP_KEY" >> "$TMP_DIR/seen"

    # Route to category
    if [ -n "$BANG" ]; then
        echo "$LINE" >> "$TMP_DIR/breaking"
    else
        case "$TYPE" in
            feat)     echo "$LINE" >> "$TMP_DIR/added" ;;
            fix)      echo "$LINE" >> "$TMP_DIR/fixed" ;;
            docs)     echo "$LINE" >> "$TMP_DIR/documentation" ;;
            *)        echo "$LINE" >> "$TMP_DIR/changed" ;;
        esac
    fi
done < <(git log --no-merges --format='%s' $RANGE --)

# --- Assemble output ---

OUTPUT=""

for section in "breaking:### Breaking" "added:### Added" "changed:### Changed" "fixed:### Fixed" "documentation:### Documentation"; do
    FILE="${section%%:*}"
    HEADER="${section#*:}"

    if [ -s "$TMP_DIR/$FILE" ]; then
        [ -n "$OUTPUT" ] && OUTPUT="${OUTPUT}
"
        OUTPUT="${OUTPUT}${HEADER}

$(cat "$TMP_DIR/$FILE")
"
    fi
done

if [ -z "$OUTPUT" ]; then
    echo "No categorizable commits found"
    exit 0
fi

# --- Dry-run or insert ---

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "=== Generated Changelog Entries ==="
    echo ""
    echo "$OUTPUT"
    echo ""
    echo "($COMMIT_COUNT commits processed, $SKIPPED filtered, $NONCONVENTIONAL non-conventional)"
    exit 0
fi

# Insert into CHANGELOG.md [Unreleased] section
if [ ! -f "$CHANGELOG" ]; then
    echo "ERROR: CHANGELOG.md not found at $CHANGELOG"
    exit 1
fi

# Extract existing [Unreleased] content (between ## [Unreleased] and next ## [)
EXISTING=$(awk '/^## \[Unreleased\]/{flag=1;next}/^## \[/{flag=0}flag' "$CHANGELOG" | sed '/^[[:space:]]*$/d')

# Build replacement content
if [ -n "$EXISTING" ]; then
    NEW_CONTENT="${EXISTING}

${OUTPUT}"
else
    NEW_CONTENT="${OUTPUT}"
fi

# Replace [Unreleased] section content
TMP_FILE=$(mktemp)
awk -v "content=${NEW_CONTENT}" '
/^## \[Unreleased\]/ {
    print
    print ""
    n = split(content, lines, "\n")
    for (i = 1; i <= n; i++) print lines[i]
    print ""
    # Skip old content until next ## [ header
    while ((getline line) > 0) {
        if (line ~ /^## \[/) { print line; break }
    }
    next
}
{print}
' "$CHANGELOG" > "$TMP_FILE" && mv "$TMP_FILE" "$CHANGELOG"

echo "  Inserted entries into [Unreleased] section"
echo "  ($COMMIT_COUNT commits processed, $SKIPPED filtered, $NONCONVENTIONAL non-conventional)"
