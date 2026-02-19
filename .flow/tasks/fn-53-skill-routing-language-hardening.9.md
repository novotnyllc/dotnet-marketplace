# fn-53-skill-routing-language-hardening.9 Category Sweep - Long Tail

## Description
Normalize all remaining skills not covered by T5-T8. This is the long-tail batch with a concrete, closed-form list from the ownership manifest.

**Size:** M
**Files:** Residual skill list from `docs/skill-routing-ownership-manifest.md` (~34 skills across build-system, cli-tools, documentation, packaging, performance, project-structure, release-management, serialization)

## Approach

- Same workflow as T6 but for residual skills
- List must be explicit and complete -- no implicit "remaining" edits
- Emit `docs/skill-routing-sweep-long-tail.md`
- After completion, verify ownership manifest shows 100% coverage (every skill assigned and completed)

## Key context

- These skills are lower-traffic but still need consistent routing language
- Some may have unique scope challenges (e.g., `dotnet-domain-modeling` vs `dotnet-efcore-architecture`)
## Acceptance
- [ ] All assigned skills have scope/out-of-scope sections
- [ ] All descriptions follow canonical style
- [ ] `docs/skill-routing-sweep-long-tail.md` emitted
- [ ] Ownership manifest shows 100% of skills assigned and completed (across T5-T9)
- [ ] Budget delta documented: no net increase
- [ ] **Similarity check**: Run similarity before and after this batch (same branch, same suppressions). `pairs_above_warn` does not increase and `unsuppressed_errors == 0`.
- [ ] `./scripts/validate-skills.sh` passes
- [ ] No skills from T6/T7/T8/T10 batches were edited
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
