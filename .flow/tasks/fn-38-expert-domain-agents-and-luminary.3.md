# fn-38-expert-domain-agents-and-luminary.3 Add luminary attribution to existing skills and update routing

## Description
Add luminary source attribution ("References" or "Knowledge Sources" sections) to 6+ existing skills and update routing (dotnet-advisor catalog and AGENTS.md) for all 5 new agents and 4 enriched existing agents. Update agent counts in AGENTS.md and CLAUDE.md (9→14).

**Size:** M
**Files:** `skills/core-csharp/dotnet-csharp-async-patterns/SKILL.md`, `skills/performance/dotnet-performance-patterns/SKILL.md`, `skills/api-development/dotnet-minimal-apis/SKILL.md`, `skills/ui-frameworks/dotnet-blazor-components/SKILL.md`, `skills/architecture/dotnet-architecture-patterns/SKILL.md`, `skills/core-csharp/dotnet-csharp-coding-standards/SKILL.md`, `skills/foundation/dotnet-advisor/SKILL.md`, `AGENTS.md`, `CLAUDE.md`

## Approach
- Add "References" sections to existing skills citing authoritative luminary sources:
  - `dotnet-csharp-async-patterns`: Toub ConfigureAwait FAQ, Fowler async guidance (already partially done at line 314)
  - `dotnet-performance-patterns`: Toub .NET Performance blog series
  - `dotnet-minimal-apis`: Fowler AspNetCoreDiagnosticScenarios
  - `dotnet-blazor-components`: Damian Edwards Blazor guidance
  - `dotnet-architecture-patterns`: Andrew Lock middleware blog, Steve Smith/Ardalis Clean Architecture
  - `dotnet-csharp-coding-standards`: Mads Torgersen C# design notes
- Update `dotnet-advisor` catalog to include routing entries for all 5 new agents: async-performance-specialist, aspnetcore-specialist, testing-specialist, cloud-specialist, and code-review-agent
- Update `AGENTS.md` delegation table with all 5 new agent entries, triggers, and scope boundaries
- Update `AGENTS.md` agent count (9→14) and `CLAUDE.md` plugin summary count (9→14 agents)
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
- [ ] AGENTS.md updated with all 5 new agent entries, triggers, and scope boundaries
- [ ] AGENTS.md agent count updated (9→14)
- [ ] CLAUDE.md plugin summary agent count updated (9→14)
- [ ] No duplicate references (check existing References sections first)
- [ ] No fn-N spec references introduced
- [ ] All four validation commands pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
