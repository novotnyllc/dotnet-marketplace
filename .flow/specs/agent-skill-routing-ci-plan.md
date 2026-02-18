# Plan: Minimal Agent Skill Usage Checks (Claude, Codex, Copilot)

**Generated**: 2026-02-18 01:13:00 EST

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
- Blocking CI runs deterministic fixture checks over the full tagged corpus.
- Live agent checks run in a separate workflow (manual/scheduled) and also default to all agents/all cases.
- Use agent logs as fallback evidence sources (for example `~/.claude`, `~/.codex`, and configured Copilot output/log paths).
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
- **status**: Not Completed

### T2: Build Single Runner
- **depends_on**: [T1]
- **location**: `tests/agent-routing/check-skills.cs`
- **description**: Implement one file-based app that runs target agent CLIs, enforces timeout, captures stdout/stderr, and extracts skill evidence. Runner expands each agent-agnostic case across all agents by default (with optional agent filters).
- **validation**: `dotnet run --file tests/agent-routing/check-skills.cs -- --help` works and default invocation executes every case for every agent, returning normalized JSON.
- **status**: Not Completed

### T3: Add Log Fallback Parsing
- **depends_on**: [T2]
- **location**: `tests/agent-routing/check-skills.cs`
- **description**: If CLI output is insufficient, parse recent log files from home dirs (`~/.claude`, `~/.codex`, and Copilot-configured locations) to find expected evidence.
- **validation**: Runner can classify cases with output-only and with log-fallback paths.
- **status**: Not Completed

### T4: Add Deterministic Blocking Check (CI)
- **depends_on**: [T3]
- **location**: `tests/agent-routing/fixtures/*`, `.github/workflows/validate.yml`
- **description**: Add fixture inputs and run the runner in fixture mode over the full category-tagged corpus as a blocking PR check.
- **validation**: CI fails on induced parser/evidence regressions and passes on baseline fixtures.
- **status**: Not Completed

### T5: Add Live Full-Corpus Workflow
- **depends_on**: [T2]
- **location**: `.github/workflows/agent-live-routing.yml`
- **description**: Add `workflow_dispatch` + optional schedule workflow that runs the agent-agnostic case set across all agents by default, writes JSON artifacts, and reports `pass|fail|infra_error`. Keep workflow structure simple (single runner entrypoint; optional agent/category filters only).
- **validation**: Workflow runs end-to-end in default run-everything mode and artifacts show per-case evidence for all agents/categories.
- **status**: Not Completed

### T6: Document and Finalize
- **depends_on**: [T4, T5]
- **location**: `README.md`, `docs/agent-routing-tests.md`
- **description**: Document exactly how to run deterministic and live checks, how evidence is matched, and how to troubleshoot auth/CLI/log access issues.
- **validation**: A contributor can run both checks from docs without extra tribal knowledge.
- **status**: Not Completed

## CI Commands
- Deterministic (blocking):
  - `./test.sh fixtures`
- Live full corpus (manual/scheduled):
  - `./test.sh live`

## Done Criteria
- PR CI blocks on deterministic regressions.
- Live workflow proves skill usage behavior for all three agents across broad category coverage.
- Evidence collection works from direct output and log fallback.
