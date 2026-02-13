# fn-14-maui-skills.1 Create MAUI development and AOT skills

## Description
Create two MAUI skills covering development patterns with honest current-state assessment and Native AOT on iOS/Mac Catalyst. Each skill follows canonical frontmatter (`name`, `description`) and uses `[skill:name]` cross-reference syntax. Both skills are registered in `plugin.json` and verified in the `dotnet-advisor` catalog.

### Deliverables
- `skills/ui-frameworks/dotnet-maui-development/SKILL.md` — MAUI development patterns: project structure (single-project with platform folders), XAML patterns (data binding, MVVM with CommunityToolkit.Mvvm, Shell navigation), platform services (partial classes, conditional compilation, DI), honest current-state assessment (VS 2026 bugs, iOS gaps, 36% YoY growth, 557% community PR increase), migration options (WinUI for Windows-only, Uno for web/Linux), .NET 11 content (XAML source gen default with `<MauiXamlInflator>XamlC</MauiXamlInflator>` revert, CoreCLR for Android default with `<UseMonoRuntime>true</UseMonoRuntime>` opt-out, `dotnet run` device selection), Hot Reload per platform
- `skills/ui-frameworks/dotnet-maui-aot/SKILL.md` — Native AOT on iOS/Mac Catalyst: compilation pipeline, up to 50% size reduction, up to 50% startup improvement, library compatibility gaps, opt-out mechanisms (`<PublishAot>false</PublishAot>`), trimming interplay (RD.xml, source generators), testing AOT builds on device
- Both skills registered in `.claude-plugin/plugin.json` `skills` array
- Verify existing `dotnet-advisor` catalog entries for both skills match implemented descriptions; deduplicate if needed

### Cross-references
- Hard: `[skill:dotnet-maui-testing]` (exists at `skills/testing/dotnet-maui-testing/SKILL.md`)
- Soft: `[skill:dotnet-native-aot]`, `[skill:dotnet-aot-wasm]`, `[skill:dotnet-ui-chooser]` (may not exist yet)

### Files modified
- `skills/ui-frameworks/dotnet-maui-development/SKILL.md` (new)
- `skills/ui-frameworks/dotnet-maui-aot/SKILL.md` (new)
- `.claude-plugin/plugin.json` (add 2 skill paths)
- `skills/foundation/dotnet-advisor/SKILL.md` (verify/deduplicate catalog entries)

## Acceptance
- [ ] `dotnet-maui-development` SKILL.md exists with `name` and `description` frontmatter
- [ ] `dotnet-maui-development` covers all 10 topics from epic Development Content Coverage table
- [ ] `dotnet-maui-development` includes .NET 11: XAML source gen default, CoreCLR for Android default, `dotnet run` device selection
- [ ] `dotnet-maui-development` includes honest current-state assessment (VS 2026 issues, iOS gaps, growth metrics)
- [ ] `dotnet-maui-development` presents migration options (WinUI, Uno) with objective guidance
- [ ] `dotnet-maui-aot` SKILL.md exists with `name` and `description` frontmatter
- [ ] `dotnet-maui-aot` covers all 7 topics from epic AOT Content Coverage table
- [ ] `dotnet-maui-aot` documents opt-out mechanisms and library compatibility gaps
- [ ] Both skills registered in `plugin.json`
- [ ] Both skills present in `dotnet-advisor` catalog; no duplicate IDs
- [ ] Hard cross-ref `[skill:dotnet-maui-testing]` present and resolvable
- [ ] Soft cross-refs `[skill:dotnet-native-aot]`, `[skill:dotnet-aot-wasm]`, `[skill:dotnet-ui-chooser]` present
- [ ] Each skill description ≤ 120 chars
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
Created dotnet-maui-development (project structure, XAML/MVVM, platform services, .NET 11 improvements, honest current-state assessment, migration options) and dotnet-maui-aot (Native AOT pipeline for iOS/Mac Catalyst, size/startup gains, library compatibility matrix, ILLink trimming, testing workflow) skills. Both registered in plugin.json and present in dotnet-advisor catalog with proper cross-references.
## Evidence
- Commits: 109d04e, 02ca624, 99306cd
- Tests: ./scripts/validate-skills.sh
- PRs: