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
- dotnet-domain-modeling cross-refs: `[skill:dotnet-efcore-patterns]`, `[skill:dotnet-architecture-patterns]`, `[skill:dotnet-efcore-architecture]`, `[skill:dotnet-validation-patterns]`
- Use latest stable package versions
- No fn-N spec references in content
- SKILL.md under 5,000 words
## Acceptance
- [ ] dotnet-domain-modeling SKILL.md created with frontmatter
- [ ] Covers aggregates, value objects, domain events, repository pattern
- [ ] Cross-references to related skills use `[skill:...]` syntax
- [ ] Description under 120 characters
- [ ] SKILL.md under 5,000 words
- [ ] No fn-N spec references in content
- [ ] Package versions are latest stable
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
