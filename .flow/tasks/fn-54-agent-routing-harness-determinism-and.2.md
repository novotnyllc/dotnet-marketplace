# fn-54-agent-routing-harness-determinism-and.2 Reshape evidence evaluation to per-token tier-gated model

## Description
Reshape evidence evaluation to per-token best-hit with `ComputeTier(agent, token, line, score)` as single source of truth. Implement explicit per-provider regexes with token attribution, and make `expected_skill` implicitly Tier 1 gated.

**Size:** M
**Files:** `tests/agent-routing/check-skills.cs`

## Approach

- Define `EvidenceHit` record: `{ string Token, int BestScore, int Tier, string SourceKind, string SourceDetail, string ProofLine }`
- Extend `EvidenceEvaluation` with `Dictionary<string, EvidenceHit> TokenHits`
- Implement `ComputeTier(string agent, string token, string line, int score)` — pure, deterministic, no side effects:
  - **Claude Tier 1 (primary):** regex `"name"\s*:\s*"Skill"` on lines also containing `"skill"\s*:\s*"(?<skill>[^"]+)"`. Token attribution: case-insensitive substring match of `token` in `<skill>` capture group. This is the strongest signal — direct skill identifier from tool_use JSON.
  - **Claude Tier 1 (secondary):** regex `Launching skill:\s*(?<skill>\S+)` (score 900). Token attribution: case-insensitive substring match of `token` in `<skill>` capture group. No heuristic "nearby context" parsing.
  - **Codex/Copilot Tier 1:** regex `Base directory for this skill:\s*(?<path>.+)`. Token attribution: normalize `<path>` separators to `/`, then require `"/" + token.ToLowerInvariant() + "/"` in `path.ToLowerInvariant()`. End-of-path match: also match `"/" + token.ToLowerInvariant()` at string end. If path doesn't contain the token → NOT Tier 1 (falls to Tier 2).
  - **All Tier 2:** score 60-800, or Tier 1 regex hit that fails token attribution.
  - **All Tier 3:** score < 60.
  - ScoreProofLine values are inputs, not tier definitions.
- Add `--self-test` flag: runs ComputeTier against built-in fixture inputs and asserts expected tiers. Fixtures must include at minimum: Claude primary Tier 1 hit (tool_use JSON with `"name":"Skill"` + `"skill":"dotnet-xunit"`), Claude secondary Tier 1 hit (`Launching skill: dotnet-xunit`), Claude Tier 2 fallback (Tier 1 regex without token attribution), Codex Tier 1 hit (path contains `/dotnet-xunit/`), Codex Tier 1 miss → Tier 2 (path lacks token), Tier 3 low score. Exits 0 on pass, 1 on failure with diff output. Invocation: `dotnet run --file tests/agent-routing/check-skills.cs -- --self-test`.
- Tie-breaker for per-token best-hit: higher tier > higher score > cli_output over log_fallback > stable ordering
- `expected_skill` implicit Tier 1: each case's `expected_skill` field auto-added to `required_skills[]` (Tier 1 gating) unless case sets `expected_skill_min_tier: 2`. This ensures Tier 1 gating is active on existing 14 cases without bulk-editing cases.json.
- Typed requirements: `required_skills[]` (Tier 1), `required_files[]` (Tier 2). Legacy `required_all_evidence` preserved with Tier 2 default. Normalization: if a legacy `required_all_evidence` token matches the pattern of a skill ID (i.e., it's also present in `expected_skill` or `required_skills`), it is treated as a `required_skills` entry in the new model to avoid contradictory tiering.
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
- [ ] Claude Tier 1 (primary): `"name":"Skill"` + `"skill":"<id>"` on same line — token attribution via `<id>` capture. Verifiable: tool_use JSON with `"skill":"dotnet-xunit"` → Tier 1 for `dotnet-xunit`
- [ ] Claude Tier 1 (secondary): `Launching skill:` with token attribution — verifiable: `Launching skill: dotnet-xunit` → Tier 1 for `dotnet-xunit`
- [ ] Codex/Copilot Tier 1: `Base directory for this skill:` requires `/<token>/` in path (case-insensitive, normalized separators) — verifiable: path `/skills/testing/dotnet-xunit/SKILL.md` → Tier 1 for `dotnet-xunit`; path without token → Tier 2
- [ ] `--self-test` flag: runs ComputeTier against fixture inputs, asserts expected tiers, exits 0 — verifiable: `dotnet run --file tests/agent-routing/check-skills.cs -- --self-test`
- [ ] `expected_skill` auto-added to required_skills (Tier 1) — verifiable: existing case with expected_skill `dotnet-xunit` requires Tier 1 evidence for that skill
- [ ] `expected_skill_min_tier: 2` opt-out works — verifiable: case with opt-out accepts Tier 2
- [ ] EvidenceEvaluation carries `TokenHits` with per-token `EvidenceHit`
- [ ] Tie-breaker: higher tier > higher score > cli_output > log_fallback > stable
- [ ] Legacy `required_all_evidence` defaults Tier 2 — all 14 cases pass
- [ ] log_fallback capped Tier 2; diagnostics-only when parallel; `--allow-log-fallback-pass` auto serial
- [ ] `weak_evidence_only` emitted when only Tier 3 evidence found

## Done summary
Implemented tier-based evidence gating with ComputeTier as single source of truth for per-provider regex + token attribution. Added 14 self-test fixtures, typed requirements (required_skills Tier 1, required_files Tier 2), implicit Tier 1 for expected_skill, log_fallback Tier 2 cap enforced during evaluation, diagnostics-only merge in fail paths, and updated docs.
## Evidence
- Commits: f685a78, 577b8ce, 746498b, fa140c0, 794ba1e, fbba803, 30794ad
- Tests: dotnet run --file tests/agent-routing/check-skills.cs -- --self-test, ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: