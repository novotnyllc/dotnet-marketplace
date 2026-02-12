# fn-5-architecture-patterns-skills.6 Integration — plugin registration, validation, and cross-reference audit

## Description
Register all 10 architecture skills in `.claude-plugin/plugin.json`, run validation, and audit cross-references and boundary statements. This is the sole owner of `plugin.json` modifications for fn-5, preventing merge conflicts.

## Acceptance
- [ ] All 10 skill paths added to `.claude-plugin/plugin.json` skills array
- [ ] `./scripts/validate-skills.sh` passes for all 10 skills (validates both `name` and `description` frontmatter)
- [ ] Repo-wide uniqueness: `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` returns empty
- [ ] Catalog-level uniqueness: new `name:` values do not conflict with any existing marketplace skill names (verify new names are not already registered in marketplace catalogs or other plugins)
- [ ] Boundary cross-references verified: `[skill:dotnet-csharp-async-patterns]`, `[skill:dotnet-csharp-dependency-injection]` present in relevant skills
- [ ] Out-of-scope statements verified for fn-3 (DI/async), fn-4 (scaffolding), fn-7 (testing), fn-19 (CI/CD)
- [ ] `[skill:dotnet-resilience]` cross-ref present in `dotnet-http-client`
- [ ] `[skill:dotnet-observability]` cross-ref present in `dotnet-container-deployment`
- [ ] Deferred fn-7 testing cross-ref placeholders present in EF Core and observability skills
- [ ] Reconciliation note documented: when fn-7 lands, replace placeholders with canonical `[skill:...]` cross-references

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
