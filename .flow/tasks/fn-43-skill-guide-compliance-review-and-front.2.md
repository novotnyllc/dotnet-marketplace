# fn-43-skill-guide-compliance-review-and-front.2 Optimize skill descriptions for routing quality and budget compliance

## Description
Apply fixes to all non-compliant skill front matter identified in Task 1's audit. Optimize descriptions for maximum routing effectiveness while reducing total budget below the WARN threshold.

**Size:** M
**Files:** All non-compliant `skills/**/SKILL.md` files (count depends on Task 1 findings)

## Approach

1. Read Task 1 findings report
2. Fix critical issues first (budget violations, name-directory mismatches, extra fields)
3. Optimize major issues (trigger specificity, keyword density, disambiguation)
4. Address minor issues (third-person voice, WHEN prefix evaluation)
5. Run `./scripts/validate-skills.sh` after each batch to track budget progress
6. Target total budget ≤11,800 chars (below 12K WARN with headroom for future skills)

### Optimization Strategies

- **Remove filler**: "WHEN writing" → context already implies when; "Helps with" → remove entirely
- **Sharpen triggers**: Replace vague verbs with specific ones ("Configure X" vs "Work with X")
- **Add keywords**: Include framework/technology names that Claude needs for routing
- **Disambiguate**: Where two skills overlap, make each description reference its unique differentiator
- **Trim redundancy**: If the skill name already conveys the domain, don't repeat it in description
- **Evaluate WHEN prefix**: Keep only where it adds routing value; drop where the technology trigger alone suffices

### Key context

- Edit only the `name` and `description` fields in SKILL.md front matter — do not modify body content
- The `name` field must match the skill directory name (e.g., `skills/core-csharp/dotnet-csharp-records/` → `name: dotnet-csharp-records`)
- Remove any extra frontmatter fields beyond `name` and `description`
- Description max: 120 chars per skill; total budget target: ≤11,800 chars
- Run `./scripts/validate-skills.sh` to verify — must show BUDGET_STATUS=OK
- Pattern reference: `CONTRIBUTING-SKILLS.md:107-148` for description formula
- `plugin-self-publish` has `disable-model-invocation: true` — excluded from budget calculation
## Acceptance
- [ ] All critical findings from Task 1 audit fixed
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
TBD

## Evidence
- Commits:
- Tests:
- PRs:
