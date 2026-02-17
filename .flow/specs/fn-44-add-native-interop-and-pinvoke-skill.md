# fn-44 Add Native Interop and P/Invoke Skill

## Overview

Add a new `dotnet-native-interop` skill covering P/Invoke patterns across all major .NET platforms (Windows, macOS, Linux, iOS, Android, WASM). Covers `[LibraryImport]` (preferred, .NET 7+) vs `[DllImport]` (legacy), cross-platform library loading, marshalling, and platform-specific considerations.

## Scope

**In:** SKILL.md for `dotnet-native-interop` under `skills/core-csharp/`, plugin.json registration, advisor routing, cross-references to `dotnet-native-aot`.

**Out:** COM interop (Windows legacy, future epic if needed). CsWin32 stays in `dotnet-winui`. JNI bridge for Android Java interop (different from P/Invoke).

**Scope boundary with `dotnet-native-aot`**: AOT skill keeps its P/Invoke section (lines 181-226) focused on AOT-specific concerns (trimming, direct pinvoke). New skill owns the general P/Invoke guidance and cross-references AOT skill for publish scenarios.

## Key Context

- `[LibraryImport]` is source-generated, AOT-compatible, preferred for new code (.NET 7+)
- `[DllImport]` still works but not AOT-compatible without manual work
- iOS requires static linking (no dynamic library loading)
- WASM has no traditional P/Invoke — uses `[JSImport]`/`[JSExport]` instead
- `NativeLibrary.SetDllImportResolver` for cross-platform library name resolution
- Struct layout (`[StructLayout]`, blittability) critical for correct marshalling
- Function pointer callbacks (`delegate* unmanaged`) vs managed delegates

## Quick commands

```bash
./scripts/validate-skills.sh
```

## Acceptance

- [ ] `skills/core-csharp/dotnet-native-interop/SKILL.md` exists with valid frontmatter
- [ ] Covers LibraryImport vs DllImport decision guidance
- [ ] Covers platform-specific concerns: Windows DLL, macOS/Linux .so/.dylib, iOS static linking, WASM limitations
- [ ] Covers marshalling patterns (structs, strings, callbacks)
- [ ] Covers NativeLibrary.SetDllImportResolver for cross-platform resolution
- [ ] Description under 120 characters
- [ ] Registered in plugin.json
- [ ] `dotnet-advisor` routing updated
- [ ] Cross-references to/from `dotnet-native-aot`, `dotnet-aot-architecture`
- [ ] All validation scripts pass

## References

- https://learn.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke
- https://learn.microsoft.com/en-us/dotnet/standard/native-interop/best-practices
- `skills/native-aot/dotnet-native-aot/SKILL.md:181-226` (AOT P/Invoke section)
- `skills/native-aot/dotnet-aot-architecture/SKILL.md:32` (LibraryImport mention)
- `skills/ui-frameworks/dotnet-winui/SKILL.md:451` (CsWin32 reference)
