# fn-53-skill-routing-language-hardening.11 Content-Preservation Verification

## Description
Mandatory verification that all intended content remains represented after normalization across T5-T10. Produce a content migration map with source-section to destination-section mapping. Run automated checks for dropped sections, broken references, self-links (errors) and cycles (report), and semantic similarity improvement.

**Size:** M
**Files:**
- `docs/skill-content-migration-map.md` (new)
- Read-only: all `skills/**/SKILL.md`, `agents/*.md`, sweep reports from T6-T9

## Approach

- Diff each SKILL.md against its pre-normalization state (git diff against the branch point)
- Build migration map: for each modified skill, list sections before/after with content status (unchanged/reworded/moved/removed)
- Run the T3 validator to check all cross-references resolve
- Check for self-referential cross-links (skill referencing itself)
- Verify no section was dropped without being moved elsewhere
- Verify total description budget: `CURRENT_DESC_CHARS < 12,000` (strictly below WARN threshold)
- **Run T13 similarity check** and compare against pre-sweep baseline: verify WARN pair count decreased or stayed the same, and no new ERROR pairs were introduced. Document before/after similarity summary.

## Key context

- Memory pitfall: "Stale not-yet-landed references must be treated consistently" -- check for `planned` status markers that should now be `implemented`
- The `dotnet-advisor` catalog sections marked `planned`/`implemented` must be verified current
- This is the quality gate before docs/CI updates in T12
- T13's similarity baseline (`scripts/similarity-baseline.json`) provides the pre-sweep state. Re-run `python3 scripts/validate-similarity.py --repo-root .` and compare against this baseline.

## Acceptance
- [ ] `docs/skill-content-migration-map.md` covers all 130 skills with section-level before/after mapping
- [ ] Zero dropped sections without documented migration target
- [ ] Zero broken cross-references across skills and agents
- [ ] Zero self-referential cross-links
- [ ] `dotnet-advisor` catalog status markers are current
- [ ] Total description budget: `CURRENT_DESC_CHARS < 12,000` (strictly less than WARN threshold)
- [ ] Similarity improvement verified: WARN pair count <= pre-sweep baseline count. No new unsuppressed ERROR pairs.
- [ ] Updated `scripts/similarity-baseline.json` with post-sweep pair data
- [ ] Similarity runs in full skills+agents mode (144 items) — verifies T3+T13 integration (shared `_agent_frontmatter.py` + wiring)
- [ ] `./scripts/validate-skills.sh` passes with zero errors and zero new warnings vs baseline
- [ ] `./scripts/validate-marketplace.sh` passes
## Done summary
Created content migration map covering all 130 skills with section-level before/after mapping; updated 14 dotnet-advisor catalog markers (12 planned→implemented, 2 (none)→implemented); verified zero broken cross-references, zero self-referential links, description budget 11,595 < 12,000, and no similarity regression.
## Evidence
- Commits: fa8d844, d3f86ac, 6e1321b
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/validate-similarity.py --repo-root . --suppressions scripts/similarity-suppressions.json --baseline scripts/similarity-baseline.json
- PRs: