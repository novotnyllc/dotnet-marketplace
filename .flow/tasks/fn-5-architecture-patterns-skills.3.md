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
Created `dotnet-observability` skill covering OpenTelemetry (traces, metrics, logs), structured logging (MS.Extensions.Logging source generators + Serilog), health checks (liveness vs readiness), and custom metrics via `System.Diagnostics.Metrics`. Note: a single-line cross-reference (`[skill:dotnet-observability]`) was inserted into `dotnet-resilience/SKILL.md` after fn-5.2 completed — this was a post-completion cross-ref fixup (not parallel authorship), consistent with the parallelizable constraint which governs initial content authorship.
## Evidence
- Commits: skills/architecture/dotnet-observability/SKILL.md created; dotnet-resilience/SKILL.md received post-completion cross-ref insertion (1 line)
- Tests: validate-skills.sh PASSED (0 errors), grep name uniqueness: no duplicates, frontmatter check: name + description present
- PRs: