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

# Read full stdin into variable
INPUT="$(cat)"

# Extract file_path from tool_input
FILE_PATH="$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')"

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
        echo "{\"systemMessage\": \"Test file modified: $FILENAME. Consider running: dotnet test --filter $TEST_CLASS\"}"
        ;;
    *.cs)
        # C# source file -- run dotnet format if available
        if command -v dotnet >/dev/null 2>&1; then
            FORMAT_OUTPUT="$(dotnet format --include "$FILE_PATH" --verbosity quiet 2>&1)" || true
            echo "{\"systemMessage\": \"dotnet format applied to $FILENAME\"}"
        else
            echo "{\"systemMessage\": \"dotnet not found in PATH -- skipping format. Install .NET SDK to enable auto-formatting.\"}"
        fi
        ;;
    *.csproj)
        # Project file -- suggest restore
        echo "{\"systemMessage\": \"Project file modified: $FILENAME. Consider running: dotnet restore\"}"
        ;;
    *.xaml)
        # XAML file -- check XML well-formedness
        if command -v xmllint >/dev/null 2>&1; then
            if xmllint --noout "$FILE_PATH" 2>/dev/null; then
                echo "{\"systemMessage\": \"XAML validation: $FILENAME is well-formed\"}"
            else
                echo "{\"systemMessage\": \"XAML validation: $FILENAME has XML errors. Check for unclosed tags or invalid syntax.\"}"
            fi
        elif command -v python3 >/dev/null 2>&1; then
            if python3 -c "import xml.etree.ElementTree as ET, sys; ET.parse(sys.argv[1])" "$FILE_PATH" 2>/dev/null; then
                echo "{\"systemMessage\": \"XAML validation: $FILENAME is well-formed\"}"
            else
                echo "{\"systemMessage\": \"XAML validation: $FILENAME has XML errors. Check for unclosed tags or invalid syntax.\"}"
            fi
        else
            echo "{\"systemMessage\": \"No XML validator found (xmllint or python3) -- skipping XAML validation for $FILENAME\"}"
        fi
        ;;
    *)
        # Other file types -- ignore silently
        exit 0
        ;;
esac

exit 0
