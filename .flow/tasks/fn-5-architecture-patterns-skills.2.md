# fn-5-architecture-patterns-skills.2 Resilience and HTTP client skills

## Description
Create two skills: `dotnet-resilience` (Polly v8 + Microsoft.Extensions.Resilience + Microsoft.Extensions.Http.Resilience, standard pipeline configuration, explicitly noting Microsoft.Extensions.Http.Polly is superseded) and `dotnet-http-client` (IHttpClientFactory with resilience pipelines, typed/named clients, DelegatingHandlers, testing).

## Acceptance
- [ ] `skills/architecture/dotnet-resilience/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/architecture/dotnet-http-client/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-resilience` recommends Polly v8 + MS.Extensions.Http.Resilience and notes Microsoft.Extensions.Http.Polly is superseded
- [ ] `dotnet-resilience` documents standard pipeline: rate limiter → total timeout → retry → circuit breaker → attempt timeout
- [ ] `dotnet-http-client` cross-references `[skill:dotnet-resilience]` for pipeline configuration
- [ ] Both skills contain out-of-scope boundary statements where applicable
- [ ] Skill `name` values are unique repo-wide
- [ ] Does NOT modify `plugin.json` (handled by fn-5.6)

## Done summary
Added dotnet-resilience (Polly v8 + MS.Extensions.Http.Resilience, standard pipeline, migration from superseded Http.Polly) and dotnet-http-client (IHttpClientFactory, typed/named clients, DelegatingHandlers, resilience integration, testing) architecture skills with full cross-references and boundary statements.
## Evidence
- Commits: b5cdfe1, 7985c5b, 5562e06
- Tests: ./scripts/validate-skills.sh
- PRs: