# fn-31-self-contained-skills-port.1 Enhance System.CommandLine skill (>= 2.0.0)

## Description
Enhance existing `skills/cli-tools/dotnet-system-commandline/SKILL.md` with ported content from dotnet-skills covering System.CommandLine >= 2.0.0 stable only (no earlier beta APIs). Enrich command hierarchy, argument/option binding, middleware pipeline, invocation context, custom type converters, and testing patterns.

**Size:** M
**Files:** skills/cli-tools/dotnet-system-commandline/SKILL.md

## Approach
- Read the existing skill first to understand current coverage
- Reference Aaronontheweb/dotnet-skills System.CommandLine content as source material (credit author)
- Merge new content into the existing skill, preserving what's already there
- Cover only >= 2.0.0 GA APIs; explicitly note that beta-era APIs (e.g., CommandHandler) are superseded by SetHandler
- Cross-ref to [skill:dotnet-csharp-coding-standards] for general patterns
- Add `## Attribution` section at bottom crediting Aaronontheweb/dotnet-skills
- No plugin.json change needed (skill already registered at `skills/cli-tools/dotnet-system-commandline`)

## Key context
- System.CommandLine 2.0.0 changed significantly from beta. Ignore CommandHandler, use SetHandler pattern.
- Skill already exists at `skills/cli-tools/dotnet-system-commandline/` and is registered in plugin.json
- Description must stay under 120 chars

## Acceptance
- [ ] Existing SKILL.md enhanced (not replaced or duplicated)
- [ ] Covers >= 2.0.0 stable API only
- [ ] Original author credited via `## Attribution` section
- [ ] Description under 120 chars
- [ ] Validation passes

## Done summary
Enhanced System.CommandLine skill from beta4 to 2.0.0 GA API: rewrote all code examples for SetAction/ParseResult patterns, added custom type parsing (CustomParser property), testing with TextWriter capture via InvocationConfiguration, DI integration without discontinued Hosting package, comprehensive beta4-to-GA migration table, and Aaronontheweb/dotnet-skills attribution.
## Evidence
- Commits: a9dfbeaffbdc15d0ba9c54c66fc9ee3d680845fa
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: