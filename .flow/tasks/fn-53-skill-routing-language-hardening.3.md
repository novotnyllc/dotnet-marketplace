# fn-53-skill-routing-language-hardening.3 Validator and Compliance Report Hardening

## Description
Extend `_validate_skills.py` with new routing-language quality checks defined in the T2 style guide. Create a standalone compliance report script that outputs per-skill compliance data for PR review. Define CI policy: zero errors, zero new warnings vs committed baseline file.

**Size:** M
**Files:**
- `scripts/_validate_skills.py` (edit)
- `scripts/validate-skills.sh` (edit -- update header docs for new output keys)
- `scripts/skill-routing-report.py` (new -- compliance report)
- `scripts/routing-warnings-baseline.json` (new -- committed baseline)
- `.github/workflows/validate.yml` (edit -- add new output key parsing)

## Approach

- New validator checks to add:
  - Scope section presence (`## Scope` header required)
  - Out-of-scope section presence (`## Out of scope` header required)
  - Out-of-scope attribution format (each out-of-scope item should reference owning skill via `[skill:]`)
  - Self-referential cross-link detection (skill referencing itself)
  - Cycle detection (A→B→A) in cross-references
- New stable CI-parseable output keys: `MISSING_SCOPE_COUNT`, `MISSING_OOS_COUNT`, `SELF_REF_COUNT`
- Compliance report script: reads all SKILL.md files, outputs JSON with per-skill compliance metrics (description length, scope coverage, ref format, overlap candidates)
- Baseline file: JSON with current warning counts, committed to repo. CI compares current run against baseline.
- Flip `--allow-planned-refs` to strict by default (broken refs = errors). Existing planned refs that are legitimate must be added to an explicit allowlist.

## Key context

- Current validator: `scripts/_validate_skills.py` checks 8 things (see docstring lines 3-17). New checks extend this list.
- Follow existing patterns: filler phrase detection uses `FILLER_PHRASES` list, new checks should follow same structure.
- Memory pitfall: "Hand-authored YAML configuration files require CI validation rules" -- baseline JSON must have CI validation.
## Acceptance
- [ ] `_validate_skills.py` has new checks: scope presence, out-of-scope presence, out-of-scope attribution, self-referential refs, cycle detection
- [ ] New stable output keys documented in `validate-skills.sh` header
- [ ] `scripts/skill-routing-report.py` generates per-skill compliance JSON
- [ ] `scripts/routing-warnings-baseline.json` committed with current counts
- [ ] `--allow-planned-refs` default flipped to strict (or policy documented if kept)
- [ ] `.github/workflows/validate.yml` parses new output keys
- [ ] `./scripts/validate-skills.sh` passes (existing skills may need allowlist entries)
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
