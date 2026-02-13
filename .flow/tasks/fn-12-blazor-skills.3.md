# fn-12-blazor-skills.3 Integrate with existing testing and communication skills

## Description
Add reverse cross-references from existing skills to the new Blazor skills, validate all hard cross-references resolve, and ensure no duplicate skill IDs in the advisor catalog.

<!-- Updated by plan-sync: fn-12-blazor-skills.1 already added reverse cross-refs to dotnet-blazor-testing -->
### File targets
- `skills/testing/dotnet-blazor-testing/SKILL.md` — verify reverse cross-refs to `[skill:dotnet-blazor-patterns]` and `[skill:dotnet-blazor-components]` exist (already added by fn-12.1)
- `skills/serialization/dotnet-realtime-communication/SKILL.md` — verify Blazor cross-ref exists (add if missing): `[skill:dotnet-blazor-patterns]`
- `skills/foundation/dotnet-advisor/SKILL.md` — validate no duplicate skill IDs after fn-12.1 additions

### Integration edits
1. In `dotnet-blazor-testing/SKILL.md`, verify reverse cross-refs already present (added by fn-12.1): `[skill:dotnet-blazor-patterns]` for hosting model context, `[skill:dotnet-blazor-components]` for component patterns being tested
2. In `dotnet-realtime-communication/SKILL.md`, verify fn-12 boundary cross-ref exists (add if missing -- currently not present in Cross-references line)
3. Run duplicate ID check on advisor catalog

### Validation commands
```bash
# Verify hard cross-refs resolve (each checked individually)
for ref in dotnet-blazor-testing dotnet-realtime-communication dotnet-api-security dotnet-playwright; do
  if find skills -path "*/$ref/SKILL.md" -print -quit | grep -q .; then
    echo "OK: $ref"
  else
    echo "MISSING: $ref"
    exit 1
  fi
done

# Soft cross-ref: dotnet-ui-chooser (optional, log but don't fail)
if find skills -path "*/dotnet-ui-chooser/SKILL.md" -print -quit | grep -q .; then
  echo "OK: dotnet-ui-chooser (soft)"
else
  echo "SKIP: dotnet-ui-chooser not yet created (soft dependency)"
fi

# Reverse cross-refs present in blazor-testing
grep "skill:dotnet-blazor-patterns" skills/testing/dotnet-blazor-testing/SKILL.md
grep "skill:dotnet-blazor-components" skills/testing/dotnet-blazor-testing/SKILL.md

# No duplicate IDs in advisor
dupes=$(grep -oP 'skill:[a-z-]+' skills/foundation/dotnet-advisor/SKILL.md | sort | uniq -d)
if [[ -n "$dupes" ]]; then
  echo "DUPLICATE IDs: $dupes"
  exit 1
fi
echo "OK: no duplicate advisor IDs"

# Full validation
./scripts/validate-skills.sh
```

## Acceptance
- [ ] `dotnet-blazor-testing` has reverse cross-refs to `[skill:dotnet-blazor-patterns]` and `[skill:dotnet-blazor-components]` (already added by fn-12.1 -- verify only)
- [ ] `dotnet-realtime-communication` has Blazor cross-ref
- [ ] No duplicate skill IDs in advisor catalog
- [ ] All hard cross-references from new Blazor skills resolve to existing skill files (`dotnet-blazor-testing`, `dotnet-realtime-communication`, `dotnet-api-security`, `dotnet-playwright`)
- [ ] Soft cross-reference `dotnet-ui-chooser` logged but not required to resolve
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
Added [skill:dotnet-blazor-patterns] cross-reference to dotnet-realtime-communication SKILL.md (Out of scope and Cross-references sections). Verified reverse cross-refs in dotnet-blazor-testing already present, no duplicate skill IDs in advisor catalog, all hard cross-references resolve, and validate-skills.sh passes.
## Evidence
- Commits: 9d1a95cae24158a4aab0644673be26970ba11ff5
- Tests: ./scripts/validate-skills.sh
- PRs: