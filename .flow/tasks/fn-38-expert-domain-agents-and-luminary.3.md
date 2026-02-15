# fn-38-expert-domain-agents-and-luminary.3 Add luminary attribution to existing skills and update routing

## Description
Add luminary source attribution ("References" or "Knowledge Sources" sections) to 6+ existing skills and update routing (dotnet-advisor catalog and AGENTS.md) for the two new agents.

**Size:** M
**Files:** `skills/core-csharp/dotnet-csharp-async-patterns/SKILL.md`, `skills/performance/dotnet-performance-patterns/SKILL.md`, `skills/api-development/dotnet-minimal-apis/SKILL.md`, `skills/ui-frameworks/dotnet-blazor-components/SKILL.md`, `skills/architecture/dotnet-architecture-patterns/SKILL.md`, `skills/core-csharp/dotnet-csharp-coding-standards/SKILL.md`, `skills/foundation/dotnet-advisor/SKILL.md`, `AGENTS.md`

## Approach
- Add "References" sections to existing skills citing authoritative luminary sources:
  - `dotnet-csharp-async-patterns`: Toub ConfigureAwait FAQ, Fowler async guidance (already partially done at line 314)
  - `dotnet-performance-patterns`: Toub .NET Performance blog series
  - `dotnet-minimal-apis`: Fowler AspNetCoreDiagnosticScenarios
  - `dotnet-blazor-components`: Damian Edwards Blazor guidance
  - `dotnet-architecture-patterns`: Andrew Lock middleware blog, Steve Smith/Ardalis Clean Architecture
  - `dotnet-csharp-coding-standards`: Mads Torgersen C# design notes
- Update `dotnet-advisor` catalog to include routing entries for new async-performance-specialist and aspnetcore-specialist agents
- Update `AGENTS.md` delegation table with new agent triggers and boundaries
- Do NOT rename agents or change existing content beyond adding references
- Reference sections do NOT count toward the description budget (they're body content, not frontmatter description)

## Key context
- Some skills already cite David Fowler (e.g., `dotnet-csharp-async-patterns:314`). Verify what exists before adding duplicates.
- Attribution pattern: "Grounded in guidance from [Name] — [Source URL]" — not "As recommended by" or "According to"
- Budget impact: zero (references are body content, not description field)
## Acceptance
- [ ] At least 6 existing skills have luminary attribution in References sections
- [ ] Attribution uses "Grounded in guidance from" pattern, not impersonation language
- [ ] dotnet-advisor catalog updated with new agent routing entries
- [ ] AGENTS.md updated with new agent entries, triggers, and scope boundaries
- [ ] No duplicate references (check existing References sections first)
- [ ] No fn-N spec references introduced
- [ ] All four validation commands pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
