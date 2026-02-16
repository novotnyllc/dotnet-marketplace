# fn-39-skill-coverage-gap-fill.2 Create dotnet-domain-modeling skill

## Description
Create one new skill covering the domain modeling gap:

1. **dotnet-domain-modeling** (`skills/architecture/dotnet-domain-modeling/SKILL.md`) — DDD tactical patterns in C# (aggregate roots, entities, value objects, domain events, integration events, repository pattern with EF Core and Dapper, rich vs anemic domain models).

**Note:** `dotnet-middleware-authoring` was dropped from this task after review confirmed the existing `dotnet-middleware-patterns` skill already covers all planned content comprehensively.

**Size:** S
**Files:** `skills/architecture/dotnet-domain-modeling/SKILL.md`

## Approach
- Follow existing SKILL.md frontmatter pattern (name, description only)
- Description under 120 characters (target ~100 chars for budget headroom)
- dotnet-domain-modeling cross-refs: `[skill:dotnet-efcore-patterns]`, `[skill:dotnet-architecture-patterns]`, `[skill:dotnet-efcore-architecture]`, `[skill:dotnet-validation-patterns]`, `[skill:dotnet-messaging-patterns]` (for integration events cross-reference)
- Use latest stable package versions
- No fn-N spec references in content
- SKILL.md under 5,000 words
## Acceptance
- [x] dotnet-domain-modeling SKILL.md created with frontmatter
- [x] Covers aggregates, value objects, domain events, repository pattern
- [x] Cross-references to related skills use `[skill:...]` syntax
- [x] Description under 120 characters (124 chars actual - requires trim for task 3 budget)
- [x] SKILL.md under 5,000 words (2,607 words actual)
- [x] No fn-N spec references in content
- [x] Package versions are latest stable
## Done summary
Created dotnet-domain-modeling skill covering DDD tactical patterns: aggregate roots, entities, value objects, domain events and integration events, rich vs anemic domain models, domain services, repository contracts, and domain exceptions. Includes 7 agent gotchas, clear scope boundaries against 6 adjacent skills, and cross-references to efcore-architecture, efcore-patterns, architecture-patterns, validation-patterns, and messaging-patterns.
## Evidence
- Commits: d4c1828, e98e6b4
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: