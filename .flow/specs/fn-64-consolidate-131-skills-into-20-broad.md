# Consolidate 131 Skills into ~20 Broad Skills

## Overview

The plugin has 131 individual skills consuming 75% of the 15,600-char routing description budget. Research shows Tier 1 plugin repos converge on 5-16 skills. RAG-MCP research shows routing accuracy drops from 43% to 13% with many tools. This epic consolidates 131 skills into ~20 broad skills with companion files for depth, improving routing accuracy while preserving all content.

Each consolidated skill gets:
- **SKILL.md** (auto-loaded on activation): overview, routing table, scope/out-of-scope, ToC pointing to companion files (~2-5KB)
- **references/** directory: topic-named companion files with deep content from merged source skills (read on demand)

## Scope

- Consolidate all 131 skill directories into ~20 new skill directories
- Create companion `references/` files preserving all source skill content
- Rewrite `dotnet-advisor` routing catalog for ~20 skills
- Update all 14 agent preloaded skill references
- Update hooks, CI gates, validators
- Delete complex eval harness (`tests/evals/`) — replace with structural validators only
- Simplify copilot smoke tests for ~20 skills
- Update all documentation for new skill count

## Out of scope

- Redirect stubs for old skill names (no external consumers)
- New skill content (consolidation only, not enhancement)
- Agent restructuring (agents stay as-is, just update references)
- New eval framework (structural validators are sufficient)

## Key decisions

1. **dotnet-advisor survives** — hooks inject it as mandatory first action; rewrite routing catalog for ~20 skills
2. **Big-bang migration** — CI count gates (`EXPECTED=131`, `--projected-skills 131`) prevent incremental approach
3. **Framework testing → UI framework groups** — `dotnet-blazor-testing` → `dotnet-blazor`, etc. (agents preload what they need)
4. **Companion file convention** — `references/` directory with topic-named `.md` files (spec-standard pattern)
5. **SKILL.md includes explicit ToC** — directs model to read specific companion files on demand
6. **debugging stays standalone** — user requirement
7. **Delete eval harness, keep structural validators** — the 8,100-line Python eval harness (tests/evals/) never ran in CI, costs real money, and all data is keyed to old 131-skill names. Structural validators (`validate-skills.sh`, `validate-marketplace.sh`, `validate-similarity.py`) catch the top bug classes (broken cross-refs, name mismatches, budget overflow, near-duplicates) deterministically in <5 seconds. With ~20 skills, routing confusion drops dramatically (RAG-MCP research), making LLM-based activation evals low-value.

## Quick commands

```bash
# Validate after changes
STRICT_REFS=1 ./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Acceptance

- [ ] ~20 consolidated skill directories replace 131 individual directories
- [ ] All source skill content preserved in SKILL.md + references/ companion files
- [ ] All 14 agents updated with correct [skill:new-name] references
- [ ] dotnet-advisor rewritten for ~20 skills
- [ ] Hooks reference valid skill names
- [ ] CI gates updated (EXPECTED count, --projected-skills)
- [ ] `tests/evals/` directory deleted (eval harness removed)
- [ ] `validate-skills.sh && validate-marketplace.sh` both pass
- [ ] Similarity baseline regenerated for ~20 skills
- [ ] Copilot smoke tests remapped for ~20 skills
- [ ] Description budget under 50% (currently 75%)
- [ ] README.md, AGENTS.md, CONTRIBUTING-SKILLS.md updated with correct skill count

## Dependencies

- fn-56 (flat layout) — DONE, established current structure
- fn-51 (frontmatter schema) — DONE, all skills have proper frontmatter
- fn-53 (routing language) — DONE, descriptions follow Action+Domain+Differentiator
- fn-55 (invocation contracts) — DONE, user-invocable field on all skills
- fn-58/fn-60/fn-62/fn-63 (eval framework) — DONE, but eval harness being deleted as too complex; structural validators survive

## References

- Agent-skills spec: agentskills.io (only SKILL.md auto-loads; companion files need explicit reads)
- Research: BiasBusters (description wording > names), RAG-MCP (accuracy drops with many tools)
- Tier 1 repos: anthropics/skills (16), vercel-labs (6), kepano/obsidian (5)
- Companion file patterns: anthropics/skills PDF skill (reference.md, forms.md), Vercel rules/ with atomic files
- OpenAI eval-skills guide: deterministic checks catch most real bugs; LLM evals are research tools, not CI gates
- anthropics/claude-plugins-official: TypeScript frontmatter validator in CI — minimal, effective
- corca-ai/claude-plugins: bash test harness pattern (pass/fail/assert_eq) — lightweight smoke testing
