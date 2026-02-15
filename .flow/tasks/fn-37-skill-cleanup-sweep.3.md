# Task 3: Update testing defaults to xUnit v3 + MTP2 and package versions

## Scope

### xUnit v3 + MTP2 migration
Update all testing guidance to use these concrete package defaults:
- `xunit.v3` (Version 1.0.0+) — replaces `xunit` (v2 package name)
- `xunit.runner.visualstudio` (Version 3.0.0+)
- `Microsoft.NET.Test.Sdk` (Version 17.13.0+) with `<UseMicrosoftTestingPlatformRunner>true</UseMicrosoftTestingPlatformRunner>`
- `coverlet.collector` (Version 6.0.4+)

Remove references to `xunit` (v2 package name) in favor of `xunit.v3`.

### Priority targets (scaffolding skills that propagate defaults)
1. `skills/project-structure/dotnet-add-testing/SKILL.md` — uses `xunit` v2 in CPM examples
2. `skills/project-structure/dotnet-scaffold-project/SKILL.md` — uses `xunit` v2 in CPM
3. `skills/project-structure/dotnet-project-structure/SKILL.md` — uses `xunit` v2 in CPM
4. `skills/testing/dotnet-xunit/SKILL.md` — already covers v3 but verify consistency

### General package version updates
Ensure all library version references use latest stable versions where referenced.

## Verification
```bash
grep -r '"xunit"' skills/ --include='*.md' | grep -v 'xunit.v3' | wc -l  # Should be 0
grep -r 'xunit.*2\.9' skills/ --include='*.md' | wc -l  # Should be 0
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
```

## Acceptance
- [ ] Zero references to `xunit` v2 package name in CPM/PackageReference examples
- [ ] All scaffolding skills use `xunit.v3` version 1.0.0+
- [ ] MTP2 runner flag documented in testing defaults
- [ ] Package versions updated to latest stable where referenced
- [ ] All four validation commands pass
