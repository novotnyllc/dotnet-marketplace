# fn-49-skill-guide-compliance-review.1 Build compliance rubric and audit all 122 skill front matter

## Description
Build a quality rubric for skill front matter and audit all 122 skills against it. Produce a categorized findings report that Task 2 will use as the fix list.

**Size:** M
**Files:** All `skills/**/SKILL.md` (122 files, read-only), output report in task spec

## Approach

1. Read every `skills/**/SKILL.md` front matter block (name, description fields)
2. Score each skill against the rubric dimensions (see below)
3. Categorize findings by severity: critical (budget/structural), major (routing quality), minor (style)
4. Record findings as a structured table in the task completion notes

### Rubric Dimensions

| # | Dimension | Check | Severity |
|---|-----------|-------|----------|
| 1 | Budget compliance | Description ≤120 chars | Critical |
| 2 | Name-directory match | `name` field matches directory path under `skills/` | Critical |
| 3 | Extra frontmatter fields | Only `name` and `description` present (no stale fields) | Major |
| 4 | Trigger specificity | Description contains clear activation trigger (technology + action) | Major |
| 5 | Keyword density | No filler words ("helps with", "guide to", "complete guide") | Major |
| 6 | Disambiguation | Description distinct from all sibling skills in same category | Major |
| 7 | Third-person voice | No "I", "you", "your" — uses third-person ("Detects...", "Configures...") | Minor |
| 8 | WHEN prefix evaluation | If present, does "WHEN" add routing value or just waste 5 chars? | Minor |

### Key context

- Current budget: 12,038 chars (WARN threshold 12,000, FAIL at 15,000)
- All 122 skills currently use the "WHEN" prefix pattern — evaluate whether each benefits from it
- `disable-model-invocation: true` removes a skill from budget; only `plugin-self-publish` uses it currently
- Description is the **sole routing signal** — Claude reads all descriptions at startup and uses language understanding to pick which to invoke
- Validator at `scripts/_validate_skills.py` already checks: frontmatter exists, name+description present, desc length >120 warning, cross-refs, budget tracking
- Validator does NOT check: name-directory match, extra fields, WHEN pattern, body structure
- Skill directories are organized by category under `skills/` (24 categories, 122 skills)
- `CONTRIBUTING-SKILLS.md:107-148` documents the description formula
## Acceptance
- [ ] Quality rubric covers all 8 dimensions listed in the approach
- [ ] All 122 skills audited (every `skills/**/SKILL.md` read and scored)
- [ ] Findings categorized by severity (critical / major / minor)
- [ ] Each finding includes: skill name, category, dimension violated, current value, suggested fix
- [ ] Budget impact estimated (current 12,038 → target after fixes)
- [ ] Overlapping skill pairs identified with disambiguation recommendations
- [ ] Skills with extra frontmatter fields flagged
- [ ] Skills with name-directory mismatches flagged
- [ ] Report written as structured markdown in task completion notes
## Done summary
Audited all 127 SKILL.md front matter files against an 8-dimension quality rubric, producing a structured compliance report with 0 critical, 9 major, and 1 systemic minor finding. Key optimization: removing WHEN prefix from 126 active skills saves 630 budget chars, bringing total below WARN threshold.
## Evidence
- Commits: 1e7fac2, 5017a9f
- Tests: validate-skills.sh, validate-marketplace.sh
- PRs: