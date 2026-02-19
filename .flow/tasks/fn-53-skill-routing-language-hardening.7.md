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
TBD

## Evidence
- Commits:
- Tests:
- PRs:
