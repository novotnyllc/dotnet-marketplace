# Task 2: Fix cross-references and remove .gitkeep files

## Scope

### Fix broken cross-references
- `dotnet-advisor` references `[skill:dotnet-scaffolding-base]` which should be `[skill:dotnet-scaffold-project]` (lines ~42, ~171)
- Grep for `dotnet-scaffolding-base` across ALL skill files, not just the advisor
- Run `validate-skills.sh` to catch any other broken cross-references

### Remove .gitkeep files
- Remove `.gitkeep` files from skill directories that contain at least one `SKILL.md` file
- Leave `.gitkeep` in genuinely empty category directories (e.g., `skills/containers/`, `skills/data-access/`) as placeholders for future categories

## Verification
```bash
grep -r 'dotnet-scaffolding-base' skills/ --include='*.md' | wc -l  # Should be 0
./scripts/validate-skills.sh  # Should pass
find skills/ -name '.gitkeep' -exec sh -c 'ls "$(dirname "$1")"/*.md 2>/dev/null | head -1' _ {} \; | wc -l  # Should be 0
```

## Acceptance
- [ ] Zero references to `dotnet-scaffolding-base` in any skill file
- [ ] All cross-references valid (validate-skills.sh passes)
- [ ] No .gitkeep files in directories that contain SKILL.md files
- [ ] .gitkeep preserved in genuinely empty category directories
