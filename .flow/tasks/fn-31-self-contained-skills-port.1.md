# fn-31-self-contained-skills-port.1 Port System.CommandLine skill (>= 2.0.0)

## Description
Create skills/cli/dotnet-system-commandline/SKILL.md covering System.CommandLine >= 2.0.0 stable only (no earlier beta APIs). Cover command hierarchy, argument/option binding, middleware pipeline, invocation context, custom type converters, and testing.

**Size:** M
**Files:** skills/cli/dotnet-system-commandline/SKILL.md, .claude-plugin/plugin.json

## Approach
- Reference Aaronontheweb/dotnet-skills System.CommandLine content as starting point (credit author)
- Adapt to our SKILL.md frontmatter format (name, description only)
- Cover only >= 2.0.0 GA APIs, explicitly note that beta-era APIs are not covered
- Cross-ref to [skill:dotnet-csharp-coding-standards] for general patterns

## Key context
- System.CommandLine 2.0.0 changed significantly from beta. Ignore CommandHandler, use SetHandler pattern.
- The cli category may need to be created
## Acceptance
- [ ] SKILL.md with required frontmatter
- [ ] Covers >= 2.0.0 stable API only
- [ ] Original author credited
- [ ] Registered in plugin.json
- [ ] Validation passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
