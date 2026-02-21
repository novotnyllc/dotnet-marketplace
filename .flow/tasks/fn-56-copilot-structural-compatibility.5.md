# fn-56-copilot-structural-compatibility.5 Update all documentation for flat layout

## Description

Update all documentation files that reference the nested `skills/<category>/<skill-name>/` directory layout to reflect the new flat `skills/<skill-name>/` structure. Update canonical skill count to 131 everywhere. Also update behavioral guidance that conflicts with Copilot compatibility (description quoting, similarity scoring).

**Size:** M
**Files:** AGENTS.md, CONTRIBUTING.md, CONTRIBUTING-SKILLS.md, README.md, docs/agent-routing-tests.md, .agents/openai.yaml, CHANGELOG.md

## Approach

1. **AGENTS.md** (and CLAUDE.md which @includes it): Update file structure diagram from `skills/<category>/<skill-name>/SKILL.md` to `skills/<skill-name>/SKILL.md`. Remove category count references. Update skill count to 131.
2. **CONTRIBUTING.md**: Update cross-provider verification section (L238-258). Update any path references. Add Copilot-specific notes if applicable.
3. **CONTRIBUTING-SKILLS.md**: Update skill authoring guide — directory creation instructions change from `skills/<category>/<name>/` to `skills/<name>/`. Update checklist items. Verify/preserve the 32-skill constraint docs already added by T4 at lines 108-147 (section "### Copilot CLI 32-Skill Display Limit") and the explicit `user-invocable` requirement at line 96; update any nested-path references within those sections if present. **Remove/replace "quote descriptions for YAML safety" guidance** (line 410) — Copilot requires unquoted descriptions. Update similarity scoring documentation to reflect removal of same-category boost (line 221 still references same-category boost and +0.15).
4. **README.md**: Update installation section to include Copilot. Update architecture diagram if it shows nested layout. Update skill count to 131.
5. **docs/agent-routing-tests.md**: Update Copilot source setup description (L22-32). Update evidence tier documentation (L93, L111) for current Copilot evidence patterns.
6. **`.agents/openai.yaml`**: Verify both `default_prompt` and `short_description` were updated in T1 (flat paths + skill count 131).
7. **CHANGELOG.md**: Add entries under `[Unreleased]` -> `### Added` for Copilot compatibility, flat layout, frontmatter migration.

## Key context

- AGENTS.md says `skills/<category>/<skill-name>/SKILL.md   # 130 skills across 22 categories` — update to `skills/<skill-name>/SKILL.md   # 131 skills`
- CONTRIBUTING-SKILLS.md has detailed directory creation instructions that assume category subdirectories
- docs/agent-routing-tests.md L93: "Copilot historically had weaker skill-load evidence for nested `dotnet-*` skills" — this is now resolved
- CHANGELOG.md uses Keep a Changelog format
- Skill count must be 131 everywhere (was inconsistently 130 in some places)

## Acceptance
- [ ] No documentation file references `skills/<category>/<skill-name>/` pattern (verified by multiple greps):
  - `grep -rn 'skills/[a-z-]*/[a-z-]*/' *.md docs/ CONTRIBUTING* README* AGENTS* CLAUDE*` returns zero matches
  - `grep -rn 'skills/.*/.*/SKILL.md' *.md docs/` returns zero matches
- [ ] AGENTS.md file structure diagram shows flat layout with count 131
- [ ] CONTRIBUTING-SKILLS.md skill creation instructions use flat layout
- [ ] CONTRIBUTING-SKILLS.md includes 32-skill constraint documentation (already added by T4 at lines 108-147; verify preserved and no stale nested-path refs within it)
- [ ] README.md mentions Copilot compatibility and skill count is 131
- [ ] docs/agent-routing-tests.md updated for current Copilot evidence patterns
- [ ] CHANGELOG.md has unreleased entries for Copilot compatibility changes
- [ ] `.agents/openai.yaml` `default_prompt` and `short_description` both reflect 131 + flat layout
- [ ] Canonical skill count (131) consistent across all docs
- [ ] CONTRIBUTING-SKILLS.md no longer advises quoting descriptions (replaced with unquoted guidance for Copilot compat)
- [ ] Similarity scoring documentation updated (no same-category boost)
- [ ] CONTRIBUTING-SKILLS.md similarity formula matches the code (no same-category boost, no category/same_category fields) and troubleshooting no longer recommends quoting descriptions

<!-- Updated by plan-sync: fn-56-copilot-structural-compatibility.4 already added 32-skill constraint docs to CONTRIBUTING-SKILLS.md (lines 108-147) and explicit user-invocable requirement (line 96); approach step 3 and acceptance criterion updated to verify/preserve rather than create -->
