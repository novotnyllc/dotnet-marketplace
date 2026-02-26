# fn-64-consolidate-131-skills-into-20-broad.9 Update agents, advisor and hooks for consolidated skills

## Description
Update all 14 agent definitions, rewrite dotnet-advisor routing catalog, and update hooks to reference the 8 consolidated skill names.

**Size:** M
**Files:** `agents/*.md` (14 files), `skills/dotnet-advisor/SKILL.md`, `scripts/hooks/session-start-context.sh`, `scripts/hooks/user-prompt-dotnet-reminder.sh`, `hooks/hooks.json`

## Approach

1. **Rewrite dotnet-advisor**: Replace 363-line routing catalog (21 categories, 131 skills) with 8 consolidated skills. The routing catalog becomes dramatically simpler — 8 entries with rich keyword descriptions pointing to the right skill. Each entry can include companion file hints (e.g., "for async patterns, read `references/async-patterns.md` from `dotnet-csharp`").
2. **Update agent preloaded skills**: Each agent's `## Preloaded Skills` section lists `[skill:old-name]` refs. Replace with `[skill:new-name]`. Examples:
   - `dotnet-testing-specialist`: 5 individual skill refs → `[skill:dotnet-testing]`
   - `dotnet-aspnetcore-specialist`: 7 individual skill refs → `[skill:dotnet-api]`
   - `dotnet-code-review-agent`: 7 individual skill refs → `[skill:dotnet-csharp]` + `[skill:dotnet-api]`
   - `dotnet-blazor-specialist`: 5 refs → `[skill:dotnet-ui]`
   - (apply pattern to all 14 agents)
3. **Update agent routing tables**: Replace all inline `[skill:old-name]` references in Knowledge Sources, Explicit Boundaries, Routing Tables with new names.
4. **Update hooks**: Both hook scripts reference `[skill:dotnet-advisor]` — this name survives. Verify no other skill refs in hooks.
5. **Verify `STRICT_REFS=1` passes**: All `[skill:name]` refs must resolve to actual skill directory names.

## Key context

- 14 agents at `agents/*.md` — each has Preloaded Skills, Knowledge Sources, Explicit Boundaries sections
- `dotnet-code-review-agent` alone references 15+ individual skill names — biggest update
- With 8 skills, agents may preload 1-2 skills instead of 5-7 (simpler, faster loading)
- Agents can specify companion file paths in their routing sections to help the model find the right deep content
- The advisor rewrite is the most impactful change — goes from 363 lines to ~50 lines
## Approach

1. **Rewrite dotnet-advisor**: Replace 363-line routing catalog (21 categories, 131 skills) with ~20 consolidated skills. Dramatically simpler decision tree.
2. **Update agent preloaded skills**: Each agent's `## Preloaded Skills` section lists `[skill:old-name]` refs. Replace with `[skill:new-name]`. Example: `dotnet-testing-specialist` changes from 5 individual skill refs to `[skill:dotnet-testing]`.
3. **Update agent routing tables**: Inline `[skill:]` references in Knowledge Sources, Explicit Boundaries, Routing Tables.
4. **Update hooks**: Both hook scripts reference `[skill:dotnet-advisor]` — this name survives, but verify no other skill refs in hooks.
5. **Verify `STRICT_REFS=1` passes**: All `[skill:name]` refs must resolve to actual skill directory names.

## Key context

- 14 agents at `agents/*.md`: dotnet-architect, dotnet-aspnetcore-specialist, dotnet-async-performance-specialist, dotnet-benchmark-designer, dotnet-blazor-specialist, dotnet-cloud-specialist, dotnet-code-review-agent, dotnet-csharp-async-patterns (wait — check this is an agent not skill), dotnet-csharp-concurrency-specialist, dotnet-maui-specialist, dotnet-performance-analyst, dotnet-security-reviewer, dotnet-testing-specialist, dotnet-uno-specialist
- Each agent has Preloaded Skills, Knowledge Sources, Explicit Boundaries sections with `[skill:]` refs
- `dotnet-code-review-agent` alone references 15+ individual skill names
## Acceptance
- [ ] dotnet-advisor SKILL.md rewritten for 8 consolidated skills
- [ ] All 14 agent files updated with correct `[skill:new-name]` references
- [ ] No `[skill:old-name]` references remain anywhere in agents/ or skills/
- [ ] Hooks verified (dotnet-advisor name survives)
- [ ] `STRICT_REFS=1 ./scripts/validate-skills.sh` passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
