# Skill Quality Fine-Tuning: Eliminate Redundancy and Normalize References

## Overview

After the fn-64 consolidation from 131 skills into 8 broad skills, the SKILL.md files and reference files have significant structural redundancy and inconsistencies that waste tokens and could degrade routing quality. This epic addresses three categories of issues:

1. **Triple redundancy in domain SKILL.md files** — Routing Table, Scope bullets, and Companion Files sections all describe the same set of topics. The advisor adds a 4th and 5th layer. ~80% of SKILL.md content is redundant.
2. **Reference file artifacts from standalone era** — 107 files still have `# dotnet-*` slug titles (old skill names), ~121 files have Scope/OOS sections with 372 stale `[skill:]` refs pointing to 63 deleted skill names.
3. **Stale documentation** — CONTRIBUTING-SKILLS.md describes `details.md` pattern (no skill uses it), style guide cites deleted skills, validator doesn't check reference files.

### Testing Context

No memory entries confirm tests were run during the fn-64 consolidation. The eval harness was deleted in fn-64. Only structural validators remain (`validate-skills.sh`, `validate-marketplace.sh`), and these don't check reference files at all. This epic includes extending the validator to prevent regressions.

### Design Decisions

Based on research of the Agent Skills specification, Anthropic best practices, and cross-repo examples:

- **Merge Routing Table + Companion Files** into a single enhanced Routing Table with a Description column. The Companion Files section is eliminated entirely — the Routing Table serves as the definitive file index.
- **Keep `## Scope`** as high-level domain categories (6-10 bullets), not per-file granularity. Keep `## Out of scope` with `[skill:]` cross-refs — preserve intent and cross-skill attributions but allow small edits to keep boundaries crisp after the routing-table merge.
- **Remove Scope/OOS from reference files.** These are holdovers from the standalone era. Removing them eliminates 372 stale `[skill:]` refs automatically and saves ~10-15 lines per file. The parent SKILL.md's Routing Table + Out of scope section provide sufficient boundary signals.
- **Handle `Cross-references:` lines**: Remove only the legacy `Cross-references:` lines that accompanied Scope/OOS blocks. Standalone cross-reference lines in modern-format files (e.g., `dotnet-csharp/references/coding-standards.md`) are kept as-is — they serve a useful navigation role.
- **Normalize reference titles** to human-readable Title Case format, preserving known acronyms (EF, MSBuild, gRPC, WinUI, MAUI, AOT, WPF, WinForms, TUI, LINQ, DI). For files with code fences before the H1 title, move the code fence below the H1 during cleanup.
- **Slim the advisor** by removing the per-topic exhaustive Routing Logic (127 lines) that duplicates every domain skill's routing table. Replace with a lean Skill Catalog (max 8 rows, no `references/*.md` paths) plus a small "Cross-domain playbooks" section (5-10 bullets naming skills only, not reference files) to preserve multi-skill routing recipes.
- **Extend the validator** to check reference files for: title existence (fence-aware H1 scanning), no stale `[skill:]` refs (fence-aware to avoid false positives in code examples). Reference `[skill:]` refs resolve against the same `known_ids` set used for SKILL.md (skills + agents), with a WARN for refs to agents in case the convention changes. Routing table file existence checks parse the `Companion File` column by header name, not position.
- **`[skill:]` syntax**: Used for both skills and agents. The `<id>` must match either a skill directory name or an agent file stem. This is an existing convention — document it explicitly in the style guide.

## Quick commands

```bash
# Validate after changes
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh

# Count redundancy reduction
wc -l skills/*/SKILL.md

# Quick check for stale refs (fence-naive, may flag agent refs — validator is authoritative)
# Checks for old 131-skill slug names like [skill:dotnet-minimal-apis]
grep -rn '\[skill:dotnet-[a-z]' skills/*/references/ | grep -v -E '\[skill:(dotnet-advisor|dotnet-api|dotnet-csharp|dotnet-debugging|dotnet-devops|dotnet-testing|dotnet-tooling|dotnet-ui)\]' | wc -l

# Verify no dotnet-* slug titles remain
grep -r '^# dotnet-' skills/*/references/*.md | wc -l
```

## Acceptance

- [ ] Each domain SKILL.md has a single Routing Table (no separate Companion Files section)
- [ ] Scope sections contain 6-10 high-level domain bullets (not per-file echoes)
- [ ] Out of scope sections preserve intent and `[skill:]` cross-refs (small edits allowed for clarity)
- [ ] No "Covers" filler phrase in any skill description
- [ ] All 145 reference file titles are human-readable Title Case (no `# dotnet-*` slugs, no missing titles)
- [ ] Title casing follows convention: Title Case, preserving known acronyms (EF, MSBuild, gRPC, WinUI, MAUI, AOT)
- [ ] Reference files have no `## Scope` or `## Out of scope` sections
- [ ] Legacy `Cross-references:` lines (accompanying Scope/OOS blocks) removed; modern standalone cross-ref lines preserved
- [ ] Zero stale `[skill:]` references across all reference files (resolves against skills + agents)
- [ ] Advisor has no `references/*.md` paths; Skill Catalog is max 8 rows; Routing Logic section removed
- [ ] Advisor has a "Cross-domain playbooks" section with 5-10 bullets naming skills only
- [ ] CONTRIBUTING-SKILLS.md uses `references/` pattern (no `details.md` references)
- [ ] Style guide cites only current 8-skill names in examples
- [ ] Style guide explicitly documents that `[skill:]` is used for both skills and agents
- [ ] Validator checks reference files (fence-aware H1 title, fence-aware stale cross-refs, routing table file existence by column name)
- [ ] `validate-skills.sh && validate-marketplace.sh` passes
- [ ] similarity-baseline.json regenerated via `validate-similarity.py` workflow

## Task Landing Order

Tasks 1 and 2 are parallel (disjoint files). Task 3 depends on Task 1. Task 4 depends on all three.

Recommended landing order: Task 2 first (bulk reference cleanup, largest diff), then Task 1 (SKILL.md restructure), then Task 3 (advisor + baseline), then Task 4 (validator + docs last, encodes final conventions).

## References

- Agent Skills Specification: https://agentskills.io/specification
- Anthropic Best Practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Validation script: `scripts/_validate_skills.py`
- Similarity validation: `scripts/validate-similarity.py`
- Style guide: `docs/skill-routing-style-guide.md`
- Skill authoring guide: `CONTRIBUTING-SKILLS.md`
- Prior consolidation: fn-64 (all 8 tasks done)
