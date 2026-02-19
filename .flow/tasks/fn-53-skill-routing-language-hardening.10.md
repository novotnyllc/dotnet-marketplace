# fn-53-skill-routing-language-hardening.10 Agent File Normalization

## Description
Normalize all 14 agent files (`agents/*.md`) to use canonical `[skill:]` cross-reference syntax. Currently 8 of 14 agents use bare-text references (~50 total). Also normalize agent description conventions.

**Size:** M
**Files:**
- All 14 `agents/*.md` files (edit)
- Read-only: `docs/skill-routing-style-guide.md`

## Approach

- Convert all bare-text skill/agent references (backtick-wrapped, bold-wrapped) to `[skill:]` syntax
- Agents confirmed to have bare refs: `dotnet-testing-specialist` (7), `dotnet-code-review-agent` (9), `dotnet-performance-analyst` (11), and 5 others
- Agents already clean: `dotnet-architect`, `dotnet-blazor-specialist`, `dotnet-uno-specialist`, `dotnet-docs-generator`, `dotnet-security-reviewer`, `dotnet-maui-specialist`
- Normalize agent description fields per style guide (resolve WHEN-prefix usage in agent descriptions)
- Verify all `[skill:]` references in agent files resolve to existing skill directories

## Key context

- Agent files are NOT validated by `_validate_skills.py` currently. Cross-ref validation must be manual or a separate check.
- Memory pitfall: "Cross-reference IDs must be canonical" -- verify each ref against actual skill name: fields.
- 5 agent descriptions currently use `WHEN` prefix. Style guide (T2) must have decided the convention before this task runs.
## Acceptance
- [ ] All 14 agent files use `[skill:]` syntax for cross-references (zero bare-text refs)
- [ ] Agent descriptions follow style guide conventions
- [ ] All `[skill:]` references in agent files resolve to existing skill directories
- [ ] `./scripts/validate-skills.sh` passes (agents not validated by this, but skills must not regress)
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
