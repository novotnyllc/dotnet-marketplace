# fn-16-native-aot-and-trimming-skills.2 Document .NET 10 ASP.NET Core AOT improvements

## Description
Add a dedicated .NET 10 ASP.NET Core AOT improvements section to the `dotnet-native-aot` skill. Documents the improved request delegate generator, expanded Minimal API AOT support, reduced linker warnings for common ASP.NET Core patterns, and any Blazor Server AOT compatibility improvements. This task edits `skills/native-aot/dotnet-native-aot/SKILL.md` only.

## Acceptance
- [ ] `dotnet-native-aot` contains a .NET 10 ASP.NET Core AOT section
- [ ] Documents improved request delegate generator for Minimal APIs
- [ ] Documents expanded AOT support for common ASP.NET Core patterns
- [ ] Documents reduced linker warning surface for ASP.NET Core
- [ ] Section clearly marked with version context (.NET 10+)
- [ ] Does NOT modify `plugin.json` (handled by fn-16.3)
- [ ] Only modifies `skills/native-aot/dotnet-native-aot/SKILL.md`

## Done summary
Expanded the .NET 10 ASP.NET Core AOT Improvements section in `dotnet-native-aot` SKILL.md with detailed, research-verified content:

- **Request Delegate Generator improvements**: Documented enhanced parameter binding scenarios, additional TypedResults support, and reduced need for manual workarounds vs .NET 8/9
- **Reduced linker warning surface**: Documented IL2xxx/IL3xxx warning reduction when upgrading from .NET 9 to .NET 10
- **OpenAPI in webapiaot template**: Documented new default OpenAPI document generation via Microsoft.AspNetCore.OpenApi
- **Runtime NativeAOT code generation**: Documented struct argument improvements, loop inversion, and method devirtualization
- **Blazor Server and SignalR status**: Accurately documented both remain NOT supported with Native AOT in .NET 10 (verified against official Microsoft Learn docs)
- **Compatibility snapshot table**: Added .NET 10 AOT feature support matrix sourced from official ASP.NET Core docs

Only `skills/native-aot/dotnet-native-aot/SKILL.md` was modified. No plugin.json changes. Validation passes with 0 errors.
## Evidence
- Commits:
- Tests: ./scripts/validate-skills.sh passes with 0 errors
- PRs: