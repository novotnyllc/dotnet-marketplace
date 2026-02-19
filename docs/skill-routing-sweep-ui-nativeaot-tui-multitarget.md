# Skill Routing Sweep Report: UI, NativeAOT, TUI, MultiTarget (T8)

Generated for fn-53-skill-routing-language-hardening.8.

## Summary

- **Skills normalized:** 24 (1 ai, 1 localization, 2 multi-targeting, 4 native-aot, 2 tui, 14 ui-frameworks)
- **Budget delta:** -122 characters (budget-negative)
- **Budget before (T8 batch):** 2,300 characters
- **Budget after (T8 batch):** 2,178 characters
- **Global CURRENT_DESC_CHARS:** 11,703 (< 12,000 threshold)
- **BUDGET_STATUS:** OK
- **Similarity pairs_above_warn:** 0 (unchanged from baseline)

## Changes Applied

All 24 skills received the following normalizations per the T2 style guide:

1. **Description:** Converted from participle/gerund leads to third-person declarative verbs (e.g., "Building WPF on .NET 8+" -> "Builds WPF on .NET 8+")
2. **## Scope:** Added explicit `## Scope` section with bullet-pointed coverage topics
3. **## Out of scope:** Converted inline `**Out of scope:**` / `**Scope boundary:**` bold labels to proper `## Out of scope` heading with bulleted cross-references
4. **Platform classifier wording:** Consistent across framework families: "Blazor components" vs "MAUI mobile" vs "Uno Platform cross-platform" vs "WinUI 3 desktop" vs "WPF desktop" vs "WinForms desktop"
5. **Cross-references:** Verified all use `[skill:]` syntax (already compliant pre-sweep)

## Before/After Description Comparison

| Skill | Before (chars) | After (chars) | Delta |
|-------|---------------|--------------|-------|
| dotnet-semantic-kernel | 98 | 88 | -10 |
| dotnet-localization | 95 | 94 | -1 |
| dotnet-multi-targeting | 87 | 87 | 0 |
| dotnet-version-upgrade | 86 | 85 | -1 |
| dotnet-aot-architecture | 92 | 90 | -2 |
| dotnet-aot-wasm | 88 | 87 | -1 |
| dotnet-native-aot | 95 | 91 | -4 |
| dotnet-trimming | 109 | 96 | -13 |
| dotnet-spectre-console | 95 | 93 | -2 |
| dotnet-terminal-gui | 99 | 97 | -2 |
| dotnet-accessibility | 98 | 94 | -4 |
| dotnet-blazor-auth | 97 | 95 | -2 |
| dotnet-blazor-components | 109 | 91 | -18 |
| dotnet-blazor-patterns | 92 | 84 | -8 |
| dotnet-maui-aot | 98 | 97 | -1 |
| dotnet-maui-development | 90 | 87 | -3 |
| dotnet-ui-chooser | 92 | 90 | -2 |
| dotnet-uno-mcp | 97 | 89 | -8 |
| dotnet-uno-platform | 92 | 88 | -4 |
| dotnet-uno-targets | 95 | 93 | -2 |
| dotnet-winforms-basics | 98 | 91 | -7 |
| dotnet-winui | 99 | 92 | -7 |
| dotnet-wpf-migration | 100 | 82 | -18 |
| dotnet-wpf-modern | 99 | 97 | -2 |
| **Total** | **2,300** | **2,178** | **-122** |

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
- No skills from T6/T7/T9/T10 batches were edited
