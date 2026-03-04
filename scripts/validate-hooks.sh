#!/usr/bin/env bash
#
# validate-hooks.sh -- Contract checks for Claude hook scripts.
#
# Verifies:
#   1. Hooks always emit valid JSON
#   2. Prompt/file-path extraction works with jq and without jq
#   3. Fallback branches are deterministic (no jq, no dotnet, no xmllint)
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

build_payload() {
    local file_path="$1"
    "$PYTHON_BIN" -c "import json,sys; print(json.dumps({'tool_input': {'file_path': sys.argv[1]}}))" "$file_path"
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
echo "OK: user-prompt-dotnet-reminder.sh detects .NET intent with/without jq"

echo "--- PostToolUse hook ---"
CSPROJ_PAYLOAD='{"tool_input":{"file_path":"src/Foo.csproj"}}'
CSPROJ_OUT="$(printf '%s' "$CSPROJ_PAYLOAD" | "$HOOK_DIR/post-edit-dotnet.sh")"
assert_json "$CSPROJ_OUT"
assert_json_path_contains "$CSPROJ_OUT" "systemMessage" "dotnet restore"
CSPROJ_OUT_NO_JQ="$(printf '%s' "$CSPROJ_PAYLOAD" | DOTNET_ARTISAN_DISABLE_JQ=1 "$HOOK_DIR/post-edit-dotnet.sh")"
assert_json "$CSPROJ_OUT_NO_JQ"
assert_json_path_contains "$CSPROJ_OUT_NO_JQ" "systemMessage" "dotnet restore"
CS_PAYLOAD='{"tool_input":{"file_path":"src/Foo.cs"}}'
CS_OUT_NO_DOTNET="$(printf '%s' "$CS_PAYLOAD" | DOTNET_ARTISAN_DISABLE_DOTNET=1 "$HOOK_DIR/post-edit-dotnet.sh")"
assert_json "$CS_OUT_NO_DOTNET"
assert_json_path_contains "$CS_OUT_NO_DOTNET" "systemMessage" "dotnet not found"

TMP_XAML="$(mktemp "${TMPDIR:-/tmp}/dotnet-artisan-hook-xaml.XXXXXX.xaml")"
trap 'rm -f "$TMP_XAML"' EXIT
printf '<Grid></Grid>\n' > "$TMP_XAML"
XAML_PAYLOAD="$(build_payload "$TMP_XAML")"
XAML_OUT="$(printf '%s' "$XAML_PAYLOAD" | DOTNET_ARTISAN_DISABLE_XMLLINT=1 "$HOOK_DIR/post-edit-dotnet.sh")"
assert_json "$XAML_OUT"
assert_json_path_contains "$XAML_OUT" "systemMessage" "well-formed"
echo "OK: post-edit-dotnet.sh handles parsing/output fallback paths"

echo ""
echo "PASSED: hook contract checks"
