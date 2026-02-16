# fn-40-fleet-review-findings-implementation.1 Trim skill descriptions for budget compliance

## Description
Trim skill descriptions across all registered skills to bring the aggregate description budget below the 12,000-char WARN threshold. Also update the stale `--projected-skills` parameter and perform a quality check on the 14 skills added by fn-30 through fn-36.

**Size:** M
**Files:** All `skills/<category>/<skill-name>/SKILL.md` files (frontmatter only), `scripts/validate-skills.sh` (projected-skills parameter)

## Approach

1. **Precondition check:** Run `jq '.skills | length' .claude-plugin/plugin.json` to confirm the skill count. If count exceeds 113 (fn-38/fn-39 may have landed), re-derive the budget target before trimming.
2. Run `./scripts/validate-skills.sh` to get current baseline (CURRENT_DESC_CHARS, per-skill lengths, BUDGET_STATUS)
3. Sort descriptions by length descending -- trim the longest first for maximum impact
4. For each description needing trimming:
   - Remove filler words ("comprehensive", "common", "best practices for")
   - Remove redundant WHEN NOT clauses (Claude infers negatives from positive triggers)
   - Shorten trigger phrases while preserving domain-specific keywords
   - Target average ~106 chars/skill to stay below 12K
5. If budget cannot reach below 12K without degrading triggering quality, raise `--warn-threshold` in `validate-skills.sh` to at most 13,000 (not the fail threshold) with rationale documented in the commit message
6. Update `--projected-skills` in `validate-skills.sh` from 100 to the actual registered skill count
7. If fn-37 has not yet removed the internal budget comment in `dotnet-advisor/SKILL.md` (line 17, `<!-- Budget: PROJECTED_SKILLS_COUNT=100 -->`), update or remove it since it references a stale count
8. Run `validate-skills.sh` after every 10-15 edits for incremental verification
9. **Quality check for 14 new skills (fn-30-fn-36):** Scan both frontmatter (description follows `[What] + [When]` formula) and body content (`[skill:]` syntax for all cross-refs, zero bare-text skill names). If body-level quality issues are found beyond cross-ref syntax (e.g., missing Agent Gotchas, inconsistent structure), file them as follow-up issues rather than fixing them in this task.

## Key context

- Validator measures description length via Python `len()` after stripping YAML quotes -- use this as authoritative measurement, not `wc -c` (up to 2-char variance)
- Descriptions must remain double-quoted in frontmatter (all currently are)
- Don't introduce block scalars (`>` or `|`) -- validator handles them but they're non-standard for this project
- fn-37 modifies SKILL.md body content; this task modifies frontmatter only. Disjoint edits but same files -- fn-37 should complete first to avoid merge conflicts.
- fn-38/fn-39 may add skills concurrently. Start by checking actual count and budget rather than assuming 113 skills.
## Approach

1. **Precondition check:** Run `jq '.skills | length' .claude-plugin/plugin.json` to confirm the skill count. If count exceeds 113 (fn-38/fn-39 may have landed), re-derive the budget target before trimming.
2. Run `./scripts/validate-skills.sh` to get current baseline (CURRENT_DESC_CHARS, per-skill lengths, BUDGET_STATUS)
3. Sort descriptions by length descending -- trim the longest first for maximum impact
4. For each description needing trimming:
   - Remove filler words ("comprehensive", "common", "best practices for")
   - Remove redundant WHEN NOT clauses (Claude infers negatives from positive triggers)
   - Shorten trigger phrases while preserving domain-specific keywords
   - Target average ~106 chars/skill to stay below 12K
5. If budget cannot reach below 12K without degrading triggering quality, raise `--warn-threshold` in `validate-skills.sh` to at most 13,000 (not the fail threshold) with rationale documented in the commit message
6. Update `--projected-skills` in `validate-skills.sh` from 100 to the actual registered skill count
7. If fn-37 has not yet removed the internal budget comment in `dotnet-advisor/SKILL.md` (line 17, `<!-- Budget: PROJECTED_SKILLS_COUNT=100 -->`), update or remove it since it references a stale count
8. Run `validate-skills.sh` after every 10-15 edits for incremental verification
9. **Quality check for 14 new skills (fn-30-fn-36):** Scan both frontmatter (description follows `[What] + [When]` formula) and body content (`[skill:]` syntax for all cross-refs, zero bare-text skill names). If body-level quality issues are found beyond cross-ref syntax (e.g., missing Agent Gotchas, inconsistent structure), file them as follow-up issues rather than fixing them in this task.

