# fn-44-add-native-interop-and-pinvoke-skill.1 Author dotnet-native-interop SKILL.md

## Description
Author `skills/core-csharp/dotnet-native-interop/SKILL.md` covering P/Invoke and native interop across Windows, macOS, Linux, iOS, Android, and WASM.

**Size:** M
**Files:** `skills/core-csharp/dotnet-native-interop/SKILL.md`

## Approach

- Follow existing skill pattern at `skills/native-aot/dotnet-native-aot/SKILL.md` for style
- Cover `[LibraryImport]` (.NET 7+, preferred) vs `[DllImport]` (legacy)
- Platform sections: Windows DLL, macOS/Linux .so/.dylib, iOS static linking, WASM `[JSImport]` note
- Cover marshalling: structs, strings, function pointers, `NativeLibrary.SetDllImportResolver`
- Reference: https://learn.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke

## Key context

- iOS does not allow dynamic library loading — must use static linking
- WASM has no traditional P/Invoke — uses `[JSImport]`/`[JSExport]` instead (mention, cross-ref)
- `dotnet-native-aot` lines 181-226 keep AOT-specific P/Invoke; this skill owns general guidance
- `CsWin32` stays in `dotnet-winui` — just add a cross-reference
## Acceptance
- [ ] SKILL.md exists at `skills/core-csharp/dotnet-native-interop/`
- [ ] Valid frontmatter with `name` and `description` (under 120 chars)
- [ ] Covers LibraryImport vs DllImport with decision guidance
- [ ] Platform-specific sections for Windows, macOS/Linux, iOS, Android, WASM
- [ ] Covers marshalling patterns (structs, strings, callbacks)
- [ ] Covers NativeLibrary.SetDllImportResolver
- [ ] Cross-reference syntax used for related skills
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
