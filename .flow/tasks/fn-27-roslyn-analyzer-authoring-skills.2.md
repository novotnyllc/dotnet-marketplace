# fn-27-roslyn-analyzer-authoring-skills.2 Register skill, update advisor catalog, and validate

## Description
Register the `dotnet-roslyn-analyzers` skill in plugin.json, add it to the dotnet-advisor catalog and routing logic, and run validation.

**Size:** S (combined with integration work to reach M)
**Files:**
- `.claude-plugin/plugin.json` (modify — add skill path)
- `skills/foundation/dotnet-advisor/SKILL.md` (modify — add catalog entry + routing)

## Approach
- Add `"skills/core-csharp/dotnet-roslyn-analyzers"` to plugin.json skills array
- Add catalog entry under category "2. Core C# & Language Patterns" in dotnet-advisor SKILL.md: `- [skill:dotnet-roslyn-analyzers] -- custom DiagnosticAnalyzer, CodeFixProvider, testing, NuGet packaging`
- Add routing entry under "### Writing or Modifying C# Code" section: `- Custom analyzers/code fixes -> [skill:dotnet-roslyn-analyzers]`
- Run `./scripts/validate-skills.sh` and `./scripts/validate-marketplace.sh`
- Verify skill name uniqueness repo-wide: `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` (expect empty)

**Note on shared files:** This task modifies `.claude-plugin/plugin.json` and `skills/foundation/dotnet-advisor/SKILL.md`, which are also modified by fn-11 tasks. If fn-11 tasks have already run, this task adds to their changes. Execute non-concurrently with fn-11 integration edits.

## Key context
- Follow convention at `skills/foundation/dotnet-advisor/SKILL.md` lines 24-41 for catalog entry format
- Follow routing convention at lines 173-180 for routing entry format
- Pitfall from memory: always register skills in plugin.json — files on disk without registration are invisible
- Pitfall from memory: cross-reference skill IDs must use canonical names — verify with grep against actual name: field

## Acceptance
- [ ] `"skills/core-csharp/dotnet-roslyn-analyzers"` added to plugin.json skills array
- [ ] Catalog entry added to dotnet-advisor under category 2 with `[skill:dotnet-roslyn-analyzers]` syntax
- [ ] Routing entry added to dotnet-advisor routing logic section
- [ ] `./scripts/validate-skills.sh` passes (BUDGET_STATUS=OK)
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] Skill name uniqueness verified repo-wide (no duplicates)
- [ ] No duplicate skill descriptions across dotnet-advisor catalog

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
