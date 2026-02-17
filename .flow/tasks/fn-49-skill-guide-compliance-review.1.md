# fn-49-skill-guide-compliance-review.1 Build compliance checklist from Anthropic skill guide and audit all skills

## Description
Download the Anthropic skill guide PDF, extract a compliance checklist, and audit all 132 skills and 14 agents against it. Store checklist and findings in version-controlled files.

**Size:** M
**Files:** `docs/skill-compliance-checklist.md` (new), `.flow/memory/compliance-findings.md` (new)

## Approach

- Fetch https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- If URL fails: search for the guide on anthropic.com, use cached/local copy, or extract from CONTRIBUTING-SKILLS.md which already references it
- Extract key structural requirements into `docs/skill-compliance-checklist.md` (version-controlled, reusable)
- Audit by category (batch the 22 categories, spot-check 2-3 skills per category, full audit for outliers)
- Store findings in `.flow/memory/compliance-findings.md` with severity: critical/warning/info
- If more than 30 skills need fixes, note split recommendation for fn-49.2

## Key context

- Guide published Jan 2026, after fn-29 fleet review completed
- Key recommendations: progressive disclosure, 1500-2000 word body target (max 5000), trigger patterns, cross-references
- Existing validation checks frontmatter but not content structure
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
- [ ] Compliance checklist committed to `docs/skill-compliance-checklist.md`
- [ ] All 22 skill categories audited (spot-check + outlier review)
- [ ] All 14 agents audited for trigger patterns and preloaded skills
- [ ] Findings stored in `.flow/memory/compliance-findings.md` with severity tags
- [ ] Split recommendation noted if >30 skills need fixes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
