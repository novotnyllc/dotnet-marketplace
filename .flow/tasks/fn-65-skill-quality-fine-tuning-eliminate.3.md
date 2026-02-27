# fn-65-skill-quality-fine-tuning-eliminate.3 Slim advisor skill and regenerate similarity baseline

## Description
Slim the advisor skill by removing redundant routing logic, add a cross-domain playbooks section, and regenerate the similarity baseline after all description changes from Task 1.

**Size:** M
**Files:** `skills/dotnet-advisor/SKILL.md`, `scripts/similarity-baseline.json`

## Approach

### 1. Slim the advisor

The advisor currently has 5 sections that overlap with domain skills:
- **Skill Catalog** (L49-88, ~40 lines): Lists each skill's topics and key companion files — duplicates each skill's own Routing Table.
- **Routing Logic** (L92-219, ~127 lines): Exhaustive decision tree mapping specific topics to specific companion files within each domain skill — duplicates every domain skill's Routing Table.

**Keep:**
- Overview and role description (L1-22)
- Immediate Routing Actions (L24-47): The initial triage rules (these are unique to the advisor)
- Default Quality Rule (currently L221-230)
- First Step instructions (currently L232-238)
- Specialist Agent Routing (if present)
- The `[skill:]` cross-ref that loads `dotnet-csharp` as baseline dependency

**Replace Skill Catalog** with a lean 8-row table: `| Skill | Summary | Differentiator |`. No per-file detail, no `references/*.md` paths. Just enough for the model to route to the right skill.

**Remove Routing Logic** entirely. Each domain skill's own Routing Table handles topic-to-file mapping.

**Add "Cross-domain playbooks" section** (5-10 bullets) to preserve multi-skill routing recipes that currently live only in the Routing Logic. Name skills only, not reference files:
- "New API service: [skill:dotnet-tooling] + [skill:dotnet-api] + [skill:dotnet-devops] + [skill:dotnet-testing]"
- "Starting a new project: [skill:dotnet-tooling] + [skill:dotnet-csharp]"
- etc.

### 2. Fix advisor description if it has "Covers" filler

Check and fix if applicable, using the same style guide rules as Task 1.

### 3. Fix the OOS bullet missing `[skill:]` attribution

Line 23 of the current advisor has an OOS bullet without a `[skill:]` ref (flagged by validator as WARN). Add the appropriate cross-reference.

### 4. Regenerate similarity baseline

The similarity baseline is managed by `scripts/validate-similarity.py`, NOT `_validate_skills.py`. After Task 1's description changes and any advisor description changes:

1. Run similarity validation to see current state: `python3 scripts/validate-similarity.py`
2. If pairs changed, update `scripts/similarity-baseline.json` with the new pairs output
3. Verify the updated baseline passes: `python3 scripts/validate-similarity.py`

Read `scripts/validate-similarity.py` to understand the exact regeneration workflow before executing.

## Key context

- The advisor is always loaded first — it is the routing entry point. The lean catalog must still contain enough info for models and agents to discover skills through it.
- The advisor's Routing Logic currently handles cross-domain scenarios (e.g., mapping "Starting a New Project" to both `dotnet-tooling` and `dotnet-api`). The new "Cross-domain playbooks" section explicitly preserves these recipes.
- 14 agent files reference `[skill:dotnet-advisor]` in their Preloaded Skills. The lean catalog must still serve agent discovery.
- `scripts/validate-similarity.py` owns the baseline, not `_validate_skills.py`.

## Acceptance
- [ ] Advisor Routing Logic section removed entirely
- [ ] Advisor Skill Catalog is max 8 rows, no `references/*.md` paths anywhere in advisor
- [ ] Advisor has a "Cross-domain playbooks" section with 5-10 bullets naming skills only (no reference file paths)
- [ ] Cross-domain routing recipes from old Routing Logic preserved in playbooks section
- [ ] No "Covers" filler in advisor description
- [ ] OOS bullet has `[skill:]` attribution (zero validator warnings)
- [ ] `similarity-baseline.json` regenerated via `validate-similarity.py` workflow and committed
- [ ] `./scripts/validate-skills.sh` passes with zero warnings
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] `python3 scripts/validate-similarity.py` passes

## Done summary
Slimmed the advisor skill from 239 to 98 lines: removed 127-line Routing Logic section, replaced verbose Skill Catalog with lean 8-row table, added 9-bullet Cross-Domain Playbooks section preserving multi-skill routing recipes, fixed OOS attribution warning, and eliminated all references/*.md paths from the advisor. Similarity baseline verified correct (empty pairs, max score 0.0).
## Evidence
- Commits: 38b418a, 178ea42
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/validate-similarity.py --repo-root . --baseline scripts/similarity-baseline.json --suppressions scripts/similarity-suppressions.json
- PRs: