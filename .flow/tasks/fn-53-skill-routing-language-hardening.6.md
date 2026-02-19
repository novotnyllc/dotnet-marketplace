# fn-53-skill-routing-language-hardening.6 Category Sweep - Core, Architecture, Performance, Build

## Description
Apply canonical routing language to skills assigned to this batch by the T1 ownership manifest. Categories: core-csharp, architecture, performance-benchmarking, msbuild-build. No overlap with T7/T8/T9.

**Size:** M
**Files:** Subset from `docs/skill-routing-ownership-manifest.md` (~30 skills)

## Approach

- Read ownership manifest to get exact skill list for this task
- For each skill: normalize description (≤120 chars, front-loaded verb, what+when), add/update `## Scope` and `## Out of scope` sections, convert all cross-refs to `[skill:]` format
- Track budget delta per skill
- Run validator after completing batch
- Emit `docs/skill-routing-sweep-core-arch-perf-build.md` with before/after stats

## Key context

- Budget-neutral: if a description grows, shorten another in the same batch
- Follow the T2 style guide exactly -- no creative reinterpretation
- Memory pitfall: "Every skill section MUST use explicit `##` headers" -- not inline bold labels
## Acceptance
- [ ] All assigned skills have scope/out-of-scope sections
- [ ] All descriptions follow canonical style (≤120 chars, front-loaded verb)
- [ ] All cross-references use `[skill:]` syntax
- [ ] `docs/skill-routing-sweep-core-arch-perf-build.md` emitted with before/after stats
- [ ] Budget delta documented: no net increase
- [ ] **Similarity check**: Run similarity before and after this batch (same branch, same suppressions). `pairs_above_warn` does not increase and `unsuppressed_errors == 0`.
- [ ] `./scripts/validate-skills.sh` passes
- [ ] No skills from T7/T8/T9/T10 batches were edited
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
