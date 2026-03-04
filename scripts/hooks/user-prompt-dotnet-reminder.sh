#!/usr/bin/env bash
# UserPromptSubmit hook: silently inject XML reminder via additionalContext.
set -euo pipefail

# Read optional hook payload from stdin to detect .NET intent even in non-.NET directories.
INPUT_JSON=""
if [ ! -t 0 ]; then
  INPUT_JSON="$(cat || true)"
fi

extract_prompt_text() {
  local json_payload="$1"

  if [ -z "$json_payload" ] || ! command -v jq &>/dev/null; then
    return 0
  fi

  printf '%s' "$json_payload" | jq -r '
    [
      .prompt,
      .userPrompt,
      .message,
      .text,
      .input.prompt,
      .input.userPrompt,
      .input.message,
      .hookInput.prompt,
      .hookInput.userPrompt,
      .hookInput.message,
      .hookSpecificInput.prompt,
      .hookSpecificInput.userPrompt,
      .hookSpecificInput.message,
      .payload.prompt,
      .payload.userPrompt
    ]
    | map(select(type == "string" and length > 0))
    | .[0] // ""
  ' 2>/dev/null || true
}

PROMPT_TEXT="$(extract_prompt_text "$INPUT_JSON")"

# Check if current directory looks like a .NET repo.
SLN_COUNT="$(find . -maxdepth 3 \( -name '*.sln' -o -name '*.slnx' \) 2>/dev/null | wc -l | tr -d ' ')" || SLN_COUNT=0
CSPROJ_COUNT="$(find . -maxdepth 3 -name '*.csproj' 2>/dev/null | wc -l | tr -d ' ')" || CSPROJ_COUNT=0
CS_COUNT="$(find . -maxdepth 4 -name '*.cs' 2>/dev/null | wc -l | tr -d ' ')" || CS_COUNT=0
HAS_GLOBAL_JSON=false
if [ -f "global.json" ]; then
  HAS_GLOBAL_JSON=true
fi

DOTNET_PROMPT=false
if [ -n "$PROMPT_TEXT" ]; then
  if printf '%s' "$PROMPT_TEXT" | grep -Eiq '(^|[^[:alnum:]_])(dotnet|\.net|c#|csproj|slnx?|msbuild|nuget|roslyn|xunit|asp\.?net|blazor|maui|winui|wpf|winforms|entity framework|ef core|benchmarkdotnet|f#)([^[:alnum:]_]|$)'; then
    DOTNET_PROMPT=true
  fi
fi

MSG=""
if [ "$SLN_COUNT" -gt 0 ] || [ "$CSPROJ_COUNT" -gt 0 ] || [ "$CS_COUNT" -gt 0 ] || [ "$HAS_GLOBAL_JSON" = true ] || [ "$DOTNET_PROMPT" = true ]; then
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
fi

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
