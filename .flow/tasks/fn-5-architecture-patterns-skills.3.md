# fn-5-architecture-patterns-skills.3 Observability skill

## Description
Create `dotnet-observability` skill covering OpenTelemetry (traces, metrics, logs), Serilog/MS.Extensions.Logging structured logging, health checks, and custom metrics.

## Acceptance
- [ ] `skills/architecture/dotnet-observability/SKILL.md` exists with `name` and `description` frontmatter
- [ ] Covers OpenTelemetry setup for traces/metrics/logs plus structured logging
- [ ] Covers health check patterns (referenced by container skills)
- [ ] Contains out-of-scope boundary statements (testing → fn-7)
- [ ] Deferred cross-ref placeholder for fn-7 `dotnet-integration-testing` (non-blocking)
- [ ] Skill `name` value is unique repo-wide
- [ ] Does NOT modify `plugin.json` (handled by fn-5.6)

## Done summary
Created `dotnet-observability` skill covering OpenTelemetry (traces, metrics, logs), structured logging (MS.Extensions.Logging source generators + Serilog), health checks (liveness vs readiness), and custom metrics via `System.Diagnostics.Metrics`. Also updated the `dotnet-resilience` skill to replace the fn-5.3 TODO placeholder with the actual `[skill:dotnet-observability]` cross-reference.
## Evidence
- Commits: skills/architecture/dotnet-observability/SKILL.md created; skills/architecture/dotnet-resilience/SKILL.md updated fn-5.3 TODO to cross-ref
- Tests: validate-skills.sh PASSED (0 errors), grep name uniqueness: no duplicates, frontmatter check: name + description present
- PRs: