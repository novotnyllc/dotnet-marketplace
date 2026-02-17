# fn-44 Add Native Interop and P/Invoke Skill

## Overview

Add a new `dotnet-native-interop` skill covering P/Invoke patterns across all major .NET platforms (Windows, macOS, Linux, iOS, Android, WASM). Covers `[LibraryImport]` (preferred, .NET 7+) vs `[DllImport]` (legacy), cross-platform library loading, marshalling, and platform-specific considerations.

**Visibility:** Implicit — auto-loaded by agents via advisor routing when P/Invoke or native interop patterns are detected. Not user-invocable.

## Scope

**In:** SKILL.md for `dotnet-native-interop` under `skills/core-csharp/`, plugin.json registration, advisor routing, cross-references to `dotnet-native-aot`.

**Out:** COM interop (Windows legacy). CsWin32 stays in `dotnet-winui`. JNI bridge for Android Java interop (different from P/Invoke). JSImport/JSExport for WASM (JavaScript interop, not native interop — covered by `dotnet-aot-wasm`).

**Scope boundary with `dotnet-native-aot`**: AOT skill keeps its P/Invoke section focused on AOT-specific concerns (trimming, direct pinvoke). New skill owns the general P/Invoke guidance and cross-references AOT skill for publish scenarios.

## Key Context

- `[LibraryImport]` is source-generated, AOT-compatible, preferred for new code (.NET 7+)
- `[DllImport]` still works but not AOT-compatible without manual work
- iOS requires static linking (no dynamic library loading)
- WASM: no traditional P/Invoke. Mention limitation only, cross-ref `[skill:dotnet-aot-wasm]` for JS interop
- `NativeLibrary.SetDllImportResolver` for cross-platform library name resolution
- Struct layout (`[StructLayout]`, blittability) critical for correct marshalling
- Function pointer callbacks (`delegate* unmanaged`) vs managed delegates
- Budget: target description ~90 chars. Total projected: 132 skills after batch.

## Quick commands

```bash
./scripts/validate-skills.sh
```

## Acceptance

- [ ] `skills/core-csharp/dotnet-native-interop/SKILL.md` exists with valid frontmatter
- [ ] Covers LibraryImport vs DllImport decision guidance
- [ ] Covers platform-specific concerns: Windows DLL, macOS/Linux .so/.dylib, iOS static linking, WASM limitation note
- [ ] Covers marshalling patterns (structs, strings, callbacks)
- [ ] Covers NativeLibrary.SetDllImportResolver for cross-platform resolution
- [ ] WASM section limited to "not supported, see [skill:dotnet-aot-wasm]"
- [ ] Description under 120 characters
- [ ] Registered in plugin.json
- [ ] `dotnet-advisor` routing updated
- [ ] Cross-references to/from `dotnet-native-aot`, `dotnet-aot-architecture`
- [ ] Integration task notes file contention with plugin.json/advisor shared files
- [ ] All validation scripts pass

## References

- https://learn.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke
- https://learn.microsoft.com/en-us/dotnet/standard/native-interop/best-practices
- `skills/native-aot/dotnet-native-aot/SKILL.md` (AOT P/Invoke section)
- `skills/native-aot/dotnet-aot-architecture/SKILL.md` (LibraryImport mention)
- `skills/ui-frameworks/dotnet-winui/SKILL.md` (CsWin32 reference)
