# fn-31-self-contained-skills-port.5 Port logging/observability and middleware skills

## Description
Create two skills: skills/observability/dotnet-structured-logging/SKILL.md for Microsoft.Extensions.Logging patterns and skills/api/dotnet-middleware-patterns/SKILL.md for ASP.NET Core middleware pipeline patterns. Port and adapt from dotnet-skills.

**Size:** M
**Files:** skills/observability/dotnet-structured-logging/SKILL.md, skills/api/dotnet-middleware-patterns/SKILL.md, .claude-plugin/plugin.json

## Approach
- Logging: structured logging, log levels, scopes, message templates (not string interpolation), high-performance logging with LoggerMessage.Define/[LoggerMessage], filtering, OpenTelemetry integration
- Middleware: pipeline ordering, custom middleware classes vs inline, short-circuit logic, request/response manipulation, exception handling middleware, conditional middleware
- Both: latest stable packages, credit original authors
## Acceptance
- [ ] Structured logging skill covers message templates, LoggerMessage, scopes
- [ ] Middleware skill covers pipeline ordering, custom middleware, short-circuit
- [ ] Latest stable packages
- [ ] Original authors credited
- [ ] Both registered in plugin.json
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
