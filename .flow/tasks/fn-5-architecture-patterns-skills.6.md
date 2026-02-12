# fn-5-architecture-patterns-skills.6 Integration — plugin registration, validation, and cross-reference audit

## Description
Register all 10 architecture skills in `.claude-plugin/plugin.json`, run validation, and audit cross-references and boundary statements. This is the sole owner of `plugin.json` modifications for fn-5, preventing merge conflicts.

## Acceptance
- [ ] All 10 skill paths added to `.claude-plugin/plugin.json` skills array
- [ ] `./scripts/validate-skills.sh` passes for all 10 skills (validates both `name` and `description` frontmatter)
- [ ] Repo-wide uniqueness: `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` returns empty
- [ ] Catalog-level uniqueness: new `name:` values do not conflict with any existing marketplace skill names (verify new names are not already registered in marketplace catalogs or other plugins)
- [ ] Boundary cross-references verified: `[skill:dotnet-csharp-async-patterns]`, `[skill:dotnet-csharp-dependency-injection]`, `[skill:dotnet-csharp-configuration]` present in relevant skills
<!-- Updated by plan-sync: fn-5.1 also cross-references [skill:dotnet-csharp-configuration] in dotnet-architecture-patterns for Options pattern -->
- [ ] Out-of-scope statements verified for fn-3 (DI/async), fn-4 (scaffolding), fn-7 (testing), fn-19 (CI/CD)
- [ ] `[skill:dotnet-resilience]` cross-ref present in `dotnet-http-client`
- [ ] `[skill:dotnet-observability]` cross-ref present in `dotnet-container-deployment`
- [ ] Deferred fn-7 testing cross-ref placeholders present in architecture-patterns, background-services, EF Core, and observability skills
<!-- Updated by plan-sync: fn-5.1 added fn-7 deferred placeholders in dotnet-architecture-patterns and dotnet-background-services, not just EF Core/observability -->
- [ ] Reconciliation note documented: when fn-7 lands, replace placeholders with canonical `[skill:...]` cross-references

## Done summary
Registered all 10 architecture skills in plugin.json, verified repo-wide name uniqueness, audited all boundary cross-references (fn-3 DI/async, fn-4 scaffolding, fn-7 testing, fn-19 CI/CD), confirmed deferred fn-7 placeholders in all 10 skills, and added FN7-RECONCILIATION.md tracking document for future cross-reference updates. Also inserted the `[skill:dotnet-observability]` cross-reference into `dotnet-resilience/SKILL.md` as part of the cross-reference audit — this edit is owned by fn-5.6 (integration task), preserving the file-disjoint constraint for fn-5.1–fn-5.5.
## Evidence
- Commits: 8b362d4589c576dde33a6c7c06f03cc458effdd8
- Tests: ./scripts/validate-skills.sh, grep -rh '^name:' skills/*/*/SKILL.md | sort | uniq -d, python3 -c 'import json; json.load(open(".claude-plugin/plugin.json"))'
- PRs: