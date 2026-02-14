# fn-15-desktop-frameworks-skills.3 Register skills, create migration guidance, and validate integrations

## Description
Register ALL 5 fn-15 skills in plugin.json, create the `dotnet-wpf-migration` skill covering context-dependent migration paths, verify/deduplicate advisor catalog entries, validate all cross-references, and update existing skills to strengthen `[skill:dotnet-ui-chooser]` references.

This task is the sole owner of `plugin.json` and `dotnet-advisor/SKILL.md` modifications for the fn-15 epic (file-disjoint convention).

**Delivers:**
- `skills/ui-frameworks/dotnet-wpf-migration/SKILL.md` — migration guidance skill
- All 5 fn-15 skills registered in `plugin.json`
- Advisor catalog entries verified/deduplicated for all 5 skills
- Cross-reference validation across all fn-15 skills
- Reverse cross-ref updates to existing framework skills

**Modifies:**
- `skills/ui-frameworks/` (1 new directory)
- `.claude-plugin/plugin.json` (register ALL 5 fn-15 skills — sole owner)
- `skills/foundation/dotnet-advisor/SKILL.md` (verify/deduplicate ALL 5 catalog entries — sole owner)

**Updates (cross-refs only):**
- `skills/ui-frameworks/dotnet-maui-development/SKILL.md` — strengthen `[skill:dotnet-ui-chooser]` from soft to hard ref
- `skills/ui-frameworks/dotnet-blazor-patterns/SKILL.md` — strengthen `[skill:dotnet-ui-chooser]` from soft to hard ref
- `skills/ui-frameworks/dotnet-uno-platform/SKILL.md` — strengthen `[skill:dotnet-ui-chooser]` from soft to hard ref

**Content requirements per epic spec:**
- 7 migration paths from WPF Migration Content Coverage table (includes UWP → Uno cross-ref)
- Context-dependent guidance (not "always migrate to X")
- `dotnet-upgrade-assistant` documented where applicable
- Decision matrix: Windows-only → WinUI; cross-platform → Uno; staying Windows → WPF .NET 8+

**Cross-references (hard):**
- `[skill:dotnet-winui]`, `[skill:dotnet-wpf-modern]`, `[skill:dotnet-uno-platform]`, `[skill:dotnet-winforms-basics]`
- `[skill:dotnet-ui-chooser]`

**Validation checks:**
- All hard cross-references across fn-15 skills resolve (grep check)
- No duplicate skill IDs in advisor catalog
- All 5 fn-15 skills registered in plugin.json
- Reverse cross-refs present in MAUI, Blazor, Uno skills

## Acceptance
- [ ] `skills/ui-frameworks/dotnet-wpf-migration/SKILL.md` exists with `name` and `description` frontmatter
- [ ] Covers all 7 migration paths: WPF .NET Framework → .NET 8+, WPF → WinUI, WPF → Uno, WinForms → .NET 8+, UWP → WinUI, UWP → Uno (cross-ref), Decision Matrix
- [ ] `dotnet-upgrade-assistant` documented for .NET Framework → .NET 8+ migrations
- [ ] Context-dependent guidance (not "always use X")
- [ ] ALL 5 fn-15 skills registered in `.claude-plugin/plugin.json`
- [ ] ALL 5 advisor catalog entries verified/deduplicated
- [ ] All hard cross-references across all 5 fn-15 skills resolve: `grep -r 'skill:[a-z-]*' skills/ui-frameworks/dotnet-{winui,wpf-modern,wpf-migration,winforms-basics,ui-chooser}/SKILL.md`
- [ ] No duplicate skill IDs in advisor catalog: `grep -oP 'skill:[a-z-]+' skills/foundation/dotnet-advisor/SKILL.md | sort | uniq -d` returns empty
- [ ] Reverse cross-refs: `[skill:dotnet-ui-chooser]` present in `dotnet-maui-development`, `dotnet-blazor-patterns`, `dotnet-uno-platform` SKILL.md files (no longer soft dep)
- [ ] All 5 fn-15 skills appear in plugin.json
- [ ] Skill description ≤ 120 chars
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
