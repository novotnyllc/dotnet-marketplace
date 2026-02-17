# Skill Guide Compliance Review and Front Matter Optimization

## Overview

Audit all 122 skill SKILL.md front matter fields for routing quality and budget compliance, then optimize descriptions to improve Claude's skill-selection accuracy while reducing the total description budget below the WARN threshold (currently 12,038 chars, WARN at 12,000).

The `description` field is Claude's **sole routing signal** — it reads all descriptions at session start and uses language understanding to choose which skill to invoke. This epic focuses on making every character count: removing filler, sharpening triggers, disambiguating overlapping skills, and ensuring keyword density serves routing.

**All work ships in a single branch — no separate PRs.**

## Scope

**In scope:**
- Quality audit of all 122 skill `name` and `description` front matter fields
- Description optimization for routing effectiveness (trigger specificity, keyword density, filler removal, disambiguation)
- Budget reduction below WARN threshold (target ≤11,800 chars to leave headroom)
- Validation script enhancements to enforce quality standards going forward
- Name-directory consistency check
- Third-person voice compliance (per Anthropic best practices)

**Out of scope:**
- SKILL.md body content changes (focus is front matter only)
- Adding new skills
- Changes to plugin.json skill registration
- Documentation overhaul (separate epic fn-48)

## Approach

1. **Build a quality rubric** covering: trigger specificity, keyword density, filler words ("WHEN" prefix overhead, redundant phrases), disambiguation between overlapping skills, name-directory match, third-person voice, budget contribution
2. **Audit all 122 skills** against the rubric, categorizing issues by severity
3. **Fix descriptions** — optimize for routing quality while staying under budget
4. **Enhance validation** to prevent regression (name-directory match, description quality heuristics)

## Quality Dimensions for Descriptions

| Dimension | Good | Bad |
|-----------|------|-----|
| Trigger specificity | "Write unit tests for Akka.NET actors using TestKit" | "Testing stuff" |
| Keyword density | Every word aids routing | Filler like "helps with", "guide to" |
| Disambiguation | Distinct from all other descriptions | Overlaps with sibling skill |
| Budget efficiency | ≤120 chars, no wasted words | 140+ chars, redundant phrasing |
| Third-person voice | "Detects code smells..." | "I help you find..." |
| Name-directory match | `name: dotnet-csharp-records` in `core-csharp/dotnet-csharp-records/` | Mismatched name/path |

## Quick commands

```bash
# Run skill validation (budget + structure)
./scripts/validate-skills.sh

# Check current budget
./scripts/validate-skills.sh 2>&1 | grep CURRENT_DESC_CHARS

# Run marketplace validation
./scripts/validate-marketplace.sh
```

## Acceptance

- [ ] All 122 skills audited against quality rubric with findings documented
- [ ] Total description budget ≤11,800 chars (below WARN threshold with headroom)
- [ ] Zero skills with descriptions >120 chars
- [ ] All skill `name` fields match their directory path
- [ ] No filler phrases ("WHEN" prefix evaluated — keep if routing value > overhead cost)
- [ ] Overlapping skill pairs have clearly disambiguated descriptions
- [ ] Third-person voice used consistently across all descriptions
- [ ] `validate-skills.sh` passes with BUDGET_STATUS=OK
- [ ] Validation script checks name-directory consistency
- [ ] No regressions — all existing validation checks still pass

## References

- `CONTRIBUTING-SKILLS.md:107-148` — Description formula and budget math
- `scripts/_validate_skills.py` — Python validator (strict YAML subset parser)
- `scripts/validate-skills.sh` — Bash wrapper with thresholds
- `.claude-plugin/plugin.json` — 122 registered skill paths
- `CLAUDE.md` — Plugin conventions and frontmatter rules
- Anthropic Agent Skills Spec: name max 64 chars, description max 1024 chars
- Description is sole routing signal — progressive disclosure: metadata → body → resources
