# fn-28-skill-authoring-how-to-manual-from.1 Create CONTRIBUTING-SKILLS.md how-to manual

## Description

Create `CONTRIBUTING-SKILLS.md` at the repo root. Merge Anthropic's "The Complete Guide to Building Skills for Claude" (all 6 chapters) with dotnet-artisan conventions into a single actionable how-to manual with 8 sections:

1. **Quick Start** — Create a skill in 5 minutes using `skills/core-csharp/dotnet-csharp-code-smells/` as the walkthrough example
2. **Skill Anatomy** — Folder structure (`skills/<category>/<skill-name>/SKILL.md`), SKILL.md format, frontmatter (`name`, `description`), optional companion files (`details.md` for extended content)
3. **Writing Effective Descriptions** — Formula (`[What] + [When] + [Triggers]`), good/bad examples, 120-char target, context budget math
4. **Writing Instructions** — Progressive disclosure (frontmatter → body → linked files), cross-reference syntax (`[skill:skill-name]`), patterns, 5,000-word SKILL.md limit
5. **Testing Your Skill** — Triggering tests, functional tests, all four validation commands with explanations
6. **Common Patterns** — The 5 patterns from the guide adapted to .NET context (sequential workflow, multi-MCP, iterative refinement, context-aware tool selection, domain-specific intelligence)
7. **Troubleshooting** — SKILL.md casing, YAML formatting, triggering issues, plus repo-specific issues (description budget, cross-reference resolution)
8. **Checklist** — Pre-commit checklist including: create folder, write SKILL.md with frontmatter, add to `plugin.json` skills array, run all four validation commands

Target under 3,000 words. Use progressive disclosure — link to external references (Anthropic guide, existing skills) rather than inlining everything.

## Acceptance

- [ ] `CONTRIBUTING-SKILLS.md` exists at repo root
- [ ] Contains all 8 sections listed above
- [ ] Covers content from all 6 Anthropic guide chapters
- [ ] Examples adapted to .NET/dotnet-artisan context (not generic)
- [ ] Documents `details.md` companion file convention
- [ ] Checklist includes plugin.json registration step
- [ ] Cross-references CONTRIBUTING.md for general contribution workflow
- [ ] Under 3,000 words total
- [ ] All four validation commands pass (regression guard — adding a new markdown file should not break anything)

## Files

- `CONTRIBUTING-SKILLS.md` (new)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
