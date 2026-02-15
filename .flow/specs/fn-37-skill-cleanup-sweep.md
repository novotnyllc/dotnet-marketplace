# Skill Cleanup Sweep

## Overview
Housekeeping pass across all skills to remove internal tracking artifacts, fix stale references, update testing defaults, and enforce package version policy.

## Scope
1. **Remove fn-N references** — 57 files contain fn-N spec references (e.g., "implemented in fn-7"). Skills should never reference internal planning IDs.
2. **Remove .gitkeep files** — 19+ unnecessary .gitkeep files in skill directories that now have content.
3. **Fix broken cross-references** — `dotnet-advisor` references `[skill:dotnet-scaffolding-base]` which should be `[skill:dotnet-scaffold-project]` (lines 42, 171)
4. **Update testing defaults** — All testing guidance should default to xUnit v3 with Microsoft.Testing.Platform v2 (MTP2), not xUnit v2
5. **Minimize third-party deps** — Replace FluentValidation references with built-in alternatives (DataAnnotations, IValidateOptions, MinimalApis.Extensions)
6. **System.CommandLine version** — Ensure any System.CommandLine references target >= 2.0.0 stable, not earlier betas
7. **Package version updates** — Ensure all library version references use latest stable (prefer stable over prerelease)
8. **Remove internal artifacts** — `skills/architecture/FN7-RECONCILIATION.md` should not ship
9. **SOLID/DRY/SRP enforcement** — Ensure architecture-related skills engrain these principles (check `dotnet-clean-architecture`, `dotnet-csharp-coding-standards`, `dotnet-architecture-patterns`)

## Quick commands
```bash
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
python3 scripts/validate_cross_agent.py
```

## Acceptance
- [ ] Zero fn-N references in any skill SKILL.md content
- [ ] Zero unnecessary .gitkeep files
- [ ] All cross-references valid (validate-skills.sh passes)
- [ ] Testing defaults updated to xUnit v3 + MTP2 across all testing skills
- [ ] Third-party dep references minimized (built-in preferred)
- [ ] System.CommandLine references target >= 2.0.0
- [ ] Package versions updated to latest stable
- [ ] FN7-RECONCILIATION.md removed
- [ ] Architecture skills reference SOLID/DRY/SRP principles
- [ ] All four validation commands pass

## References
- Context-scout findings: 57 files with fn-N refs, 19 .gitkeep files
- `skills/foundation/dotnet-advisor/SKILL.md:42,171` — broken cross-ref
- `skills/architecture/FN7-RECONCILIATION.md` — internal artifact to remove
- https://stormwild.github.io/blog/post/srp-mistakes-csharp-dotnet/ — SRP anti-patterns reference
