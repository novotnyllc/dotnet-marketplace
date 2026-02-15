# Skill Cleanup Sweep

## Overview
Housekeeping pass across all skills to remove internal tracking artifacts, fix stale references, update testing defaults, and enforce package version policy.

## Scope

### 1. Remove fn-N references
57 files contain fn-N spec references (e.g., "implemented in fn-7", "owned by fn-8"). Skills should never reference internal planning IDs.

**Replacement rule**: Remove all `fn-N` references. Where a `[skill:...]` cross-reference already exists on the same line, simply delete the `(fn-N)` suffix. Where the fn-N reference is the only pointer (e.g., "owned by fn-8"), replace with the appropriate `[skill:...]` reference or delete the sentence if no skill mapping exists.

### 2. Remove .gitkeep files
19+ unnecessary .gitkeep files in skill directories that now have content.

**Safety rule**: Only remove `.gitkeep` if the directory contains at least one `SKILL.md` file. Leave `.gitkeep` in genuinely empty category directories (e.g., `skills/containers/`, `skills/data-access/`) — these are placeholders for future skill categories.

### 3. Fix broken cross-references
- `dotnet-advisor` references `[skill:dotnet-scaffolding-base]` which should be `[skill:dotnet-scaffold-project]` (lines 42, 171)
- Grep for `dotnet-scaffolding-base` across ALL skill files, not just the advisor

### 4. Update testing defaults to xUnit v3 + MTP2
All testing guidance should default to xUnit v3 with Microsoft.Testing.Platform v2 (MTP2).

**Concrete package defaults for all examples:**
- `xunit.v3` (Version 1.0.0+) — replaces `xunit` (v2 package name)
- `xunit.runner.visualstudio` (Version 3.0.0+)
- `Microsoft.NET.Test.Sdk` (Version 17.13.0+) with `<UseMicrosoftTestingPlatformRunner>true</UseMicrosoftTestingPlatformRunner>`
- `coverlet.collector` (Version 6.0.4+)

Remove references to `xunit` (v2 package name) in favor of `xunit.v3`. **Priority targets**: scaffolding skills (`dotnet-add-testing`, `dotnet-scaffold-project`, `dotnet-project-structure`) that propagate defaults to new projects.

### 5. Minimize third-party deps
Ensure FluentValidation is positioned as an opt-in for complex validation scenarios, not a default. Verify all skills that mention FluentValidation also mention built-in alternatives first (DataAnnotations, IValidateOptions, .NET 10 `AddValidation`). The current `dotnet-input-validation` decision tree is close to correct — verify it recommends built-in first.

### 6. System.CommandLine version
System.CommandLine 2.0 has **no stable release** — it remains at `2.0.0-beta4.*` pre-release. Verify references use the latest `2.0.0-beta4.*` version. Add a note that no stable 2.0 release exists yet. Remove any references to older beta versions (beta1, beta2, beta3).

### 7. Package version updates
Ensure all library version references use latest stable (prefer stable over prerelease). See concrete xUnit/MTP2 versions in scope item #4.

### 8. Remove internal artifacts
- `skills/architecture/FN7-RECONCILIATION.md` should not ship — delete it
- Remove internal budget tracking comments from skill files (e.g., `<!-- Budget: PROJECTED_SKILLS_COUNT=... -->` in `dotnet-advisor`)

### 9. SOLID/DRY/SRP enforcement
Ensure architecture-related skills engrain these principles (check `dotnet-clean-architecture`, `dotnet-csharp-coding-standards`, `dotnet-architecture-patterns`). This is independent of other scope items and targets a different set of files.

## Quick commands
```bash
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
python3 scripts/validate_cross_agent.py
```

## Acceptance

### Automated (validated by scripts + grep)
- [ ] Zero fn-N references in any skill SKILL.md content (`grep -r 'fn-[0-9]' skills/ --include='*.md'` returns 0 hits, excluding FN7-RECONCILIATION.md which is deleted)
- [ ] Zero unnecessary .gitkeep files (only remain in genuinely empty category dirs)
- [ ] All cross-references valid (validate-skills.sh passes)
- [ ] FN7-RECONCILIATION.md removed
- [ ] No internal budget tracking comments in skill files
- [ ] All four validation commands pass
- [ ] Zero references to `xunit` v2 package name in CPM/PackageReference examples (`grep -r '"xunit"' skills/ --include='*.md'` returns 0 hits)

### Manual review
- [ ] Testing defaults updated to xUnit v3 + MTP2 across all testing and scaffolding skills
- [ ] FluentValidation positioned as opt-in for complex scenarios, built-in recommended first
- [ ] System.CommandLine references use latest beta4 and note pre-release status
- [ ] Package versions updated to latest stable where referenced
- [ ] Architecture skills reference SOLID/DRY/SRP principles

## References
- Context-scout findings: 57 files with fn-N refs, 19 .gitkeep files
- `skills/foundation/dotnet-advisor/SKILL.md:42,171` — broken cross-ref
- `skills/architecture/FN7-RECONCILIATION.md` — internal artifact to remove
- https://stormwild.github.io/blog/post/srp-mistakes-csharp-dotnet/ — SRP anti-patterns reference
