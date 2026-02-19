# Agent Routing Tests

This document describes the minimal routing test system used to verify that Claude, Codex, and Copilot discover and use expected skills.

## Files

- `tests/agent-routing/cases.json`: broad case corpus (same prompts across Claude/Codex/Copilot)
- `tests/agent-routing/check-skills.cs`: single .NET file-based runner
- `test.sh`: single entrypoint script
- `.github/workflows/agent-live-routing.yml`: manual/scheduled live checks

## Commands

- Live full-corpus checks:
  - `./test.sh`
  - Proof log (default): `tests/agent-routing/artifacts/tool-use-proof.log`

## Source Setup (Default)

`test.sh` now prepares agent sources before running checks, so tests target this repo version:

- Claude: disables user-scope `dotnet-artisan`, points marketplace `dotnet-artisan` to this repo path, installs local scope plugin.
- Copilot: repoints marketplace `dotnet-artisan` to this repo path and reinstalls/updates `dotnet-artisan@dotnet-artisan`.
- Codex: syncs `skills/*/*` from this repo into `~/.codex/skills/<skill-name>`.
- Cleanup: removes `apps/` before and after each run to avoid persisted generated app scaffolds.

Use `--skip-source-setup` only for debugging:

- `./test.sh --skip-source-setup --agents claude --case-id advisor-routing-maintainable-app`

Note: source setup updates local plugin/marketplace state in `~/.claude` and `~/.copilot`.

## Optional Filters

Pass extra runner args through `test.sh`.

Examples:

- One agent:
  - `./test.sh --agents codex`
- Specific categories:
  - `./test.sh --category api,testing`
- Fail on infra errors:
  - `./test.sh --fail-on-infra`
- Dedicated copilot-negative routing assertion:
  - `./test.sh --case-id uno-mcp-routing-skill-id-only --timeout-seconds 180 --output /tmp/uno-routing.json`
  - Expected matrix: `claude=pass`, `codex=pass`, `copilot=fail` (failure kind `skill_not_loaded`).

## Runner Behavior

- Expands each case across selected agents.
- Copilot is expected to fail routing for nested `dotnet-*` skills (missing skill-load evidence), while Claude/Codex should pass.
- Executes agent command templates with timeout.
- Evaluates evidence from stdout/stderr for tool usage + skill-file reads.
- Always falls back to recent logs from agent home dirs.
- Emits JSON with statuses: `pass`, `fail`, `infra_error`.
- Includes `timed_out` per result so partial-output passes are visible.
- Includes `failure_kind` for failed results (`skill_not_loaded`, `missing_skill_file_evidence`, `missing_activity_evidence`, `mixed_evidence_missing`, `unknown`).
- Includes `tool_use_proof_lines` per result and writes a plain-text proof log file.

Evidence currently gates on:

- `required_all_evidence`: all tokens must appear. Evidence tokens differ by agent type:
  - **Claude**: Uses definitive Skill-tool invocation tokens (`"Launching skill: <skill-id>"` or `{"skill":"<skill-id>"}`). SKILL.md file-read evidence is excluded because Claude does not reliably emit file-read traces. The runner extracts launched skill IDs from structured JSON output and `Launching skill:` log lines.
  - **Non-Claude (Codex, Copilot)**: Uses skill-specific file paths (`"<skill-id>/SKILL.md"`) instead of the generic `"SKILL.md"` token. This prevents false-positive matches from incidental SKILL.md mentions in unrelated output. When `expected_skill` is set, only the skill-specific path is required. The generic `"SKILL.md"` token is used only as a fallback when no `expected_skill` is configured.
- `required_any_evidence`: at least one activity token must appear. Defaults also include Copilot log activity markers (`function_call`, MCP startup/config lines).
- `require_skill_file` (optional, default `true`): when `false`, only skill-id loading is required (useful for dedicated cross-agent routing assertions).

### Failure Taxonomy

The `failure_kind` field on failed results uses the following classification:

- `skill_not_loaded`: The expected skill ID was not found in output (but activity evidence was present).
- `missing_skill_file_evidence`: The skill-specific file path token (e.g. `dotnet-xunit/SKILL.md`) was missing, but the skill ID was matched. Detected via tokens ending with `/SKILL.md` or equal to the generic `SKILL.md`.
- `missing_activity_evidence`: No activity tokens (tool_use, read_file, etc.) were found, but skill evidence was present.
- `mixed_evidence_missing`: Both skill ID and activity evidence were missing.
- `unknown`: None of the above patterns matched.

Proof log options:

- `--proof-log <path>`: write a plain-text log containing matched tool-use evidence lines.

## Environment Variables

Command template overrides:

- `AGENT_CLAUDE_TEMPLATE`
- `AGENT_CODEX_TEMPLATE`
- `AGENT_COPILOT_TEMPLATE`

Default templates are used when unset.

Log fallback root overrides (path-separated list):

- `AGENT_CLAUDE_LOG_DIRS`
- `AGENT_CODEX_LOG_DIRS`
- `AGENT_COPILOT_LOG_DIRS`

## GitHub Workflows

- `agent-live-routing.yml` runs live checks via `workflow_dispatch` or schedule and uploads JSON artifacts.

## Troubleshooting

- `infra_error` means the runner could not start the command (for example, missing CLI or invalid template).
- `fail` with `timed_out: true` means the agent ran but did not produce required skill/tool evidence before timeout.
- If evidence is present in logs but not stdout/stderr, ensure fallback log paths are correct.
- For local debugging, write output to a file:
  - `./test.sh --output /tmp/live-routing.json`
