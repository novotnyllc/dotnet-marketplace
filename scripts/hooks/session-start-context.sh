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

has_jq() {
    [ "${DOTNET_ARTISAN_DISABLE_JQ:-0}" != "1" ] && command -v jq >/dev/null 2>&1
}

# Check if current directory contains .NET project indicators using first-hit scans.
HAS_SOLUTION=false
if find . -maxdepth 3 \( -name '*.sln' -o -name '*.slnx' \) -print -quit 2>/dev/null | grep -q .; then
    HAS_SOLUTION=true
fi

HAS_CSPROJ=false
if find . -maxdepth 3 -name '*.csproj' -print -quit 2>/dev/null | grep -q .; then
    HAS_CSPROJ=true
fi

HAS_GLOBAL_JSON=false
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
if [ "$HAS_SOLUTION" = true ] || [ "$HAS_CSPROJ" = true ] || [ "$HAS_GLOBAL_JSON" = true ]; then
    CONTEXT="Mandatory first action for every task: invoke [skill:using-dotnet]. Mandatory second action: invoke [skill:dotnet-advisor]. Do not plan, reason, design, or implement until both have been invoked, then follow advisor routing to load additional skills and apply their standards."
    PROJECT_CONTEXT="This is a .NET project"
    if [ -n "$TFM" ]; then
        PROJECT_CONTEXT="This is a .NET project ($TFM)"
    fi
    if [ "$HAS_CSPROJ" = true ]; then
        PROJECT_CONTEXT="$PROJECT_CONTEXT with project files"
    fi
    if [ "$HAS_SOLUTION" = true ]; then
        PROJECT_CONTEXT="$PROJECT_CONTEXT in solution files"
    fi
    if [ "$HAS_GLOBAL_JSON" = true ]; then
        PROJECT_CONTEXT="$PROJECT_CONTEXT and global.json"
    fi
    PROJECT_CONTEXT="$PROJECT_CONTEXT."
    CONTEXT="$CONTEXT $PROJECT_CONTEXT"
fi

if has_jq; then
    jq -Rn --arg additionalContext "$CONTEXT" '{additionalContext: $additionalContext}'
else
    ESCAPED_CONTEXT="$(printf '%s' "$CONTEXT" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\r/\\r/g; s/\t/\\t/g')"
    printf '{"additionalContext":"%s"}\n' "$ESCAPED_CONTEXT"
fi

exit 0
