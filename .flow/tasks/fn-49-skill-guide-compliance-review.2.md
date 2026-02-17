# fn-49-skill-guide-compliance-review.2 Optimize skill descriptions for routing quality and budget compliance

## Description
Apply fixes to all non-compliant skill front matter identified in Task 1's audit. Optimize descriptions for maximum routing effectiveness while reducing total budget below the WARN threshold.

**Size:** M
**Files:** All 127 `skills/**/SKILL.md` files (WHEN removal is systemic; 16 skills also need disambiguation rewording)

## Approach

1. Read Task 1 findings report at `.flow/reports/fn-49.1-compliance-audit.md`
2. **Priority 1 — Remove WHEN prefix from all 127 skills** (systemic, saves 630 budget chars; audit concluded NONE add routing value). Capitalize the new first word after removal. Include `plugin-self-publish` for consistency even though it is budget-excluded.
3. **Priority 2 — Disambiguate 8 overlapping pairs** (16 skills, findings M-1 through M-7 and M-9). Apply suggested rewording from the audit report, then apply WHEN removal on top (audit suggestions still show WHEN for readability).
4. **Priority 3 — Remove filler word** from `dotnet-csharp-async-patterns` (finding M-8: remove "Covers", saves 7 chars)
5. Run `./scripts/validate-skills.sh` after each batch to track budget progress
6. Target total budget ≤11,800 chars (current baseline is 12,417; projected after all fixes ~11,730)

### Optimization Strategies

- **Remove WHEN prefix unconditionally**: Strip `WHEN ` (5 chars) from all 127 descriptions and capitalize the next word. The audit confirmed WHEN provides zero disambiguation signal since every skill uses it uniformly.
- **Disambiguate overlapping pairs**: Apply the audit's suggested descriptions for findings M-1 through M-7 and M-9 (8 pairs, 16 skills). Each suggestion sharpens the unique differentiator between the pair.
- **Remove filler verbs**: Drop "Covers" from `dotnet-csharp-async-patterns` (M-8). Check for other filler during editing but the audit found only this one instance.
- **Sharpen triggers**: Replace vague verbs with specific ones ("Configure X" vs "Work with X") where encountered
- **Add keywords**: Include framework/technology names that Claude needs for routing where missing
- **Trim redundancy**: If the skill name already conveys the domain, don't repeat it in description

### Key context

- Edit only the `name` and `description` fields in SKILL.md front matter — do not modify body content
- The `name` field must match the skill directory name (e.g., `skills/core-csharp/dotnet-csharp-records/` → `name: dotnet-csharp-records`)
- Remove any extra frontmatter fields beyond `name` and `description`
- Description max: 120 chars per skill; total budget target: ≤11,800 chars
- Run `./scripts/validate-skills.sh` to verify — must show BUDGET_STATUS=OK
- Pattern reference: `CONTRIBUTING-SKILLS.md:107-148` for description formula
- `plugin-self-publish` has `disable-model-invocation: true` — excluded from budget calculation
## Acceptance
<!-- Updated by plan-sync: fn-49.1 produced 0 critical findings, 9 major, 1 systemic minor; audit report at .flow/reports/fn-49.1-compliance-audit.md; baseline budget is 12,417 not 12,038; all 127 skills need WHEN removal -->
- [ ] All critical findings from Task 1 audit fixed (Task 1 found 0 critical — this is a no-op confirmation)
- [ ] All major findings from Task 1 audit fixed
- [ ] Minor findings addressed where practical
- [ ] Total description budget ≤11,800 chars
- [ ] Zero skills with descriptions >120 chars
- [ ] All `name` fields match their directory path
- [ ] No extra frontmatter fields (only `name` and `description`)
- [ ] Third-person voice used consistently
- [ ] Overlapping skill pairs have clearly disambiguated descriptions
- [ ] `./scripts/validate-skills.sh` passes with BUDGET_STATUS=OK
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] No SKILL.md body content changed (front matter only)
## Done summary
Optimized all 127 skill descriptions: removed WHEN prefix systemically, disambiguated 8 overlapping pairs (M-1 through M-7, M-9), removed filler word (M-8), and trimmed 12 longest descriptions. Budget reduced from 12,515 to 11,774 chars (below 11,800 target).
## Evidence
- Commits: f19dbd48ebcfdff2b75fb015a25dcddfb4635bdf
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: