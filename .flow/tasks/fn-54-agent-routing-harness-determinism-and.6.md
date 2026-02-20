# fn-54-agent-routing-harness-determinism-and.6 Update operator docs for telemetry, evidence tiers, and provider matrix

## Description
Update operator documentation for all new harness features: run IDs, lifecycle telemetry, ComputeTier function, typed requirements, failure categories, log scan gating, disallowed tier gating, provider matrix, and targeted reruns.

**Size:** S
**Files:** `docs/agent-routing-tests.md`, `test.sh` (help block only)

## Approach

- "Run IDs and Telemetry" section: batch_run_id/unit_run_id, lifecycle transitions, ARTIFACT_DIR discovery
- "Evidence Tiers" section: ComputeTier function, provider-aware Tier 1 signals (Claude: tool_use/Launching; Codex/Copilot: Base directory marker only), per-token best-hit model, typed requirements (required_skills vs required_files vs legacy required_all_evidence)
- "Log Fallback Policy" section: Tier 2 cap, diagnostics-only when parallel, --allow-log-fallback-pass, --enable-log-scan flags
- "Failure Categories" section: timeout/transport/assertion (parse deferred). Distinction from mismatch failure_kind.
- "Case Schema" section: required_skills, required_files, optional_skills, disallowed_skills (with disallowed_min_tier), provider_aliases
- "Targeted Reruns" section with examples: `./test.sh --agents claude --case-id foundation-version-detection`
- "Provider Matrix and Deltas" section: CI matrix, baseline schema, regression rules, timeout handling, missing artifact behavior
- Update failure taxonomy table: mismatch kinds (weak_evidence_only, disallowed_hit, optional_only, mixed) + categories (timeout, transport, assertion)

## Key context

- Current doc (110 lines) covers: files, commands, source setup, filters, evidence semantics, env vars, troubleshooting
- Memory: "grep-verifiable ACs" — each section verifiable by unique heading

## Acceptance
- [ ] `grep "Run IDs" docs/agent-routing-tests.md` finds telemetry section
- [ ] `grep "Evidence Tiers" docs/agent-routing-tests.md` finds tier explanation with ComputeTier
- [ ] `grep "Log Fallback" docs/agent-routing-tests.md` finds fallback policy section
- [ ] `grep "Failure Categories" docs/agent-routing-tests.md` finds timeout/transport/assertion docs
- [ ] `grep "Case Schema" docs/agent-routing-tests.md` finds schema documentation
- [ ] `grep "Targeted Reruns" docs/agent-routing-tests.md` finds rerun examples
- [ ] `grep "Provider Matrix" docs/agent-routing-tests.md` finds CI matrix section
- [ ] Failure taxonomy includes: weak_evidence_only, disallowed_hit, optional_only, mixed, timeout, transport, assertion
- [ ] test.sh --help documents --max-parallel, --artifacts-root, --enable-log-scan, --self-test, MAX_CONCURRENCY

## Done summary
Updated operator docs (docs/agent-routing-tests.md) and test.sh help block for all harness features from T1-T5.

### Changes
- docs/agent-routing-tests.md: Added sections for Run IDs and Telemetry, Evidence Tiers (ComputeTier, per-token model, self-test), Log Fallback Policy, Failure Categories (failure_kind + failure_category), Case Schema (all fields including typed requirements, provider aliases), Targeted Reruns, Provider Matrix and Deltas (CI matrix, baseline schema, regression rules, timeout/missing handling)
- test.sh: Help block documents --max-parallel, --artifacts-root, --enable-log-scan, --self-test, MAX_CONCURRENCY, and all other runner flags
- All 9 grep-verifiable ACs pass
- Validation passes (0 errors)
- Commits: 99e268f, 71019c4
## Evidence
- Commits: 99e268f, 71019c4
- Tests: validate-skills.sh PASSED, validate-marketplace.sh PASSED
- PRs: