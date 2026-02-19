# fn-53-skill-routing-language-hardening.12 Contributor Guidance, CI Gates, and Rollout

## Description
Update all contributor-facing documentation to codify routing-language standards including similarity avoidance guidance. Update CI gates to enforce the new policy including similarity baseline regression detection. Tighten agent bare-ref gating. Add CHANGELOG entry. Publish final compliance summary.

**Size:** M
**Files:**
- `CONTRIBUTING-SKILLS.md` (edit -- final pass incorporating T2 style guide + T3 validator + T13 similarity + T11 verification results)
- `CONTRIBUTING.md` (edit -- sync cross-reference syntax, description budget sections)
- `CLAUDE.md` (edit -- update cross-ref example if T2 changed format, add routing-language key rule)
- `.github/workflows/validate.yml` (edit -- enforce zero-new-warnings policy with per-key baseline comparison, enable similarity baseline regression, tighten agent bare-ref gates, add new stable keys to job summary)
- `CHANGELOG.md` (edit -- add entry under `## [Unreleased]` / `### Changed`)
- `docs/skill-routing-final-summary.md` (new -- compliance summary)

## Approach

- Update `CONTRIBUTING-SKILLS.md` Section 3 with final canonical rules, add reference to style guide, update pre-commit checklist with routing-language items. **Add new section on avoiding description overlap**: explain the similarity detection tool, how to run it locally, what thresholds mean, how to request a suppression if a pair is intentionally similar.
- Update `CONTRIBUTING.md` quick-reference to match
- Update `CLAUDE.md` cross-reference example to show canonical format
- **Tighten agent bare-ref CI gate**: T3 reports `AGENT_BARE_REF_COUNT` and `AGENTSMD_BARE_REF_COUNT` as informational. After T10 normalizes agents (T10 completion guaranteed by T12's dependency on T11 which depends on T10), T12 makes these counts gating (fail on >0). Update `validate.yml` accordingly.
- **Enable similarity baseline regression (phase 2)**: T3 wired similarity in error-only mode (no --baseline). T12 upgrades to full baseline regression gating: `python3 scripts/validate-similarity.py --repo-root . --baseline scripts/similarity-baseline.json --suppressions scripts/similarity-suppressions.json`. Fail if any new WARN+ pairs appear that are not in baseline or suppression list. This is safe because all sweeps (T5-T10) are complete.
- Add CI step to validate.yml: compare current per-key warning counts against `scripts/routing-warnings-baseline.json`, fail if any key increased
- **Add new stable keys to `$GITHUB_OUTPUT` and job summary table** in `validate.yml` — at minimum the gating keys (`MISSING_SCOPE_COUNT`, `SELF_REF_COUNT`, `AGENT_BARE_REF_COUNT`, `AGENTSMD_BARE_REF_COUNT`, `MAX_SIMILARITY_SCORE`, `PAIRS_ABOVE_WARN`, `PAIRS_ABOVE_ERROR`)
- CHANGELOG entry: "Changed: Standardized routing language across all 130 skills and 14 agents for reliable skill discovery. Added semantic similarity detection to prevent description overlap."
- Emit final compliance summary with aggregate stats including similarity improvement metrics

## Key context

- Follow Keep a Changelog format for CHANGELOG.md
- `CLAUDE.md` is loaded into every Claude session -- keep additions concise
- Memory pitfall: "Skill/category counts in prose AND Mermaid diagrams must both be updated" -- check for count references
- The similarity detection script (`scripts/validate-similarity.py`) must be documented for contributors so they know to run it before submitting PRs with description changes
- T12 depends on T11, which depends on T6-T10 (including T10). This guarantees agent normalization is complete before tightening the agent bare-ref gate.

## Acceptance
- [ ] `CONTRIBUTING-SKILLS.md` fully reflects canonical routing-language rules and references style guide
- [ ] `CONTRIBUTING-SKILLS.md` has section on avoiding description overlap (similarity tool usage, thresholds, suppression requests)
- [ ] `CONTRIBUTING.md` quick-reference section synced with CONTRIBUTING-SKILLS.md
- [ ] `CLAUDE.md` cross-reference example uses canonical format
- [ ] `.github/workflows/validate.yml` enforces zero-new-warnings policy via per-key baseline comparison
- [ ] `.github/workflows/validate.yml` gates on `AGENT_BARE_REF_COUNT == 0` and `AGENTSMD_BARE_REF_COUNT == 0` (tightened from informational)
- [ ] `.github/workflows/validate.yml` enables similarity baseline regression check (`--baseline` flag added)
- [ ] `.github/workflows/validate.yml` exports new stable keys to `$GITHUB_OUTPUT` and job summary table
- [ ] `CHANGELOG.md` has entry for routing language standardization (including similarity detection)
- [ ] `docs/skill-routing-final-summary.md` emitted with compliance stats (including similarity improvement metrics)
- [ ] `./scripts/validate-skills.sh` passes
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] CI pipeline passes end-to-end
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
