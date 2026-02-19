# Plan: Minimal Agent Skill Usage Checks (Claude, Codex, Copilot)

**Generated**: 2026-02-18 02:04:06 EST

## Goal
Ensure each agent can discover and use expected skills, with checks runnable in CI.

## Scope
- Keep execution simple.
- Keep coverage broad across skill categories and all three agents.
- Use one executable test runner, one manifest, and one standard command path.

## Core Decisions
- Use one .NET 10 file-based runner: `tests/agent-routing/check-skills.cs`.
- Use one shell wrapper for short commands: `./test.sh`.
- Use one shared manifest: `tests/agent-routing/cases.json`.
- Manifest is broad and tagged by category (for example: foundation, testing, ci-cd, api, architecture, security, performance, ui).
- Cases are agent-agnostic (define each case once); execution fans out per agent in the runner/workflow.
- Default behavior is `run everything`: all cases, all agents.
- Live agent checks run in a separate workflow (manual/scheduled) and also default to all agents/all cases.
- Use agent logs as fallback evidence sources (for example `~/.claude`, `~/.codex`, and configured Copilot output/log paths).
- Routing success is evidence-driven: agent output/logs must show tool activity signals (for example `tool_use`, `read_file`, `file_search`, `command_execution`, `Glob`, `Grep`, `mcp:`), not just a prose answer.
- No test framework by default. If we add one later, use `xunit.v3.mtp-v2` with `dotnet run --file ...` (not `dotnet test <file>.cs`).

## Dependency Graph

```text
T1 -> T2 -> T3 -> T4
          \-> T5
T4 + T5 -> T6
```

## Tasks

### T1: Define Broad Case Corpus
- **depends_on**: []
- **location**: `tests/agent-routing/cases.json`
- **description**: Create a broad agent-agnostic corpus with fields: `case_id`, `category`, `prompt`, `expected_skill`, `required_evidence`. Include enough cases to cover major skill categories.
- **validation**: Manifest is JSON-valid, category-tagged, and has no agent-specific duplication.
- **status**: Completed
- **log**: Added 13 agent-agnostic routing cases spanning foundation, testing, ci-cd, api, architecture, security, performance, ui, data, build, aot, and cli categories, including a dedicated copilot-negative routing case.
- **files edited/created**: `tests/agent-routing/cases.json`

### T2: Build Single Runner
- **depends_on**: [T1]
- **location**: `tests/agent-routing/check-skills.cs`
- **description**: Implement one file-based app that runs target agent CLIs, enforces timeout, captures stdout/stderr, and extracts skill evidence. Runner expands each agent-agnostic case across all agents by default (with optional agent filters).
- **validation**: `dotnet run --file tests/agent-routing/check-skills.cs -- --help` works and default invocation executes every case for every agent, returning normalized JSON.
- **status**: Completed
- **log**: Implemented live mode, argument parsing, timeout/process execution, normalized JSON output, and pass/fail/infra_error classification logic. Evidence matching prioritizes tool-activity signals (`required_any_evidence`) and explicit skill-load evidence. Added single-command entrypoint in `test.sh`.
- **files edited/created**: `tests/agent-routing/check-skills.cs`, `test.sh`

### T3: Add Log Fallback Parsing
- **depends_on**: [T2]
- **location**: `tests/agent-routing/check-skills.cs`
- **description**: If CLI output is insufficient, parse recent log files from home dirs (`~/.claude`, `~/.codex`, and Copilot-configured locations) to find expected evidence.
- **validation**: Runner can classify cases with output-only and with log-fallback paths.
- **status**: Completed
- **log**: Added fallback log scanning with default roots and env-var overrides (`AGENT_*_LOG_DIRS`) and integrated fallback evidence evaluation into live classification so tool usage can be proven from logs when stdout/stderr is incomplete.
- **files edited/created**: `tests/agent-routing/check-skills.cs`

### T4: Keep CI Routing Live-Only
- **depends_on**: [T3]
- **location**: `.github/workflows/agent-live-routing.yml`
- **description**: Keep routing verification live-only and use the live workflow as the routing source of truth.
- **validation**: Routing checks run through live workflow only.
- **status**: Completed
- **log**: Removed fixture artifacts and fixture-mode gating. Routing verification now relies on live evidence (output/logs) only.
- **files edited/created**: `tests/agent-routing/check-skills.cs`, `test.sh`, `.github/workflows/agent-live-routing.yml`, `docs/agent-routing-tests.md`

### T5: Add Live Full-Corpus Workflow
- **depends_on**: [T2]
- **location**: `.github/workflows/agent-live-routing.yml`
- **description**: Add `workflow_dispatch` + optional schedule workflow that runs the agent-agnostic case set across all agents by default, writes JSON artifacts, and reports `pass|fail|infra_error`. Keep workflow structure simple (single runner entrypoint; optional agent/category filters only).
- **validation**: Workflow runs end-to-end in default run-everything mode and artifacts show per-case evidence for all agents/categories.
- **status**: Completed
- **log**: Added new live workflow with manual/scheduled triggers, optional agent/category/fail-on-infra inputs, artifact upload, and job summary metrics.
- **files edited/created**: `.github/workflows/agent-live-routing.yml`

### T6: Document and Finalize
- **depends_on**: [T4, T5]
- **location**: `README.md`, `docs/agent-routing-tests.md`
- **description**: Document exactly how to run live checks, how evidence is matched, and how to troubleshoot auth/CLI/log access issues.
- **validation**: A contributor can run checks from docs without extra tribal knowledge.
- **status**: Completed
- **log**: Added focused routing-check documentation and linked commands from README. Documented runner behavior, env overrides, workflows, and troubleshooting.
- **files edited/created**: `README.md`, `docs/agent-routing-tests.md`

## CI Commands
- Live full corpus (manual/scheduled):
  - `./test.sh`

## Done Criteria
- Live workflow proves skill usage behavior for all three agents across broad category coverage.
- Evidence collection works from direct output and log fallback.
