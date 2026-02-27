# fn-65-skill-quality-fine-tuning-eliminate.1 Restructure domain SKILL.md files: eliminate triple redundancy and fix descriptions

## Description
Restructure all 7 domain SKILL.md files (dotnet-api, dotnet-csharp, dotnet-debugging, dotnet-devops, dotnet-testing, dotnet-tooling, dotnet-ui) to eliminate the triple redundancy between Routing Table, Scope, and Companion Files sections.

**Size:** M
**Files:** `skills/dotnet-api/SKILL.md`, `skills/dotnet-csharp/SKILL.md`, `skills/dotnet-debugging/SKILL.md`, `skills/dotnet-devops/SKILL.md`, `skills/dotnet-testing/SKILL.md`, `skills/dotnet-tooling/SKILL.md`, `skills/dotnet-ui/SKILL.md`

## Approach

For each of the 7 domain SKILL.md files:

1. **Merge Routing Table + Companion Files** into a single enhanced Routing Table with 4 columns: `| Topic | Keywords | Description | Companion File |`. The Description column absorbs the one-line descriptions from the old Companion Files section. Then delete the `## Companion Files` section entirely.

2. **Trim `## Scope`** to 6-10 high-level domain category bullets. Currently Scope echoes per-file topics from the Routing Table. Instead, use broad groupings (e.g., for dotnet-api: "ASP.NET Core web APIs (minimal and controller-based)", "API versioning, OpenAPI, and documentation", "Security, authentication, and input validation"). Do NOT list every reference file topic.

3. **Preserve `## Out of scope` intent and `[skill:]` cross-refs.** Do not copy OOS verbatim — review each bullet after the merge to ensure boundaries remain crisp. If a Companion Files removal makes an OOS bullet vague, tighten the wording. All `[skill:]` attributions must remain.

4. **Fix "Covers" filler** in all skill descriptions flagged by the validator's filler-phrase detection. Rewrite using the Action + Domain + Differentiator formula per `docs/skill-routing-style-guide.md`. Keep budget-neutral.

5. **Note:** `dotnet-debugging` has a different structure (no formal Routing Table, uses Diagnostic Workflow sections). Adapt the same principle: ensure no duplicate file listings, add a lean Routing Table, remove the Companion Files section.

## Key context

- The Companion Files section and Routing Table carry the same information in different formats. Example from `dotnet-api/SKILL.md`: Routing Table row `| Minimal APIs | endpoint, route group, filter, TypedResults | references/minimal-apis.md |` vs Companion Files bullet `- references/minimal-apis.md -- Minimal API route groups, filters, TypedResults, OpenAPI`.
- Current total description chars: 2584 of 15600 budget (17% used). Plenty of room.
- The "Overview" paragraphs with "Baseline dependency" and "Most-shared companion" guidance (lines 14-16 in most skills) should be preserved — these are unique loading hints.
- 5 skills with "Covers" filler: check `scripts/_validate_skills.py` line 94-100 for the exact filler patterns.

## Acceptance
- [ ] Each domain SKILL.md has exactly ONE Routing Table (4 columns: Topic, Keywords, Description, Companion File)
- [ ] No `## Companion Files` section exists in any SKILL.md
- [ ] `## Scope` has 6-10 high-level bullets per skill (not per-file echoes)
- [ ] `## Out of scope` preserves intent and all `[skill:]` cross-refs (small edits allowed for clarity after merge)
- [ ] Zero "Covers" filler phrases in any description (validator produces 0 filler warnings)
- [ ] Overview paragraphs with baseline dependency / most-shared companion guidance preserved
- [ ] `./scripts/validate-skills.sh` passes
- [ ] Total description chars remain under 15600 budget

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
