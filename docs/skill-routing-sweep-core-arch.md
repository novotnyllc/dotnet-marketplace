# Skill Routing Sweep Report: Core, Architecture (T6)

Generated for fn-53-skill-routing-language-hardening.6.

## Summary

- **Skills normalized:** 30 (13 architecture, 17 core-csharp)
- **Budget delta:** -71 characters (budget-negative)
- **Budget before (T6 batch):** 2,837 characters
- **Budget after (T6 batch):** 2,766 characters
- **Global CURRENT_DESC_CHARS:** 11,918 (< 12,000 threshold)
- **BUDGET_STATUS:** OK
- **Similarity pairs_above_warn:** 0 (unchanged from baseline)

## Changes Applied

All 30 skills received the following normalizations per the T2 style guide:

1. **Description:** Converted from participle/gerund leads to third-person declarative verbs (e.g., "Using .NET Aspire" -> "Orchestrates .NET Aspire apps")
2. **## Scope:** Added explicit `## Scope` section with bullet-pointed coverage topics
3. **## Out of scope:** Converted inline `**Out of scope:**` / `**Scope boundary:**` bold labels to proper `## Out of scope` heading with bulleted cross-references
4. **Cross-references:** Verified all use `[skill:]` syntax (already compliant pre-sweep)

## Before/After Description Comparison

| Skill | Before (chars) | After (chars) | Delta |
|-------|---------------|--------------|-------|
| dotnet-aspire-patterns | 98 | 96 | -2 |
| dotnet-background-services | 94 | 92 | -2 |
| dotnet-container-deployment | 94 | 92 | -2 |
| dotnet-containers | 93 | 92 | -1 |
| dotnet-data-access-strategy | 101 | 88 | -13 |
| dotnet-domain-modeling | 95 | 93 | -2 |
| dotnet-efcore-architecture | 90 | 96 | +6 |
| dotnet-http-client | 93 | 92 | -1 |
| dotnet-messaging-patterns | 93 | 91 | -2 |
| dotnet-observability | 87 | 85 | -2 |
| dotnet-resilience | 96 | 94 | -2 |
| dotnet-solid-principles | 91 | 81 | -10 |
| dotnet-structured-logging | 95 | 93 | -2 |
| dotnet-channels | 91 | 88 | -3 |
| dotnet-csharp-async-patterns | 97 | 97 | 0 |
| dotnet-csharp-code-smells | 89 | 86 | -3 |
| dotnet-csharp-concurrency-patterns | 106 | 105 | -1 |
| dotnet-csharp-configuration | 89 | 92 | +3 |
| dotnet-csharp-dependency-injection | 98 | 90 | -8 |
| dotnet-csharp-modern-patterns | 95 | 95 | 0 |
| dotnet-csharp-nullable-reference-types | 92 | 90 | -2 |
| dotnet-csharp-source-generators | 97 | 92 | -5 |
| dotnet-csharp-type-design-performance | 109 | 98 | -11 |
| dotnet-editorconfig | 100 | 98 | -2 |
| dotnet-file-io | 85 | 88 | +3 |
| dotnet-io-pipelines | 95 | 93 | -2 |
| dotnet-linq-optimization | 97 | 96 | -1 |
| dotnet-native-interop | 93 | 91 | -2 |
| dotnet-roslyn-analyzers | 96 | 94 | -2 |
| dotnet-validation-patterns | 88 | 88 | 0 |
| **Total** | **2,837** | **2,766** | **-71** |

## Similarity Check

| Metric | Before | After |
|--------|--------|-------|
| pairs_above_warn | 0 | 0 |
| pairs_above_error | 0 | 0 |
| unsuppressed_errors | 0 | 0 |
| max_score | 0.5429 | 0.5429 |

## Validation

- `./scripts/validate-skills.sh` -- PASSED (0 errors)
- `./scripts/validate-marketplace.sh` -- PASSED (0 errors)
- No skills from T7/T8/T9/T10 batches were edited
