# fn-20: Packaging and Publishing Skills

## Overview
Delivers comprehensive NuGet package authoring, MSIX packaging, and release management skills covering modern package creation, signing, distribution, versioning strategy, and release lifecycle. These are **depth skills** focused on the packaging/publishing *concepts* — when to use, configuration, signing, and distribution. CI pipeline execution for these packaging steps is owned by fn-19 (`[skill:dotnet-gha-publish]`, `[skill:dotnet-ado-publish]`); fn-20 owns the packaging knowledge itself. Project-level configuration (CPM, SourceLink, nuget.config) is owned by fn-4 (`[skill:dotnet-project-structure]`); fn-20 owns NuGet package authoring for library consumers.

**Skills (4 total):**
- `dotnet-nuget-authoring` — NuGet package authoring: SDK-style csproj properties, source generator packaging, multi-TFM packages, symbol packages, package signing, validation, API compatibility
- `dotnet-msix` — MSIX packaging pipeline: creation, signing with certificates, distribution channels (Microsoft Store, App Installer, sideloading), auto-update, CI build integration
- `dotnet-github-releases` — GitHub Releases for .NET: release creation, asset attachment, release notes generation (auto-generated, changelog-based, conventional commits), pre-release management
- `dotnet-release-management` — Release lifecycle: NBGV, SemVer strategy, changelog generation, pre-release workflows, version bumping, release branching

**Agents:** None for this epic. Packaging guidance is delivered through skills only. The `dotnet-architect` agent can load packaging skills contextually via `[skill:dotnet-nuget-authoring]` or `[skill:dotnet-msix]` references.

**Naming convention:** All skills use `dotnet-` prefix. Noun style for reference skills. Directory: `skills/packaging/` for NuGet/MSIX/GitHub-Releases; `skills/release-management/` for release-management.

## Dependencies

**Hard epic dependencies:**
- fn-19 (CI/CD): `[skill:dotnet-gha-publish]` and `[skill:dotnet-ado-publish]` must exist for CI publish workflow cross-refs in NuGet and MSIX skills

**Soft epic dependencies:**
- fn-4 (Project Structure): `[skill:dotnet-project-structure]` owns CPM, SourceLink, nuget.config — fn-20 cross-refs without re-teaching
- fn-16 (Native AOT): `[skill:dotnet-native-aot]` for AOT+MSIX scenarios — soft cross-ref
- fn-17 (CLI Tools): `[skill:dotnet-cli-release-pipeline]` and `[skill:dotnet-cli-packaging]` for scope boundary cross-refs — already shipped
- fn-13 (UI Frameworks): `[skill:dotnet-winui]` for WinUI MSIX packaging modes — already shipped

## .NET Version Policy

**Baseline:** .NET 8.0+ (LTS)

| Component | Version | Notes |
|-----------|---------|-------|
| NuGet SDK-style packaging | .NET 8+ | `dotnet pack`, `PackageReference`, `PackageId` |
| Source generator packaging | .NET 8+ | `IIncrementalGenerator`, `buildTransitive` folder layout |
| Package validation | .NET 8+ | `Microsoft.DotNet.ApiCompat.Task` for API compat |
| MSIX packaging | Windows 10 build 19041+ | Minimum for Windows App SDK 1.6+ |
| MSIX auto-update | Windows 10 build 1709+ | App Installer protocol |
| Microsoft Store submission | Windows App SDK 1.6+ | Store submission API |
| MSIX bundle format | Windows 10 build 1709+ | `.msixbundle` for multi-arch |
| NBGV | .NET 8+ | `Nerdbank.GitVersioning` for version calculation |
| GitHub Releases API | N/A | Platform-independent |

## Conventions

- **Frontmatter:** Required fields are `name` and `description` only
- **Cross-reference syntax:** `[skill:skill-name]` for all skill references
- **Description budget:** Target < 120 characters per skill description
- **Out-of-scope format:** "**Out of scope:**" paragraph with epic ownership attribution
- **Code examples:** XML for MSBuild/csproj, YAML for CI snippets (cross-ref only), PowerShell/bash for CLI commands

