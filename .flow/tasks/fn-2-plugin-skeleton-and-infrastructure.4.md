## Description
Create the `dotnet-project-analysis` skill that helps agents understand .NET solution structure, project references, and build configuration.

**Size:** M
**Files:**
- `skills/foundation/dotnet-project-analysis/SKILL.md`

## Approach

1. Use `/plugin-dev:skill-development` for frontmatter requirements
2. Write frontmatter with required fields: `name`, `description` (canonical set from epic)
3. Skill instructs agent to analyze:
   - `.sln`/`.slnx` for solution structure and project list
   - Project references (`<ProjectReference>`) for dependency graph
   - `Directory.Build.props` / `Directory.Build.targets` for centralized config
   - `Directory.Packages.props` for Central Package Management
   - `.editorconfig` for coding style settings
   - `nuget.config` for package sources
4. Output: project dependency graph, shared config locations, CPM status
5. Guide agent on navigation: "entry point is Program.cs", "startup config in appsettings.json"
6. Detect common project types: web API, console, class lib, test, MAUI, Blazor, etc.
7. Cross-reference version detection using `[skill:dotnet-version-detection]` syntax for TFM info

## Key context

- Reference dotnet-skills `project-structure` skill for conventions (.slnx, Directory.Build.props)
- Modern .NET uses .slnx (new format) alongside .sln (legacy)
- Central Package Management via Directory.Packages.props is the recommended approach
- This skill is foundational - agents need to understand project layout before doing anything
- Required frontmatter: `name`, `description` (canonical set from epic spec)
- Cross-references MUST use `[skill:name]` syntax (machine-parseable, validated in CI)

## Acceptance
- [ ] SKILL.md has valid frontmatter (name, description)
- [ ] Skill reads .sln and .slnx solution files
- [ ] Skill maps project references into dependency understanding
- [ ] Skill detects Directory.Build.props/targets centralized config
- [ ] Skill detects Central Package Management (Directory.Packages.props)
- [ ] Skill identifies common project types (web, console, lib, test, MAUI, Blazor)
- [ ] Skill guides agent to entry points and config files
- [ ] Cross-references use `[skill:dotnet-version-detection]` syntax for TFM info

## Done summary

## Evidence
