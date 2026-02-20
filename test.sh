#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
RUNNER="$REPO_ROOT/tests/agent-routing/check-skills.cs"
CASES="$REPO_ROOT/tests/agent-routing/cases.json"
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
APPS_DIR="$REPO_ROOT/apps"

log() {
    echo "[test.sh] $*"
}

have_cmd() {
    command -v "$1" >/dev/null 2>&1
}

contains_agent() {
    local needle="$1"
    local haystack="$2"
    [[ ",${haystack}," == *",${needle},"* ]]
}

cleanup_generated_apps() {
    if [[ -d "$APPS_DIR" ]]; then
        log "Cleaning generated apps directory: $APPS_DIR"
        rm -rf "$APPS_DIR"
    fi
}

prepare_claude_plugin() {
    if ! have_cmd claude; then
        log "WARNING: claude CLI not found; skipping Claude plugin source setup."
        return
    fi

    log "Preparing Claude plugin source (local repo)."
    claude plugin disable 'dotnet-artisan@dotnet-artisan' -s user >/dev/null 2>&1 || true
    claude plugin marketplace remove dotnet-artisan >/dev/null 2>&1 || true
    claude plugin marketplace add "$REPO_ROOT" >/dev/null
    claude plugin install dotnet-artisan -s local >/dev/null 2>&1 || \
        claude plugin update dotnet-artisan >/dev/null 2>&1 || true

    if ! claude plugin marketplace list | grep -F "Source: Directory ($REPO_ROOT)" >/dev/null; then
        log "ERROR: Claude marketplace dotnet-artisan is not pointing at $REPO_ROOT"
        return 1
    fi
}

prepare_copilot_plugin() {
    if ! have_cmd copilot; then
        log "WARNING: copilot CLI not found; skipping Copilot plugin source setup."
        return
    fi

    log "Preparing Copilot plugin source (local repo)."
    if ! copilot plugin marketplace list | grep -F "dotnet-artisan (Local: $REPO_ROOT)" >/dev/null 2>&1; then
        copilot plugin marketplace remove -f dotnet-artisan >/dev/null 2>&1 || true
        copilot plugin marketplace add "$REPO_ROOT" >/dev/null
    fi

    copilot plugin install dotnet-artisan@dotnet-artisan >/dev/null 2>&1 || \
        copilot plugin update dotnet-artisan@dotnet-artisan >/dev/null 2>&1 || true

    if ! copilot plugin marketplace list | grep -F "dotnet-artisan (Local: $REPO_ROOT)" >/dev/null; then
        log "ERROR: Copilot marketplace dotnet-artisan is not pointing at $REPO_ROOT"
        return 1
    fi
}

prepare_codex_skills() {
    if ! have_cmd codex; then
        log "WARNING: codex CLI not found; skipping Codex skill sync."
        return
    fi

    if [[ ! -d "$REPO_ROOT/skills" ]]; then
        log "ERROR: skills directory not found at $REPO_ROOT/skills"
        return 1
    fi

    if ! have_cmd rsync; then
        log "ERROR: rsync is required to sync Codex skills."
        return 1
    fi

    local -a skill_dirs=()
    while IFS= read -r skill_dir; do
        skill_dirs+=("$skill_dir")
    done < <(find "$REPO_ROOT/skills" -mindepth 2 -maxdepth 2 -type d | sort)

    local total_skills="${#skill_dirs[@]}"
    if (( total_skills == 0 )); then
        log "ERROR: No skill directories found under $REPO_ROOT/skills"
        return 1
    fi

    log "Syncing $total_skills repo skills into Codex skill home: $CODEX_SKILLS_DIR"
    mkdir -p "$CODEX_SKILLS_DIR"

    local sync_started_at
    sync_started_at="$(date +%s)"

    local synced_count=0
    for skill_dir in "${skill_dirs[@]}"; do
        synced_count=$((synced_count + 1))
        skill_name="$(basename "$skill_dir")"
        skill_dest="$CODEX_SKILLS_DIR/$skill_name"
        mkdir -p "$skill_dest"
        rsync -a --delete "$skill_dir"/ "$skill_dest"/

        if (( synced_count % 25 == 0 || synced_count == total_skills )); then
            log "Codex skill sync progress: $synced_count/$total_skills"
        fi
    done

    local repo_sha
    repo_sha="$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)"
    printf '%s\n' "$REPO_ROOT@$repo_sha" > "$CODEX_SKILLS_DIR/.dotnet-artisan-source"

    local sync_finished_at
    sync_finished_at="$(date +%s)"
    log "Codex skill sync finished in $((sync_finished_at - sync_started_at))s."
}