## Scope Boundaries

| Concern | fn-20 owns | Other epic owns | Enforcement |
|---------|-----------|-----------------|-------------|
| NuGet package authoring | SDK csproj properties, package metadata, source generator packaging, multi-TFM, signing, validation, API compat | fn-4: `dotnet-project-structure` (CPM, SourceLink, nuget.config, NuGet Audit, lock files) | Cross-ref `[skill:dotnet-project-structure]`; no re-teach CPM/SourceLink |
| NuGet CI publish workflows | Scope boundary only — cross-ref to CI skills | fn-19: `dotnet-gha-publish`, `dotnet-ado-publish` (NuGet push, container push CI YAML) | Cross-ref `[skill:dotnet-gha-publish]`/`[skill:dotnet-ado-publish]`; no re-teach CI workflows |
| CLI tool packaging | NuGet package authoring for libraries (not CLI tools) | fn-17: `dotnet-cli-packaging` (Homebrew, apt, winget, Scoop, `dotnet tool`) | Cross-ref `[skill:dotnet-cli-packaging]`; no re-teach CLI distribution |
| MSIX packaging | MSIX creation, signing, distribution, Store, auto-update | fn-13: `dotnet-winui` (WinUI MSIX vs unpackaged modes, Package.appxmanifest basics) | Cross-ref `[skill:dotnet-winui]`; no re-teach WinUI packaging mode comparison |
| MSIX in CI | MSIX build/sign steps for CI pipelines | fn-19: `dotnet-gha-patterns`, `dotnet-ado-patterns` (general CI patterns) | Cross-ref CI skills for pipeline structure; fn-20 owns MSIX-specific CI steps |
| GitHub Releases | Release creation, assets, notes, pre-release for .NET projects | fn-17: `dotnet-cli-release-pipeline` (CLI-specific release automation with checksums) | Cross-ref `[skill:dotnet-cli-release-pipeline]`; no re-teach CLI release pipeline |
| Release management | NBGV, SemVer, changelogs, release lifecycle | fn-4: `plugin-self-publish` (plugin-specific release workflow) | Cross-ref `[skill:plugin-self-publish]`; no re-teach plugin release |
| AOT + MSIX | MSIX packaging with AOT-published binaries (CI config only) | fn-16: `dotnet-native-aot` (AOT MSBuild properties) | Cross-ref `[skill:dotnet-native-aot]`; no re-teach AOT config |

## Cross-Reference Classification

| Target Skill | Type | Used By | Notes |
|---|---|---|---|
| `[skill:dotnet-project-structure]` | Hard | `dotnet-nuget-authoring` | CPM, SourceLink — do not re-teach |
| `[skill:dotnet-gha-publish]` | Hard | `dotnet-nuget-authoring`, `dotnet-github-releases` | CI publish workflows |
| `[skill:dotnet-ado-publish]` | Hard | `dotnet-nuget-authoring` | ADO publish workflows |
| `[skill:dotnet-winui]` | Hard | `dotnet-msix` | WinUI MSIX packaging modes |
| `[skill:dotnet-native-aot]` | Soft | `dotnet-msix` | AOT + MSIX scenarios |
| `[skill:dotnet-cli-release-pipeline]` | Hard | `dotnet-github-releases` | Scope boundary |
| `[skill:dotnet-cli-packaging]` | Hard | `dotnet-nuget-authoring` | Scope boundary |
| `[skill:dotnet-add-ci]` | Soft | All | Starter template context |
| `[skill:plugin-self-publish]` | Hard | `dotnet-release-management` | Scope boundary |

## Task Decomposition

