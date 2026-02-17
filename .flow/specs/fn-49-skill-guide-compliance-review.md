# fn-49 Skill Guide Compliance Review

## Overview

Audit all skills and agents against Anthropic's published "Complete Guide to Building Skills for Claude" (Jan 2026). Identify gaps in structure, content depth, progressive disclosure, and cross-referencing. Fix non-compliant skills and update validation.

**Dependencies:** Runs after fn-48 (documentation overhaul). All skills and docs should be up-to-date before auditing.

This is distinct from fn-29 (Fleet Skill Review, done) which was a quality sweep. This epic targets compliance with the Anthropic skill guide published after fn-29 completed.

## Scope

**In:** Audit all 132 skills against the Anthropic skill guide checklist. Audit all 14 agents. Fix structural/content issues. Update validation scripts if new checks are needed.

**Out:** Adding new skills (other epics handle that). Changing plugin architecture.

## Key Context

- Guide: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- Key guide recommendations: progressive disclosure (metadata→body→references), 1500-2000 word body target (max 5000), clear trigger patterns, cross-references, structured sections
- Existing validation (`validate-skills.sh`) checks frontmatter but not content structure
- Audit approach: download PDF, extract checklist into `docs/skill-compliance-checklist.md` (version-controlled, reusable). Store findings in `.flow/memory/compliance-findings.md`.

## Quick commands

```bash
./scripts/validate-skills.sh
```

## Acceptance

- [ ] Compliance checklist extracted from Anthropic skill guide and committed to `docs/skill-compliance-checklist.md`
- [ ] All skills audited against checklist (batch by category)
- [ ] All 14 agents audited for trigger patterns and preloaded skill lists
- [ ] Non-compliant skills fixed (structure, descriptions, cross-refs)
- [ ] Findings stored in `.flow/memory/compliance-findings.md`
- [ ] Validation scripts updated with any new structural checks
- [ ] All validation scripts pass after fixes
- [ ] If more than 30 skills need fixes, split into separate PRs: critical fixes first, then warnings

## References

- https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- `scripts/validate-skills.sh` (existing validation)
- `CONTRIBUTING-SKILLS.md` (current authoring guide)
- fn-29 spec (prior fleet review)
