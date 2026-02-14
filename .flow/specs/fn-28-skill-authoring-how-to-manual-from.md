# fn-28: Skill Authoring How-To Manual from Anthropic Guide

## Overview

Distill Anthropic's "The Complete Guide to Building Skills for Claude" (33-page PDF) into a concise, actionable how-to manual (`CONTRIBUTING-SKILLS.md`) tailored specifically to this repo's conventions. The manual should be the single reference a contributor needs to author, test, and ship a new skill in dotnet-artisan.

## Source Material

PDF: "The Complete Guide to Building Skills for Claude" by Anthropic (33 pages, 6 chapters)

### Key Concepts from the Guide (full distillation)

**Chapter 1 — Fundamentals:**
- A skill is a folder containing SKILL.md (required), scripts/, references/, assets/ (all optional)
- Progressive disclosure: 3 levels — YAML frontmatter (always in system prompt), SKILL.md body (loaded when relevant), linked files (loaded on demand)
- Composability: skills work alongside others, don't assume sole capability
- Portability: skills work across Claude.ai, Claude Code, and API
- MCP + Skills: MCP = connectivity (tools), Skills = knowledge (workflows)

**Chapter 2 — Planning and Design:**
- Start with 2-3 concrete use cases before writing
- Three use case categories: (1) Document/Asset Creation, (2) Workflow Automation, (3) MCP Enhancement
- Define success criteria: triggering accuracy (90% target), workflow efficiency (tool call count), reliability (0 failed API calls)
- File structure: kebab-case folder, SKILL.md (exact case), no README.md inside skill folder
- YAML frontmatter: `name` (kebab-case, matches folder), `description` (what + when + triggers, under 1024 chars)
- Optional fields: `license`, `compatibility`, `metadata` (author, version, mcp-server)
- Security: no XML angle brackets in frontmatter, no "claude"/"anthropic" in name
- Description formula: `[What it does] + [When to use it] + [Key capabilities]`
- Instructions structure: Steps > Examples > Troubleshooting
- Best practices: be specific/actionable, include error handling, reference bundled resources, use progressive disclosure

**Chapter 3 — Testing and Iteration:**
- Three testing levels: manual (Claude.ai), scripted (Claude Code), programmatic (skills API)
- Pro tip: iterate on single challenging task first, then extract into skill
- Test categories: (1) Triggering tests, (2) Functional tests, (3) Performance comparison
- skill-creator skill can generate, review, and iterate on skills
- Iteration signals: undertriggering (add more description keywords), overtriggering (add negative triggers, be more specific), execution issues (improve instructions, add error handling)

**Chapter 4 — Distribution and Sharing:**
- Upload to Claude.ai via Settings > Capabilities > Skills, or place in Claude Code skills directory
- Organization-level deployment available (Dec 2025)
- Agent Skills is an open standard (like MCP)
- API: /v1/skills endpoint, container.skills parameter, Claude Agent SDK
- Recommended: host on GitHub with README (repo-level, not inside skill), link from MCP docs

**Chapter 5 — Patterns and Troubleshooting:**
- Pattern 1: Sequential workflow orchestration (multi-step, ordered, with dependencies)
- Pattern 2: Multi-MCP coordination (workflows spanning multiple services)
- Pattern 3: Iterative refinement (quality improves with iteration loops)
- Pattern 4: Context-aware tool selection (same outcome, different tools per context)
- Pattern 5: Domain-specific intelligence (specialized knowledge beyond tool access)
- Troubleshooting: upload errors (SKILL.md casing), frontmatter issues (YAML formatting), triggering issues (description quality), MCP connection issues, instructions not followed (too verbose/buried/ambiguous)
- Advanced: bundle validation scripts for critical checks instead of relying on language instructions
- Keep SKILL.md under 5,000 words; move details to references/

**Chapter 6 — Resources:**
- Official: Best Practices Guide, Skills Documentation, API Reference, MCP Documentation
- Examples: github.com/anthropics/skills
- Tools: skill-creator skill, validation tooling

### dotnet-artisan Specific Conventions (overlay)

- Frontmatter: only `name` and `description` required (our convention is stricter than the guide's 1024 char limit — we target under 120 chars)
- Cross-reference syntax: `[skill:skill-name]`
- Total context budget: 15,000 chars (warn at 12,000)
- Validation: `validate-skills.sh`, `validate-marketplace.sh`, `generate_dist.py --strict`, `validate_cross_agent.py`
- Categories: 21 categories, 101 skills currently
- Agents: 9 specialist agents in agents/ directory
- Registration: new skills must be added to `.claude-plugin/plugin.json` skills array

## Scope

### Task 1: Create CONTRIBUTING-SKILLS.md How-To Manual

Write `CONTRIBUTING-SKILLS.md` that merges the Anthropic guide's best practices with dotnet-artisan repo conventions into a single actionable document.

**Structure:**
1. Quick Start (create a skill in 5 minutes)
2. Skill Anatomy (folder structure, SKILL.md, frontmatter)
3. Writing Effective Descriptions (formula, good/bad examples, budget constraints)
4. Writing Instructions (progressive disclosure, patterns, cross-references)
5. Testing Your Skill (triggering, functional, validation commands)
6. Common Patterns (the 5 patterns from the guide, adapted to .NET context)
7. Troubleshooting (from the guide + repo-specific issues)
8. Checklist (pre-commit checklist adapted from the guide's Reference A)

### Task 2: Update CONTRIBUTING.md to Reference Skills Guide

Add a section to the existing CONTRIBUTING.md that points contributors to the new CONTRIBUTING-SKILLS.md for skill-specific authoring guidance.

## Quick commands

- `./scripts/validate-skills.sh`
- `./scripts/validate-marketplace.sh`
- `python3 scripts/generate_dist.py --strict`
- `python3 scripts/validate_cross_agent.py`

## Acceptance

- [ ] `CONTRIBUTING-SKILLS.md` exists at repo root
- [ ] Covers all 6 chapters from the Anthropic guide
- [ ] Adapts examples to .NET/dotnet-artisan context
- [ ] Includes repo-specific validation commands and conventions
- [ ] References existing CONTRIBUTING.md for general contribution workflow
- [ ] Under 3,000 words (concise, actionable)
- [ ] CONTRIBUTING.md updated with cross-reference
- [ ] All four validation commands pass
- [ ] Manual is actionable enough for new contributors to author a skill from scratch

## References

- Source PDF: "The Complete Guide to Building Skills for Claude" by Anthropic
- CONTRIBUTING.md (existing contribution guide)
- CLAUDE.md (repo conventions)
- Agent Skills open standard: https://github.com/anthropics/agent-skills