### fn-20.1: Create NuGet authoring and MSIX skills — parallelizable with fn-20.2
**Delivers:** `dotnet-nuget-authoring`, `dotnet-msix`
- `skills/packaging/dotnet-nuget-authoring/SKILL.md`
- `skills/packaging/dotnet-msix/SKILL.md`
- Both require `name` and `description` frontmatter
- Cross-references:
  - `[skill:dotnet-project-structure]` (fn-4) for CPM, SourceLink — do not re-teach
  - `[skill:dotnet-gha-publish]` / `[skill:dotnet-ado-publish]` (fn-19) for CI publish workflows — do not re-teach
  - `[skill:dotnet-cli-packaging]` (fn-17) scope boundary
  - `[skill:dotnet-winui]` (fn-13) for WinUI MSIX packaging modes — do not re-teach
  - `[skill:dotnet-native-aot]` (fn-16) for AOT+MSIX scenarios
- Each skill must contain out-of-scope boundary statements
- Does NOT modify `plugin.json` or `dotnet-advisor/SKILL.md` (handled by fn-20.3)

### fn-20.2: Create GitHub Releases and Release Management skills — parallelizable with fn-20.1
**Delivers:** `dotnet-github-releases`, `dotnet-release-management`
- `skills/packaging/dotnet-github-releases/SKILL.md`
- `skills/release-management/dotnet-release-management/SKILL.md`
- Both require `name` and `description` frontmatter
- Cross-references:
  - `[skill:dotnet-cli-release-pipeline]` (fn-17) scope boundary
  - `[skill:dotnet-gha-publish]` / `[skill:dotnet-gha-patterns]` (fn-19) for CI workflow cross-refs
  - `[skill:plugin-self-publish]` (fn-2) scope boundary for release management
- Each skill must contain out-of-scope boundary statements
- Does NOT modify `plugin.json` or `dotnet-advisor/SKILL.md` (handled by fn-20.3)

### fn-20.3: Integration — plugin registration, advisor catalog, validation, cross-reference reconciliation (depends on fn-20.1, fn-20.2)
**Delivers:** Plugin registration, advisor update, cross-reference reconciliation, validation
- Registers all 4 skill paths in `.claude-plugin/plugin.json` under `skills` array:
  - `skills/packaging/dotnet-nuget-authoring`
  - `skills/packaging/dotnet-msix`
  - `skills/packaging/dotnet-github-releases`
  - `skills/release-management/dotnet-release-management`
- Updates `skills/foundation/dotnet-advisor/SKILL.md`:
  - Section 15 ("Packaging & Publishing") from `planned` to `implemented`
  - Section 16 ("Release Management") from `planned` to `implemented`
  - Updates `[skill:dotnet-nuget-modern]` reference to `[skill:dotnet-nuget-authoring]` (name change)
  - Verifies all skill names match their SKILL.md `name` frontmatter values exactly
- Resolves any `<!-- TODO(fn-20) -->` placeholders in existing skills (run `grep -r 'TODO(fn-20)' skills/` — expect empty, but verify)
- Runs repo-wide skill name uniqueness check
- Runs `./scripts/validate-skills.sh`
- Validates cross-references present in all 4 skills
- Single owner of `plugin.json` — eliminates merge conflicts

**Execution order:** fn-20.1 and fn-20.2 are parallelizable (file-disjoint, no shared file edits). fn-20.3 depends on both fn-20.1 and fn-20.2.

## Key Context
- Central Package Management is the modern standard for multi-project NuGet version management — owned by `dotnet-project-structure`
- fn-20's `dotnet-nuget-authoring` focuses on creating packages (for library authors), not consuming them
- MSIX is the modern Windows app packaging format (replaces ClickOnce, MSI for many scenarios)
- `dotnet-winui` already covers MSIX packaged vs unpackaged deployment modes — fn-20's `dotnet-msix` goes deeper into signing, distribution, Store submission, and auto-update
- GitHub Releases + NBGV provide a complete release lifecycle for .NET projects
- `dotnet-cli-release-pipeline` (fn-17) covers CLI-specific release automation — fn-20's `dotnet-github-releases` covers general .NET project releases
- The advisor catalog lists these skills under sections 15 (Packaging & Publishing) and 16 (Release Management) — both go to `implemented` after fn-20
- fn-27 (Roslyn Analyzer Authoring) has a scope boundary note: "Analyzer-specific NuGet layout — cross-ref to fn-20 when it lands"

## Quick Commands
```bash
# Validate all 4 skills exist with frontmatter
for s in dotnet-nuget-authoring dotnet-msix dotnet-github-releases; do
  test -f "skills/packaging/$s/SKILL.md" && \
  grep -q "^name:" "skills/packaging/$s/SKILL.md" && \
  grep -q "^description:" "skills/packaging/$s/SKILL.md" && \
  echo "OK: $s" || echo "MISSING: $s"
done
test -f "skills/release-management/dotnet-release-management/SKILL.md" && \
grep -q "^name:" "skills/release-management/dotnet-release-management/SKILL.md" && \
grep -q "^description:" "skills/release-management/dotnet-release-management/SKILL.md" && \
echo "OK: dotnet-release-management" || echo "MISSING: dotnet-release-management"

# Repo-wide skill name uniqueness
grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d  # expect empty

# Verify scope boundary statements in all 4 skills
grep -l "Out of scope\|out of scope\|Scope boundary" skills/packaging/*/SKILL.md skills/release-management/*/SKILL.md | wc -l  # expect 4

# Verify cross-references
grep -r "\[skill:dotnet-project-structure\]" skills/packaging/
grep -r "\[skill:dotnet-gha-publish\]" skills/packaging/
grep -r "\[skill:dotnet-winui\]" skills/packaging/
grep -r "\[skill:dotnet-cli-release-pipeline\]" skills/packaging/ skills/release-management/
grep -r "\[skill:dotnet-cli-packaging\]" skills/packaging/
grep -r "\[skill:plugin-self-publish\]" skills/release-management/

# Verify no TODO(fn-20) placeholders remain
grep -r "TODO(fn-20)" skills/  # expect empty after fn-20.3

# Verify plugin.json registration (after fn-20.3)
for s in dotnet-nuget-authoring dotnet-msix dotnet-github-releases; do
  grep -q "skills/packaging/$s" .claude-plugin/plugin.json && echo "OK: $s" || echo "MISSING: $s"
done
grep -q "skills/release-management/dotnet-release-management" .claude-plugin/plugin.json && \
echo "OK: dotnet-release-management" || echo "MISSING: dotnet-release-management"

# Verify advisor sections updated (after fn-20.3)
grep "### 15. Packaging" skills/foundation/dotnet-advisor/SKILL.md | grep -v "planned"
grep "### 16. Release" skills/foundation/dotnet-advisor/SKILL.md | grep -v "planned"

# Canonical validation
./scripts/validate-skills.sh
```

