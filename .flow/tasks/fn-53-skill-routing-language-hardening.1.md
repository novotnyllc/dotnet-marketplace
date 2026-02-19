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
- Compute pairwise textual overlap (Jaccard on token sets or simple substring matching -- no embeddings needed)
- Identify the 16 skills with zero routing markers: `dotnet-advisor`, `dotnet-csharp-coding-standards`, `dotnet-csharp-async-patterns`, `dotnet-csharp-dependency-injection`, `dotnet-project-analysis`, `dotnet-project-structure`, `dotnet-scaffold-project`, and 9 others
- Count bare-text references in `agents/*.md` files (currently ~50 across 8 agents)
- Ownership assignment: divide 130 skills into T5 (foundation + high-traffic ~16), T6 (~30), T7 (~25), T8 (~25), T9 (~30 long tail), T10 (14 agent files). Each skill path appears in exactly one task.

## Key context

- Budget is currently at 12,345 chars (WARN at 12,000). Record per-skill char counts for budget tracking during sweeps.
- Prior art: fn-29 `docs/fleet-review-rubric.md` has 11-dimension review rubric. Reference but do not duplicate.
- Memory pitfall: "Proposed replacement descriptions must have character counts verified" -- use consistent `echo -n | wc -c` measurement.
## Acceptance
- [ ] `docs/skill-routing-audit-baseline.md` exists with data for all 130 skills
- [ ] Each skill entry includes: description length, overlap risk (top-3 most similar), cross-ref count, routing marker coverage (scope/out-of-scope/trigger: yes/no)
- [ ] `docs/skill-routing-ownership-manifest.md` maps every skill path to exactly one task (T5-T10)
- [ ] Zero overlaps in ownership (no skill path appears in two tasks)
- [ ] Agent file bare-text reference count documented per agent
- [ ] `./scripts/validate-skills.sh` still passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
