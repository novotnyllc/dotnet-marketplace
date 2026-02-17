#!/usr/bin/env bash
#
# session-start-context.sh -- SessionStart hook for .NET project detection.
#
# Checks if the current directory is a .NET project and injects context
# about SDK version and project structure.
#
# Output: JSON with additionalContext on stdout.
# Exit code: always 0 (never blocks).

set -uo pipefail

# Check if current directory contains .NET project indicators
SLN_COUNT=0
CSPROJ_COUNT=0
HAS_GLOBAL_JSON=false

# Count solution files (group -o expressions with parentheses)
SLN_COUNT="$(find . -maxdepth 3 \( -name '*.sln' -o -name '*.slnx' \) 2>/dev/null | wc -l | tr -d ' ')" || SLN_COUNT=0

# Count project files
CSPROJ_COUNT="$(find . -maxdepth 3 -name '*.csproj' 2>/dev/null | wc -l | tr -d ' ')" || CSPROJ_COUNT=0

# Check for global.json
if [ -f "global.json" ]; then
    HAS_GLOBAL_JSON=true
fi

# If no .NET indicators found, exit silently
if [ "$SLN_COUNT" -eq 0 ] && [ "$CSPROJ_COUNT" -eq 0 ] && [ "$HAS_GLOBAL_JSON" = false ]; then
    exit 0
fi

# Extract TFM from first .csproj found
TFM=""
FIRST_CSPROJ="$(find . -maxdepth 3 -name '*.csproj' -print -quit 2>/dev/null)" || true
if [ -n "$FIRST_CSPROJ" ]; then
    # Extract TargetFramework or first TargetFrameworks entry (portable sed, no PCRE)
    TFM="$(sed -n 's/.*<TargetFramework[s]\{0,1\}>\([^<;]*\).*/\1/p' "$FIRST_CSPROJ" 2>/dev/null | head -1)" || true
fi

# Build context message
CONTEXT="This is a .NET project"
if [ -n "$TFM" ]; then
    CONTEXT="This is a .NET project ($TFM)"
fi
if [ "$CSPROJ_COUNT" -gt 0 ]; then
    CONTEXT="$CONTEXT with $CSPROJ_COUNT project(s)"
fi
if [ "$SLN_COUNT" -gt 0 ]; then
    CONTEXT="$CONTEXT in $SLN_COUNT solution(s)"
fi
CONTEXT="$CONTEXT."

echo "{\"additionalContext\": \"$CONTEXT\"}"
exit 0
