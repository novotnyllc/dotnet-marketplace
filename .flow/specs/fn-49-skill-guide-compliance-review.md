# fn-49 Skill Guide Compliance Review

## Overview

Audit all skills and agents against Anthropic's published "Complete Guide to Building Skills for Claude" (Jan 2026). Identify gaps in structure, content depth, progressive disclosure, and cross-referencing. Produce a remediation plan and fix non-compliant skills.

This is distinct from fn-29 (Fleet Skill Review, done) which was a quality sweep. This epic specifically targets compliance with the Anthropic skill guide's recommendations.

## Scope

**In:** Audit all 122+ skills against the Anthropic skill guide checklist. Audit all 14 agents. Fix structural/content issues found. Update validation scripts if new checks are needed.

**Out:** Adding new skills (other epics handle that). Changing plugin architecture.

**Scope boundary with fn-29**: fn-29 was a general quality review (done). This epic is a targeted compliance check against the published Anthropic guide, which was released after fn-29 completed.

## Key Context

- Guide: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- Key guide recommendations: progressive disclosure (metadata→body→references), 1500-2000 word body target (max 5000), clear trigger patterns, cross-references, structured sections
- Existing validation (`validate-skills.sh`) checks frontmatter and naming but not content structure or depth
- This is a review+fix epic, not just a report — remediations are implemented

## Quick commands

```bash
./scripts/validate-skills.sh
```

## Acceptance

- [ ] Compliance audit checklist created from the Anthropic skill guide
- [ ] All skills audited against checklist (batch by category)
- [ ] Non-compliant skills fixed (structure, descriptions, cross-refs)
- [ ] Agents audited for trigger patterns and preloaded skill lists
- [ ] Validation scripts updated with any new structural checks
- [ ] All validation scripts pass after fixes

## References

- https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- `scripts/validate-skills.sh` (existing validation)
- `CONTRIBUTING-SKILLS.md` (current authoring guide)
- fn-29 spec (prior fleet review, for context on what was already fixed)