## Key context

- Validator measures description length via Python `len()` after stripping YAML quotes -- use this as authoritative measurement, not `wc -c` (up to 2-char variance)
- Descriptions must remain double-quoted in frontmatter (all currently are)
- Don't introduce block scalars (`>` or `|`) -- validator handles them but they're non-standard for this project
- fn-37 modifies SKILL.md body content; this task modifies frontmatter only. Disjoint edits but same files -- fn-37 should complete first to avoid merge conflicts.
- fn-38/fn-39 may add skills concurrently. Start by checking actual count and budget rather than assuming 113 skills.
## Approach

1. Run `./scripts/validate-skills.sh` to get current baseline (CURRENT_DESC_CHARS, per-skill lengths)
2. Sort descriptions by length descending -- trim the longest first for maximum impact
3. For each description needing trimming:
   - Remove filler words ("comprehensive", "common", "best practices for")
   - Remove redundant WHEN NOT clauses (Claude infers negatives from positive triggers)
   - Shorten trigger phrases while preserving domain-specific keywords
   - Target average ~106 chars/skill (113 × 106 = 11,978, safely below 12K)
4. If budget cannot reach below 12K without degrading triggering quality, document the case for raising `--warn-threshold` to 13,000 in `validate-skills.sh` (L43-L47) with rationale that 113 skills > the original 100-skill calibration
5. Run `validate-skills.sh` after every 10-15 edits for incremental verification
6. For the 14 new skills (fn-30-fn-36): verify descriptions follow `[What] + [When]` formula per `CONTRIBUTING-SKILLS.md` L113, verify all cross-refs use `[skill:]` syntax

## Key context

- Validator measures description length via Python `len()` after stripping YAML quotes -- use this as authoritative measurement, not `wc -c` (up to 2-char variance)
- Descriptions must remain double-quoted in frontmatter (all 113 currently are)
- Don't introduce block scalars (`>` or `|`) -- validator handles them but they're non-standard for this project
- `[skill:name]` cross-refs inside descriptions are NOT common -- descriptions are short metadata, not prose. Cross-refs live in SKILL.md body.
- The `--projected-skills 100` parameter in validate-skills.sh was calibrated for the original skill count. With 113 skills, budget pressure is structural.
## Acceptance
- [ ] Aggregate CURRENT_DESC_CHARS below 12,000 in `validate-skills.sh` output OR `--warn-threshold` raised to at most 13,000 with rationale in commit message
- [ ] Zero individual descriptions over 120 chars (maintained from current state)
- [ ] `--projected-skills` in `validate-skills.sh` updated to match actual registered skill count
- [ ] All 14 skills from fn-30 through fn-36 verified: descriptions follow `[What] + [When]` formula
- [ ] All 14 skills from fn-30 through fn-36 verified: cross-refs use `[skill:]` syntax in both frontmatter and body (zero bare-text skill names)
- [ ] Body-level quality issues in new skills (if any) filed as follow-up, not blocking
- [ ] Stale `dotnet-advisor` budget comment removed or updated (if fn-37 hasn't handled it)
- [ ] `./scripts/validate-skills.sh` passes with zero errors
- [ ] `python3 scripts/generate_dist.py --strict` passes (cross-ref validation)
- [ ] No description trimming degrades triggering quality (reviewer judgment)
## Done summary
Trimmed 84 skill descriptions from 13,481 to 11,948 total chars (below 12,000 WARN threshold), updated --projected-skills from 100 to 121, and fixed 2 bare cross-refs in dotnet-library-api-compat to use [skill:] syntax. Quality-checked all 12 new skills from fn-30-fn-36: all follow [What]+[When] formula and use proper cross-ref syntax.
## Evidence
- Commits: 4c1812431e5227d21a1a27b637d8a91ccf0a2527
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: