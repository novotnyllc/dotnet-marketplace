#!/usr/bin/env bash
# UserPromptSubmit hook: silently inject XML reminder via additionalContext.
set -euo pipefail

read -r -d '' MSG <<'EOF' || true
<system-reminder>
<dotnet-artisan-routing>
1. Mandatory first action: invoke [skill:dotnet-advisor].
2. Do not plan, reason, design, or implement until [skill:dotnet-advisor] has been invoked.
3. Follow advisor routing and invoke the relevant downstream skills.
4. Apply standards defined by the routed skills.
</dotnet-artisan-routing>
</system-reminder>
EOF

if command -v jq &>/dev/null; then
  jq -n --arg ctx "$MSG" '{
    hookSpecificOutput: {
      hookEventName: "UserPromptSubmit",
      additionalContext: $ctx
    }
  }'
else
  # Fallback: manual JSON with printf escaping newlines
  ESCAPED=$(printf '%s' "$MSG" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr '\n' ' ' | sed 's/ /\\n/g')
  printf '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"%s"}}\n' "$ESCAPED"
fi

exit 0