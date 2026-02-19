#!/usr/bin/env bash
# UserPromptSubmit hook: inject concise XML reminder on every prompt.

set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

INPUT="$(cat)"
if [ -z "$(echo "$INPUT" | jq -r '.user_prompt // .prompt // .message // empty')" ]; then
  exit 0
fi

MSG=$(cat <<'EOF'
<system-reminder>
<dotnet-artisan-routing>
1. Mandatory first action: invoke [skill:dotnet-advisor].
2. Do not plan, reason, design, or implement until [skill:dotnet-advisor] has been invoked.
3. Follow advisor routing and invoke the relevant downstream skills.
4. Apply standards defined by the routed skills.
</dotnet-artisan-routing>
</system-reminder>
EOF
)

jq -n --arg msg "$MSG" '{systemMessage: $msg, hookSpecificOutput: {hookEventName: "UserPromptSubmit", additionalContext: $msg}}'
exit 0
