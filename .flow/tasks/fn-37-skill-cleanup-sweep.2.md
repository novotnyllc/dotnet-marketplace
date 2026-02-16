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

## Done summary
Removed 17 unnecessary .gitkeep files from skill category directories that contain SKILL.md content, preserved .gitkeep in 2 genuinely empty category directories (containers, data-access), and fixed stale dotnet-scaffolding-base reference to dotnet-scaffold-project in docs/dotnet-artisan-spec.md.
## Evidence
- Commits: 4fd352f3006ea03612b12fe22ed7f1bfad3d5e6c
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: