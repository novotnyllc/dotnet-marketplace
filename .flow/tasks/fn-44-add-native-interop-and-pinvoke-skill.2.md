# fn-44-add-native-interop-and-pinvoke-skill.2 Integrate dotnet-native-interop into plugin registry and routing

## Description
Register `dotnet-native-interop` in plugin.json, add routing entry in `dotnet-advisor`, and add cross-references to/from `dotnet-native-aot`, `dotnet-aot-architecture`, and `dotnet-winui`.

**Size:** S
**Files:** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`, `skills/native-aot/dotnet-native-aot/SKILL.md`, `skills/native-aot/dotnet-aot-architecture/SKILL.md`, `skills/ui-frameworks/dotnet-winui/SKILL.md`, `scripts/validate-skills.sh`

## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor`
- Add `[skill:dotnet-native-interop]` cross-references in AOT skills and WinUI (CsWin32 reference)
- Update `--projected-skills` in validate-skills.sh

## File contention warning

**plugin.json and dotnet-advisor SKILL.md are shared files** modified by all 5 integration tasks (fn-43.2 through fn-47.2). These tasks must NOT run in parallel. Run sequentially.
## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor`
- Add `[skill:dotnet-native-interop]` cross-references in AOT skills and WinUI (CsWin32 reference)
- Update `--projected-skills` count in validation
## Acceptance
- [ ] plugin.json includes `skills/core-csharp/dotnet-native-interop`
- [ ] `dotnet-advisor` has routing entry for native interop
- [ ] Cross-references added in `dotnet-native-aot`, `dotnet-aot-architecture`, `dotnet-winui`
- [ ] `--projected-skills` incremented in validate-skills.sh
- [ ] All four validation scripts pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
