#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
RUNNER="$REPO_ROOT/tests/agent-routing/check-skills.cs"
CASES="$REPO_ROOT/tests/agent-routing/cases.json"
FIXTURES="$REPO_ROOT/tests/agent-routing/fixtures"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    cat <<'EOF'
Usage:
  ./test.sh fixtures [extra runner args...]
  ./test.sh live [extra runner args...]

Examples:
  ./test.sh fixtures
  ./test.sh live
  ./test.sh live --agents codex --category api
EOF
    exit 0
fi

mode="${1:-live}"
if [[ $# -gt 0 ]]; then
    shift
fi

if [[ ! -f "$RUNNER" ]]; then
    echo "ERROR: Runner not found: $RUNNER"
    exit 1
fi

case "$mode" in
    fixtures)
        exec dotnet run --file "$RUNNER" -- \
            --mode fixtures \
            --input "$FIXTURES" \
            --run-all \
            "$@"
        ;;
    live)
        exec dotnet run --file "$RUNNER" -- \
            --mode live \
            --input "$CASES" \
            --run-all \
            "$@"
        ;;
    *)
        echo "ERROR: Unknown mode '$mode' (expected: fixtures|live)"
        echo "Run: ./test.sh --help"
        exit 2
        ;;
esac
