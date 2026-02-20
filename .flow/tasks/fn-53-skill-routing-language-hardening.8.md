# fn-53-skill-routing-language-hardening.8 Category Sweep - UI, NativeAOT, TUI, MultiTarget

## Description
Apply canonical routing language to skills assigned to this batch: ai, localization, multi-targeting, native-aot, tui, ui-frameworks categories. No overlap with T6/T7/T9.

**Size:** M
**Files:** Subset from `docs/skill-routing-ownership-manifest.md` (~24 skills)

## Approach

- Same workflow as T6 but for UI/NativeAOT/TUI/MultiTarget categories
- Align platform classifier wording across frameworks (Blazor vs MAUI vs Uno vs WinUI)
- Emit `docs/skill-routing-sweep-ui-nativeaot-tui-multitarget.md`

## Key context

- UI framework skills need clear scope boundaries: "Blazor components" vs "MAUI mobile" vs "Uno cross-platform" vs "WinUI desktop"
- AOT skills overlap with several framework skills. Scope boundaries are critical.
## Acceptance
- [ ] All assigned skills have scope/out-of-scope sections
- [ ] All descriptions follow canonical style
- [ ] Platform classifier wording is consistent across framework families
- [ ] `docs/skill-routing-sweep-ui-nativeaot-tui-multitarget.md` emitted
- [ ] Budget delta documented: no net increase
- [ ] **Similarity check**: Run similarity before and after this batch (same branch, same suppressions). `pairs_above_warn` does not increase and `unsuppressed_errors == 0`.
- [ ] `./scripts/validate-skills.sh` passes
- [ ] No skills from T6/T7/T9/T10 batches were edited
## Done summary
Normalized all 24 T8-assigned skills (ai, localization, multi-targeting, native-aot, tui, ui-frameworks) to canonical routing language: verb-led descriptions, explicit ## Scope and ## Out of scope headings with [skill:] cross-references, consistent platform classifier wording. Budget delta: -122 chars (global 11,703 < 12,000 threshold). Similarity pairs_above_warn: 0 (unchanged). Sweep report emitted at docs/skill-routing-sweep-ui-nativeaot-tui-multitarget.md.
## Evidence
- Commits: abcb7d5, f266599
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: