# fn-53-skill-routing-language-hardening.5 Normalize Foundation and High-Traffic Skills

## Description
Apply canonical routing language (from T2 style guide) to the foundation skills and all high-traffic skills listed in `tests/agent-routing/cases.json`. Normalize AGENTS.md routing index. These are the most-routed skills and set the pattern for subsequent sweeps.

**Size:** M
**Files:**
- `skills/foundation/dotnet-advisor/SKILL.md` (edit)
- `skills/foundation/dotnet-version-detection/SKILL.md` (edit)
- `AGENTS.md` (edit -- routing index + delegation patterns table)
- ~14 additional skills referenced in `tests/agent-routing/cases.json` (edit)
- Read-only: `docs/skill-routing-ownership-manifest.md` (task list), `docs/skill-routing-style-guide.md` (rules)

## Approach

- Read ownership manifest to confirm which skills belong to this task (T5 batch only)
- Apply style guide rules: scope/out-of-scope sections, cross-ref format, description normalization
- For `dotnet-advisor`: add routing markers (currently zero markers), update specialist routing section to use `[skill:]` syntax instead of bold text
- For `AGENTS.md`: convert Agent Delegation Patterns table bare-text skill names to `[skill:]` syntax, normalize Scope Boundaries section
- Run `./scripts/validate-skills.sh` after each batch of changes
- Track budget delta: record before/after description char counts. Must stay budget-neutral.

## Key context

- `dotnet-advisor` is the central router. Its SKILL.md has specialist references using `**name**` bold format (lines 334-338). Convert to `[skill:]`.
- `AGENTS.md` delegation patterns table (lines 74-89) lists preloaded skills as bare comma-separated names. Convert.
- The 14 cases.json skills are the highest-traffic paths. Getting these right first ensures routing test reliability.
- Memory pitfall: "Cross-reference IDs must be canonical" -- verify each ref against actual `SKILL.md` name: fields.
## Acceptance
- [ ] Foundation skills (`dotnet-advisor`, `dotnet-version-detection`) have scope/out-of-scope sections and canonical descriptions
- [ ] `dotnet-advisor` specialist routing uses `[skill:]` syntax (no bold-text agent names)
- [ ] AGENTS.md routing index uses `[skill:]` syntax throughout
- [ ] All ~14 high-traffic skills from `cases.json` normalized per style guide
- [ ] All cross-references use canonical `[skill:]` syntax
- [ ] Budget delta documented: total chars before vs after. No increase.
- [ ] `./scripts/validate-skills.sh` passes
- [ ] Existing routing test cases still pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
