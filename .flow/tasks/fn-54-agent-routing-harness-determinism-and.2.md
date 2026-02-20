# fn-54-agent-routing-harness-determinism-and.2 Reshape evidence evaluation to per-token tier-gated model

## Description
Reshape evidence evaluation to per-token best-hit with `ComputeTier(agent, token, line, score)` as single source of truth. Implement explicit per-provider regexes with token attribution, and make `expected_skill` implicitly Tier 1 gated.

**Size:** M
**Files:** `tests/agent-routing/check-skills.cs`

## Approach

- Define `EvidenceHit` record: `{ string Token, int BestScore, int Tier, string SourceKind, string SourceDetail, string ProofLine }`
- Extend `EvidenceEvaluation` with `Dictionary<string, EvidenceHit> TokenHits`
- Implement `ComputeTier(string agent, string token, string line, int score)`:
  - **Claude Tier 1:** regex `"name"\s*:\s*"Skill"` (score 1000) OR `Launching skill:\s*(?<skill>.+)` (score 900). Token attribution: derive from `<skill>` capture group or `"input"` JSON context. Must contain token substring.
  - **Codex/Copilot Tier 1:** regex `Base directory for this skill:\s*(?<path>.+)`. Token attribution: require `/<token>/` in `<path>`. If path doesn't contain the required_skill token → NOT Tier 1 for that token (falls to Tier 2).
  - **All Tier 2:** score 60-800, or Tier 1 regex hit without token attribution.
  - **All Tier 3:** score < 60.
  - ScoreProofLine values are inputs, not tier definitions.
- Tie-breaker for per-token best-hit: higher tier > higher score > cli_output over log_fallback > stable ordering
- `expected_skill` implicit Tier 1: each case's `expected_skill` field auto-added to `required_skills[]` (Tier 1 gating) unless case sets `expected_skill_min_tier: 2`. This ensures Tier 1 gating is active on existing 14 cases without bulk-editing cases.json.
- Typed requirements: `required_skills[]` (Tier 1), `required_files[]` (Tier 2). Legacy `required_all_evidence` preserved with Tier 2 default.
- `EvidenceEvaluation.Merge()`: select strongest hit per token, cap all log_fallback at Tier 2
- When `MaxParallel > 1`: log_fallback diagnostics-only. `--allow-log-fallback-pass` (default false, auto serial).
- Log scanning: uses per-agent-per-batch snapshot from T4. Off when parallel by default.
- `weak_evidence_only` failure kind when all evidence is Tier 3

## Key context

- `ScoreProofLine()` at L729-774 produces scores — inputs to ComputeTier
- `EvidenceEvaluation.Merge()` at L1382 merges without strength — this gets reshaped
- `BuildRequiredAllEvidence()` at L863 has Claude SKILL.md skipping — compatible with tier system
- Generic file reads remain Tier 2 for ALL providers — prevents "read the docs" false positives
- `expected_skill` is present on all 14 existing cases — implicit Tier 1 activates gating immediately

## Acceptance
- [ ] `ComputeTier(agent, token, line, score)` exists with explicit regexes per provider
- [ ] Claude Tier 1: `"name":"Skill"` / `Launching skill:` with token attribution — verifiable: proof line with `Launching skill: dotnet-xunit` → Tier 1 for `dotnet-xunit`
- [ ] Codex/Copilot Tier 1: `Base directory for this skill:` requires `/<token>/` in path — verifiable: path `/skills/testing/dotnet-xunit/SKILL.md` → Tier 1 for `dotnet-xunit`; path without token → Tier 2
- [ ] `expected_skill` auto-added to required_skills (Tier 1) — verifiable: existing case with expected_skill `dotnet-xunit` requires Tier 1 evidence for that skill
- [ ] `expected_skill_min_tier: 2` opt-out works — verifiable: case with opt-out accepts Tier 2
- [ ] EvidenceEvaluation carries `TokenHits` with per-token `EvidenceHit`
- [ ] Tie-breaker: higher tier > higher score > cli_output > log_fallback > stable
- [ ] Legacy `required_all_evidence` defaults Tier 2 — all 14 cases pass
- [ ] log_fallback capped Tier 2; diagnostics-only when parallel; `--allow-log-fallback-pass` auto serial
- [ ] `weak_evidence_only` emitted when only Tier 3 evidence found
