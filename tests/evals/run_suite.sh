#!/usr/bin/env bash
# run_suite.sh -- Run all 4 eval types and capture results + metrics
#
# Usage:
#   ./tests/evals/run_suite.sh
#   ./tests/evals/run_suite.sh --dry-run
#   ./tests/evals/run_suite.sh --runs=5
#   ./tests/evals/run_suite.sh --cli=codex
#
# CLI tools (claude, codex, copilot) handle their own authentication.
# No API keys needed.
#
# Run counts follow fn-60.1 spec:
#   Activation and Confusion: always 1 run (no multi-run)
#   Effectiveness and Size Impact: configurable via --runs (default 3)
#
# Output:
#   - Individual result JSON files in tests/evals/results/
#   - Summary metrics printed to stderr
#   - Suite summary JSON written to tests/evals/results/suite_summary.json
#   - Runners emit TOTAL_CALLS=/COST_USD=/ABORTED=/N_CASES=/FAIL_FAST= on stdout

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
EVALS_DIR="$REPO_ROOT/tests/evals"
RESULTS_DIR="$EVALS_DIR/results"
MULTI_RUNS="${RUNS:-3}"
DRY_RUN=""
CLI_OVERRIDE=""

# Parse args
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN="--dry-run" ;;
    --runs=*) MULTI_RUNS="${arg#--runs=}" ;;
    --cli=*) CLI_OVERRIDE="--cli ${arg#--cli=}" ;;
    *) echo "Unknown arg: $arg" >&2; exit 1 ;;
  esac
done

# Validate MULTI_RUNS is a positive integer
if ! [[ "$MULTI_RUNS" =~ ^[1-9][0-9]*$ ]]; then
  echo "ERROR: --runs must be a positive integer, got: '$MULTI_RUNS'" >&2
  exit 1
fi

mkdir -p "$RESULTS_DIR"

echo "[suite] Starting eval suite (effectiveness/size_impact runs=$MULTI_RUNS)" >&2
echo "[suite] Results dir: $RESULTS_DIR" >&2

SUITE_START=$(date +%s)
ABORT_DETECTED=0
RUNNER_FAILURES=0

# Initialize all cost/call/case variables to "0" (prevents float("") crash
# if a runner is skipped due to fail-fast or error)
ACT_COST="0"
ACT_CALLS="0"
ACT_CASES="0"
ACT_EXIT=0
ACT_RESULT=""
ACT_STDOUT=""
ACT_FAIL_FAST="0"
ACT_FAIL_FAST_REASON=""

CONF_COST="0"
CONF_CALLS="0"
CONF_CASES="0"
CONF_EXIT=0
CONF_RESULT=""
CONF_STDOUT=""
CONF_FAIL_FAST="0"
CONF_FAIL_FAST_REASON=""

EFF_COST="0"
EFF_CALLS="0"
EFF_CASES="0"
EFF_EXIT=0
EFF_RESULT=""
EFF_STDOUT=""
EFF_FAIL_FAST="0"
EFF_FAIL_FAST_REASON=""

SIZE_COST="0"
SIZE_CALLS="0"
SIZE_CASES="0"
SIZE_EXIT=0
SIZE_RESULT=""
SIZE_STDOUT=""
SIZE_FAIL_FAST="0"
SIZE_FAIL_FAST_REASON=""

# Track which runners triggered fail-fast
FAIL_FAST_RUNNERS=""
SUITE_SKIP_REMAINING=0

# Parse stable machine-parseable keys from runner stdout
# Returns empty string if key is missing (distinguishing from actual "0" value)
parse_runner_key() {
  local output="$1"
  local key="$2"
  local value
  value=$(echo "$output" | grep "^${key}=" | tail -n 1 | sed "s/^${key}=//")
  echo "$value"
}

# Classify whether a fail-fast reason is permanent (non-retryable) or transient.
# Permanent: auth failures, permission errors, CLI not found, bad flags.
# Transient: rate limits, timeouts, overloaded.
is_permanent_fail_fast() {
  local reason="$1"
  local reason_lower
  reason_lower=$(echo "$reason" | tr '[:upper:]' '[:lower:]')
  case "$reason_lower" in
    *"authentication"*|*"not authorized"*|*"permission"*) return 0 ;;
    *"not found in path"*|*"not installed"*|*"cli not found"*) return 0 ;;
    *"unknown option"*|*"invalid flag"*|*"unexpected argument"*) return 0 ;;
    *"exit"*"code 2"*|*"exit"*"code 126"*|*"exit"*"code 127"*) return 0 ;;
    *"401"*|*"403"*) return 0 ;;
    *"does not support"*) return 0 ;;
    *) return 1 ;;
  esac
}

# Run a runner, capturing stdout (key-value lines) and stderr (logs) separately
run_runner() {
  local label="$1"
  shift
  local stdout_output=""
  local stderr_output=""
  local exit_code=0

  echo "" >&2
  echo "============================================" >&2
  echo "[suite] Running $label eval..." >&2
  echo "============================================" >&2

  # Capture stdout and stderr separately
  local tmp_stdout
  tmp_stdout=$(mktemp)
  local tmp_stderr
  tmp_stderr=$(mktemp)

  "$@" >"$tmp_stdout" 2>"$tmp_stderr" || exit_code=$?

  stdout_output=$(cat "$tmp_stdout")
  stderr_output=$(cat "$tmp_stderr")
  rm -f "$tmp_stdout" "$tmp_stderr"

  # Print stderr logs
  echo "$stderr_output" >&2

  if [ $exit_code -ne 0 ]; then
    echo "[suite] WARNING: $label runner exited with code $exit_code" >&2
    RUNNER_FAILURES=$((RUNNER_FAILURES + 1))
  fi

  # Parse ABORTED key
  local runner_aborted
  runner_aborted=$(parse_runner_key "$stdout_output" "ABORTED")
  if [ "$runner_aborted" = "1" ]; then
    echo "[suite] WARNING: $label runner aborted (cap limit or fail-fast)" >&2
    ABORT_DETECTED=1
  fi

  # Return output via globals
  RUNNER_STDOUT="$stdout_output"
  RUNNER_STDERR="$stderr_output"
  RUNNER_EXIT_CODE=$exit_code
}

# --- L3 Activation (always 1 run per fn-60.1 spec) ---
run_runner "L3 Activation" python3 "$EVALS_DIR/run_activation.py" $DRY_RUN $CLI_OVERRIDE
ACT_STDOUT="$RUNNER_STDOUT"
ACT_EXIT=$RUNNER_EXIT_CODE
ACT_COST=$(parse_runner_key "$ACT_STDOUT" "COST_USD")
ACT_CALLS=$(parse_runner_key "$ACT_STDOUT" "TOTAL_CALLS")
ACT_CASES=$(parse_runner_key "$ACT_STDOUT" "N_CASES")
ACT_COST="${ACT_COST:-0}"
ACT_CALLS="${ACT_CALLS:-0}"
ACT_CASES="${ACT_CASES:-0}"
if [ -z "$(parse_runner_key "$ACT_STDOUT" "COST_USD")" ] || [ -z "$(parse_runner_key "$ACT_STDOUT" "TOTAL_CALLS")" ] || [ -z "$(parse_runner_key "$ACT_STDOUT" "N_CASES")" ]; then
  echo "[suite] ERROR: L3 Activation runner missing expected output keys" >&2
  RUNNER_FAILURES=$((RUNNER_FAILURES + 1))
fi

# Parse FAIL_FAST
ACT_FAIL_FAST=$(parse_runner_key "$ACT_STDOUT" "FAIL_FAST")
ACT_FAIL_FAST="${ACT_FAIL_FAST:-0}"
if [ "$ACT_FAIL_FAST" = "1" ]; then
  ACT_FAIL_FAST_REASON=$(parse_runner_key "$ACT_STDOUT" "FAIL_FAST_REASON")
  FAIL_FAST_RUNNERS="${FAIL_FAST_RUNNERS:+$FAIL_FAST_RUNNERS,}activation"
  echo "[suite] WARNING: L3 Activation triggered fail-fast: $ACT_FAIL_FAST_REASON" >&2
  if is_permanent_fail_fast "$ACT_FAIL_FAST_REASON"; then
    echo "[suite] Permanent error detected -- skipping remaining runners" >&2
    SUITE_SKIP_REMAINING=1
  fi
fi

# Extract result file path from stderr
ACT_RESULT=$(echo "$RUNNER_STDERR" | grep -o 'Results written to: .*\.json' | tail -n 1 | sed 's/Results written to: //' || echo "")

# --- L4 Confusion (always 1 run per fn-60.1 spec) ---
if [ "$SUITE_SKIP_REMAINING" = "1" ]; then
  echo "" >&2
  echo "============================================" >&2
  echo "[suite] SKIPPING L4 Confusion Matrix (permanent fail-fast from prior runner)" >&2
  echo "============================================" >&2
else
  run_runner "L4 Confusion Matrix" python3 "$EVALS_DIR/run_confusion_matrix.py" $DRY_RUN $CLI_OVERRIDE
  CONF_STDOUT="$RUNNER_STDOUT"
  CONF_EXIT=$RUNNER_EXIT_CODE
  CONF_COST=$(parse_runner_key "$CONF_STDOUT" "COST_USD")
  CONF_CALLS=$(parse_runner_key "$CONF_STDOUT" "TOTAL_CALLS")
  CONF_CASES=$(parse_runner_key "$CONF_STDOUT" "N_CASES")
  CONF_COST="${CONF_COST:-0}"
  CONF_CALLS="${CONF_CALLS:-0}"
  CONF_CASES="${CONF_CASES:-0}"
  if [ -z "$(parse_runner_key "$CONF_STDOUT" "COST_USD")" ] || [ -z "$(parse_runner_key "$CONF_STDOUT" "TOTAL_CALLS")" ] || [ -z "$(parse_runner_key "$CONF_STDOUT" "N_CASES")" ]; then
    echo "[suite] ERROR: L4 Confusion runner missing expected output keys" >&2
    RUNNER_FAILURES=$((RUNNER_FAILURES + 1))
  fi

  # Parse FAIL_FAST
  CONF_FAIL_FAST=$(parse_runner_key "$CONF_STDOUT" "FAIL_FAST")
  CONF_FAIL_FAST="${CONF_FAIL_FAST:-0}"
  if [ "$CONF_FAIL_FAST" = "1" ]; then
    CONF_FAIL_FAST_REASON=$(parse_runner_key "$CONF_STDOUT" "FAIL_FAST_REASON")
    FAIL_FAST_RUNNERS="${FAIL_FAST_RUNNERS:+$FAIL_FAST_RUNNERS,}confusion"
    echo "[suite] WARNING: L4 Confusion triggered fail-fast: $CONF_FAIL_FAST_REASON" >&2
    if is_permanent_fail_fast "$CONF_FAIL_FAST_REASON"; then
      echo "[suite] Permanent error detected -- skipping remaining runners" >&2
      SUITE_SKIP_REMAINING=1
    fi
  fi

  CONF_RESULT=$(echo "$RUNNER_STDERR" | grep -o 'Results written to: .*\.json' | tail -n 1 | sed 's/Results written to: //' || echo "")
fi

# --- L5 Effectiveness (multi-run) ---
if [ "$SUITE_SKIP_REMAINING" = "1" ]; then
  echo "" >&2
  echo "============================================" >&2
  echo "[suite] SKIPPING L5 Effectiveness (permanent fail-fast from prior runner)" >&2
  echo "============================================" >&2
else
  run_runner "L5 Effectiveness" python3 "$EVALS_DIR/run_effectiveness.py" --runs "$MULTI_RUNS" $DRY_RUN $CLI_OVERRIDE
  EFF_STDOUT="$RUNNER_STDOUT"
  EFF_EXIT=$RUNNER_EXIT_CODE
  EFF_COST=$(parse_runner_key "$EFF_STDOUT" "COST_USD")
  EFF_CALLS=$(parse_runner_key "$EFF_STDOUT" "TOTAL_CALLS")
  EFF_CASES=$(parse_runner_key "$EFF_STDOUT" "N_CASES")
  EFF_COST="${EFF_COST:-0}"
  EFF_CALLS="${EFF_CALLS:-0}"
  EFF_CASES="${EFF_CASES:-0}"
  if [ -z "$(parse_runner_key "$EFF_STDOUT" "COST_USD")" ] || [ -z "$(parse_runner_key "$EFF_STDOUT" "TOTAL_CALLS")" ] || [ -z "$(parse_runner_key "$EFF_STDOUT" "N_CASES")" ]; then
    echo "[suite] ERROR: L5 Effectiveness runner missing expected output keys" >&2
    RUNNER_FAILURES=$((RUNNER_FAILURES + 1))
  fi

  # Parse FAIL_FAST
  EFF_FAIL_FAST=$(parse_runner_key "$EFF_STDOUT" "FAIL_FAST")
  EFF_FAIL_FAST="${EFF_FAIL_FAST:-0}"
  if [ "$EFF_FAIL_FAST" = "1" ]; then
    EFF_FAIL_FAST_REASON=$(parse_runner_key "$EFF_STDOUT" "FAIL_FAST_REASON")
    FAIL_FAST_RUNNERS="${FAIL_FAST_RUNNERS:+$FAIL_FAST_RUNNERS,}effectiveness"
    echo "[suite] WARNING: L5 Effectiveness triggered fail-fast: $EFF_FAIL_FAST_REASON" >&2
    if is_permanent_fail_fast "$EFF_FAIL_FAST_REASON"; then
      echo "[suite] Permanent error detected -- skipping remaining runners" >&2
      SUITE_SKIP_REMAINING=1
    fi
  fi

  EFF_RESULT=$(echo "$RUNNER_STDERR" | grep -o 'Results written to: .*\.json' | tail -n 1 | sed 's/Results written to: //' || echo "")
fi

# --- L6 Size Impact (multi-run) ---
if [ "$SUITE_SKIP_REMAINING" = "1" ]; then
  echo "" >&2
  echo "============================================" >&2
  echo "[suite] SKIPPING L6 Size Impact (permanent fail-fast from prior runner)" >&2
  echo "============================================" >&2
else
  run_runner "L6 Size Impact" python3 "$EVALS_DIR/run_size_impact.py" --runs "$MULTI_RUNS" $DRY_RUN $CLI_OVERRIDE
  SIZE_STDOUT="$RUNNER_STDOUT"
  SIZE_EXIT=$RUNNER_EXIT_CODE
  SIZE_COST=$(parse_runner_key "$SIZE_STDOUT" "COST_USD")
  SIZE_CALLS=$(parse_runner_key "$SIZE_STDOUT" "TOTAL_CALLS")
  SIZE_CASES=$(parse_runner_key "$SIZE_STDOUT" "N_CASES")
  SIZE_COST="${SIZE_COST:-0}"
  SIZE_CALLS="${SIZE_CALLS:-0}"
  SIZE_CASES="${SIZE_CASES:-0}"
  if [ -z "$(parse_runner_key "$SIZE_STDOUT" "COST_USD")" ] || [ -z "$(parse_runner_key "$SIZE_STDOUT" "TOTAL_CALLS")" ] || [ -z "$(parse_runner_key "$SIZE_STDOUT" "N_CASES")" ]; then
    echo "[suite] ERROR: L6 Size Impact runner missing expected output keys" >&2
    RUNNER_FAILURES=$((RUNNER_FAILURES + 1))
  fi

  # Parse FAIL_FAST
  SIZE_FAIL_FAST=$(parse_runner_key "$SIZE_STDOUT" "FAIL_FAST")
  SIZE_FAIL_FAST="${SIZE_FAIL_FAST:-0}"
  if [ "$SIZE_FAIL_FAST" = "1" ]; then
    SIZE_FAIL_FAST_REASON=$(parse_runner_key "$SIZE_STDOUT" "FAIL_FAST_REASON")
    FAIL_FAST_RUNNERS="${FAIL_FAST_RUNNERS:+$FAIL_FAST_RUNNERS,}size_impact"
    echo "[suite] WARNING: L6 Size Impact triggered fail-fast: $SIZE_FAIL_FAST_REASON" >&2
  fi

  SIZE_RESULT=$(echo "$RUNNER_STDERR" | grep -o 'Results written to: .*\.json' | tail -n 1 | sed 's/Results written to: //' || echo "")
fi

# --- Suite Summary ---
SUITE_END=$(date +%s)
SUITE_DURATION=$((SUITE_END - SUITE_START))

# Compute totals via python (avoids floating point issues in bash)
export _SUITE_ACT_COST="$ACT_COST"
export _SUITE_CONF_COST="$CONF_COST"
export _SUITE_EFF_COST="$EFF_COST"
export _SUITE_SIZE_COST="$SIZE_COST"

TOTAL_COST=$(python3 -c "
import os
costs = [
    float(os.environ.get('_SUITE_ACT_COST', '0') or '0'),
    float(os.environ.get('_SUITE_CONF_COST', '0') or '0'),
    float(os.environ.get('_SUITE_EFF_COST', '0') or '0'),
    float(os.environ.get('_SUITE_SIZE_COST', '0') or '0'),
]
print(round(sum(costs), 4))
")

export _SUITE_ACT_CALLS="$ACT_CALLS"
export _SUITE_CONF_CALLS="$CONF_CALLS"
export _SUITE_EFF_CALLS="$EFF_CALLS"
export _SUITE_SIZE_CALLS="$SIZE_CALLS"

TOTAL_CALLS=$(python3 -c "
import os
calls = [
    int(os.environ.get('_SUITE_ACT_CALLS', '0') or '0'),
    int(os.environ.get('_SUITE_CONF_CALLS', '0') or '0'),
    int(os.environ.get('_SUITE_EFF_CALLS', '0') or '0'),
    int(os.environ.get('_SUITE_SIZE_CALLS', '0') or '0'),
]
print(sum(calls))
")

# Count result files from this run
RESULT_FILES="$ACT_RESULT $CONF_RESULT $EFF_RESULT $SIZE_RESULT"
THIS_RUN_COUNT=0
for f in $RESULT_FILES; do
  if [ -n "$f" ] && [ -f "$f" ]; then THIS_RUN_COUNT=$((THIS_RUN_COUNT + 1)); fi
done

echo "" >&2
echo "============================================" >&2
echo "[suite] === Suite Complete ===" >&2
echo "  Duration: ${SUITE_DURATION}s" >&2
echo "  Total cost: \$$TOTAL_COST" >&2
echo "  Total calls: $TOTAL_CALLS" >&2
echo "  Abort detected: $ABORT_DETECTED" >&2
echo "  Runner failures: $RUNNER_FAILURES" >&2
echo "  Fail-fast runners: ${FAIL_FAST_RUNNERS:-none}" >&2
echo "  Result files (this run): $THIS_RUN_COUNT" >&2
echo "============================================" >&2

# Write suite summary (only for real runs)
if [ -z "$DRY_RUN" ]; then
  export _SUITE_RESULTS_DIR="$RESULTS_DIR"
  export _SUITE_DURATION="$SUITE_DURATION"
  export _SUITE_TOTAL_COST="$TOTAL_COST"
  export _SUITE_TOTAL_CALLS="$TOTAL_CALLS"
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
  export _SUITE_FAIL_FAST_RUNNERS="${FAIL_FAST_RUNNERS:-}"

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

# Parse fail-fast runners list
ff_raw = os.environ.get("_SUITE_FAIL_FAST_RUNNERS", "")
fail_fast_runners = [r.strip() for r in ff_raw.split(",") if r.strip()] if ff_raw else []

suite = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "duration_seconds": int(os.environ["_SUITE_DURATION"]),
    "total_cost": float(os.environ["_SUITE_TOTAL_COST"]),
    "total_calls": int(os.environ.get("_SUITE_TOTAL_CALLS", "0") or "0"),
    "abort_detected": os.environ["_SUITE_ABORT"] != "0",
    "runner_failures": int(os.environ["_SUITE_FAILURES"]),
    "multi_runs": int(os.environ["_SUITE_MULTI_RUNS"]),
    "fail_fast_runners": fail_fast_runners,
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
