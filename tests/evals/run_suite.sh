#!/usr/bin/env bash
# run_suite.sh -- Run all 4 eval types and capture results + metrics
#
# Usage:
#   ANTHROPIC_API_KEY=sk-... ./tests/evals/run_suite.sh
#   ./tests/evals/run_suite.sh --dry-run
#
# Environment:
#   ANTHROPIC_API_KEY  Required for real runs (not dry-run)
#   RUNS               Number of runs per case (default: 3)
#
# Output:
#   - Individual result JSON files in tests/evals/results/
#   - Summary metrics printed to stderr
#   - Suite summary JSON written to tests/evals/results/suite_summary.json

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
EVALS_DIR="$REPO_ROOT/tests/evals"
RESULTS_DIR="$EVALS_DIR/results"
RUNS="${RUNS:-3}"
DRY_RUN=""

# Parse args
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN="--dry-run" ;;
    --runs=*) RUNS="${arg#--runs=}" ;;
    *) echo "Unknown arg: $arg" >&2; exit 1 ;;
  esac
done

mkdir -p "$RESULTS_DIR"

# Check API key unless dry-run
if [ -z "$DRY_RUN" ]; then
  if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    echo "ERROR: ANTHROPIC_API_KEY is not set. Set it or use --dry-run." >&2
    exit 1
  fi
  echo "[suite] ANTHROPIC_API_KEY is set (length=${#ANTHROPIC_API_KEY})" >&2
fi

echo "[suite] Starting eval suite (runs=$RUNS)" >&2
echo "[suite] Results dir: $RESULTS_DIR" >&2

SUITE_START=$(date +%s)
ABORT_DETECTED=0

# Helper to extract cost from runner output
extract_cost() {
  local output="$1"
  echo "$output" | grep -o 'Total cost: \$[0-9.]*' | grep -o '[0-9.]*' 2>/dev/null || echo "0"
}

# --- L3 Activation ---
echo "" >&2
echo "============================================" >&2
echo "[suite] Running L3 Activation eval..." >&2
echo "============================================" >&2
ACT_OUTPUT=$(python3 "$EVALS_DIR/run_activation.py" --runs "$RUNS" $DRY_RUN 2>&1) || true
echo "$ACT_OUTPUT" >&2

if echo "$ACT_OUTPUT" | grep -q "ABORT"; then
  echo "[suite] WARNING: Activation runner aborted (cost cap)" >&2
  ABORT_DETECTED=1
fi

ACT_COST=$(extract_cost "$ACT_OUTPUT")

# --- L4 Confusion ---
echo "" >&2
echo "============================================" >&2
echo "[suite] Running L4 Confusion Matrix eval..." >&2
echo "============================================" >&2
CONF_OUTPUT=$(python3 "$EVALS_DIR/run_confusion_matrix.py" --runs "$RUNS" $DRY_RUN 2>&1) || true
echo "$CONF_OUTPUT" >&2

if echo "$CONF_OUTPUT" | grep -q "ABORT"; then
  echo "[suite] WARNING: Confusion runner aborted (cost cap)" >&2
  ABORT_DETECTED=1
fi

CONF_COST=$(extract_cost "$CONF_OUTPUT")

# --- L5 Effectiveness ---
echo "" >&2
echo "============================================" >&2
echo "[suite] Running L5 Effectiveness eval..." >&2
echo "============================================" >&2
EFF_OUTPUT=$(python3 "$EVALS_DIR/run_effectiveness.py" --runs "$RUNS" $DRY_RUN 2>&1) || true
echo "$EFF_OUTPUT" >&2

if echo "$EFF_OUTPUT" | grep -q "ABORT"; then
  echo "[suite] WARNING: Effectiveness runner aborted (cost cap)" >&2
  ABORT_DETECTED=1
fi

EFF_COST=$(extract_cost "$EFF_OUTPUT")

# --- L6 Size Impact ---
echo "" >&2
echo "============================================" >&2
echo "[suite] Running L6 Size Impact eval..." >&2
echo "============================================" >&2
SIZE_OUTPUT=$(python3 "$EVALS_DIR/run_size_impact.py" --runs "$RUNS" $DRY_RUN 2>&1) || true
echo "$SIZE_OUTPUT" >&2

if echo "$SIZE_OUTPUT" | grep -q "ABORT"; then
  echo "[suite] WARNING: Size impact runner aborted (cost cap)" >&2
  ABORT_DETECTED=1
fi

SIZE_COST=$(extract_cost "$SIZE_OUTPUT")

# --- Suite Summary ---
SUITE_END=$(date +%s)
SUITE_DURATION=$((SUITE_END - SUITE_START))

# Calculate total cost
TOTAL_COST=$(python3 -c "print(round($ACT_COST + $CONF_COST + $EFF_COST + $SIZE_COST, 4))")

echo "" >&2
echo "============================================" >&2
echo "[suite] === Suite Complete ===" >&2
echo "  Duration: ${SUITE_DURATION}s" >&2
echo "  Total cost: \$$TOTAL_COST" >&2
echo "  Abort detected: $ABORT_DETECTED" >&2
echo "============================================" >&2

# Count result files
RESULT_COUNT=$(find "$RESULTS_DIR" -maxdepth 1 -name '*.json' -not -name 'suite_summary.json' 2>/dev/null | wc -l | tr -d ' ')
echo "  Result files: $RESULT_COUNT" >&2

# Write suite summary (only for real runs)
if [ -z "$DRY_RUN" ]; then
  python3 -c "
import json, glob, os
from datetime import datetime, timezone

results_dir = '$RESULTS_DIR'
files = sorted(glob.glob(os.path.join(results_dir, '*.json')))

# Read latest result for each eval type
latest = {}
for f in files:
    if os.path.basename(f) == 'suite_summary.json':
        continue
    with open(f) as fh:
        data = json.load(fh)
    eval_type = data.get('meta', {}).get('eval_type', 'unknown')
    latest[eval_type] = {
        'file': os.path.basename(f),
        'run_id': data.get('meta', {}).get('run_id'),
        'cost': data.get('meta', {}).get('total_cost', 0),
        'summary': data.get('summary', {}),
    }

suite = {
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'duration_seconds': $SUITE_DURATION,
    'total_cost': $TOTAL_COST,
    'abort_detected': bool($ABORT_DETECTED),
    'runs': $RUNS,
    'eval_types': latest,
}

with open(os.path.join(results_dir, 'suite_summary.json'), 'w') as fh:
    json.dump(suite, fh, indent=2)
print('[suite] Suite summary written to results/suite_summary.json')
" >&2
fi

echo "" >&2
echo "[suite] Done." >&2
