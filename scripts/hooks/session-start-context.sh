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

# Extract TFM from first .csproj found
TFM=""
FIRST_CSPROJ="$(find . -maxdepth 3 -name '*.csproj' -print -quit 2>/dev/null)" || true
if [ -n "$FIRST_CSPROJ" ]; then
    # Extract TargetFramework or first TargetFrameworks entry (portable sed, no PCRE)
    TFM="$(sed -n 's/.*<TargetFramework[s]\{0,1\}>\([^<;]*\).*/\1/p' "$FIRST_CSPROJ" 2>/dev/null | head -1)" || true
fi

# Build context message; inject only for .NET repositories.
CONTEXT=""

# Add routing instruction and project-specific context only when .NET indicators exist
if [ "$SLN_COUNT" -gt 0 ] || [ "$CSPROJ_COUNT" -gt 0 ] || [ "$HAS_GLOBAL_JSON" = true ]; then
    CONTEXT="Mandatory first action for every task: invoke [skill:dotnet-advisor]. Do not plan, reason, design, or implement until it has been invoked, then follow its routing to load additional skills and apply their standards."
    PROJECT_CONTEXT="This is a .NET project"
    if [ -n "$TFM" ]; then
        PROJECT_CONTEXT="This is a .NET project ($TFM)"
    fi
    if [ "$CSPROJ_COUNT" -gt 0 ]; then
        PROJECT_CONTEXT="$PROJECT_CONTEXT with $CSPROJ_COUNT project(s)"
    fi
    if [ "$SLN_COUNT" -gt 0 ]; then
        PROJECT_CONTEXT="$PROJECT_CONTEXT in $SLN_COUNT solution(s)"
    fi
    PROJECT_CONTEXT="$PROJECT_CONTEXT."
    CONTEXT="$CONTEXT $PROJECT_CONTEXT"
fi

if command -v jq >/dev/null 2>&1; then
    jq -Rn --arg additionalContext "$CONTEXT" '{additionalContext: $additionalContext}'
else
    ESCAPED_CONTEXT="$(printf '%s' "$CONTEXT" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\r/\\r/g; s/\t/\\t/g')"
    printf '{"additionalContext":"%s"}\n' "$ESCAPED_CONTEXT"
fi

exit 0
