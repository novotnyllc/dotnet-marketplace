#!/usr/bin/env bash
# UserPromptSubmit hook: silently inject XML reminder via additionalContext.
set -euo pipefail

has_jq() {
  [ "${DOTNET_ARTISAN_DISABLE_JQ:-0}" != "1" ] && command -v jq >/dev/null 2>&1
}

python_cmd() {
  if [ "${DOTNET_ARTISAN_DISABLE_PYTHON:-0}" = "1" ] || [ "${DOTNET_ARTISAN_DISABLE_PYTHON3:-0}" = "1" ]; then
    return 1
  fi

  if command -v python3 >/dev/null 2>&1; then
    echo "python3"
    return 0
  fi

  if command -v python >/dev/null 2>&1; then
    echo "python"
    return 0
  fi

  return 1
}

has_python() {
  python_cmd >/dev/null 2>&1
}

# Read optional hook payload from stdin to detect .NET intent even in non-.NET directories.
INPUT_JSON=""
if [ ! -t 0 ]; then
  INPUT_JSON="$(cat || true)"
fi

extract_prompt_text() {
  local json_payload="$1"

  if [ -z "$json_payload" ]; then
    return 0
  fi

  if has_jq; then
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
    return 0
  fi

  if has_python; then
    local py
    py="$(python_cmd)"
    printf '%s' "$json_payload" | "$py" -c "import json, sys
try:
    payload = json.load(sys.stdin)
except Exception:
    print('', end='')
    raise SystemExit(0)
if not isinstance(payload, dict):
    print('', end='')
    raise SystemExit(0)
candidates = [
    payload.get('prompt'),
    payload.get('userPrompt'),
    payload.get('message'),
    payload.get('text'),
]
for key in ('input', 'hookInput', 'hookSpecificInput', 'payload'):
    node = payload.get(key)
    if isinstance(node, dict):
        candidates.extend([node.get('prompt'), node.get('userPrompt'), node.get('message')])
for item in candidates:
    if isinstance(item, str) and item:
        print(item, end='')
        break"
  fi
}

PROMPT_TEXT="$(extract_prompt_text "$INPUT_JSON")"

emit_user_prompt_context() {
  local ctx="$1"

  if has_jq; then
    jq -n --arg ctx "$ctx" '{
      hookSpecificOutput: {
        hookEventName: "UserPromptSubmit",
        additionalContext: $ctx
      }
    }'
    return 0
  fi

  # Fallback JSON encoder when jq is unavailable.
  local escaped
  escaped="$(printf '%s' "$ctx" | sed -e ':a' -e 'N' -e '$!ba' -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r/\\r/g' -e 's/\t/\\t/g' -e 's/\n/\\n/g')"
  printf '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"%s"}}\n' "$escaped"
}

# Check if current directory looks like a .NET repo using first-hit scans.
HAS_SOLUTION=false
if find . -maxdepth 3 \( -name '*.sln' -o -name '*.slnx' \) -print -quit 2>/dev/null | grep -q .; then
  HAS_SOLUTION=true
fi

HAS_CSPROJ=false
if find . -maxdepth 3 -name '*.csproj' -print -quit 2>/dev/null | grep -q .; then
  HAS_CSPROJ=true
fi

HAS_CS=false
if find . -maxdepth 4 -name '*.cs' -print -quit 2>/dev/null | grep -q .; then
  HAS_CS=true
fi

HAS_GLOBAL_JSON=false
if [ -f "global.json" ]; then
  HAS_GLOBAL_JSON=true
fi

IS_DOTNET_REPO=false
if [ "$HAS_SOLUTION" = true ] || [ "$HAS_CSPROJ" = true ] || [ "$HAS_CS" = true ] || [ "$HAS_GLOBAL_JSON" = true ]; then
  IS_DOTNET_REPO=true
fi

DOTNET_PROMPT=false
ALREADY_REQUESTS_USING_DOTNET=false
if [ -n "$PROMPT_TEXT" ]; then
  if printf '%s' "$PROMPT_TEXT" | grep -Eiq '(^|[^[:alnum:]_])(dotnet|\.net|c#|csproj|slnx?|msbuild|nuget|roslyn|xunit|asp\.?net|blazor|maui|winui|wpf|winforms|entity framework|ef core|benchmarkdotnet|f#)([^[:alnum:]_]|$)'; then
    DOTNET_PROMPT=true
  fi

  # Suppress reminders only when step 1 is already explicit.
  # Mentioning dotnet-advisor alone is not enough because using-dotnet
  # must run first in the contract.
  if printf '%s' "$PROMPT_TEXT" | grep -Eiq '(\$using-dotnet|\[skill:using-dotnet\]|(^|[^[:alnum:]_-])using-dotnet([^[:alnum:]_-]|$))'; then
    ALREADY_REQUESTS_USING_DOTNET=true
  fi
fi

MSG=""
if { [ "$IS_DOTNET_REPO" = true ] || [ "$DOTNET_PROMPT" = true ]; } && [ "$ALREADY_REQUESTS_USING_DOTNET" = false ]; then
  read -r -d '' MSG <<'EOF' || true
<system-reminder>
<dotnet-artisan-routing>
1. Mandatory first action: invoke [skill:using-dotnet].
2. Mandatory second action: invoke [skill:dotnet-advisor].
3. Do not plan, reason, design, or implement until both routing skills have been invoked.
4. Follow advisor routing and invoke the relevant downstream skills.
5. Apply standards defined by the routed skills.
</dotnet-artisan-routing>
</system-reminder>
EOF
fi

emit_user_prompt_context "$MSG"

exit 0
