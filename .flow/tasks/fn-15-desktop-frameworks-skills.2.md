# fn-15-desktop-frameworks-skills.2 Create dotnet-ui-chooser decision tree skill

## Description
Create the `dotnet-ui-chooser` skill — a comprehensive UI framework decision tree covering all .NET UI frameworks. This is the cross-cutting skill referenced by MAUI, Uno, Blazor, and desktop framework skills.

**Delivers:**
- `skills/ui-frameworks/dotnet-ui-chooser/SKILL.md` — framework selection decision tree

**Modifies:**
- `skills/ui-frameworks/` (1 new directory with SKILL.md file only)
- Does NOT modify `plugin.json` or `dotnet-advisor` — task 3 owns all registration

**Content requirements per epic spec:**
- 5 decision factors from UI Chooser Content Coverage table (Target Platforms, Team Expertise, UI Complexity, Performance Needs, Migration Path)
- Covers all framework categories: Web (Blazor Server/WASM/Hybrid), cross-platform (MAUI, Uno, Avalonia), Windows-only (WinUI, WPF, WinForms)
- Decision tree format with structured "if target X, consider Y" guidance
- Trade-off comparison tables
- Must be objective — present trade-offs, not recommend one framework
- Mentions Avalonia as a community alternative (brief, not owned by this plugin)

**Cross-references (all hard):**
- `[skill:dotnet-blazor-patterns]`
- `[skill:dotnet-maui-development]`
- `[skill:dotnet-uno-platform]`
- `[skill:dotnet-winui]` (created in task 1)
- `[skill:dotnet-wpf-modern]` (created in task 1)
- `[skill:dotnet-winforms-basics]` (created in task 1)

**Conventions:**
- Canonical frontmatter: `name` and `description` only
- Description ≤ 120 chars
- `[skill:name]` cross-reference syntax throughout
- Objective tone — this is a decision support skill, not a recommendation engine

## Acceptance
- [ ] `skills/ui-frameworks/dotnet-ui-chooser/SKILL.md` exists with `name` and `description` frontmatter
- [ ] Covers all 5 decision factors from UI Chooser Content Coverage table
- [ ] Covers Web frameworks: Blazor Server, Blazor WebAssembly, Blazor Hybrid
- [ ] Covers cross-platform: MAUI, Uno Platform, Avalonia (brief)
- [ ] Covers Windows-only: WinUI 3, WPF, WinForms
- [ ] Decision tree format with structured guidance (not "always use X")
- [ ] Trade-off comparison tables present
- [ ] Objective tone — presents trade-offs, not recommendations
- [ ] All 6 hard cross-refs present and resolvable: blazor-patterns, maui-development, uno-platform, winui, wpf-modern, winforms-basics
- [ ] Skill description ≤ 120 chars
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
Created dotnet-ui-chooser decision tree skill covering all 5 decision factors (target platforms, team expertise, UI complexity, performance needs, migration path) across Web (Blazor Server/WASM/Hybrid), cross-platform (MAUI, Uno, Avalonia), and Windows-only (WinUI, WPF, WinForms) frameworks with trade-off comparison tables and objective guidance.
## Evidence
- Commits: 493bb8d, 63b0aa2
- Tests: ./scripts/validate-skills.sh
- PRs: