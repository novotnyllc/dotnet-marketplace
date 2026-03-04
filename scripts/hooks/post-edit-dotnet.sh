#!/usr/bin/env bash
#
# post-edit-dotnet.sh -- PostToolUse hook for Write|Edit events.
#
# Reads JSON from stdin, extracts tool_input.file_path, and dispatches
# by file extension: test files, .cs, .csproj, .xaml.
#
# Output: JSON with systemMessage on stdout.
# Exit code: always 0 (never blocks; advise only).

set -euo pipefail

emit_system_message() {
    local message="$1"

    if command -v jq >/dev/null 2>&1; then
        jq -Rn --arg msg "$message" '{systemMessage: $msg}'
        return 0
    fi

    local escaped
    escaped="$(printf '%s' "$message" | sed -e ':a' -e 'N' -e '$!ba' -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r/\\r/g' -e 's/\t/\\t/g' -e 's/\n/\\n/g')"
    printf '{"systemMessage":"%s"}\n' "$escaped"
}

extract_file_path() {
    local json_payload="$1"

    if [ -z "$json_payload" ]; then
        return 0
    fi

    if command -v jq >/dev/null 2>&1; then
        printf '%s' "$json_payload" | jq -r '.tool_input.file_path // .toolInput.file_path // empty' 2>/dev/null || true
        return 0
    fi

    if command -v python3 >/dev/null 2>&1; then
        printf '%s' "$json_payload" | python3 -c "import json, sys
try:
    payload = json.load(sys.stdin)
except Exception:
    print('', end='')
    raise SystemExit(0)
if not isinstance(payload, dict):
    print('', end='')
    raise SystemExit(0)
for key in ('tool_input', 'toolInput'):
    candidate = payload.get(key)
    if isinstance(candidate, dict):
        path = candidate.get('file_path')
        if isinstance(path, str) and path:
            print(path, end='')
            break"
    fi
}

# Read full stdin into variable
INPUT="$(cat || true)"
FILE_PATH="$(extract_file_path "$INPUT")"

# If no file path, nothing to do
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Extract just the filename for pattern matching
FILENAME="$(basename "$FILE_PATH")"

case "$FILE_PATH" in
    *Tests.cs|*Test.cs)
        # Test file -- suggest running related tests
        TEST_CLASS="${FILENAME%.cs}"
        emit_system_message "Test file modified: $FILENAME. Consider running: dotnet test --filter $TEST_CLASS"
        ;;
    *.cs)
        # C# source file -- run dotnet format if available
        if command -v dotnet >/dev/null 2>&1; then
            if dotnet format --include "$FILE_PATH" --verbosity quiet >/dev/null 2>&1; then
                emit_system_message "dotnet format applied to $FILENAME"
            else
                emit_system_message "dotnet format could not format $FILENAME automatically. Consider running: dotnet format --include \"$FILE_PATH\""
            fi
        else
            emit_system_message "dotnet not found in PATH -- skipping format. Install .NET SDK to enable auto-formatting."
        fi
        ;;
    *.csproj)
        # Project file -- suggest restore
        emit_system_message "Project file modified: $FILENAME. Consider running: dotnet restore"
        ;;
    *.xaml)
        # XAML file -- check XML well-formedness
        if command -v xmllint >/dev/null 2>&1; then
            if xmllint --noout "$FILE_PATH" 2>/dev/null; then
                emit_system_message "XAML validation: $FILENAME is well-formed"
            else
                emit_system_message "XAML validation: $FILENAME has XML errors. Check for unclosed tags or invalid syntax."
            fi
        elif command -v python3 >/dev/null 2>&1; then
            if python3 -c "import xml.etree.ElementTree as ET, sys; ET.parse(sys.argv[1])" "$FILE_PATH" 2>/dev/null; then
                emit_system_message "XAML validation: $FILENAME is well-formed"
            else
                emit_system_message "XAML validation: $FILENAME has XML errors. Check for unclosed tags or invalid syntax."
            fi
        else
            emit_system_message "No XML validator found (xmllint or python3) -- skipping XAML validation for $FILENAME"
        fi
        ;;
    *)
        # Other file types -- ignore silently
        exit 0
        ;;
esac

exit 0
