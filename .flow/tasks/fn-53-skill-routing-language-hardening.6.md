# fn-53-skill-routing-language-hardening.6 Category Sweep - Core, Architecture

## Description
Apply canonical routing language to skills assigned to this batch by the T1 ownership manifest. Categories: core-csharp, architecture. No overlap with T7/T8/T9.

**Size:** M
**Files:** Subset from `docs/skill-routing-ownership-manifest.md` (~30 skills)

## Approach

- Read ownership manifest to get exact skill list for this task
- For each skill: normalize description (≤120 chars, front-loaded verb, what+when), add/update `## Scope` and `## Out of scope` sections, convert all cross-refs to `[skill:]` format
- Track budget delta per skill
- Run validator after completing batch
- Emit `docs/skill-routing-sweep-core-arch.md` with before/after stats

## Key context

- Budget-neutral: if a description grows, shorten another in the same batch
- Follow the T2 style guide exactly -- no creative reinterpretation
- Memory pitfall: "Every skill section MUST use explicit `##` headers" -- not inline bold labels
## Acceptance
- [ ] All assigned skills have scope/out-of-scope sections
- [ ] All descriptions follow canonical style (≤120 chars, front-loaded verb)
- [ ] All cross-references use `[skill:]` syntax
- [ ] `docs/skill-routing-sweep-core-arch.md` emitted with before/after stats
- [ ] Budget delta documented: no net increase
- [ ] **Similarity check**: Run similarity before and after this batch (same branch, same suppressions). `pairs_above_warn` does not increase and `unsuppressed_errors == 0`.
- [ ] `./scripts/validate-skills.sh` passes
- [ ] No skills from T7/T8/T9/T10 batches were edited
## Done summary
Normalized 30 T6 skills (13 architecture, 17 core-csharp) to canonical routing language: verb-led descriptions, explicit ## Scope and ## Out of scope sections, budget-negative delta of -71 chars (11,918 total). Emitted docs/skill-routing-sweep-core-arch.md with before/after stats.
## Evidence
- Commits: 9f7e6a9e494207bbae1409a84e0872eb2af6c4c1
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/validate-similarity.py --repo-root .
- PRs: