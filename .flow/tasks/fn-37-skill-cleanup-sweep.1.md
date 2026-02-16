# Task 1: Remove fn-N references and internal artifacts

## Scope
- Remove all `fn-N` references from skill SKILL.md files (57 files identified)
- Delete `skills/architecture/FN7-RECONCILIATION.md`
- Remove internal budget tracking comments (e.g., `<!-- Budget: PROJECTED_SKILLS_COUNT=... -->`)

## Replacement rule
- Where a `[skill:...]` cross-reference already exists on the same line, delete the `(fn-N)` suffix
- Where the fn-N reference is the only pointer (e.g., "owned by fn-8"), replace with the appropriate `[skill:...]` reference or delete the sentence if no skill mapping exists
- In out-of-scope sections that list fn-N ownership, remove the entire ownership line

## Verification
```bash
grep -r 'fn-[0-9]' skills/ --include='*.md' | grep -v '.gitkeep' | wc -l  # Should be 0
test ! -f skills/architecture/FN7-RECONCILIATION.md  # Should pass
grep -r 'Budget:.*PROJECTED' skills/ --include='*.md' | wc -l  # Should be 0
```

## Acceptance
- [ ] Zero fn-N references in any skill SKILL.md content
- [ ] FN7-RECONCILIATION.md deleted
- [ ] No internal budget tracking comments in skill files
- [ ] All four validation commands pass

## Done summary
Removed all fn-N planning references from 50 skill SKILL.md files, deleted FN7-RECONCILIATION.md internal artifact, removed budget tracking HTML comments from dotnet-advisor, and replaced standalone fn-N pointers with proper [skill:...] cross-references (fn-12 -> dotnet-blazor-auth, fn-19 -> appropriate CI/CD skills, fn-10 -> dotnet-version-upgrade/dotnet-multi-targeting, etc.).
## Evidence
- Commits: cb66c5a4db10df42d0a22c30d4866f268a255b52
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py, grep -r 'fn-[0-9]' skills/ --include='*.md' | wc -l  # returned 0, grep -r 'Budget:.*PROJECTED' skills/ --include='*.md' | wc -l  # returned 0, test ! -f skills/architecture/FN7-RECONCILIATION.md  # passed
- PRs: