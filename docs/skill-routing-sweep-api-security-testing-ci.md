# Skill Routing Sweep Report: API, Security, Testing, CI (T7)

Generated for fn-53-skill-routing-language-hardening.7.

## Summary

- **Skills normalized:** 26 (8 api-development, 7 cicd, 2 security, 9 testing)
- **Budget delta:** -84 characters (budget-negative)
- **Budget before (T7 batch):** 2,388 characters
- **Budget after (T7 batch):** 2,304 characters
- **Global CURRENT_DESC_CHARS:** 11,834 (< 12,000 threshold)
- **BUDGET_STATUS:** OK
- **Similarity pairs_above_warn:** 0 (unchanged from baseline)

## Changes Applied

All 26 skills received the following normalizations per the T2 style guide:

1. **Description:** Converted from participle/gerund leads to third-person declarative verbs (e.g., "Implementing API auth" -> "Secures ASP.NET Core APIs")
2. **## Scope:** Added explicit `## Scope` section with bullet-pointed coverage topics
3. **## Out of scope:** Converted inline `**Out of scope:**` / `**Scope boundary:**` bold labels to proper `## Out of scope` heading with bulleted cross-references
4. **Cross-references:** Verified all use `[skill:]` syntax (already compliant pre-sweep)
5. **fn-36 skills:** Both `dotnet-library-api-compat` and `dotnet-api-surface-validation` included and normalized

## Before/After Description Comparison

| Skill | Before (chars) | After (chars) | Delta |
|-------|---------------|--------------|-------|
| dotnet-api-security | 98 | 91 | -7 |
| dotnet-api-surface-validation | 95 | 90 | -5 |
| dotnet-api-versioning | 89 | 87 | -2 |
| dotnet-csharp-api-design | 103 | 95 | -8 |
| dotnet-input-validation | 88 | 87 | -1 |
| dotnet-library-api-compat | 94 | 92 | -2 |
| dotnet-middleware-patterns | 87 | 85 | -2 |
| dotnet-openapi | 87 | 86 | -1 |
| dotnet-ado-build-test | 89 | 88 | -1 |
| dotnet-ado-patterns | 100 | 88 | -12 |
| dotnet-ado-publish | 95 | 94 | -1 |
| dotnet-ado-unique | 93 | 91 | -2 |
| dotnet-gha-deploy | 87 | 85 | -2 |
| dotnet-gha-patterns | 98 | 90 | -8 |
| dotnet-gha-publish | 91 | 90 | -1 |
| dotnet-cryptography | 93 | 86 | -7 |
| dotnet-secrets-management | 91 | 84 | -7 |
| dotnet-blazor-testing | 89 | 87 | -2 |
| dotnet-integration-testing | 90 | 88 | -2 |
| dotnet-maui-testing | 86 | 87 | +1 |
| dotnet-playwright | 92 | 91 | -1 |
| dotnet-snapshot-testing | 89 | 88 | -1 |
| dotnet-test-quality | 100 | 95 | -5 |
| dotnet-testing-strategy | 87 | 86 | -1 |
| dotnet-ui-testing-core | 87 | 85 | -2 |
| dotnet-uno-testing | 90 | 88 | -2 |
| **Total** | **2,388** | **2,304** | **-84** |

## Similarity Check

| Metric | Before | After |
|--------|--------|-------|
| pairs_above_warn | 0 | 0 |
| pairs_above_error | 0 | 0 |
| unsuppressed_errors | 0 | 0 |
| max_score | 0.5429 | 0.5416 |

## Validation

- `./scripts/validate-skills.sh` -- PASSED (0 errors)
- `./scripts/validate-marketplace.sh` -- PASSED (0 errors)
- No skills from T6/T8/T9/T10 batches were edited
