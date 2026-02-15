# Self-Contained Skills Port

## Overview
The spec references Aaronontheweb/dotnet-skills as reference material but the plugin must be fully self-contained. Port all relevant skills from dotnet-skills, adapting them to our standards (SKILL.md frontmatter, cross-reference syntax, description budget, no fn-N references). Credit original authors in each ported skill.

## Scope
Skills to port/adapt from dotnet-skills. Several already exist and should be **enhanced** rather than duplicated:

### Enhance existing skills (port additional content into them)
- **System.CommandLine** (`skills/cli-tools/dotnet-system-commandline/`) — enhance with >= 2.0.0 GA patterns, SetAction, CustomParser, testing
<!-- Updated by plan-sync: fn-31-self-contained-skills-port.1 used SetAction (not SetHandler) and CustomParser property (not "custom type converters") -->
- **gRPC** (`skills/serialization/dotnet-grpc/`) — enhance with interceptors, streaming patterns, gRPC-Web, deadline/cancellation
- **SignalR / real-time** (`skills/serialization/dotnet-realtime-communication/`) — enhance with hub design, strongly-typed hubs, groups, scaling with Redis backplane
- **Logging/Observability** (`skills/architecture/dotnet-observability/`) — enhance with structured logging patterns, LoggerMessage, message templates, scopes

### Create new skills (no existing equivalent)
- **Built-in validation patterns** — DataAnnotations, IValidatableObject, IValidateOptions, MinimalApis.Extensions validation. Prefer built-in over FluentValidation.
- **SOLID/DRY/SRP principles** — concrete C# anti-patterns and fixes, cross-ref to `[skill:dotnet-architecture-patterns]` for clean arch/vertical slices
- **Middleware patterns** — ASP.NET Core middleware pipeline, ordering, custom middleware, short-circuit logic. Place in `skills/api-development/` (existing category).

**Budget constraint**: Currently at 12,458/15,000 chars with 101 skills. Enhancing 4 existing skills adds 0 new descriptions. Creating 3 new skills × ~120 chars = ~360 chars → projected ~12,818. Well under the 15,000 fail threshold.

**Key rules**:
- Skills must never reference internal spec IDs (fn-N). No mention of implementation tracking.
- Each task must check for existing skill overlap before creating anything new.
- plugin.json registration only needed for the 3 new skills (existing skills are already registered).

**Package version policy**: Always use latest stable versions of libraries.

**Attribution format**: Add an `## Attribution` section at the bottom of each ported/enhanced skill body with:
```
Adapted from [Aaronontheweb/dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) (MIT license).
```

## Quick commands
```bash
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
```

## Acceptance
- [ ] All ported/enhanced skills have SKILL.md with required frontmatter (name, description)
- [ ] Original author credited via `## Attribution` section in each ported skill
- [ ] System.CommandLine skill enhanced to cover >= 2.0.0 GA only
- [ ] Built-in validation patterns preferred over FluentValidation
- [ ] Architecture skill engrains SOLID/DRY/SRP with concrete C# anti-patterns and fixes; cross-refs `[skill:dotnet-architecture-patterns]` for clean arch/vertical slices
- [ ] No fn-N spec references in any skill content (spec files in .flow/ are exempt)
- [ ] Description budget remains under 15,000 chars total
- [ ] New skills (3) registered in plugin.json; existing skills (4) already registered
- [ ] Cross-references use `[skill:name]` syntax with correct skill names
- [ ] All validation commands pass
- [ ] No duplicate skills created (enhance existing over create new)

## References
- Aaronontheweb/dotnet-skills — source material (MIT license)
- https://stormwild.github.io/blog/post/srp-mistakes-csharp-dotnet/ — SRP anti-patterns reference
- `skills/` — existing skill structure to follow
- `.claude-plugin/plugin.json` — skill registration
