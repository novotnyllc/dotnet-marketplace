# fn-53-skill-routing-language-hardening.12 Contributor Guidance, CI Gates, and Rollout

## Description
Update all contributor-facing documentation to codify routing-language standards including similarity avoidance guidance. Update CI gates to enforce the new policy including similarity regression detection. Add CHANGELOG entry. Publish final compliance summary.

**Size:** M
**Files:**
- `CONTRIBUTING-SKILLS.md` (edit -- final pass incorporating T2 style guide + T3 validator + T13 similarity + T11 verification results)
- `CONTRIBUTING.md` (edit -- sync cross-reference syntax, description budget sections)
- `CLAUDE.md` (edit -- update cross-ref example if T2 changed format, add routing-language key rule)
- `.github/workflows/validate.yml` (edit -- enforce zero-new-warnings policy with baseline comparison, add similarity baseline comparison step)
- `CHANGELOG.md` (edit -- add entry under `## [Unreleased]` / `### Changed`)
- `docs/skill-routing-final-summary.md` (new -- compliance summary)

## Approach

- Update `CONTRIBUTING-SKILLS.md` Section 3 with final canonical rules, add reference to style guide, update pre-commit checklist with routing-language items. **Add new section on avoiding description overlap**: explain the similarity detection tool, how to run it locally, what thresholds mean, how to request a suppression if a pair is intentionally similar.
- Update `CONTRIBUTING.md` quick-reference to match
- Update `CLAUDE.md` cross-reference example to show canonical format
- **Tighten agent bare-ref CI gate**: T3 reports `AGENT_BARE_REF_COUNT` and `AGENTSMD_BARE_REF_COUNT` as informational. After T10 normalizes agents, T12 makes these counts gating (fail on >0). Update `validate.yml` accordingly.
- Add CI step to validate.yml: compare current warnings against `scripts/routing-warnings-baseline.json`, fail if increased
- **Add CI step for similarity**: run `python3 scripts/validate-similarity.py --repo-root . --baseline scripts/similarity-baseline.json --suppressions scripts/similarity-suppressions.json` — fail if new pairs above WARN appear that are not in baseline or suppression list
- CHANGELOG entry: "Changed: Standardized routing language across all 130 skills and 14 agents for reliable skill discovery. Added semantic similarity detection to prevent description overlap."
- Emit final compliance summary with aggregate stats including similarity improvement metrics

## Key context

- Follow Keep a Changelog format for CHANGELOG.md
- `CLAUDE.md` is loaded into every Claude session -- keep additions concise
- Memory pitfall: "Skill/category counts in prose AND Mermaid diagrams must both be updated" -- check for count references
- The similarity detection script (`scripts/validate-similarity.py`) must be documented for contributors so they know to run it before submitting PRs with description changes

## Acceptance
- [ ] `CONTRIBUTING-SKILLS.md` fully reflects canonical routing-language rules and references style guide
- [ ] `CONTRIBUTING-SKILLS.md` has section on avoiding description overlap (similarity tool usage, thresholds, suppression requests)
- [ ] `CONTRIBUTING.md` quick-reference section synced with CONTRIBUTING-SKILLS.md
- [ ] `CLAUDE.md` cross-reference example uses canonical format
- [ ] `.github/workflows/validate.yml` enforces zero-new-warnings policy
- [ ] `.github/workflows/validate.yml` gates on `AGENT_BARE_REF_COUNT == 0` and `AGENTSMD_BARE_REF_COUNT == 0` (tightened from informational)
- [ ] `.github/workflows/validate.yml` has similarity regression check (baseline comparison)
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
