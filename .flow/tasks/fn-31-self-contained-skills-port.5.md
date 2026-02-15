# fn-31-self-contained-skills-port.5 Enhance observability and create middleware patterns skill

## Description
Enhance existing `skills/architecture/dotnet-observability/SKILL.md` with structured logging patterns (LoggerMessage, message templates, scopes). Create new `skills/api-development/dotnet-middleware-patterns/SKILL.md` for ASP.NET Core middleware pipeline patterns. Port and adapt from dotnet-skills.

**Size:** M
**Files:** skills/architecture/dotnet-observability/SKILL.md, skills/api-development/dotnet-middleware-patterns/SKILL.md, .claude-plugin/plugin.json

## Approach
- **Observability** (`skills/architecture/dotnet-observability/`): Read existing skill first. Enhance with structured logging via Microsoft.Extensions.Logging, log levels, scopes, message templates (not string interpolation), high-performance logging with LoggerMessage.Define/[LoggerMessage], filtering, OpenTelemetry integration. No new plugin.json entry needed.
- **Middleware** (new: `skills/api-development/dotnet-middleware-patterns/`): Place in `api-development/` category (matches existing API skills). Cover pipeline ordering, custom middleware classes vs inline, short-circuit logic, request/response manipulation, exception handling middleware, conditional middleware. Register in plugin.json.
- Both: latest stable packages, credit original authors via `## Attribution` section

## Acceptance
- [ ] Existing observability skill enhanced with structured logging patterns
- [ ] New middleware skill in `skills/api-development/` (correct category)
- [ ] Middleware covers pipeline ordering, custom middleware, short-circuit
- [ ] Latest stable packages
- [ ] Original authors credited via `## Attribution` section
- [ ] Middleware skill registered in plugin.json
- [ ] Descriptions under 120 chars
- [ ] Validation passes

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
