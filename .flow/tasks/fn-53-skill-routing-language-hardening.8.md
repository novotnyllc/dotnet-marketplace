# fn-53-skill-routing-language-hardening.8 Category Sweep - UI, NativeAOT, CLI, TUI

## Description
Apply canonical routing language to skills assigned to this batch: blazor, uno-platform, maui, desktop-frameworks, native-aot-trimming, cli-tools, tui categories. No overlap with T6/T7/T9.

**Size:** M
**Files:** Subset from `docs/skill-routing-ownership-manifest.md` (~25 skills)

## Approach

- Same workflow as T6 but for UI/NativeAOT/CLI/TUI categories
- Align platform classifier wording across frameworks (Blazor vs MAUI vs Uno vs WinUI)
- Emit `docs/skill-routing-sweep-ui-nativeaot-cli-tui.md`

## Key context

- UI framework skills need clear scope boundaries: "Blazor components" vs "MAUI mobile" vs "Uno cross-platform" vs "WinUI desktop"
- AOT skills overlap with several framework skills. Scope boundaries are critical.
## Acceptance
- [ ] All assigned skills have scope/out-of-scope sections
- [ ] All descriptions follow canonical style
- [ ] Platform classifier wording is consistent across framework families
- [ ] `docs/skill-routing-sweep-ui-nativeaot-cli-tui.md` emitted
- [ ] Budget delta documented: no net increase
- [ ] `./scripts/validate-skills.sh` passes
- [ ] No skills from T6/T7/T9/T10 batches were edited
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
