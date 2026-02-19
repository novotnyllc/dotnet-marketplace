# fn-53-skill-routing-language-hardening.7 Category Sweep - API, Security, Testing, CI

## Description
Apply canonical routing language to skills assigned to this batch: api-development, security, testing, cicd categories. No overlap with T6/T8/T9.

**Size:** M
**Files:** Subset from `docs/skill-routing-ownership-manifest.md` (~26 skills)

## Approach

- Same workflow as T6 but for API/Security/Testing/CI categories
- Must include the two fn-36 skills (`dotnet-library-api-compat`, `dotnet-api-surface-validation`)
- Emit `docs/skill-routing-sweep-api-security-testing-ci.md`

## Key context

- fn-36 added two new API skills that must be included in 100% coverage
- Testing skills have significant overlap risk (e.g., `dotnet-testing-strategy` vs `dotnet-xunit` vs `dotnet-integration-testing`). Pay extra attention to scope boundaries.
## Acceptance
- [ ] All assigned skills have scope/out-of-scope sections
- [ ] All descriptions follow canonical style
- [ ] All cross-references use `[skill:]` syntax
- [ ] fn-36 skills included
- [ ] `docs/skill-routing-sweep-api-security-testing-ci.md` emitted
- [ ] Budget delta documented: no net increase
- [ ] **Similarity check**: Run similarity before and after this batch (same branch, same suppressions). `pairs_above_warn` does not increase and `unsuppressed_errors == 0`.
- [ ] `./scripts/validate-skills.sh` passes
- [ ] No skills from T6/T8/T9/T10 batches were edited
## Done summary
Normalized all 26 T7 skills (8 api-development, 7 cicd, 2 security, 9 testing) to canonical routing language: verb-led descriptions, explicit ## Scope and ## Out of scope sections with [skill:] cross-references. Budget delta: -92 chars (global CURRENT_DESC_CHARS: 11,826). fn-36 skills included. All validations pass.
## Evidence
- Commits: 7b95ffc, 210f993, b26f770, 07ebe5a
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/validate-similarity.py
- PRs: