# fn-53-skill-routing-language-hardening.12 Contributor Guidance, CI Gates, and Rollout

## Description
Update all contributor-facing documentation to codify routing-language standards. Update CI gates to enforce the new policy. Add CHANGELOG entry. Publish final compliance summary.

**Size:** M
**Files:**
- `CONTRIBUTING-SKILLS.md` (edit -- final pass incorporating T2 style guide + T3 validator + T11 verification results)
- `CONTRIBUTING.md` (edit -- sync cross-reference syntax, description budget sections)
- `CLAUDE.md` (edit -- update cross-ref example if T2 changed format, add routing-language key rule)
- `.github/workflows/validate.yml` (edit -- enforce zero-new-warnings policy with baseline comparison)
- `CHANGELOG.md` (edit -- add entry under `## [Unreleased]` / `### Changed`)
- `docs/skill-routing-final-summary.md` (new -- compliance summary)

## Approach

- Update `CONTRIBUTING-SKILLS.md` Section 3 with final canonical rules, add reference to style guide, update pre-commit checklist with routing-language items
- Update `CONTRIBUTING.md` quick-reference to match
- Update `CLAUDE.md` cross-reference example to show canonical format
- Add CI step to validate.yml: compare current warnings against `scripts/routing-warnings-baseline.json`, fail if increased
- CHANGELOG entry: "Changed: Standardized routing language across all 130 skills and 14 agents for reliable skill discovery"
- Emit final compliance summary with aggregate stats

## Key context

- Follow Keep a Changelog format for CHANGELOG.md
- `CLAUDE.md` is loaded into every Claude session -- keep additions concise
- Memory pitfall: "Skill/category counts in prose AND Mermaid diagrams must both be updated" -- check for count references
## Acceptance
- [ ] `CONTRIBUTING-SKILLS.md` fully reflects canonical routing-language rules and references style guide
- [ ] `CONTRIBUTING.md` quick-reference section synced with CONTRIBUTING-SKILLS.md
- [ ] `CLAUDE.md` cross-reference example uses canonical format
- [ ] `.github/workflows/validate.yml` enforces zero-new-warnings policy
- [ ] `CHANGELOG.md` has entry for routing language standardization
- [ ] `docs/skill-routing-final-summary.md` emitted with compliance stats
- [ ] `./scripts/validate-skills.sh` passes
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] CI pipeline passes end-to-end
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
