# fn-9-agent-meta-skills.2 Csproj reading and solution navigation skills

## Description
Create two meta-skills focused on "how to orient" for agents working with .NET:

1. **`dotnet-csproj-reading`** at `skills/agent-meta-skills/dotnet-csproj-reading/SKILL.md` — covers 6 subsections. Each subsection includes: annotated XML example and common modification patterns.

2. **`dotnet-solution-navigation`** at `skills/agent-meta-skills/dotnet-solution-navigation/SKILL.md` — covers 5 subsections. Each subsection includes: discovery commands/heuristics and example output.

Both skills follow the required section structure: frontmatter, overview/scope, prerequisites, main content, slopwatch anti-patterns section, cross-references, references.

This task **depends on fn-9.1 completion** (not stubs) — fn-9.2 owns plugin.json registration and cross-reference validation for all 4 skills, so fn-9.1 must be complete before fn-9.2 can be marked done.

## File Ownership
- `skills/agent-meta-skills/dotnet-csproj-reading/SKILL.md` (create)
- `skills/agent-meta-skills/dotnet-solution-navigation/SKILL.md` (create)
- `.claude-plugin/plugin.json` (modify — add all 4 fn-9 skills to skills array)

## Acceptance
### dotnet-csproj-reading
- [ ] SKILL.md created with frontmatter (`name`, `description`)
- [ ] Has required sections: overview/scope, prerequisites, main content, slopwatch, cross-refs, references
- [ ] Subsection (1) SDK-style structure: annotated XML example + modification patterns
- [ ] Subsection (2) PropertyGroup conventions: annotated XML showing TFM, nullable, implicit usings, output type + modification patterns
- [ ] Subsection (3) ItemGroup patterns: annotated XML showing PackageReference, ProjectReference, None/Content + modification patterns
- [ ] Subsection (4) Condition expressions: annotated XML showing multi-targeting conditions + modification patterns
- [ ] Subsection (5) Directory.Build.props AND Directory.Build.targets: annotated XML for both + modification patterns
- [ ] Subsection (6) Directory.Packages.props: annotated XML showing CPM + modification patterns
- [ ] Dedicated "## Slopwatch Anti-Patterns" section covering: `<NoWarn>` in csproj, suppressed analyzers in props
- [ ] All 3 required outbound cross-refs present per matrix

### dotnet-solution-navigation
- [ ] SKILL.md created with frontmatter (`name`, `description`)
- [ ] Has required sections: overview/scope, prerequisites, main content, slopwatch, cross-refs, references
- [ ] Subsection (1) entry points: discovery commands + example output for >=3 patterns (Program.cs, top-level statements, worker services)
- [ ] Subsection (2) solution formats: commands for both .sln and .slnx parsing + example output
- [ ] Subsection (3) dependency traversal: commands for ProjectReference chain discovery + example output
- [ ] Subsection (4) config file locations: commands to find appsettings, launchSettings, Directory.Build.props + example output
- [ ] Subsection (5) solution layouts: >=2 patterns documented (e.g. src/tests, vertical slice) with example directory trees
- [ ] Dedicated "## Slopwatch Anti-Patterns" section covering: disabled/skipped tests in test project discovery
- [ ] All 3 required outbound cross-refs present per matrix

### Integration (all 4 skills)
- [ ] fn-9.1 is complete (not stubs) before marking fn-9.2 done
- [ ] All 4 fn-9 skills registered in `.claude-plugin/plugin.json` with exact paths:
  - `skills/agent-meta-skills/dotnet-agent-gotchas`
  - `skills/agent-meta-skills/dotnet-build-analysis`
  - `skills/agent-meta-skills/dotnet-csproj-reading`
  - `skills/agent-meta-skills/dotnet-solution-navigation`
- [ ] Full cross-reference matrix validated (all refs per Quick Commands in epic spec)
- [ ] No deep implementation overlap — brief warning + cross-ref only per overlap rubric

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
