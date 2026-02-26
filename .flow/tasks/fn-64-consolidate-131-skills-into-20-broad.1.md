# fn-64-consolidate-131-skills-into-20-broad.1 Comprehensive skill audit and consolidation map

## Description
Read all 131 SKILL.md files and produce a definitive consolidation mapping: which skills merge into which consolidated skill, what content goes in SKILL.md vs references/ companion files, and where every unmapped skill lands.

**Size:** M
**Files:** All 131 `skills/*/SKILL.md` (read-only), task spec output

## Approach

1. Read every SKILL.md frontmatter + body (size, description, scope, key content areas)
2. Identify natural groupings by domain affinity, cross-reference patterns, and agent preloaded skills
3. For each proposed consolidated skill, list:
   - Source skills being merged
   - What goes in SKILL.md overview (~2-5KB target)
   - What goes in `references/<topic>.md` companion files
   - Routing description (under 400 chars)
4. Resolve all unmapped skills identified in gap analysis (~37 skills)
5. Decide: dotnet-advisor routing catalog rewrite scope
6. Decide: framework-specific testing skills placement (UI group vs testing group)
7. Document companion file naming convention (`references/<topic>.md`)

## Key context

- Gap analysis identified 37 unmapped skills including: dotnet-advisor, dotnet-aspire-patterns, dotnet-semantic-kernel, dotnet-localization, dotnet-messaging-patterns, dotnet-domain-modeling, dotnet-background-services, framework-testing skills, agent meta-skills
- Only SKILL.md auto-loads on activation; companion files need explicit model reads
- SKILL.md must include ToC directing model to companion files
- Target: ~20 consolidated skills, each under 400 chars description
- Existing companion files: 2 details.md, 10 examples.md, 1 reference/ dir with 16 files — all must migrate
## Acceptance
- [ ] Every one of the 131 current skills has an explicit destination (merged into X, or dropped with rationale)
- [ ] Each consolidated skill has: name, description (<400 chars), source skills list, SKILL.md content outline, references/ file list
- [ ] Framework-testing placement decided with rationale
- [ ] dotnet-advisor fate decided (rewrite scope documented)
- [ ] Companion file naming convention documented
- [ ] Target consolidated skill count finalized (expect ~20)
- [ ] No skill left unmapped
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
