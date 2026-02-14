# fn-20-packaging-and-publishing-skills.1 Create NuGet authoring and MSIX skills

## Description
Create two packaging skills: `dotnet-nuget-authoring` (NuGet package authoring for library authors) and `dotnet-msix` (MSIX packaging pipeline). Both go in `skills/packaging/`. Each skill needs `name` and `description` frontmatter, comprehensive content with code examples, out-of-scope boundary statements, and cross-references to related skills. This task is parallelizable with fn-20.2 (file-disjoint).

**`dotnet-nuget-authoring`** covers:
- SDK-style `.csproj` package properties (`PackageId`, `PackageTags`, `PackageReadmeFile`, `PackageLicenseExpression`, `PackageProjectUrl`, etc.)
- Source generator packaging (multi-target analyzers/generators, `analyzers/dotnet/cs/` folder layout, `buildTransitive/` for props/targets, `IncludeBuildOutput=false`)
- Multi-TFM NuGet packages (when and how to multi-target for NuGet)
- Symbol packages (snupkg) and deterministic builds
- Package signing (author signing with certificates, repository signing overview)
- Package validation (`dotnet pack --validate`, `Microsoft.DotNet.ApiCompat.Task` for API compatibility)
- NuGet versioning strategies (SemVer 2.0, pre-release suffixes, NBGV integration cross-ref)
- Does NOT re-teach CPM, SourceLink, nuget.config (cross-ref `[skill:dotnet-project-structure]`)
- Does NOT re-teach CI publish workflows (cross-ref `[skill:dotnet-gha-publish]`/`[skill:dotnet-ado-publish]`)
- Does NOT re-teach CLI tool packaging (cross-ref `[skill:dotnet-cli-packaging]`)

**`dotnet-msix`** covers:
- MSIX package creation (from csproj with `<WindowsPackageType>`, WAP project for desktop bridging)
- Signing with certificates (self-signed for dev, trusted CA for production, Microsoft Store signing)
- Distribution channels (Microsoft Store submission, App Installer sideloading, enterprise deployment)
- Auto-update configuration (App Installer XML, version checking, differential updates)
- MSIX bundle format for multi-architecture (`.msixbundle`)
- CI/CD MSIX build steps (MSBuild targets for packaging in CI)
- Windows SDK version requirements (build 19041+ for base, 1709+ for auto-update)
- Does NOT re-teach WinUI packaged vs unpackaged comparison (cross-ref `[skill:dotnet-winui]`)
- Does NOT re-teach AOT configuration (cross-ref `[skill:dotnet-native-aot]`)
- Does NOT re-teach general CI patterns (cross-ref CI skills)

**Files created:**
- `skills/packaging/dotnet-nuget-authoring/SKILL.md`
- `skills/packaging/dotnet-msix/SKILL.md`

**Files NOT modified:** `plugin.json`, `dotnet-advisor/SKILL.md` (handled by fn-20.3)

## Acceptance
- [ ] `skills/packaging/dotnet-nuget-authoring/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-nuget-authoring` covers SDK csproj properties, source generator packaging, multi-TFM, symbol packages, signing, validation, API compat
- [ ] `dotnet-nuget-authoring` cross-refs `[skill:dotnet-project-structure]` for CPM/SourceLink without re-teaching
- [ ] `dotnet-nuget-authoring` cross-refs `[skill:dotnet-gha-publish]`/`[skill:dotnet-ado-publish]` for CI without re-teaching
- [ ] `dotnet-nuget-authoring` cross-refs `[skill:dotnet-cli-packaging]` with scope boundary
- [ ] `dotnet-nuget-authoring` contains out-of-scope boundary statement
- [ ] `skills/packaging/dotnet-msix/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-msix` covers MSIX creation, signing, distribution channels, auto-update, bundles, CI steps
- [ ] `dotnet-msix` documents Windows SDK version requirements
- [ ] `dotnet-msix` cross-refs `[skill:dotnet-winui]` without re-teaching packaging modes
- [ ] `dotnet-msix` cross-refs `[skill:dotnet-native-aot]` for AOT+MSIX
- [ ] `dotnet-msix` contains out-of-scope boundary statement
- [ ] Description frontmatter < 120 chars per skill

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
