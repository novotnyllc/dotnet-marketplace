# Self-Contained Skills Port

## Overview
The spec references Aaronontheweb/dotnet-skills as reference material but the plugin must be fully self-contained. Port all relevant skills from dotnet-skills, adapting them to our standards (SKILL.md frontmatter, cross-reference syntax, description budget, no fn-N references). Credit original authors in each ported skill.

## Scope
Skills to port/adapt from dotnet-skills (not already covered by existing skills):
- **System.CommandLine** (>= 2.0.0 only, not earlier betas) — CLI app patterns, command hierarchy, argument binding
- **FluentValidation alternatives** — Minimize third-party deps; cover built-in DataAnnotations, IValidatableObject, IValidateOptions, MinimalApis.Extensions validation
- **Logging/Observability** — Structured logging with Microsoft.Extensions.Logging, OpenTelemetry patterns
- **Middleware patterns** — ASP.NET Core middleware pipeline, request/response manipulation
- **gRPC** — service definitions, client/server patterns, streaming, interceptors
- **SignalR** — real-time communication patterns, hub design, client integration
- **Architecture principles** — DRY, SRP, SOLID principles deeply engrained (reference: https://stormwild.github.io/blog/post/srp-mistakes-csharp-dotnet/), clean architecture, vertical slices

**Budget constraint**: Currently at 12,458/15,000 chars with 101 skills. Each new skill description must stay under 120 chars. Prefer extending existing skills over creating new ones where overlap exists.

**Key rule**: Skills must never reference internal spec IDs (fn-N). No mention of implementation tracking.

**Package version policy**: Always use latest stable versions of libraries. If existing reference is a prerelease, update to latest prerelease; if a higher stable exists, prefer stable.

## Quick commands
```bash
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
```

## Acceptance
- [ ] All ported skills have SKILL.md with required frontmatter (name, description)
- [ ] Original author credited in each ported skill (attribution section or note)
- [ ] System.CommandLine skill covers >= 2.0.0 only
- [ ] Built-in validation patterns preferred over FluentValidation
- [ ] Architecture skill engrain SOLID/DRY/SRP with concrete C# anti-patterns and fixes
- [ ] No fn-N spec references in any skill content
- [ ] Description budget remains under 15,000 chars total
- [ ] All skills registered in plugin.json
- [ ] Cross-references use `[skill:name]` syntax
- [ ] All validation commands pass

## References
- Aaronontheweb/dotnet-skills — source material (MIT license)
- https://stormwild.github.io/blog/post/srp-mistakes-csharp-dotnet/ — SRP anti-patterns reference
- `skills/` — existing skill structure to follow
- `.claude-plugin/plugin.json` — skill registration
