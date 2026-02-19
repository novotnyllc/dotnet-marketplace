# Skill Routing Sweep Report: Long Tail (T9)

Generated for fn-53-skill-routing-language-hardening.9.

## Summary

- **Skills normalized:** 34 (3 build-system, 6 cli-tools, 5 documentation, 3 packaging, 5 performance, 7 project-structure, 1 release-management, 4 serialization)
- **Budget delta:** -108 characters (budget-negative)
- **Budget before (T9 batch):** 3,194 characters
- **Budget after (T9 batch):** 3,086 characters
- **Global CURRENT_DESC_CHARS:** 11,595 (< 12,000 threshold)
- **BUDGET_STATUS:** OK
- **Similarity pairs_above_warn:** 0 (unchanged from baseline)

## Changes Applied

All 34 skills received the following normalizations per the T2 style guide:

1. **Description:** Converted from participle/gerund leads to third-person declarative verbs (e.g., "Diagnosing slow builds" -> "Diagnoses slow builds")
2. **## Scope:** Added explicit `## Scope` section with bullet-pointed coverage topics
3. **## Out of scope:** Converted inline `**Scope boundary:**` / `**Out of scope:**` bold labels to proper `## Out of scope` heading with bulleted cross-references
4. **Cross-references:** Verified all use `[skill:]` syntax (already compliant pre-sweep)

## Before/After Description Comparison

| Skill | Before (chars) | After (chars) | Delta |
|-------|---------------|--------------|-------|
| dotnet-build-optimization | 86 | 86 | 0 |
| dotnet-msbuild-authoring | 116 | 93 | -23 |
| dotnet-msbuild-tasks | 89 | 88 | -1 |
| dotnet-cli-architecture | 96 | 95 | -1 |
| dotnet-cli-distribution | 93 | 92 | -1 |
| dotnet-cli-packaging | 87 | 86 | -1 |
| dotnet-cli-release-pipeline | 88 | 87 | -1 |
| dotnet-system-commandline | 112 | 97 | -15 |
| dotnet-tool-management | 86 | 84 | -2 |
| dotnet-api-docs | 90 | 89 | -1 |
| dotnet-documentation-strategy | 92 | 91 | -1 |
| dotnet-github-docs | 92 | 91 | -1 |
| dotnet-mermaid-diagrams | 94 | 93 | -1 |
| dotnet-xml-docs | 91 | 90 | -1 |
| dotnet-github-releases | 91 | 90 | -1 |
| dotnet-msix | 94 | 93 | -1 |
| dotnet-nuget-authoring | 90 | 89 | -1 |
| dotnet-benchmarkdotnet | 117 | 91 | -26 |
| dotnet-ci-benchmarking | 92 | 91 | -1 |
| dotnet-gc-memory | 99 | 87 | -12 |
| dotnet-performance-patterns | 88 | 91 | +3 |
| dotnet-profiling | 93 | 92 | -1 |
| dotnet-add-analyzers | 97 | 95 | -2 |
| dotnet-add-ci | 93 | 91 | -2 |
| dotnet-add-testing | 88 | 86 | -2 |
| dotnet-artifacts-output | 90 | 95 | +5 |
| dotnet-modernize | 95 | 94 | -1 |
| dotnet-project-structure | 93 | 90 | -3 |
| dotnet-scaffold-project | 94 | 93 | -1 |
| dotnet-release-management | 93 | 92 | -1 |
| dotnet-grpc | 87 | 85 | -2 |
| dotnet-realtime-communication | 96 | 94 | -2 |
| dotnet-serialization | 100 | 94 | -6 |
| dotnet-service-communication | 92 | 91 | -1 |
| **Total** | **3,194** | **3,086** | **-108** |

## Similarity Check

| Metric | Before | After |
|--------|--------|-------|
| pairs_above_warn | 0 | 0 |
| pairs_above_error | 0 | 0 |
| unsuppressed_errors | 0 | 0 |
| max_score | 0.5416 | 0.5416 |

## Validation

- `./scripts/validate-skills.sh` -- PASSED (0 errors)
- `./scripts/validate-marketplace.sh` -- PASSED (0 errors)
- No skills from T6/T7/T8/T10 batches were edited
