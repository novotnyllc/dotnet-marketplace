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
- [ ] test.sh --help documents --max-parallel, --artifacts-root, --enable-log-scan, MAX_CONCURRENCY
