# PRD: Routing Reliability and Skill Invocation Integrity

## Document Control

- Status: Draft
- Owner: dotnet-artisan maintainers
- Last updated: 2026-02-19
- Related Flow epics:
  - `fn-54-agent-routing-harness-determinism-and`
  - `fn-57-skill-content-invocation-contracts-and`

## Problem Statement

The routing test system correctly catches many failures, but it still has gaps that reduce confidence:

- Runs can appear stuck without clear progress output.
- Parallelizable test units are not fully exploited for faster feedback.
- Evidence matching can allow false positives from weak or fallback signals.
- Prompt and provider nondeterminism can blur true regressions.
- Skill content can be valid but still weakly invocable, leading to skipped skill usage.

We need a stronger system that verifies skills are actually used (not skipped), while protecting behavior across Codex, Copilot, and Claude.

## Goals

1. Make routing test execution transparent and observable in real time.
2. Increase throughput with safe parallelism and isolated run artifacts.
3. Improve evidence integrity so required-skill assertions are reliable.
4. Encode nondeterminism-aware evaluation semantics without masking regressions.
5. Strengthen SKILL.md content so invocation signals are explicit and testable.
6. Prevent provider-targeted fixes from regressing non-target providers.

## Non-Goals

- Replacing the full test harness with a new framework.
- Overfitting prompts or expectations to one provider.
- Rewriting domain guidance just to satisfy test mechanics.

## Success Metrics

- Median local routing test duration reduced by at least 40% for equivalent scope.
- 100% of runs show lifecycle progress (queued, running, completed/failed/timeout).
- False-positive rate from fallback/weak evidence reduced to near zero in regression corpus.
- Cross-agent matrix reports provider deltas per case in every CI run.
- Priority skills updated with invocation contract coverage and validated in CI.

## Scope

### Workstream A: Technical Harness Updates

1. `test.sh` lifecycle telemetry
- Emit stable run IDs for each prompt-agent unit.
- Print per-run and aggregate progress with totals.
- Classify failure reasons (`timeout`, `transport`, `parse`, `assertion`).

2. Bounded parallelization with isolation
- Run independent prompt-agent units concurrently.
- Support `MAX_CONCURRENCY` and serial fallback mode.
- Isolate logs/artifacts per run ID to prevent cross-run contamination.

3. Evidence extraction and scoring hardening (`tests/agent-routing/check-skills.cs`)
- Define evidence tiers:
  - Tier 1: direct skill invocation
  - Tier 2: tool/action proxy evidence
  - Tier 3: weak hints
- Require high-confidence evidence for required-skill assertions.
- Ensure fallback logs cannot pass required assertions by themselves.

4. Nondeterminism-aware evaluator semantics (`tests/agent-routing/cases.json`)
- Support `required`, `optional`, and `disallowed` skill expectations.
- Support provider alias mapping for equivalent skill IDs.
- Emit granular mismatch reasons (missing required, disallowed hit, optional-only, mixed).

5. Cross-agent regression guardrails
- Matrix execution for Codex, Copilot, Claude with explicit status by provider.
- Provider delta summary in CI artifacts.
- Merge-blocking rule for “target fix regressed another provider.”

6. Operator docs
- Update debugging and triage workflow in routing test docs.
- Document targeted reruns, provider filtering, and evidence interpretation.

### Workstream B: Skill Content Updates

1. Invocation contract spec for SKILL.md
- Define required invocation cues in descriptions/body.
- Enforce explicit `## Scope` and `## Out of scope` boundaries.
- Preserve machine-parseable cross-references (`[skill:name]`).

2. High-traffic skill and agent updates
- Update top-routed skills and key agents with stronger trigger signals.
- Keep description-budget compliance and routing-style consistency.

3. Validation/linting
- Extend `validate-skills` checks for invocation-contract compliance.
- Add actionable errors with file and section targeting.
- Support staged rollout mode if needed.

4. Content-level regression tests
- Add positive and negative controls by priority domains.
- Ensure tests distinguish:
  - correct alternate route
  - skipped required skill
  - disallowed route

5. Cross-provider change policy
- Require explicit cross-provider verification for provider-targeted changes.
- Add PR checklist updates and documented decision criteria.

## Functional Requirements

1. Runner telemetry
- The system must emit progress lines for all run lifecycle transitions.
- The system must include run IDs in terminal and artifact outputs.

2. Execution model
- The system must support bounded parallel execution with deterministic final summary ordering.
- The system must keep serial mode for debugging.

3. Evidence model
- The system must separate high-confidence invocation evidence from weak generic activity.
- The system must not treat fallback logs as sufficient proof of required skill usage.

4. Case schema
- The system must allow required/optional/disallowed skill sets.
- The system must allow provider-specific alias mapping.

5. Skill content
- Priority skills must include invocation-aligned language and explicit boundaries.
- Skill and agent references must use `[skill:name]` syntax.

6. CI policy
- CI must publish provider-specific results and regression deltas.
- CI must fail if a provider-targeted fix causes regressions in non-target providers.

## Non-Functional Requirements

- Reliability: no artifact collision across parallel runs.
- Observability: all failed runs provide failure category and supporting evidence pointers.
- Maintainability: schema and lint rules are documented and versioned.
- Portability: changes work across Codex, Copilot, Claude with no provider-specific hacks as primary strategy.

## Rollout Plan

1. Phase 1: Harness observability and parallelization
- Implement telemetry + run IDs.
- Add bounded concurrency + isolation.

2. Phase 2: Evidence and evaluator hardening
- Introduce evidence tiers and strict required-skill handling.
- Add nondeterminism-aware schema semantics.

3. Phase 3: Skill contract and content migration
- Publish invocation contract spec.
- Update high-traffic skills/agents.
- Enable linting gates.

4. Phase 4: Guardrails and policy enforcement
- Ship cross-agent regression matrix deltas in CI.
- Enforce cross-provider PR policy/checklist.

## Risks and Mitigations

- Risk: stricter evidence rules increase false negatives initially.
  - Mitigation: run side-by-side comparison mode before full gate enforcement.

- Risk: parallelism introduces flaky ordering-dependent bugs.
  - Mitigation: isolate artifacts by run ID and keep deterministic final summary sorting.

- Risk: content updates drift from routing-style constraints.
  - Mitigation: enforce style + invocation contract in validator.

- Risk: provider behavior drift breaks assumptions.
  - Mitigation: keep provider-specific baselines and report deltas per run.

## Acceptance Criteria

1. A full local run displays lifecycle progress and run IDs for each prompt-agent unit.
2. Parallel execution is enabled with bounded concurrency and no artifact collisions.
3. Required-skill assertions cannot pass using weak/fallback evidence alone.
4. Case schema supports required/optional/disallowed expectations with provider aliases.
5. CI reports per-provider outcomes and blocks regressions on non-target providers.
6. Priority skills and agents satisfy invocation contract checks in validator + CI.

## Dependencies

- Existing routing hardening baseline from `fn-53`.
- Routing test files:
  - `test.sh`
  - `tests/agent-routing/check-skills.cs`
  - `tests/agent-routing/cases.json`
  - `.github/workflows/agent-live-routing.yml`
  - `docs/agent-routing-tests.md`
- Routing style rules:
  - `docs/skill-routing-style-guide.md`

## Open Questions

1. Should optional-skill matches contribute to score, or only affect diagnostics?
2. What is the default retry policy in CI for timeouts vs deterministic assertion failures?
3. Should provider baselines live in repo or be generated from rolling historical artifacts?
