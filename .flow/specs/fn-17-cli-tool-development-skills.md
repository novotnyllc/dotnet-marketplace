# fn-17: CLI Tool Development Skills

## Overview
Delivers comprehensive CLI tool development skills covering System.CommandLine API, CLI application architecture patterns (clig.dev), distribution strategy (Native AOT, dotnet tool, single-file), multi-platform packaging (Homebrew, apt/deb, winget, Scoop, Chocolatey), and unified release pipelines. These are **CLI-focused** skills that teach how to build, distribute, and maintain .NET CLI tools. General AOT compilation lives in fn-16; general CI/CD patterns in fn-19; project scaffolding in fn-4.

## Scope
**Skills (5 total):**
- `dotnet-system-commandline` — System.CommandLine 2.0 API: RootCommand, Command, Option<T>, Argument<T>, middleware pipeline, hosting integration (`UseCommandHandler`), tab completion, `--version`/`--help` auto-generation, dependency injection, `IConsole` abstraction
- `dotnet-cli-architecture` — Layered CLI design patterns (clig.dev): command → handler → service architecture, configuration precedence (appsettings + env vars + CLI args), structured logging in CLI context, exit code conventions, stdin/stdout/stderr patterns, testing CLI apps (in-process invocation, output assertion)
- `dotnet-cli-distribution` — CLI distribution strategy: Native AOT single-file publish for CLI tools, RID matrix (linux-x64, osx-arm64, win-x64, linux-arm64), self-contained vs framework-dependent trade-offs, `dotnet tool` packaging as alternative, size optimization for CLI binaries
- `dotnet-cli-packaging` — Multi-platform packaging: Homebrew formula (binary tap, cask), apt/deb (dpkg-deb), winget manifest (YAML schema, PR to winget-pkgs), Scoop manifest, Chocolatey, `dotnet tool` global/local, NuGet distribution
- `dotnet-cli-release-pipeline` — Unified release CI/CD: GitHub Actions workflow producing all formats from single trigger, build matrix per RID, artifact staging, GitHub Releases with checksums, automated formula/manifest PR creation, versioning (SemVer + git tags)

**Naming convention:** All skills use `dotnet-` prefix. `dotnet-system-commandline` uses library name (only library in this space). Others use descriptive noun style.

## Dependencies

**Hard epic dependencies:**
- fn-16 (Native AOT): `[skill:dotnet-native-aot]` and `[skill:dotnet-aot-architecture]` must exist for cross-refs in distribution skill

**Soft epic dependencies:**
- fn-5 (Architecture): `[skill:dotnet-containers]` for container distribution context — already shipped
- fn-4 (Project Structure): `[skill:dotnet-scaffold-project]` for project scaffolding cross-refs — already shipped
- fn-19 (CI/CD): Scope boundary — fn-17 owns CLI-specific release pipeline; fn-19 owns general CI/CD patterns
- fn-7 (Testing): `[skill:dotnet-testing-strategy]` for CLI testing cross-refs — deferred placeholder if not shipped

## .NET Version Policy

**Baseline:** .NET 8.0+

| Component | Version | Notes |
|-----------|---------|-------|
| System.CommandLine | 2.0.0-beta4 | Pre-release NuGet package; API surface stable (used by `dotnet` CLI itself) |
| Native AOT for CLI | .NET 8+ | Console app AOT since .NET 7; full support .NET 8+ |
| dotnet tool packaging | .NET 8+ | Global/local tools |
| Single-file publish | .NET 8+ | Mature; recommended for CLI distribution |

**Note:** System.CommandLine 2.0's beta status must be documented with production readiness assessment. The API is stable and battle-tested (powers the `dotnet` CLI), but the NuGet package version remains pre-release.

## Conventions

- **Frontmatter:** Required fields are `name` and `description` only
- **Cross-reference syntax:** `[skill:skill-name]` for all skill references
- **Description budget:** Target < 120 characters per skill description
- **Out-of-scope format:** "**Out of scope:**" paragraph with epic ownership attribution
- **Code examples:** Use `.NET 8.0+` TFM unless demonstrating version-specific features

## Scope Boundaries

| Concern | fn-17 owns | Other epic owns | Enforcement |
|---------|-----------|-----------------|-------------|
| Native AOT compilation | CLI-specific AOT publish (RID matrix, single-file, when to choose AOT) | fn-16: general AOT pipeline, trimming, ILLink, MSBuild properties | Cross-ref to `[skill:dotnet-native-aot]`; no re-teaching AOT MSBuild |
| CI/CD | CLI-specific release pipeline (build→package→release) | fn-19: general CI/CD patterns, matrix builds, deploy pipelines | Scope boundary statement; fn-17 focuses on CLI artifact pipeline |
| Project scaffolding | CLI project structure patterns | fn-4: general scaffolding | Cross-ref to `[skill:dotnet-scaffold-project]` |
| Container distribution | CLI in container context only (brief mention) | fn-5: general container patterns (`[skill:dotnet-containers]`) | Cross-ref; no re-teaching container patterns |
| Testing CLI apps | CLI-specific testing (process invocation, output assertion, System.CommandLine.Testing) | fn-7: general testing strategies | Cross-ref to fn-7 skills; deferred placeholder if not shipped |
| DI in CLI context | CLI hosting + DI integration | fn-3: general DI patterns (`[skill:dotnet-csharp-dependency-injection]`) | Cross-ref; no re-teaching DI |

## Cross-Reference Classification

| Target Skill | Type | Notes |
|---|---|---|
| `[skill:dotnet-native-aot]` | Hard | AOT publish for CLI distribution |
| `[skill:dotnet-aot-architecture]` | Hard | AOT-safe patterns for CLI tools |
| `[skill:dotnet-containers]` | Soft | Container-based CLI distribution |
| `[skill:dotnet-scaffold-project]` | Soft | CLI project scaffolding |
| `[skill:dotnet-csharp-dependency-injection]` | Soft | DI in CLI hosting context |
| `[skill:dotnet-testing-strategy]` | Soft | CLI testing cross-ref (deferred) |

## Task Decomposition

### fn-17.1: Create System.CommandLine and CLI architecture skills (no dependencies)
**Delivers:** `dotnet-system-commandline`, `dotnet-cli-architecture`
- `skills/cli-tools/dotnet-system-commandline/SKILL.md`
- `skills/cli-tools/dotnet-cli-architecture/SKILL.md`
- Both require `name` and `description` frontmatter
- `dotnet-system-commandline` covers: RootCommand, Command, Option<T>, Argument<T>, middleware, hosting integration, tab completion, auto-generated help/version, DI, IConsole, beta status assessment
- `dotnet-cli-architecture` covers: clig.dev principles, layered architecture, configuration precedence, logging, exit codes, stdin/stdout/stderr, testing CLI apps
- Each skill must contain out-of-scope boundary statements
- Does NOT modify `plugin.json` (handled by fn-17.3)

### fn-17.2: Create distribution, packaging, and release pipeline skills (depends on fn-17.1, fn-16.1)
**Delivers:** `dotnet-cli-distribution`, `dotnet-cli-packaging`, `dotnet-cli-release-pipeline`
- `skills/cli-tools/dotnet-cli-distribution/SKILL.md`
- `skills/cli-tools/dotnet-cli-packaging/SKILL.md`
- `skills/cli-tools/dotnet-cli-release-pipeline/SKILL.md`
- `dotnet-cli-distribution` covers: when to choose AOT vs framework-dependent vs dotnet tool, RID matrix strategy, single-file publish, size optimization for CLI binaries — cross-refs `[skill:dotnet-native-aot]` for AOT MSBuild
- `dotnet-cli-packaging` covers: Homebrew formula (binary tap, cask), apt/deb packaging, winget manifest, Scoop, Chocolatey, dotnet tool global/local, NuGet
- `dotnet-cli-release-pipeline` covers: unified GitHub Actions workflow, build matrix per RID, artifact staging, GitHub Releases with checksums, automated formula/manifest PRs, SemVer + git tags
- Each skill must contain out-of-scope boundary statements
- **Depends on fn-17.1** (architecture patterns context for distribution)
- **Depends on fn-16.1** (`[skill:dotnet-native-aot]` must exist for hard cross-refs)
- Does NOT modify `plugin.json` (handled by fn-17.3)

### fn-17.3: Integration — plugin registration, validation, and cross-reference audit (depends on fn-17.1, fn-17.2)
**Delivers:** Plugin registration and validation for all 5 skills
- Registers all 5 skill paths in `.claude-plugin/plugin.json`
- Runs repo-wide uniqueness check on skill `name` frontmatter
- Runs `./scripts/validate-skills.sh`
- Validates cross-references use canonical skill IDs and resolve to existing skills
- Validates scope boundary statements present in each skill
- Updates existing `<!-- TODO(fn-17) -->` placeholders in other skills (check `dotnet-native-aot` for CLI cross-ref placeholder)
- Validates soft cross-refs noted but not enforced
- Single owner of `plugin.json` modifications

**Execution order:** fn-17.1 → fn-17.2 → fn-17.3 (serial; fn-17.1 and fn-17.2 are file-disjoint but fn-17.2 has logical dependency on fn-17.1 for cross-ref consistency)

## Key Context
- System.CommandLine is the modern standard for .NET CLI apps (not CommandLineParser, Spectre.Console.Cli, or Cocona)
- System.CommandLine 2.0 is pre-release but battle-tested (powers the `dotnet` CLI itself)
- CLI apps benefit significantly from Native AOT (fast startup, no runtime dependency, smaller binary)
- clig.dev provides language-agnostic CLI design principles (exit codes, stderr for diagnostics, stdout for data, machine-readable output)
- Unified CI/CD pipeline maximizes maintainability across package manager formats
- Homebrew is primary for macOS, apt/deb for Debian/Ubuntu, winget for Windows 10+, Scoop for Windows power users
- `dotnet tool` packaging is the simplest distribution but requires .NET runtime on target
- Native AOT + single-file is the gold standard for CLI distribution (zero dependencies on target)

## Quick Commands
```bash
# Validate all 5 skills exist with frontmatter
for s in dotnet-system-commandline dotnet-cli-architecture dotnet-cli-distribution dotnet-cli-packaging dotnet-cli-release-pipeline; do
  test -f "skills/cli-tools/$s/SKILL.md" && echo "OK: $s" || echo "MISSING: $s"
done

# Validate frontmatter has required fields (name AND description)
for s in skills/cli-tools/*/SKILL.md; do
  grep -q "^name:" "$s" && grep -q "^description:" "$s" && echo "OK: $s" || echo "MISSING FRONTMATTER: $s"
done

# Repo-wide skill name uniqueness check
grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d  # expect empty

# Canonical frontmatter validation
./scripts/validate-skills.sh

# Verify cross-references
grep -r "\[skill:dotnet-native-aot\]" skills/cli-tools/
grep -r "\[skill:dotnet-aot-architecture\]" skills/cli-tools/
grep -r "\[skill:dotnet-containers\]" skills/cli-tools/

# Verify AOT boundary (cross-ref not re-teach)
grep -c "PublishAot" skills/cli-tools/dotnet-cli-distribution/SKILL.md  # expect 0-1 mentions (cross-ref context only)

# Verify scope boundary statements
grep -l "Out of scope\|out of scope\|Scope boundary" skills/cli-tools/*/SKILL.md | wc -l  # expect 5

# Verify plugin.json registration (after fn-17.3)
for s in dotnet-system-commandline dotnet-cli-architecture dotnet-cli-distribution dotnet-cli-packaging dotnet-cli-release-pipeline; do
  grep -q "skills/cli-tools/$s" .claude-plugin/plugin.json && echo "OK: $s" || echo "MISSING: $s"
done

# Verify TODO(fn-17) placeholders resolved (after fn-17.3)
grep -r "TODO(fn-17)" skills/  # expect empty after fn-17.3

# Verify System.CommandLine beta status documented
grep -i "beta\|pre-release" skills/cli-tools/dotnet-system-commandline/SKILL.md  # expect match

# Verify CLI testing coverage
grep -i "testing\|test" skills/cli-tools/dotnet-cli-architecture/SKILL.md  # expect match
```

## Acceptance Criteria
1. All 5 skills exist at `skills/cli-tools/<skill-name>/SKILL.md` with `name` and `description` frontmatter
2. `dotnet-system-commandline` covers full System.CommandLine 2.0 API: RootCommand, Command, Option<T>, Argument<T>, middleware pipeline, hosting integration, tab completion, auto-generated help/version
3. `dotnet-system-commandline` documents System.CommandLine 2.0 beta status with production readiness assessment
4. `dotnet-cli-architecture` covers clig.dev principles: layered command → handler → service architecture, configuration precedence, structured logging, exit code conventions, stdin/stdout/stderr patterns
5. `dotnet-cli-architecture` covers CLI testing: in-process invocation via `CommandLineBuilder`, stdout/stderr capture, exit code assertion
6. `dotnet-cli-distribution` covers distribution strategy: when to choose Native AOT vs framework-dependent vs `dotnet tool`, RID matrix, single-file publish, size optimization
7. `dotnet-cli-distribution` cross-references `[skill:dotnet-native-aot]` — does not re-teach AOT MSBuild configuration
8. `dotnet-cli-packaging` covers all major formats: Homebrew formula, apt/deb, winget manifest, Scoop, Chocolatey, `dotnet tool` global/local, NuGet
9. `dotnet-cli-release-pipeline` covers unified GitHub Actions workflow producing all formats from single trigger with build matrix, artifact staging, GitHub Releases with checksums
10. `dotnet-cli-release-pipeline` cross-references fn-19 CI/CD skills with scope boundary — does not re-teach general CI patterns
11. Skills cross-reference fn-16 AOT skills, fn-5 container skills, fn-3 DI skills using canonical skill IDs — not re-teach
12. Each skill contains explicit out-of-scope boundary statements for related epics (fn-16 AOT, fn-19 CI/CD, fn-3 DI, fn-7 testing)
13. All 5 skills registered in `.claude-plugin/plugin.json` (fn-17.3)
14. `./scripts/validate-skills.sh` passes for all 5 skills
15. Skill `name` frontmatter values are unique repo-wide
16. Existing `<!-- TODO(fn-17) -->` placeholders in other skills are resolved with canonical cross-refs (fn-17.3)
17. Execution order: fn-17.1 → fn-17.2 → fn-17.3 (serial)

## Test Notes
- Verify `dotnet-cli-distribution` cross-refs `[skill:dotnet-native-aot]` and does not duplicate AOT MSBuild property docs
- Verify `dotnet-cli-packaging` covers at least 5 package formats (Homebrew, apt/deb, winget, Scoop, dotnet tool)
- Verify `dotnet-system-commandline` documents beta status with production readiness note
- Verify `dotnet-cli-architecture` covers CLI testing patterns
- Verify `dotnet-cli-release-pipeline` covers GitHub Actions unified workflow
- Run `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` to confirm no duplicate names
- Verify scope boundary statements in all 5 skills
- Verify `plugin.json` contains all 5 CLI skill paths after fn-17.3
- Verify existing fn-17 TODO placeholders in AOT skills are resolved

## References
- System.CommandLine: https://learn.microsoft.com/en-us/dotnet/standard/commandline/
- CLI Guidelines (clig.dev): https://clig.dev/
- .NET tool packaging: https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools-how-to-create
- Homebrew formula cookbook: https://docs.brew.sh/Formula-Cookbook
- winget manifest: https://learn.microsoft.com/en-us/windows/package-manager/package/manifest
- Native AOT deployment: https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/
- Single-file deployment: https://learn.microsoft.com/en-us/dotnet/core/deploying/single-file/overview
