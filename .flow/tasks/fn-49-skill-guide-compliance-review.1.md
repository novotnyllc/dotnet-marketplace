# fn-49-skill-guide-compliance-review.1 Build compliance checklist from Anthropic skill guide and audit all skills

## Description
Download and read the Anthropic skill guide PDF. Extract a concrete compliance checklist. Audit all 122+ skills and 14 agents against it. Produce a categorized findings report.

**Size:** M
**Files:** None created — output is a findings list stored in this task spec as comments

## Approach

- Fetch https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- Extract key structural requirements: frontmatter, progressive disclosure, word count targets, trigger patterns, cross-references
- Compare against existing `CONTRIBUTING-SKILLS.md` conventions — note gaps
- Audit by category (batch the 22 categories, spot-check 2-3 skills per category, full audit for outliers)
- Classify findings: critical (blocking), warning (should fix), info (nice to have)

## Key context

- Guide published Jan 2026, after fn-29 fleet review completed
- Existing validation (`validate-skills.sh`) checks frontmatter but not content structure
- Body target: 1500-2000 words, max 5000
- Progressive disclosure: metadata (frontmatter) → body (structured sections) → references
## Acceptance
- [ ] Compliance checklist extracted from Anthropic skill guide
- [ ] All skill categories audited (spot-check + outlier review)
- [ ] All 14 agents audited for trigger patterns and preloaded skills
- [ ] Findings categorized as critical/warning/info
- [ ] Findings recorded in task spec for fn-49.2 consumption
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
