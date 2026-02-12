# fn-9: Agent Meta-Skills

## Overview
Delivers meta-skills that teach agents how to work effectively with .NET projects: common gotchas, build output analysis, .csproj reading/modification, and solution navigation. These are skills-only (no agent)—they improve agent behavior across all .NET tasks by providing reference material agents load contextually.

## Scope Boundary
**In scope:** Guidance for AI agents working with .NET codebases: identifying common mistakes, interpreting build output, understanding project files, and navigating solution structure.

**Out of scope / Owned by other skills:**
- Async/await deep patterns (implementation detail) — owned by `[skill:dotnet-csharp-async-patterns]`
- Dependency injection patterns — owned by `[skill:dotnet-csharp-dependency-injection]`
- Nullable reference types usage — owned by `[skill:dotnet-csharp-nullable-reference-types]`
- Source generator configuration — owned by `[skill:dotnet-csharp-source-generators]`
- Test framework usage — owned by `[skill:dotnet-testing-strategy]`
- Security patterns — owned by fn-8 security skills

The boundary is: fn-9 skills cover "what agents get wrong and how to orient in a .NET codebase"; deep implementation patterns belong to domain-specific skills. Where gotchas overlap other skills, fn-9 provides a brief warning and cross-references the canonical skill.

**Overlap rubric:** Each gotcha subsection MUST include (1) a brief warning of the mistake, (2) anti-pattern code, (3) corrected code, and (4) a `[skill:...]` cross-reference to the canonical skill. It MUST NOT include full implementation walkthroughs — those belong to the referenced skill.

## Skills
Each skill lives at `skills/agent-meta-skills/<skill-name>/SKILL.md` (folder-per-skill convention).

- `dotnet-agent-gotchas` — Common mistakes agents make with .NET code, organized by category:
  1. Async/await misuse (blocking on async, missing ConfigureAwait, fire-and-forget)
  2. NuGet package errors (wrong package names, version conflicts, deprecated packages)
  3. Deprecated API usage (BinaryFormatter, WebClient, older crypto APIs)
  4. Project structure mistakes (wrong SDK, missing PackageReference, broken project refs)
  5. Nullable reference type annotation errors (wrong null-forgiving, missing nullable enable)
  6. Source generator misconfiguration (missing partial, wrong output type)
  7. Trimming/AOT warning suppression instead of fixing
  8. Test organization anti-patterns (tests in prod project, wrong test framework config)
  9. DI registration errors (missing registrations, wrong lifetimes, captive dependencies)
  Each category MUST include: anti-pattern code example, corrected code example, and `[skill:...]` cross-reference to the canonical skill.

- `dotnet-build-analysis` — Help agents interpret MSBuild build output:
  1. Error code reference (CS, MSB, NU, IDE, CA prefix meanings)
  2. NuGet restore failure patterns and fixes
  3. Analyzer warning interpretation and suppression guidance
  4. Multi-targeting build output differences
  5. Common "works locally, fails in CI" patterns
  Each subsection MUST include: example output snippet, diagnosis steps, and fix pattern.

- `dotnet-csproj-reading` — Teach agents to read and safely modify .csproj files:
  1. SDK-style project structure (Project Sdk="...", implicit imports)
  2. PropertyGroup conventions (TFM, nullable, implicit usings, output type)
  3. ItemGroup patterns (PackageReference, ProjectReference, None/Content)
  4. Condition expressions and multi-targeting
  5. Directory.Build.props and Directory.Build.targets
  6. Directory.Packages.props (central package management)
  Each subsection MUST include: annotated XML example and common modification patterns.

- `dotnet-solution-navigation` — Teach agents to orient in .NET solutions:
  1. Entry point discovery: Program.cs, top-level statements, worker services, test projects (not just Program.cs)
  2. Solution file formats (.sln and .slnx) and project listing
  3. Project dependency graph traversal (ProjectReference chains)
  4. Configuration file locations (appsettings*.json, launchSettings.json, Directory.Build.props)
  5. Common solution layouts (src/tests/docs, vertical slice, modular monolith)
  Each subsection MUST include: discovery commands/heuristics and example output.

## Required Skill Section Structure
Every skill MUST include these sections (in order):
1. Frontmatter (`name`, `description`)
2. Overview / scope boundary
3. Prerequisites (minimum .NET version, required tools)
4. Main content sections (per skill definition above)
5. Slopwatch Anti-Patterns section (per mapping table below)
6. Cross-references (`[skill:...]` per matrix below)
7. References (external links)

## Slopwatch Anti-Pattern Checklist
All 4 skills MUST include a dedicated "## Slopwatch Anti-Patterns" section referencing these slopwatch-derived anti-patterns where relevant (from dotnet-skills):
- Disabled/skipped tests (`[Fact(Skip=...)]`, `#if false`, commented-out test methods)
- Warning suppressions (`#pragma warning disable`, `[SuppressMessage]`, `<NoWarn>`)
- Empty catch blocks (`catch { }`, `catch (Exception) { }`)
- Silenced analyzers without justification
- Removed assertions from tests

Each skill maps to specific slopwatch checks:
| Skill | Slopwatch Checks |
|---|---|
| `dotnet-agent-gotchas` | All 5 (overview of each as agent mistakes) |
| `dotnet-build-analysis` | Warning suppressions, silenced analyzers |
| `dotnet-csproj-reading` | `<NoWarn>` in csproj, suppressed analyzers in props |
| `dotnet-solution-navigation` | Disabled/skipped tests in test project discovery |

## Cross-Reference Matrix
Each skill MUST include outbound `[skill:...]` cross-references as follows:

| Skill | Required Outbound Refs |
|---|---|
| `dotnet-agent-gotchas` | `dotnet-csharp-async-patterns`, `dotnet-csharp-dependency-injection`, `dotnet-csharp-nullable-reference-types`, `dotnet-csharp-source-generators`, `dotnet-testing-strategy`, `dotnet-security-owasp` |
| `dotnet-build-analysis` | `dotnet-agent-gotchas`, `dotnet-csproj-reading`, `dotnet-project-structure` |
| `dotnet-csproj-reading` | `dotnet-project-structure`, `dotnet-build-analysis`, `dotnet-agent-gotchas` |
| `dotnet-solution-navigation` | `dotnet-project-structure`, `dotnet-csproj-reading`, `dotnet-testing-strategy` |

## Minimum Supported Versions
- .NET: 8.0+ (LTS baseline); note when features require 9.0+ or 10.0+
- MSBuild: SDK-style projects only (no legacy .csproj)

## Quick Commands
```bash
# Smoke test: verify gotchas skill lists common mistake categories
grep -c "^##" skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md  # expect >=9

# Validate MSBuild error code prefixes in build analysis
grep -E "CS[0-9]|MSB[0-9]|NU[0-9]|IDE[0-9]|CA[0-9]" skills/agent-meta-skills/dotnet-build-analysis/SKILL.md

# Validate build analysis subsections (NuGet restore, analyzer warnings, multi-targeting, CI drift)
grep -i "NuGet restore\|analyzer warn\|multi-target\|fails in CI\|works locally" skills/agent-meta-skills/dotnet-build-analysis/SKILL.md

# Test csproj reading covers Directory.Build.props, .targets, and central package management
grep -i "Directory\.Build\.props\|Directory\.Build\.targets\|Directory\.Packages\.props" skills/agent-meta-skills/dotnet-csproj-reading/SKILL.md

# Verify solution navigation covers multiple entry point patterns
grep -i "top-level\|worker\|Program\.cs" skills/agent-meta-skills/dotnet-solution-navigation/SKILL.md

# Verify .sln and .slnx coverage
grep -i "\.sln\|\.slnx" skills/agent-meta-skills/dotnet-solution-navigation/SKILL.md

# Verify common solution layouts documented
grep -i "vertical slice\|modular monolith\|src/tests" skills/agent-meta-skills/dotnet-solution-navigation/SKILL.md

# Verify exact skill paths registered in plugin.json (one per skill)
grep -q '"skills/agent-meta-skills/dotnet-agent-gotchas"' .claude-plugin/plugin.json && echo "gotchas: OK" || echo "gotchas: MISSING"
grep -q '"skills/agent-meta-skills/dotnet-build-analysis"' .claude-plugin/plugin.json && echo "build-analysis: OK" || echo "build-analysis: MISSING"
grep -q '"skills/agent-meta-skills/dotnet-csproj-reading"' .claude-plugin/plugin.json && echo "csproj-reading: OK" || echo "csproj-reading: MISSING"
grep -q '"skills/agent-meta-skills/dotnet-solution-navigation"' .claude-plugin/plugin.json && echo "solution-nav: OK" || echo "solution-nav: MISSING"

# Verify Prerequisites section exists in each skill
for skill in dotnet-agent-gotchas dotnet-build-analysis dotnet-csproj-reading dotnet-solution-navigation; do
  grep -l "## Prerequisites" "skills/agent-meta-skills/$skill/SKILL.md" 2>/dev/null && echo "$skill: Prerequisites OK" || echo "$skill: Prerequisites MISSING"
done

# Verify Slopwatch Anti-Patterns section exists in each skill
for skill in dotnet-agent-gotchas dotnet-build-analysis dotnet-csproj-reading dotnet-solution-navigation; do
  grep -l "## Slopwatch" "skills/agent-meta-skills/$skill/SKILL.md" 2>/dev/null && echo "$skill: Slopwatch OK" || echo "$skill: Slopwatch MISSING"
done

# Full cross-reference matrix validation (every required ref per skill)
# dotnet-agent-gotchas requires 6 refs
grep -q "skill:dotnet-csharp-async-patterns" skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md && echo "gotchas->async: OK" || echo "gotchas->async: MISSING"
grep -q "skill:dotnet-csharp-dependency-injection" skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md && echo "gotchas->di: OK" || echo "gotchas->di: MISSING"
grep -q "skill:dotnet-csharp-nullable-reference-types" skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md && echo "gotchas->nrt: OK" || echo "gotchas->nrt: MISSING"
grep -q "skill:dotnet-csharp-source-generators" skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md && echo "gotchas->srcgen: OK" || echo "gotchas->srcgen: MISSING"
grep -q "skill:dotnet-testing-strategy" skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md && echo "gotchas->testing: OK" || echo "gotchas->testing: MISSING"
grep -q "skill:dotnet-security-owasp" skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md && echo "gotchas->owasp: OK" || echo "gotchas->owasp: MISSING"
# dotnet-build-analysis requires 3 refs
grep -q "skill:dotnet-agent-gotchas" skills/agent-meta-skills/dotnet-build-analysis/SKILL.md && echo "build->gotchas: OK" || echo "build->gotchas: MISSING"
grep -q "skill:dotnet-csproj-reading" skills/agent-meta-skills/dotnet-build-analysis/SKILL.md && echo "build->csproj: OK" || echo "build->csproj: MISSING"
grep -q "skill:dotnet-project-structure" skills/agent-meta-skills/dotnet-build-analysis/SKILL.md && echo "build->projstruct: OK" || echo "build->projstruct: MISSING"
# dotnet-csproj-reading requires 3 refs
grep -q "skill:dotnet-project-structure" skills/agent-meta-skills/dotnet-csproj-reading/SKILL.md && echo "csproj->projstruct: OK" || echo "csproj->projstruct: MISSING"
grep -q "skill:dotnet-build-analysis" skills/agent-meta-skills/dotnet-csproj-reading/SKILL.md && echo "csproj->build: OK" || echo "csproj->build: MISSING"
grep -q "skill:dotnet-agent-gotchas" skills/agent-meta-skills/dotnet-csproj-reading/SKILL.md && echo "csproj->gotchas: OK" || echo "csproj->gotchas: MISSING"
# dotnet-solution-navigation requires 3 refs
grep -q "skill:dotnet-project-structure" skills/agent-meta-skills/dotnet-solution-navigation/SKILL.md && echo "solnav->projstruct: OK" || echo "solnav->projstruct: MISSING"
grep -q "skill:dotnet-csproj-reading" skills/agent-meta-skills/dotnet-solution-navigation/SKILL.md && echo "solnav->csproj: OK" || echo "solnav->csproj: MISSING"
grep -q "skill:dotnet-testing-strategy" skills/agent-meta-skills/dotnet-solution-navigation/SKILL.md && echo "solnav->testing: OK" || echo "solnav->testing: MISSING"
```

## Acceptance Criteria
1. All 4 skills written at `skills/agent-meta-skills/<name>/SKILL.md` with required frontmatter (`name`, `description`)
2. Each skill follows the required section structure: overview/scope, prerequisites, main content, slopwatch anti-patterns section, cross-references, references
3. Agent gotchas skill covers all 9 mistake categories, each with: (a) brief mistake warning, (b) anti-pattern code, (c) corrected code, (d) `[skill:...]` cross-reference — no full implementation walkthroughs
4. Build analysis skill covers all 5 subsections, each with: example output snippet, diagnosis steps, and fix pattern:
   - (a) >=5 error code prefixes (CS, MSB, NU, IDE, CA)
   - (b) NuGet restore failure patterns
   - (c) Analyzer warning interpretation and suppression guidance
   - (d) Multi-targeting build output differences
   - (e) "Works locally, fails in CI" patterns
5. Csproj reading skill covers all 6 subsections, each with: annotated XML example and common modification patterns:
   - (a) SDK-style project structure
   - (b) PropertyGroup conventions
   - (c) ItemGroup patterns
   - (d) Condition expressions and multi-targeting
   - (e) Directory.Build.props AND Directory.Build.targets
   - (f) Directory.Packages.props (central package management)
6. Solution navigation skill covers all 5 subsections, each with: discovery commands/heuristics and example output:
   - (a) >=3 entry point patterns (Program.cs, top-level statements, worker services)
   - (b) .sln and .slnx format guidance
   - (c) Project dependency traversal (ProjectReference chains)
   - (d) Configuration file locations (appsettings, launchSettings, Directory.Build.props)
   - (e) >=2 common solution layouts documented
7. Slopwatch anti-patterns: each skill has a dedicated "## Slopwatch Anti-Patterns" section covering its assigned checks per mapping table with concrete examples
8. Cross-references validated per full matrix (every `[skill:...]` ref verified via grep — see Quick Commands)
9. All 4 skills registered in `.claude-plugin/plugin.json` skills array with exact paths verified
10. No deep implementation overlap with domain skills per overlap rubric (brief warning + cross-ref, no walkthroughs)

## Task Breakdown and Dependencies
- **fn-9.1**: Agent gotchas + build analysis skills (skills that focus on "what goes wrong")
- **fn-9.2**: Csproj reading + solution navigation skills (skills that focus on "how to orient"). **Depends on fn-9.1 completion** — fn-9.2 owns plugin.json registration and cross-reference validation for all 4 skills, so fn-9.1 must be complete (not stubs) before fn-9.2 can be marked done.

Tasks touch disjoint skill directories. Shared file: `.claude-plugin/plugin.json` — fn-9.2 is the integration owner for plugin.json registration of all 4 skills.

## Test Notes
- Validate gotchas skill against real-world agent mistake patterns (async blocking, wrong packages, etc.)
- Verify each build analysis subsection has example output + diagnosis + fix (not just topic mention)
- Validate each csproj reading subsection has annotated XML example (not just topic mention)
- Validate each solution navigation subsection has discovery commands + example output
- Confirm csproj reading covers Directory.Build.targets (not just .props)
- Confirm solution navigation covers solutions with both .sln and .slnx formats
- Confirm solution navigation documents >=2 layout patterns (e.g. src/tests, vertical slice)
- Confirm overlap rubric: gotchas subsections are warning + cross-ref, not full walkthroughs

## References
- MSBuild Reference: https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild
- .NET Project SDK: https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview
- Central Package Management: https://learn.microsoft.com/en-us/nuget/consume-packages/Central-Package-Management
- Directory.Build.props: https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory
- dotnet-skills slopwatch: https://github.com/Aaronontheweb/dotnet-skills