## Acceptance Criteria
1. All 4 skills exist at their respective paths with `name` and `description` frontmatter
2. `dotnet-nuget-authoring` covers SDK-style csproj package properties (`PackageId`, `PackageTags`, `PackageReadmeFile`, `PackageLicenseExpression`), source generator packaging (multi-target analyzers, `buildTransitive` folder), multi-TFM packages, symbol packages (snupkg), package signing (author signing, certificate management), package validation (`dotnet pack --validate`, `Microsoft.DotNet.ApiCompat.Task`), and NuGet versioning strategies
3. `dotnet-nuget-authoring` cross-references `[skill:dotnet-project-structure]` for CPM and SourceLink — does NOT re-teach these topics
4. `dotnet-nuget-authoring` cross-references `[skill:dotnet-gha-publish]`/`[skill:dotnet-ado-publish]` for CI publish workflows — does NOT re-teach pipeline YAML
5. `dotnet-nuget-authoring` cross-references `[skill:dotnet-cli-packaging]` with scope boundary statement
6. `dotnet-msix` covers MSIX creation (from csproj, WAP project), signing with certificates (self-signed, trusted CA, Store), distribution channels (Microsoft Store submission, App Installer, sideloading), auto-update configuration, MSIX bundle for multi-arch, and CI/CD MSIX build steps
7. `dotnet-msix` cross-references `[skill:dotnet-winui]` for WinUI MSIX packaging modes — does NOT re-teach packaged vs unpackaged comparison
8. `dotnet-msix` cross-references `[skill:dotnet-native-aot]` for AOT+MSIX scenarios
9. `dotnet-msix` documents Windows SDK version requirements (build 19041+ for base MSIX, build 1709+ for auto-update)
10. `dotnet-github-releases` covers release creation via `gh release create` and `softprops/action-gh-release`, asset attachment (NuGet packages, binaries, SBOMs), release notes generation strategies (auto-generated, changelog-based, conventional commits), and pre-release management
11. `dotnet-github-releases` cross-references `[skill:dotnet-cli-release-pipeline]` with scope boundary — does NOT re-teach CLI-specific release automation
12. `dotnet-release-management` covers NBGV (`Nerdbank.GitVersioning`) setup and usage, SemVer strategy for .NET libraries and apps, changelog generation (Keep a Changelog format, auto-generation tools), pre-release version workflows, and release branching patterns
13. `dotnet-release-management` cross-references `[skill:plugin-self-publish]` with scope boundary
14. Each skill contains explicit out-of-scope boundary statements for related epics
15. All 4 skills registered in `.claude-plugin/plugin.json` (fn-20.3)
16. `skills/foundation/dotnet-advisor/SKILL.md` section 15 updated from `planned` to `implemented` (fn-20.3)
17. `skills/foundation/dotnet-advisor/SKILL.md` section 16 updated from `planned` to `implemented` (fn-20.3)
18. Advisor `[skill:dotnet-nuget-modern]` reference updated to `[skill:dotnet-nuget-authoring]` (fn-20.3)
19. All `<!-- TODO(fn-20) -->` placeholders in existing skills verified resolved (fn-20.3)
20. `./scripts/validate-skills.sh` passes for all 4 skills
21. Skill `name` frontmatter values are unique repo-wide (no duplicates)
22. fn-20.1 and fn-20.2 are fully parallelizable (file-disjoint, no shared file edits)
23. fn-20.3 depends on fn-20.1 + fn-20.2 and is the single owner of `plugin.json`
24. All advisor skill names match their SKILL.md `name` frontmatter values exactly

## Test Notes
- Verify `dotnet-nuget-authoring` includes SDK-style csproj XML examples for package metadata
- Verify `dotnet-nuget-authoring` includes source generator NuGet package layout example (`analyzers/dotnet/cs/`, `buildTransitive/`)
- Verify `dotnet-msix` includes signing certificate examples (self-signed for dev, trusted CA for production)
- Verify `dotnet-msix` includes Microsoft Store submission guidance
- Verify `dotnet-msix` includes App Installer XML example for auto-update
- Verify `dotnet-github-releases` includes `gh release create` CLI examples
- Verify `dotnet-github-releases` includes `softprops/action-gh-release` YAML example (cross-ref only if already in fn-19 skills)
- Verify `dotnet-release-management` includes NBGV `version.json` example
- Verify `dotnet-release-management` includes CHANGELOG.md format example
- Verify scope boundary statements clearly differentiate fn-20 from fn-4 (project structure), fn-13 (WinUI), fn-17 (CLI), fn-19 (CI/CD)
- Run `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` to confirm no duplicate names repo-wide

## References
- NuGet package creation: https://learn.microsoft.com/en-us/nuget/create-packages/overview
- NuGet package signing: https://learn.microsoft.com/en-us/nuget/create-packages/sign-a-package
- Source generator packaging: https://learn.microsoft.com/en-us/dotnet/standard/analyzers/using-source-generators
- API compatibility analysis: https://learn.microsoft.com/en-us/dotnet/fundamentals/apicompat/overview
- MSIX overview: https://learn.microsoft.com/en-us/windows/msix/overview
- MSIX signing: https://learn.microsoft.com/en-us/windows/msix/package/signing-package-overview
- Microsoft Store submission: https://learn.microsoft.com/en-us/windows/apps/publish/
- App Installer: https://learn.microsoft.com/en-us/windows/msix/app-installer/app-installer-root
- GitHub Releases: https://docs.github.com/en/repositories/releasing-projects-on-github
- NBGV: https://github.com/dotnet/Nerdbank.GitVersioning
- Keep a Changelog: https://keepachangelog.com/
- SourceLink: https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/sourcelink
