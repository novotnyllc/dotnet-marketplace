# Agent Routing Harness Determinism and Observability

## Overview

Harden the agent routing test harness (`test.sh` + `check-skills.cs`) with lifecycle telemetry, evidence-tier gating, nondeterminism-aware evaluation semantics, and cross-provider regression guardrails. Builds on fn-53 (Skill Routing Language Hardening).

**PRD:** `.flow/specs/prd-routing-reliability-and-skill-invocation.md`
**PRD amendment:** `parse` failure category deferred to future structured-output epic. PRD to be updated with rationale: current runner performs substring matching, not JSON parsing — no meaningful parse operation exists to classify. The `timeout`, `transport`, and `assertion` categories cover all current failure modes.

## Scope

- Add stable run IDs (batch + unit) and lifecycle progress output per prompt-agent unit
- Isolate ALL artifacts (results.json + tool-use-proof.log) per batch run under `<artifacts-root>/<batch_run_id>/`
- Set sensible MAX_CONCURRENCY default (4) with env var override
- Reshape evidence evaluation to per-token best-hit model with tier/source tracking
- Implement `ComputeTier(agent, token, line, score)` with explicit regex + capture strategy per provider
- Introduce typed evidence requirements and make `expected_skill` implicitly Tier 1
- Prevent log_fallback from satisfying Tier 1; disable log_fallback pass-promotion when parallel
- Optimize log scanning: per-agent-per-batch snapshot, gated behind flag when parallel
- Extend `CaseDefinition` with `optional_skills[]`, `disallowed_skills[]` (tier-gated), `provider_aliases{}`
- Add mismatch classification (missing_required, disallowed_hit, optional_only, mixed) + failure categories (timeout, transport, assertion)
- Convert CI to GHA strategy matrix with base-branch-head baseline comparison and mechanically enforceable regression gate
- Update operator docs

## Design decisions

- **Run ID scheme:** `batch_run_id` (per RunAsync) + `unit_run_id` (per work item). T1 owns run ID generation, JSON fields, and lifecycle progress. T4 consumes `batch_run_id` for artifact directory naming, `--artifacts-root`, `ARTIFACT_DIR` emission, and default proof log path.
- **Artifact isolation — batch-level only, always written:** Runner always writes `<artifacts-root>/<batch_run_id>/results.json` and `<artifacts-root>/<batch_run_id>/tool-use-proof.log` regardless of `--output` flag. `--output` is preserved for backward compat (writes an additional copy) but the batch dir copy is unconditional. This means CI never needs to pass `--output` — the batch dir is the single source of truth. No per-unit subdirectories — two files per batch is sufficient for current debuggability. Per-unit directories deferred until concrete per-unit artifacts exist. JSON is also written to stdout as before (convenience copy). `test.sh` hardcoded `PROOF_LOG` path removed.
- **ARTIFACT_DIR is protocol output (always emitted):** Emitted once per run on stderr as a raw line: exactly `ARTIFACT_DIR=<absolute-path>` with no prefix, no timestamp, no brackets, no extra fields. Emitted immediately after batch directory creation, before any work items start. Not implemented through `LogProgress()` — uses direct `Console.Error.WriteLine()` to avoid any formatting. `--no-progress` only suppresses lifecycle transition lines (queued/running/completed/etc), never protocol lines. CI parses with: `grep '^ARTIFACT_DIR=' stderr.log | cut -d= -f2-`.
- **Per-token evidence model:** `EvidenceEvaluation` carries `Dictionary<string, EvidenceHit>` where `EvidenceHit = { BestScore, Tier, SourceKind, SourceDetail, ProofLine }`. Merge selects strongest hit per token. Tie-breaker: higher tier > higher score > cli_output over log_fallback > stable ordering.
- **ComputeTier — deterministic per-provider regex + token attribution:**
  - Claude Tier 1 (primary): regex `"name"\s*:\s*"Skill"` on lines also containing `"skill"\s*:\s*"(?<skill>[^"]+)"`. Token attribution: case-insensitive substring match of `token` in `<skill>` capture group. This is the strongest signal — direct skill identifier from tool_use JSON.
  - Claude Tier 1 (secondary): regex `Launching skill:\s*(?<skill>\S+)` (score 900). Token attribution: case-insensitive substring match of `token` in `<skill>` capture group. No heuristic "nearby context" parsing.
  - Codex/Copilot Tier 1: regex `Base directory for this skill:\s*(?<path>.+)`. Token attribution: normalize `<path>` separators to `/`, then require `"/" + token.ToLowerInvariant() + "/"` present in `path.ToLowerInvariant()`. End-of-path without trailing slash also matches via `"/" + token.ToLowerInvariant()` at string end. If path doesn't contain the token → NOT Tier 1 for that token.
  - All providers Tier 2: score 60-800, or Tier 1 regex match that fails token attribution.
  - All providers Tier 3: score < 60.
  - ScoreProofLine values are inputs. The function is pure and deterministic — no side effects, no ambient state.
- **`expected_skill` implicit Tier 1:** Each case's `expected_skill` field is implicitly treated as a `required_skills` entry (Tier 1 gating) unless the case sets `expected_skill_min_tier: 2` to opt out. This ensures Tier 1 gating is active on the existing 14-case corpus without bulk-editing cases.json.
- **Typed evidence requirements (explicit):** `required_skills[]` (Tier 1), `required_files[]` (Tier 2). Legacy `required_all_evidence` preserved with Tier 2 default. `expected_skill` auto-added to required_skills.
- **Log fallback policy:** Capped at Tier 2. Diagnostics-only when max_parallel > 1. `--allow-log-fallback-pass` (default false, auto-enabled serial). `--enable-log-scan` (default off parallel, on serial).
- **Log snapshot:** Once per agent per batch.
- **Disallowed tier gating:** `disallowed_min_tier` (default 2). Tier 3 matches diagnostics only.
- **Failure categories (deterministic mapping):** `timeout` if `TimedOut==true`; `transport` if process failed to start, CLI missing, or status is `infra_error`; `assertion` if evidence gating failed and not timed out. Mapping is evaluated in priority order (timeout > transport > assertion). (`parse` deferred — see PRD amendment above.)
- **CI baseline comparison — ref-based policy:** Workflow adds a `baseline_ref` input (default: `main`). Workflow uses `actions/checkout` with `fetch-depth: 0` and explicit `git fetch origin <baseline_ref>`, then extracts baseline via `git show origin/<baseline_ref>:tests/agent-routing/provider-baseline.json`. For `schedule` runs, `baseline_ref` defaults to `main`. For `workflow_dispatch`, operator can override to compare against any branch. Note: current workflow triggers are `workflow_dispatch` + `schedule` only (no `pull_request`), so `GITHUB_BASE_REF` is not available. If a PR trigger is added in the future, `baseline_ref` can default to `$GITHUB_BASE_REF` in that context. Baseline edits in branches are allowed but regression is still detected vs the baseline ref version.
- **CI baseline schema:** `{ expected_status: pass|fail|infra_error, allow_timeout: false }` per case per provider. Timeout comparison: `timed_out && !allow_timeout` → regression. Missing artifact/results.json → hard fail.
- **CI baseline missing-entry policy (two-file comparison):** The summarize step loads TWO baselines: (1) the **ref baseline** from `git show origin/<baseline_ref>:tests/agent-routing/provider-baseline.json` and (2) the **current baseline** from the checked-in `tests/agent-routing/provider-baseline.json` in the working tree. Behavior:
  - Every `(case_id, provider)` in results MUST have an entry in the **current baseline** — missing → hard failure: `"ERROR: No baseline entry for case '<case_id>' provider '<provider>'. Update provider-baseline.json."`. This ensures contributors add baseline entries when adding cases.
  - Regression comparison only applies to entries that exist in BOTH the ref baseline and results. Entries present in results + current baseline but absent from ref baseline are classified as **new coverage** (logged in delta table as `NEW`, no regression comparison). This prevents deadlocking case evolution — new cases pass CI without requiring `baseline_ref` to point at itself.
- **CI matrix:** `fail-fast: false`. `continue-on-error: true` copilot (infra only, not regressions).
- **Default MAX_CONCURRENCY:** 4.
- **Retry policy / timeout+evidence:** out of scope / preserved.

## Task ordering

Strict sequential (no parallel work within check-skills.cs):

```
T1 (run IDs + lifecycle + failure categories)
  → T4 (artifact isolation + concurrency + log scan + proof log)
    → T2 (ComputeTier + per-token model + typed requirements + expected_skill implicit Tier 1)
      → T3 (schema extensions + tier-gated disallowed + mismatch classification)
        → T5 (CI matrix + base-branch-head baseline + regression gate)
          → T6 (docs)
```

## Quick commands

```bash
./test.sh --agents claude --max-parallel 4
./test.sh
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Acceptance

- [ ] batch_run_id (UUID) in ResultEnvelope; unit_run_id (UUID) in each AgentResult
- [ ] Lifecycle transitions on stderr with run IDs
- [ ] `ARTIFACT_DIR=<path>` on stderr as raw line (no prefix/timestamp, always emitted, not suppressed by `--no-progress`); both results.json and tool-use-proof.log written unconditionally to batch dir
- [ ] `--artifacts-root` overrides base; no hardcoded proof log path in test.sh
- [ ] MAX_CONCURRENCY defaults to 4, env override, flag precedence
- [ ] `ComputeTier(agent, token, line, score)` is single tier source of truth with explicit regexes
- [ ] Codex/Copilot Tier 1 requires `/<token>/` in `Base directory` path (case-insensitive, normalized separators) — attribution verified
- [ ] Deterministic self-test: `--self-test` flag runs ComputeTier against fixture inputs and asserts expected tiers (at least: Claude primary Tier 1 via `"skill":"..."` field, Claude secondary Tier 1 via `Launching skill:`, Claude Tier 2 fallback, Codex Tier 1 hit, Codex Tier 1 miss → Tier 2, Tier 3 low score)
- [ ] `expected_skill` implicitly Tier 1 gated (existing cases enforce skill invocation, not just file reads)
- [ ] At least one AC per provider demonstrating Tier 1 gating is active (not just implemented but unused)
- [ ] Per-token EvidenceHit in evaluation; log_fallback capped Tier 2; diagnostics-only when parallel
- [ ] Log snapshot once per agent per batch; scanning off when parallel by default
- [ ] `disallowed_skills` tier-gated at min Tier 2; Tier 3 diagnostics only
- [ ] Mismatch kinds: missing_required, disallowed_hit, optional_only, mixed
- [ ] failure_category: timeout, transport, assertion (parse deferred with PRD amendment)
- [ ] CI matrix with `baseline_ref` input (default `main`) for baseline comparison; `timed_out && !allow_timeout` → regression
- [ ] Missing artifact → hard fail; missing current-baseline entry → hard fail; new case_id absent from ref baseline → `NEW` (no regression gate, logged in delta table)
- [ ] CI matrix jobs upload artifacts with `if: always()` so summarize always has data
- [ ] CI uses `fetch-depth: 0` and explicit `git fetch origin <baseline_ref>` for baseline ref availability
- [ ] Operator docs updated for all features
- [ ] All existing tests pass

## References

- PRD: `.flow/specs/prd-routing-reliability-and-skill-invocation.md`
- Predecessor: fn-53
- Key files: `test.sh`, `tests/agent-routing/check-skills.cs`, `tests/agent-routing/cases.json`, `.github/workflows/agent-live-routing.yml`, `docs/agent-routing-tests.md`