prepare_agent_sources() {
    local agents_csv="$1"
    local do_setup="${2:-1}"
    if [[ "$do_setup" != "1" ]]; then
        log "Skipping local source setup (--skip-source-setup)."
        return
    fi

    if contains_agent "claude" "$agents_csv"; then
        prepare_claude_plugin
    fi
    if contains_agent "copilot" "$agents_csv"; then
        prepare_copilot_plugin
    fi
    if contains_agent "codex" "$agents_csv"; then
        prepare_codex_skills
    fi
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    cat <<'EOF'
Usage:
  ./test.sh [options] [runner args...]

Examples:
  ./test.sh
  ./test.sh --agents codex --category api
  ./test.sh --skip-source-setup --agents claude --case-id advisor-routing-maintainable-app
  ./test.sh --agents claude --max-parallel 4

Wrapper options:
  --skip-source-setup   Do not repoint/sync local plugin and skill sources before run

Runner options (passed through to check-skills.cs):
  --agents <csv>            Agents filter (default: claude,codex,copilot)
  --category <csv>          Category filter
  --case-id <csv>           Case-id filter
  --timeout-seconds <int>   Per-invocation timeout (default: 90)
  --max-parallel <int>      Max concurrent runs (default: 4; env MAX_CONCURRENCY fallback)
  --artifacts-root <path>   Base directory for per-batch artifact isolation
                            (default: tests/agent-routing/artifacts)
  --enable-log-scan         Enable log file scanning (default: on serial, off parallel)
  --disable-log-scan        Disable log file scanning
  --allow-log-fallback-pass Allow log fallback to promote pass when parallel
  --log-max-files <int>     Max log files to scan per agent (default: 60)
  --log-max-bytes <int>     Max bytes to read per log file (default: 300000)
  --no-progress             Disable stderr lifecycle progress output
  --self-test               Run ComputeTier self-test fixtures and exit
  --output <path>           Optional additional JSON output path (backward compat)
  --proof-log <path>        Optional additional proof log path (backward compat)
  --fail-on-infra           Exit non-zero when infra_error exists
  --help                    Show this help

Environment:
  MAX_CONCURRENCY           Fallback for --max-parallel (flag takes precedence)

Artifacts:
  Results and proof logs are always written to <artifacts-root>/<batch_run_id>/.
  ARTIFACT_DIR=<path> is emitted on stderr (parseable via: grep '^ARTIFACT_DIR=' stderr.log).
EOF
    exit 0
fi

if [[ ! -f "$RUNNER" ]]; then
    echo "ERROR: Runner not found: $RUNNER"
    exit 1
fi

RUNNER_ARGS=()
SELECTED_AGENTS="claude,codex,copilot"
DO_SOURCE_SETUP=1

while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip-source-setup)
            DO_SOURCE_SETUP=0
            shift
            ;;
        --agents)
            if [[ $# -lt 2 ]]; then
                echo "ERROR: Missing value for --agents"
                exit 1
            fi
            SELECTED_AGENTS="$2"
            RUNNER_ARGS+=("$1" "$2")
            shift 2
            ;;
        *)
            RUNNER_ARGS+=("$1")
            shift
            ;;
    esac
done

prepare_agent_sources "$SELECTED_AGENTS" "$DO_SOURCE_SETUP"
cleanup_generated_apps
trap cleanup_generated_apps EXIT

set +e
dotnet run --file "$RUNNER" -- \
    --input "$CASES" \
    --run-all \
    "${RUNNER_ARGS[@]}"
run_exit=$?
set -e

exit "$run_exit"
