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
- Convert CI to GHA strategy matrix with merge-base baseline comparison and mechanically enforceable regression gate
- Update operator docs

## Design decisions

- **Run ID scheme:** `batch_run_id` (per RunAsync) + `unit_run_id` (per work item). All artifact-related functionality (batch dir creation, `--artifacts-root`, `ARTIFACT_DIR` emission, default proof log path) owned exclusively by T4.
- **Artifact isolation — ALL files under batch dir:** Runner writes both `results.json` AND `tool-use-proof.log` under `<artifacts-root>/<batch_run_id>/` by default. No `--proof-log` needed — proof log path resolves relative to batch dir automatically. `test.sh` hardcoded `PROOF_LOG` path removed.
- **Per-token evidence model:** `EvidenceEvaluation` carries `Dictionary<string, EvidenceHit>` where `EvidenceHit = { BestScore, Tier, SourceKind, SourceDetail, ProofLine }`. Merge selects strongest hit per token. Tie-breaker: higher tier > higher score > cli_output over log_fallback > stable ordering.
- **ComputeTier — explicit per-provider regex + token attribution:**
  - Claude Tier 1: regex `"name"\s*:\s*"Skill"` (score 1000) OR `Launching skill:\s*(?<skill>.+)` (score 900). Token derived from `<skill>` capture group or surrounding JSON `"input"` context.
  - Codex/Copilot Tier 1: regex `Base directory for this skill:\s*(?<path>.+)`. Token derived: require `/<token>/` in `<path>` to attribute the hit. If path doesn't contain the required_skill token, it's NOT a Tier 1 hit for that token.
  - All providers Tier 2: score 60-800, or Tier 1 regex match that can't be attributed to a specific token.
  - All providers Tier 3: score < 60.
  - ScoreProofLine values are inputs. The function is deterministic.
- **`expected_skill` implicit Tier 1:** Each case's `expected_skill` field is implicitly treated as a `required_skills` entry (Tier 1 gating) unless the case sets `expected_skill_min_tier: 2` to opt out. This ensures Tier 1 gating is active on the existing 14-case corpus without bulk-editing cases.json.
- **Typed evidence requirements (explicit):** `required_skills[]` (Tier 1), `required_files[]` (Tier 2). Legacy `required_all_evidence` preserved with Tier 2 default. `expected_skill` auto-added to required_skills.
- **Log fallback policy:** Capped at Tier 2. Diagnostics-only when max_parallel > 1. `--allow-log-fallback-pass` (default false, auto-enabled serial). `--enable-log-scan` (default off parallel, on serial).
- **Log snapshot:** Once per agent per batch.
- **Disallowed tier gating:** `disallowed_min_tier` (default 2). Tier 3 matches diagnostics only.
- **Failure categories:** `timeout`, `transport`, `assertion`. (`parse` deferred — see PRD amendment above.)
- **CI baseline comparison — merge-base policy:** For PRs, compare against `provider-baseline.json` from the merge base (`git show origin/${GITHUB_BASE_REF}:tests/agent-routing/provider-baseline.json`). Baseline edits in the PR are allowed but regression is still detected vs the base-branch version. For pushes to main, compare against the checked-in file. This prevents "update baseline to make CI pass" without the regression being visible.
- **CI baseline schema:** `{ expected_status: pass|fail|infra_error, allow_timeout: false }` per case per provider. Timeout comparison: `timed_out && !allow_timeout` → regression. Missing artifact/results.json → hard fail.
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
        → T5 (CI matrix + merge-base baseline + regression gate)
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
- [ ] `ARTIFACT_DIR=<path>` on stderr; both results.json and tool-use-proof.log under batch dir
- [ ] `--artifacts-root` overrides base; no hardcoded proof log path in test.sh
- [ ] MAX_CONCURRENCY defaults to 4, env override, flag precedence
- [ ] `ComputeTier(agent, token, line, score)` is single tier source of truth with explicit regexes
- [ ] Codex/Copilot Tier 1 requires `/<token>/` in `Base directory` path — attribution verified
- [ ] `expected_skill` implicitly Tier 1 gated (existing cases enforce skill invocation, not just file reads)
- [ ] At least one AC per provider demonstrating Tier 1 gating is active (not just implemented but unused)
- [ ] Per-token EvidenceHit in evaluation; log_fallback capped Tier 2; diagnostics-only when parallel
- [ ] Log snapshot once per agent per batch; scanning off when parallel by default
- [ ] `disallowed_skills` tier-gated at min Tier 2; Tier 3 diagnostics only
- [ ] Mismatch kinds: missing_required, disallowed_hit, optional_only, mixed
- [ ] failure_category: timeout, transport, assertion (parse deferred with PRD amendment)
- [ ] CI matrix with merge-base baseline comparison; `timed_out && !allow_timeout` → regression
- [ ] Missing artifact → hard fail; baseline edits visible as PR diff
- [ ] Operator docs updated for all features
- [ ] All existing tests pass

## References

- PRD: `.flow/specs/prd-routing-reliability-and-skill-invocation.md`
- Predecessor: fn-53
- Key files: `test.sh`, `tests/agent-routing/check-skills.cs`, `tests/agent-routing/cases.json`, `.github/workflows/agent-live-routing.yml`, `docs/agent-routing-tests.md`
