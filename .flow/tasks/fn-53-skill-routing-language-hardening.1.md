# fn-53-skill-routing-language-hardening.1 Baseline Audit and Ownership Manifest

## Description
Build a baseline inventory covering all 130 skills: description length, overlap risk score (pairwise textual similarity), cross-skill reference count/format, routing marker coverage (scope/out-of-scope/trigger sections), and routing hotspots from `tests/agent-routing/cases.json`. Produce an ownership manifest mapping each skill path to exactly one downstream editing task (T5-T10) with zero overlaps.

**Size:** M
**Files:**
- `docs/skill-routing-audit-baseline.md` (new)
- `docs/skill-routing-ownership-manifest.md` (new)
- Read-only: all `skills/**/SKILL.md`, `tests/agent-routing/cases.json`, `agents/*.md`

## Approach

- Script-driven audit: iterate all SKILL.md files, extract frontmatter descriptions, count `[skill:]` refs, check for `## Scope`, `## Out of scope`, `## Trigger` sections
- Compute preliminary pairwise textual overlap using simple word-set Jaccard (Jaccard on token sets with domain stopwords removed). This is a PRELIMINARY measure — T13 builds the production-quality multi-signal similarity script. T1 uses simple Jaccard to identify the top-N overlap hotspots for the audit report.
- Identify the exact set of skills with zero routing markers via automated scan (measured by the generated baseline report)
- Count bare-text references in `agents/*.md` files (measured by the generated baseline report)
- Ownership assignment: divide 130 skills into T5 (foundation + high-traffic), T6, T7, T8, T9, T10 (14 agent files). Exact counts per task documented in the manifest. Each skill path appears in exactly one task.

## Key context

- Budget is currently at 12,345 chars (WARN at 12,000). Record per-skill char counts for budget tracking during sweeps.
- Prior art: fn-29, fn-37 (cleanup sweep), fn-49 (compliance review), fn-51 (frontmatter) contain review rubrics and patterns. Reference relevant `.flow/specs/` entries but do not duplicate content.
- Memory pitfall: "Proposed replacement descriptions must have character counts verified" -- use consistent `echo -n | wc -c` measurement.
- T13 will build a proper multi-signal similarity script. T1 only needs simple Jaccard for the audit baseline to identify overlap hotspots.

## Ownership manifest format

Format: Markdown table with columns `| Skill Path | Category | Assigned Task | Notes |`. Sorted by assigned task then path. T5-T9 filter their batch by the Assigned Task column. T10 is always the 14 agent files.

## Acceptance
- [ ] `docs/skill-routing-audit-baseline.md` exists with data for all 130 skills
- [ ] Each skill entry includes: description length, overlap risk (top-3 most similar by Jaccard), cross-ref count, routing marker coverage (scope/out-of-scope/trigger: yes/no)
- [ ] `docs/skill-routing-ownership-manifest.md` maps every skill path to exactly one task (T5-T10) using the specified table format
- [ ] Zero overlaps in ownership (no skill path appears in two tasks)
- [ ] Agent file bare-text reference count documented per agent
- [ ] `./scripts/validate-skills.sh` still passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
