# fn-8-security-skills.1 OWASP and secrets management skills

## Description
Create the `dotnet-security-owasp` and `dotnet-secrets-management` skills at `skills/security/<name>/SKILL.md`.

**dotnet-security-owasp:** Cover all 10 OWASP Top 10 (2021) categories with .NET-specific mitigation patterns. Each category gets a section with: vulnerability description, .NET-specific risk, mitigation code example, and gotchas. As the canonical owner of deprecated pattern warnings, include warnings for CAS, APTCA, .NET Remoting, DCOM, and BinaryFormatter.

**dotnet-secrets-management:** Cloud-agnostic secrets guidance: user secrets for local development, environment variables for production, IConfiguration binding patterns, secret rotation guidance, managed identity mention as production best practice, anti-patterns (secrets in source/appsettings.json/hardcoded connection strings).

Both skills must follow the folder-per-skill convention with standard frontmatter (`name`, `description`), scope boundary, prerequisites, ≥2 code examples each, gotchas/pitfalls, cross-references per the epic matrix, and references including ASP.NET Core security documentation links.

**File ownership (this task):**
- `skills/security/dotnet-security-owasp/SKILL.md` (create)
- `skills/security/dotnet-secrets-management/SKILL.md` (create)

**Files NOT owned by this task (fn-8.2 owns):**
- `skills/security/dotnet-cryptography/SKILL.md`
- `agents/dotnet-security-reviewer.md`
- `.claude-plugin/plugin.json` (final registration in fn-8.2)

## Acceptance
- [ ] `dotnet-security-owasp` skill at `skills/security/dotnet-security-owasp/SKILL.md` with frontmatter (`name`, `description`)
- [ ] OWASP skill has sections for all 10 OWASP Top 10 (2021) categories (A01–A10)
- [ ] Each OWASP category has .NET-specific mitigation code example
- [ ] OWASP skill warns against deprecated patterns: CAS, APTCA, .NET Remoting, DCOM, BinaryFormatter
- [ ] OWASP skill includes ASP.NET Core security documentation links in references
- [ ] `dotnet-secrets-management` skill at `skills/security/dotnet-secrets-management/SKILL.md` with frontmatter
- [ ] Secrets skill covers: user secrets (local dev), environment variables (production), IConfiguration binding, secret rotation, managed identity mention
- [ ] Secrets skill documents anti-patterns: secrets in source, appsettings.json, hardcoded connection strings
- [ ] Secrets skill includes ASP.NET Core security documentation links in references
- [ ] Both skills have: scope boundary, prerequisites, ≥2 code examples, gotchas/pitfalls, references
- [ ] Cross-references verified by grep:
  - `grep "skill:dotnet-secrets-management" skills/security/dotnet-security-owasp/SKILL.md` -- match
  - `grep "skill:dotnet-cryptography" skills/security/dotnet-security-owasp/SKILL.md` -- match
  - `grep "skill:dotnet-csharp-coding-standards" skills/security/dotnet-security-owasp/SKILL.md` -- match
  - `grep "skill:dotnet-security-owasp" skills/security/dotnet-secrets-management/SKILL.md` -- match
  - `grep "skill:dotnet-csharp-configuration" skills/security/dotnet-secrets-management/SKILL.md` -- match

## Done summary
Created dotnet-security-owasp and dotnet-secrets-management skills covering all 10 OWASP Top 10 (2021) categories with .NET-specific mitigations, deprecated pattern warnings (CAS, APTCA, .NET Remoting, DCOM, BinaryFormatter), and comprehensive secrets lifecycle guidance (user secrets, environment variables, IConfiguration binding, rotation with IHostedService, managed identity, anti-patterns).
## Evidence
- Commits: 5a84e06, d3b72da, 98e979f
- Tests: grep -c OWASP categories (10/10), grep cross-references (all verified), grep deprecated patterns (CAS/APTCA/.NET Remoting/DCOM/BinaryFormatter)
- PRs: