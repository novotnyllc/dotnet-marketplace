#!/usr/bin/env bash
# verify-content-fixes.sh -- Re-verify L5/L6 for task .4 edited skills.
#
# Must be run OUTSIDE a nested Claude Code session (unset CLAUDECODE if needed).
# Uses --runs 3 --regenerate for statistical confidence per fn-60.5 spec.
#
# Skills to verify:
#   L5 (effectiveness):  dotnet-xunit, dotnet-csharp-coding-standards
#   L6 (size impact):    dotnet-xunit, dotnet-csharp-coding-standards,
#                        dotnet-windbg-debugging, dotnet-ado-patterns
#
# Usage:
#   ./tests/evals/verify-content-fixes.sh
#   CLAUDECODE= ./tests/evals/verify-content-fixes.sh   # if inside nested session

set -euo pipefail
cd "$(dirname "$0")/../.."

# Fail fast if running inside a nested Claude Code session
if [[ -n "${CLAUDECODE-}" ]]; then
  echo "ERROR: CLAUDECODE is set; eval CLI cannot run inside nested Claude Code." >&2
  echo "Run this outside Claude Code, or: env -u CLAUDECODE $0" >&2
  exit 2
fi

echo "=== L5 Effectiveness re-verification (--runs 3 --regenerate) ==="
echo ""

echo "[1/2] dotnet-xunit L5..."
python3 tests/evals/run_effectiveness.py --skill dotnet-xunit --runs 3 --regenerate
echo ""

echo "[2/2] dotnet-csharp-coding-standards L5..."
python3 tests/evals/run_effectiveness.py --skill dotnet-csharp-coding-standards --runs 3 --regenerate
echo ""

echo "=== L6 Size Impact re-verification (--runs 3 --regenerate) ==="
echo ""

echo "[1/4] dotnet-xunit L6..."
python3 tests/evals/run_size_impact.py --skill dotnet-xunit --runs 3 --regenerate
echo ""

echo "[2/4] dotnet-csharp-coding-standards L6..."
python3 tests/evals/run_size_impact.py --skill dotnet-csharp-coding-standards --runs 3 --regenerate
echo ""

echo "[3/4] dotnet-windbg-debugging L6..."
python3 tests/evals/run_size_impact.py --skill dotnet-windbg-debugging --runs 3 --regenerate
echo ""

echo "[4/4] dotnet-ado-patterns L6..."
python3 tests/evals/run_size_impact.py --skill dotnet-ado-patterns --runs 3 --regenerate
echo ""

echo "=== Skill & marketplace validation ==="
echo ""
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
echo ""

echo "=== Done ==="
echo "Check results in tests/evals/results/ for new run IDs."
echo "Update eval-progress.json with verified status after reviewing results."
