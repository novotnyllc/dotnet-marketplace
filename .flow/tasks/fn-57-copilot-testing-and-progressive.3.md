# fn-57-copilot-testing-and-progressive.3 Progressive disclosure for oversized skills

## Description

Refactor all oversized skills (>500 lines) into progressive disclosure format: core SKILL.md (<500 lines) plus sibling reference files. Per dotnet-skills-evals data, truncation actually improved results for oversized skills — extra content was "actively confusing" the model.

**Size:** M (repetitive pattern across 11+ skills)
**Files:** skills/dotnet-mermaid-diagrams/, skills/dotnet-grpc/, skills/dotnet-roslyn-analyzers/, skills/dotnet-terminal-gui/, skills/dotnet-observability/, skills/dotnet-system-commandline/, skills/dotnet-xml-docs/, skills/dotnet-ado-patterns/, skills/dotnet-maui-development/, skills/dotnet-architecture-patterns/, skills/dotnet-msbuild-tasks/ (and any others >500 lines)

## Approach

For each oversized skill:

1. **Identify content tiers**:
   - **Core** (SKILL.md): Problem space, key patterns, routing rules, scope/OOS, essential gotchas — must stay under 500 lines
   - **Examples** (examples.md): Detailed code examples, before/after patterns
   - **Reference** (reference.md): API reference, configuration options, complete parameter lists
   - **Common mistakes** (common-mistakes.md): Anti-patterns, debugging tips, migration gotchas

2. **Extract to sibling files**: Move detailed content from SKILL.md into appropriate sibling files. Use **normal file references** (NOT `[skill:]` syntax — that is ONLY for referencing other skills/agents by ID). Example:
   ```markdown
   For detailed examples, see `examples.md` in this skill directory.
   For API reference, see `reference.md`.
   ```
   How platforms access sibling files:
   - Claude Code: Read tool loads sibling files on demand
   - Copilot: Model can request files via tool when SKILL.md body references them

3. **Preserve `[skill:]` cross-references**: Any `[skill:]` cross-references to OTHER SKILLS in extracted content must be preserved in the sibling files. `[skill:]` is ONLY for referencing other skills/agents by their ID.

4. **Verify line counts**: Each refactored SKILL.md must be under 500 lines.

**Priority order** (by size, most oversized first):
1. dotnet-mermaid-diagrams (874 lines)
2. dotnet-grpc (856 lines)
3. dotnet-roslyn-analyzers (770 lines)
4. dotnet-terminal-gui (754 lines)
5. dotnet-observability (739 lines)
6. dotnet-system-commandline (731 lines)
7. dotnet-xml-docs (687 lines)
8. dotnet-ado-patterns (682 lines)
9. dotnet-maui-development (674 lines)
10. dotnet-architecture-patterns (672 lines)
11. dotnet-msbuild-tasks (665 lines)

## Key context

- Agent Skills spec recommends SKILL.md under 500 lines with sibling files for overflow
- dotnet-skills-evals data: For akka-net-management (685 lines), truncation to 500 lines IMPROVED results
- The `dotnet-windbg-debugging` skill already uses a `reference/` directory with 16 files — this is the existing pattern
- Two skills already use `details.md` companion files (`dotnet-csharp-code-smells`, `dotnet-roslyn-analyzers`)
- Sibling file access in Copilot is verified by fn-57.1 smoke tests (progressive disclosure test cases)

## Acceptance
- [ ] All 11 identified skills have SKILL.md under 500 lines
- [ ] Each refactored skill has at least one sibling file (examples.md, reference.md, or common-mistakes.md)
- [ ] No content is lost — all extracted content exists in sibling files
- [ ] Core SKILL.md files retain routing essentials: scope, OOS, key patterns, cross-references to other skills
- [ ] Sibling files referenced via normal file paths (e.g., "See `examples.md`"), NOT via `[skill:]` syntax
- [ ] `[skill:]` cross-references to OTHER SKILLS preserved in both core and sibling files
- [ ] `./scripts/validate-skills.sh` passes after changes
- [ ] `find skills -name SKILL.md -exec sh -c 'lines=$(wc -l < "$1"); [ "$lines" -gt 500 ] && echo "$1: $lines"' _ {} \;` returns zero matches
- [ ] Sibling file naming follows existing convention (reference/, examples.md, details.md)
