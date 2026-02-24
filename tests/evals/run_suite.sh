#!/usr/bin/env bash
# run_suite.sh -- Run all 4 eval types and capture results + metrics
#
# Usage:
#   ANTHROPIC_API_KEY=sk-... ./tests/evals/run_suite.sh
#   ./tests/evals/run_suite.sh --dry-run
#   ./tests/evals/run_suite.sh --runs=5
#
# Environment:
#   ANTHROPIC_API_KEY  Required for real runs (not dry-run)
#
# Run counts follow fn-60.1 spec:
#   Activation and Confusion: always 1 run (no multi-run)
#   Effectiveness and Size Impact: configurable via --runs (default 3)
#
# Output:
#   - Individual result JSON files in tests/evals/results/
#   - Summary metrics printed to stderr
#   - Suite summary JSON written to tests/evals/results/suite_summary.json

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
EVALS_DIR="$REPO_ROOT/tests/evals"
RESULTS_DIR="$EVALS_DIR/results"
MULTI_RUNS="${RUNS:-3}"
DRY_RUN=""

# Parse args
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN="--dry-run" ;;
    --runs=*) MULTI_RUNS="${arg#--runs=}" ;;
    *) echo "Unknown arg: $arg" >&2; exit 1 ;;
  esac
done

# Issue #1: Validate MULTI_RUNS is a positive integer
if ! [[ "$MULTI_RUNS" =~ ^[1-9][0-9]*$ ]]; then
  echo "ERROR: --runs must be a positive integer, got: '$MULTI_RUNS'" >&2
  exit 1
fi

mkdir -p "$RESULTS_DIR"

# Check API key unless dry-run
if [ -z "$DRY_RUN" ]; then
  if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    echo "ERROR: ANTHROPIC_API_KEY is not set. Set it or use --dry-run." >&2
    exit 1
  fi
  echo "[suite] ANTHROPIC_API_KEY is set (length=${#ANTHROPIC_API_KEY})" >&2
fi

echo "[suite] Starting eval suite (effectiveness/size_impact runs=$MULTI_RUNS)" >&2
echo "[suite] Results dir: $RESULTS_DIR" >&2

SUITE_START=$(date +%s)
ABORT_DETECTED=0
RUNNER_FAILURES=0

# Issue #5: Extract cost safely -- take only the last match to handle multi-line output
extract_cost() {
  local output="$1"
  local cost
  cost=$(echo "$output" | grep -o 'Total cost: \$[0-9.]*' | tail -n 1 | grep -o '[0-9.]*' 2>/dev/null || echo "0")
  # Validate it looks like a number
  if [[ "$cost" =~ ^[0-9]+\.?[0-9]*$ ]]; then
    echo "$cost"
  else
    echo "0"
  fi
}

# Issue #2: Extract result file path from runner output
extract_result_path() {
  local output="$1"
  echo "$output" | grep -o 'Results written to: .*\.json' | tail -n 1 | sed 's/Results written to: //' || echo ""
}

# Issue #6: Run a runner and capture exit code + output
run_runner() {
  local label="$1"
  shift
  local output=""
  local exit_code=0

  echo "" >&2
  echo "============================================" >&2
  echo "[suite] Running $label eval..." >&2
  echo "============================================" >&2

  output=$("$@" 2>&1) || exit_code=$?
  echo "$output" >&2

  if [ $exit_code -ne 0 ]; then
    echo "[suite] WARNING: $label runner exited with code $exit_code" >&2
    RUNNER_FAILURES=$((RUNNER_FAILURES + 1))
  fi

  if echo "$output" | grep -q "ABORT"; then
    echo "[suite] WARNING: $label runner aborted (cost cap)" >&2
    ABORT_DETECTED=1
  fi

  # Return output via a global (bash doesn't support returning strings)
  RUNNER_OUTPUT="$output"
  RUNNER_EXIT_CODE=$exit_code
}

# Track result files produced by this suite run
RESULT_FILES=""

# --- L3 Activation (always 1 run per fn-60.1 spec) ---
run_runner "L3 Activation" python3 "$EVALS_DIR/run_activation.py" $DRY_RUN
ACT_OUTPUT="$RUNNER_OUTPUT"
ACT_EXIT=$RUNNER_EXIT_CODE
ACT_COST=$(extract_cost "$ACT_OUTPUT")
ACT_RESULT=$(extract_result_path "$ACT_OUTPUT")
if [ -n "$ACT_RESULT" ]; then RESULT_FILES="$RESULT_FILES $ACT_RESULT"; fi

# --- L4 Confusion (always 1 run per fn-60.1 spec) ---
run_runner "L4 Confusion Matrix" python3 "$EVALS_DIR/run_confusion_matrix.py" $DRY_RUN
CONF_OUTPUT="$RUNNER_OUTPUT"
CONF_EXIT=$RUNNER_EXIT_CODE
CONF_COST=$(extract_cost "$CONF_OUTPUT")
CONF_RESULT=$(extract_result_path "$CONF_OUTPUT")
if [ -n "$CONF_RESULT" ]; then RESULT_FILES="$RESULT_FILES $CONF_RESULT"; fi

# --- L5 Effectiveness (multi-run) ---
run_runner "L5 Effectiveness" python3 "$EVALS_DIR/run_effectiveness.py" --runs "$MULTI_RUNS" $DRY_RUN
EFF_OUTPUT="$RUNNER_OUTPUT"
EFF_EXIT=$RUNNER_EXIT_CODE
EFF_COST=$(extract_cost "$EFF_OUTPUT")
EFF_RESULT=$(extract_result_path "$EFF_OUTPUT")
if [ -n "$EFF_RESULT" ]; then RESULT_FILES="$RESULT_FILES $EFF_RESULT"; fi

# --- L6 Size Impact (multi-run) ---
run_runner "L6 Size Impact" python3 "$EVALS_DIR/run_size_impact.py" --runs "$MULTI_RUNS" $DRY_RUN
SIZE_OUTPUT="$RUNNER_OUTPUT"
SIZE_EXIT=$RUNNER_EXIT_CODE
SIZE_COST=$(extract_cost "$SIZE_OUTPUT")
SIZE_RESULT=$(extract_result_path "$SIZE_OUTPUT")
if [ -n "$SIZE_RESULT" ]; then RESULT_FILES="$RESULT_FILES $SIZE_RESULT"; fi

# --- Suite Summary ---
SUITE_END=$(date +%s)
SUITE_DURATION=$((SUITE_END - SUITE_START))

# Issue #1: Pass values via environment to avoid shell interpolation into Python
export _SUITE_ACT_COST="$ACT_COST"
export _SUITE_CONF_COST="$CONF_COST"
export _SUITE_EFF_COST="$EFF_COST"
export _SUITE_SIZE_COST="$SIZE_COST"

TOTAL_COST=$(python3 -c "
import os
costs = [
    float(os.environ.get('_SUITE_ACT_COST', '0')),
    float(os.environ.get('_SUITE_CONF_COST', '0')),
    float(os.environ.get('_SUITE_EFF_COST', '0')),
    float(os.environ.get('_SUITE_SIZE_COST', '0')),
]
print(round(sum(costs), 4))
")

# Issue #7: Count only result files from this suite run
THIS_RUN_COUNT=0
for f in $RESULT_FILES; do
  if [ -f "$f" ]; then THIS_RUN_COUNT=$((THIS_RUN_COUNT + 1)); fi
done

echo "" >&2
echo "============================================" >&2
echo "[suite] === Suite Complete ===" >&2
echo "  Duration: ${SUITE_DURATION}s" >&2
echo "  Total cost: \$$TOTAL_COST" >&2
echo "  Abort detected: $ABORT_DETECTED" >&2
echo "  Runner failures: $RUNNER_FAILURES" >&2
echo "  Result files (this run): $THIS_RUN_COUNT" >&2
echo "============================================" >&2

# Write suite summary (only for real runs)
if [ -z "$DRY_RUN" ]; then
  # Issue #1, #2, #3: Pass all values via environment, use captured result paths,
  # and wrap JSON loading in try/except
  export _SUITE_RESULTS_DIR="$RESULTS_DIR"
  export _SUITE_DURATION="$SUITE_DURATION"
  export _SUITE_TOTAL_COST="$TOTAL_COST"
  export _SUITE_ABORT="$ABORT_DETECTED"
  export _SUITE_FAILURES="$RUNNER_FAILURES"
  export _SUITE_MULTI_RUNS="$MULTI_RUNS"
  export _SUITE_ACT_RESULT="${ACT_RESULT:-}"
  export _SUITE_CONF_RESULT="${CONF_RESULT:-}"
  export _SUITE_EFF_RESULT="${EFF_RESULT:-}"
  export _SUITE_SIZE_RESULT="${SIZE_RESULT:-}"
  export _SUITE_ACT_EXIT="$ACT_EXIT"
  export _SUITE_CONF_EXIT="$CONF_EXIT"
  export _SUITE_EFF_EXIT="$EFF_EXIT"
  export _SUITE_SIZE_EXIT="$SIZE_EXIT"

  python3 -c '
import json, os, sys
from datetime import datetime, timezone

results_dir = os.environ["_SUITE_RESULTS_DIR"]

def load_result(path):
    """Load a result JSON file safely, returning None on error."""
    if not path or not os.path.isfile(path):
        return None
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[suite] WARNING: Failed to load {path}: {exc}", file=sys.stderr)
        return None

# Load results from the exact files produced by this run
result_map = {
    "activation": (os.environ.get("_SUITE_ACT_RESULT", ""), int(os.environ.get("_SUITE_ACT_EXIT", "0"))),
    "confusion": (os.environ.get("_SUITE_CONF_RESULT", ""), int(os.environ.get("_SUITE_CONF_EXIT", "0"))),
    "effectiveness": (os.environ.get("_SUITE_EFF_RESULT", ""), int(os.environ.get("_SUITE_EFF_EXIT", "0"))),
    "size_impact": (os.environ.get("_SUITE_SIZE_RESULT", ""), int(os.environ.get("_SUITE_SIZE_EXIT", "0"))),
}

eval_types = {}
for eval_type, (path, exit_code) in result_map.items():
    data = load_result(path)
    entry = {
        "file": os.path.basename(path) if path else None,
        "exit_code": exit_code,
        "status": "ok" if exit_code == 0 and data else ("error" if exit_code != 0 else "no_output"),
    }
    if data:
        entry["run_id"] = data.get("meta", {}).get("run_id")
        entry["cost"] = data.get("meta", {}).get("total_cost", 0)
        entry["summary"] = data.get("summary", {})
    eval_types[eval_type] = entry

suite = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "duration_seconds": int(os.environ["_SUITE_DURATION"]),
    "total_cost": float(os.environ["_SUITE_TOTAL_COST"]),
    "abort_detected": os.environ["_SUITE_ABORT"] != "0",
    "runner_failures": int(os.environ["_SUITE_FAILURES"]),
    "multi_runs": int(os.environ["_SUITE_MULTI_RUNS"]),
    "eval_types": eval_types,
}

out_path = os.path.join(results_dir, "suite_summary.json")
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(suite, fh, indent=2)
print(f"[suite] Suite summary written to {out_path}", file=sys.stderr)
' >&2
fi

echo "" >&2
echo "[suite] Done." >&2
