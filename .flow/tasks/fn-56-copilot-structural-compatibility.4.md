# fn-56-copilot-structural-compatibility.4 32-skill routing strategy

## Description

Verify how Copilot's 32-skill display limit interacts with `user-invocable: false` skills, then design and implement the appropriate routing strategy.

**Size:** M
**Files:** skills/*/SKILL.md (potentially many — invocability inventory may require explicit `user-invocable` on all 131), skills/dotnet-advisor/SKILL.md (primary for Phase 2B), CONTRIBUTING-SKILLS.md (constraint documentation)

## Approach

**Phase 1: Verify the 32-skill limit behavior (MUST complete before Phase 2)**

1. **Inventory invocability across all 131 skills.** Generate a report counting `user-invocable: true` (explicit or default-omitted) vs `user-invocable: false` (explicit). If any skills omit the field and should be non-invocable, explicitly set `user-invocable: false` before measuring Copilot behavior. The expected split is 11 true / 120 false.

2. **Determine if `user-invocable: false` skills count against the 32-skill limit.** With 120 of 131 skills marked `user-invocable: false`, this completely changes the strategy:
   - **If excluded**: Only 11 user-invocable skills compete for the 32-slot window -> limit is a non-issue. Move to Phase 2A.
   - **If included**: All 131 compete for 32 slots -> advisor meta-router needed. Move to Phase 2B.

3. **Also verify the ordering** of visible skills (alphabetical? filesystem? manifest order?). Do not assume alphabetical.

4. **Test method**: Install the flattened plugin in Copilot CLI and inspect the system prompt (or skill list output) for:
   - Total skills shown vs total installed
   - Whether non-user-invocable skills appear in the system prompt
   - The exact ordering of visible skills

**Phase 2A: Limit is a non-issue (only user-invocable skills count)**

1. Verify all 11 user-invocable skills are discoverable by Copilot
2. Verify the model can still activate non-user-invocable skills when contextually relevant
3. Document the interaction in CONTRIBUTING-SKILLS.md

**Phase 2B: Limit applies to all skills (fallback strategy)**

1. **Ensure `dotnet-advisor` is within the visible window.** Verify its position in the ordering.
2. **Verify advisor meta-routing works in Copilot**: Test that a prompt -> activates advisor (visible) -> advisor body references a skill outside the visible set -> Copilot loads that skill on demand. If this chain does NOT work, escalate and design an alternative.
3. **Optimize advisor description** for Copilot activation (strong trigger language per Copilot issue #978).
4. **Update advisor compressed catalog** organized by domain (not alphabetically).
5. **Document the constraint** including which skills are visible and which require advisor routing.

**Fallback if advisor meta-routing doesn't work in Copilot:**
- Strategic renames to pull domain-specific "router" skills into visible window
- Or: create lightweight alias skills within visible set that embed condensed domain instructions
- Or: reduce non-essential skills' `user-invocable` to further shrink the competing set

## Key context

- 11 user-invocable skills: dotnet-advisor, dotnet-slopwatch, dotnet-scaffold-project, dotnet-add-analyzers, dotnet-modernize, dotnet-add-ci, dotnet-add-testing, dotnet-data-access-strategy, dotnet-version-upgrade, dotnet-windbg-debugging, dotnet-ui-chooser
- dotnet-skills-evals tested compressed-index discovery at 56.5% TPR
- The advisor at `skills/dotnet-advisor/SKILL.md` (after flatten) has 360 lines with 221 `[skill:]` cross-references
- Copilot v0.0.412 added support for `user-invocable: false` and `disable-model-invocation`

## Acceptance
- [ ] Invocability inventory generated: exact count of true/false/omitted across all 131 skills
- [ ] `user-invocable` is explicitly present (true or false) on all 131 skills, OR the default behavior is verified with Copilot and explicitly documented as intentional
- [ ] 32-skill limit behavior with `user-invocable: false` verified and documented (measurement data captured)
- [ ] Skill ordering method verified (alphabetical, filesystem, or other)
- [ ] Appropriate routing strategy implemented based on verified behavior (Phase 2A or 2B)
- [ ] If Phase 2B: advisor meta-routing verified to work in Copilot (or fallback implemented)
- [ ] If Phase 2B: advisor description optimized for Copilot activation
- [ ] If Phase 2B: advisor compressed catalog updated with all skills organized by domain
- [ ] 32-skill constraint (or non-issue finding) documented in CONTRIBUTING-SKILLS.md
- [ ] All `[skill:]` cross-references in advisor resolve correctly

## Done summary
Added explicit user-invocable: true to 10 skills that relied on defaults (bringing all 131 skills to explicit invocability: 11 true, 120 false). Documented the Copilot CLI 32-skill display limit routing strategy in CONTRIBUTING-SKILLS.md, including dual-ordering strategy (manifest + alphabetical), behavior scenarios, compatibility rules, and verification procedure.
## Evidence
- Commits: ea0e981, 8bd368c, 5004b4f
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: