# fn-38-expert-domain-agents-and-luminary.3 Add luminary attribution to existing skills and update routing

## Description
Add luminary source attribution ("References" or "Knowledge Sources" sections) to remaining skills not yet enriched and update routing (dotnet-advisor catalog and AGENTS.md) for all 5 new agents and 4 enriched existing agents. Update agent counts in AGENTS.md and CLAUDE.md (9→14).
<!-- Updated by plan-sync: fn-38.5 already added Knowledge Sources to dotnet-csharp-async-patterns, dotnet-csharp-coding-standards, dotnet-csharp-modern-patterns, dotnet-architecture-patterns, dotnet-solid-principles, and dotnet-middleware-patterns -->

**Size:** M
**Files:** `skills/performance/dotnet-performance-patterns/SKILL.md`, `skills/api-development/dotnet-minimal-apis/SKILL.md`, `skills/ui-frameworks/dotnet-blazor-components/SKILL.md`, `skills/foundation/dotnet-advisor/SKILL.md`, `AGENTS.md`, `CLAUDE.md`

## Approach
- Add "Knowledge Sources" sections to remaining skills not yet enriched by fn-38.5:
  - `dotnet-performance-patterns`: Toub .NET Performance blog series (no Knowledge Sources yet)
  - `dotnet-minimal-apis`: Fowler AspNetCoreDiagnosticScenarios (no Knowledge Sources yet)
  - `dotnet-blazor-components`: Damian Edwards Blazor guidance (no Knowledge Sources yet)
- Skills already enriched by fn-38.5 (do NOT duplicate):
  - `dotnet-csharp-async-patterns`: already has Knowledge Sources (Cleary, Fowler, Toub) at line 312
  - `dotnet-csharp-coding-standards`: already has Knowledge Sources (Torgersen) at line 382
  - `dotnet-architecture-patterns`: already has Knowledge Sources (Bogard, Chapsas) at line 639
  - `dotnet-solid-principles`: already has Knowledge Sources (Smith/Ardalis, Bogard) at line 631
  - `dotnet-middleware-patterns`: already has Knowledge Sources (Andrew Lock) at line 554
  - `dotnet-csharp-modern-patterns`: already has Knowledge Sources (Torgersen) at line 368
- Update `dotnet-advisor` catalog to include routing entries for all 5 new agents: async-performance-specialist, aspnetcore-specialist, testing-specialist, cloud-specialist, and code-review-agent
- Update `AGENTS.md` delegation table with all 5 new agent entries, triggers, and scope boundaries
- Update `AGENTS.md` agent count (9→14) and `CLAUDE.md` plugin summary count (9→14 agents)
- Do NOT rename agents or change existing content beyond adding references
- Reference sections do NOT count toward the description budget (they're body content, not frontmatter description)

## Key context
- fn-38.5 already added Knowledge Sources to 6 skills and 5 agents. Verify what exists before adding duplicates.
- Attribution pattern: "Grounded in guidance from [Name] — [Source URL]" — not "As recommended by" or "According to"
- Budget impact: zero (references are body content, not description field)
- Note: fn-38.5 placed Andrew Lock in `dotnet-middleware-patterns` and aspnetcore-specialist (not `dotnet-architecture-patterns`). Steve Smith/Ardalis went to `dotnet-solid-principles` (not `dotnet-architecture-patterns`). These placements are more precise to each luminary's domain.
## Acceptance
- [ ] At least 3 remaining skills have luminary attribution added in Knowledge Sources sections (dotnet-performance-patterns, dotnet-minimal-apis, dotnet-blazor-components)
- [ ] Attribution uses "Grounded in guidance from" pattern, not impersonation language
- [ ] dotnet-advisor catalog updated with new agent routing entries
- [ ] AGENTS.md updated with all 5 new agent entries, triggers, and scope boundaries
- [ ] AGENTS.md agent count updated (9→14)
- [ ] CLAUDE.md plugin summary agent count updated (9→14)
- [ ] No duplicate references (check existing References sections first)
- [ ] No fn-N spec references introduced
- [ ] All four validation commands pass
## Done summary
Added Knowledge Sources sections to 3 skills (dotnet-performance-patterns, dotnet-minimal-apis, dotnet-blazor-components) with luminary attribution using "Grounded in guidance from" pattern. Updated dotnet-advisor routing catalog and AGENTS.md delegation table with all 5 new specialist agents. Updated agent count from 9 to 14 across AGENTS.md and CLAUDE.md.
## Evidence
- Commits: 79dd69e22e17bd0343994416ffc70f97c6cbd001
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: