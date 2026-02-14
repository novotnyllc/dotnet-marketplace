# fn-17.2 Create distribution, packaging, and release pipeline skills

## Description
Create the three skills covering CLI distribution strategy, multi-platform packaging formats, and unified release CI/CD pipeline. These skills teach how to ship .NET CLI tools to end users across all major platforms.

## Delivers
- `skills/cli-tools/dotnet-cli-distribution/SKILL.md`
- `skills/cli-tools/dotnet-cli-packaging/SKILL.md`
- `skills/cli-tools/dotnet-cli-release-pipeline/SKILL.md`

## Acceptance
- [ ] `dotnet-cli-distribution` covers: when to choose Native AOT vs framework-dependent vs `dotnet tool`, RID matrix strategy (linux-x64, osx-arm64, win-x64, linux-arm64), single-file publish, size optimization for CLI binaries
- [ ] `dotnet-cli-distribution` cross-references `[skill:dotnet-native-aot]` — does not re-teach AOT MSBuild configuration (PublishAot, ILLink, etc.)
- [ ] `dotnet-cli-packaging` covers: Homebrew formula authoring (binary tap, cask), apt/deb packaging (dpkg-deb), winget manifest (YAML schema, PR to winget-pkgs), Scoop manifest, Chocolatey, `dotnet tool` global/local packaging, NuGet distribution
- [ ] `dotnet-cli-release-pipeline` covers: unified GitHub Actions workflow producing all formats from single trigger, build matrix per RID, artifact staging, GitHub Releases with checksums, automated formula/manifest PR creation, versioning strategy (SemVer + git tags)
- [ ] `dotnet-cli-release-pipeline` cross-references fn-19 CI/CD skills with scope boundary statement — does not re-teach general CI patterns
- [ ] All three skills have `name` and `description` frontmatter (< 120 chars each)
- [ ] Out-of-scope boundary statements for fn-16 (general AOT), fn-19 (general CI/CD), fn-5 (containers)
- [ ] Does NOT modify `plugin.json` (handled by fn-17.3)

## Dependencies
- fn-17.1 (architecture patterns context for distribution; soft dependency for cross-ref consistency)
- fn-16.1 (`[skill:dotnet-native-aot]` must exist for hard cross-refs)

## Done summary
Created three CLI tool skills: dotnet-cli-distribution (AOT vs framework-dependent vs dotnet tool, RID matrix, single-file publish, size optimization), dotnet-cli-packaging (Homebrew formula/tap, apt/deb, winget, Scoop, Chocolatey, dotnet tool, NuGet), and dotnet-cli-release-pipeline (unified GitHub Actions workflow, build matrix, artifact staging, GitHub Releases with checksums, automated formula/manifest PR creation, SemVer versioning).
## Evidence
- Commits: 1e6504459a23bfe2d5e0b80f2a54ee43e5b24b9b, c2b6d896fe1c39aa832636889fe05be49dc1f874
- Tests: ./scripts/validate-skills.sh
- PRs: