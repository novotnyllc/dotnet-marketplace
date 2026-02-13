# fn-12-blazor-skills.1 Create Blazor skills (patterns, components, auth)

## Description
Create three Blazor SKILL.md files covering hosting models/render modes, component architecture, and authentication. Each skill targets `skills/ui-frameworks/<name>/SKILL.md` with canonical frontmatter (`name`, `description`). Register all 3 skills in `plugin.json` and add catalog/routing entries in `dotnet-advisor`.

### File targets
- `skills/ui-frameworks/dotnet-blazor-patterns/SKILL.md` — hosting models, render modes (InteractiveServer, InteractiveWebAssembly, InteractiveAuto, Static SSR, Hybrid), routing, enhanced navigation, streaming rendering, AOT-safe patterns, project setup
- `skills/ui-frameworks/dotnet-blazor-components/SKILL.md` — component lifecycle, state management (cascading values, DI, browser storage), JS interop (AOT-safe), EditForm validation, QuickGrid, .NET 11 preview features marked `<!-- net11-preview -->` with source links
- `skills/ui-frameworks/dotnet-blazor-auth/SKILL.md` — AuthorizeView, CascadingAuthenticationState, Identity UI scaffolding, role/policy-based auth, per-hosting-model auth flow differences (cookie vs token), external providers
- `.claude-plugin/plugin.json` — add 3 skill paths to `skills` array
- `skills/foundation/dotnet-advisor/SKILL.md` — add catalog entries and routing for 3 new skills

### Cross-references required
- `[skill:dotnet-blazor-testing]` — bUnit testing (do not duplicate content)
- `[skill:dotnet-realtime-communication]` — standalone SignalR patterns
- `[skill:dotnet-api-security]` — API-level auth (JWT, OAuth/OIDC)
- `[skill:dotnet-ui-chooser]` — soft cross-ref (may not exist yet)
- `[skill:dotnet-playwright]` — E2E testing

### AOT requirements
Document in `dotnet-blazor-patterns`: source-gen serialization, trim-safe JS interop, linker config, anti-patterns, `[DynamicallyAccessedMembers]` annotations.

### .NET version policy
- Baseline .NET 8.0+
- .NET 10 stable features documented when net10.0 TFM detected
- .NET 11 preview features marked `<!-- net11-preview -->` with net10.0 fallback
- Each preview feature section must include a source link to official docs/announcement

## Acceptance
- [ ] 3 SKILL.md files created at `skills/ui-frameworks/dotnet-blazor-{patterns,components,auth}/SKILL.md`
- [ ] Each skill has `name` and `description` frontmatter
- [ ] All 5 hosting models/render modes documented in patterns skill
- [ ] Per-mode behavior differences documented in each skill where relevant
- [ ] AOT-safe patterns section in patterns skill
- [ ] .NET 11 preview features marked with `<!-- net11-preview -->` and each includes a source link
- [ ] Cross-references present (blazor-testing, realtime-communication, api-security, ui-chooser soft, playwright)
- [ ] 3 skills registered in `plugin.json` (verified per-skill)
- [ ] 3 skills added to advisor catalog and routing (no duplicate IDs)
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
Created three Blazor SKILL.md files (dotnet-blazor-patterns, dotnet-blazor-components, dotnet-blazor-auth) covering all five hosting models/render modes, component lifecycle, state management, JS interop, EditForm validation, QuickGrid, auth flows, AOT-safe patterns, and .NET 11 preview features. Registered all 3 skills in plugin.json and added reverse cross-refs to dotnet-blazor-testing.
## Evidence
- Commits: 79e96e0, 2a04eed, bde6e0e
- Tests: ./scripts/validate-skills.sh
- PRs: