## Description
Create the `dotnet-advisor` router/index skill that serves as the always-loaded entry point for the plugin. This skill must contain a compressed catalog of ALL 19 planned skill categories (with implemented/planned status markers) and route agents to the right specialist skills based on context.

**Size:** M
**Files:**
- `skills/foundation/dotnet-advisor/SKILL.md`

## Approach

1. Use `/plugin-dev:skill-development` to understand SKILL.md frontmatter requirements
2. Write frontmatter with required fields: `name`, `description` (canonical set from epic)
3. Write precise trigger description: triggers on ANY .NET development query
4. Use WHEN + WHEN NOT pattern in description for reliable auto-triggering
5. Body contains compressed skill catalog with ALL 19 categories as explicit stubs:
   - Each category has status marker: `implemented` or `planned`
   - ~50 chars per skill entry
   - Foundation skills marked as `implemented`, Wave 1-3 skills marked as `planned`
6. Routing logic: "if doing X, load skills Y and Z" for each major scenario
7. Include version detection trigger: "first, check what .NET version via [skill:dotnet-version-detection]"
8. Use `[skill:name]` cross-reference syntax throughout
9. **CRITICAL**: Validate budget thresholds:
   - Router description: <500 chars, target <120 chars
   - Budget constants: PROJECTED_SKILLS_COUNT=95, MAX_DESC_CHARS=120
   - Projected max: 95 x 120 = 11,400 (under 12,000 warn threshold)
   - WARN at 12,000, FAIL at 15,000

## Key context

- Combined all-skill descriptions: WARN at 12,000 chars, FAIL at 15,000 (hard platform limit)
- Router description should be <500 chars but highly specific to .NET triggers
- Router body is only loaded on invocation (progressive disclosure) so can be larger
- All 19 categories MUST appear as stubs even if skills are not yet implemented
- Use `[skill:skill-name]` for all cross-references (machine-parseable, validated in CI)
- Use `/plugin-dev:skill-reviewer` to validate description triggering effectiveness
- Required frontmatter: `name`, `description` (canonical set from epic spec)

## Acceptance
- [ ] SKILL.md has valid frontmatter (name, description)
- [ ] Description triggers on .NET-related queries (test with: "create API", "add tests", "fix async")
- [ ] Description does NOT trigger on non-.NET queries
- [ ] Body contains compressed catalog of all 19 planned skill categories with status markers
- [ ] Routing logic covers all 19 spec categories
- [ ] Cross-references use `[skill:name]` syntax
- [ ] Cross-references version detection as first step
- [ ] Router description under 500 chars
- [ ] Projected budget math validated: 95 x 120 = 11,400 (under 12,000 warn)
- [ ] `/plugin-dev:skill-reviewer` rates description as effective for triggering

## Done summary

## Evidence
