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
