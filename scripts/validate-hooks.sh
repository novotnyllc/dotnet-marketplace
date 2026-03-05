#!/usr/bin/env bash
#
# validate-hooks.sh -- Contract checks for Claude hook scripts.
#
# Verifies:
#   1. Hooks always emit valid JSON
#   2. Prompt extraction works with jq and without jq
#   3. Reminder suppression works when prompt already requests using-dotnet
#
# This is a behavior test; it does not require a real Claude runtime.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
HOOK_DIR="$REPO_ROOT/scripts/hooks"

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "ERROR: python/python3 is required for hook validation."
    exit 1
fi

assert_json() {
    local payload="$1"
    printf '%s' "$payload" | "$PYTHON_BIN" -c "import json,sys; json.load(sys.stdin)" >/dev/null
}

assert_json_path_contains() {
    local payload="$1"
    local path="$2"
    local expected="$3"
    printf '%s' "$payload" | "$PYTHON_BIN" -c "import json,sys
data = json.load(sys.stdin)
path = sys.argv[1].split('.')
expected = sys.argv[2]
node = data
for part in path:
    if isinstance(node, dict) and part in node:
        node = node[part]
    else:
        raise SystemExit(f'Missing JSON path: {\".\".join(path)}')
if not isinstance(node, str):
    raise SystemExit(f'Path is not a string: {\".\".join(path)}')
if expected not in node:
    raise SystemExit(f'Expected substring not found at {\".\".join(path)}: {expected!r}')" "$path" "$expected"
}

assert_json_path_string() {
    local payload="$1"
    local path="$2"
    printf '%s' "$payload" | "$PYTHON_BIN" -c "import json,sys
data = json.load(sys.stdin)
path = sys.argv[1].split('.')
node = data
for part in path:
    if isinstance(node, dict) and part in node:
        node = node[part]
    else:
        raise SystemExit(f'Missing JSON path: {\".\".join(path)}')
if not isinstance(node, str):
    raise SystemExit(f'Path is not a string: {\".\".join(path)}')" "$path"
}

echo "=== Hook Contract Validation ==="

echo "--- SessionStart hook ---"
SESSION_OUT="$("$HOOK_DIR/session-start-context.sh")"
assert_json "$SESSION_OUT"
assert_json_path_string "$SESSION_OUT" "additionalContext"
SESSION_OUT_NO_JQ="$(DOTNET_ARTISAN_DISABLE_JQ=1 "$HOOK_DIR/session-start-context.sh")"
assert_json "$SESSION_OUT_NO_JQ"
assert_json_path_string "$SESSION_OUT_NO_JQ" "additionalContext"
echo "OK: session-start-context.sh emits valid JSON with/without jq"

echo "--- UserPromptSubmit hook ---"
PROMPT_PAYLOAD='{"prompt":"create a new .NET API with minimal endpoints"}'
PROMPT_OUT="$(printf '%s' "$PROMPT_PAYLOAD" | "$HOOK_DIR/user-prompt-dotnet-reminder.sh")"
assert_json "$PROMPT_OUT"
assert_json_path_contains "$PROMPT_OUT" "hookSpecificOutput.additionalContext" "Mandatory first action"
PROMPT_OUT_NO_JQ="$(printf '%s' "$PROMPT_PAYLOAD" | DOTNET_ARTISAN_DISABLE_JQ=1 "$HOOK_DIR/user-prompt-dotnet-reminder.sh")"
assert_json "$PROMPT_OUT_NO_JQ"
assert_json_path_contains "$PROMPT_OUT_NO_JQ" "hookSpecificOutput.additionalContext" "Mandatory first action"
SUPPRESS_PAYLOAD='{"prompt":"Use $using-dotnet first, then $dotnet-advisor for this .NET request."}'
SUPPRESS_OUT="$(printf '%s' "$SUPPRESS_PAYLOAD" | "$HOOK_DIR/user-prompt-dotnet-reminder.sh")"
assert_json "$SUPPRESS_OUT"
assert_json_path_string "$SUPPRESS_OUT" "hookSpecificOutput.additionalContext"
assert_json_path_contains "$SUPPRESS_OUT" "hookSpecificOutput.additionalContext" ""
if printf '%s' "$SUPPRESS_OUT" | "$PYTHON_BIN" -c "import json,sys; data=json.load(sys.stdin); raise SystemExit(0 if data['hookSpecificOutput']['additionalContext'] else 1)"; then
    echo "ERROR: reminder should be suppressed when prompt already includes using-dotnet"
    exit 1
fi

ADVISOR_ONLY_PAYLOAD='{"prompt":"Use $dotnet-advisor first, then route this .NET request."}'
ADVISOR_ONLY_OUT="$(printf '%s' "$ADVISOR_ONLY_PAYLOAD" | "$HOOK_DIR/user-prompt-dotnet-reminder.sh")"
assert_json "$ADVISOR_ONLY_OUT"
assert_json_path_contains "$ADVISOR_ONLY_OUT" "hookSpecificOutput.additionalContext" "Mandatory first action: invoke [skill:using-dotnet]."

echo "OK: user-prompt-dotnet-reminder.sh enforces using-dotnet first and suppresses only true duplicates"

echo ""
echo "PASSED: hook contract checks"
