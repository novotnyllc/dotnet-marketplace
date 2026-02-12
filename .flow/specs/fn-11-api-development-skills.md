# fn-11: API Development Skills

## Overview
Delivers modern API development skills covering minimal APIs, API versioning, OpenAPI/Swagger integration, API security patterns, and comprehensive input validation.

## Scope
**Skills (5 total):**
- `dotnet-minimal-apis` - Minimal APIs as the modern default: route groups, filters, endpoint filter pipeline, OpenAPI 3.1, organization patterns for scale. References `[skill:dotnet-input-validation]` for validation depth.
- `dotnet-api-versioning` - API versioning with Microsoft.AspNetCore.Mvc.Versioning, URL versioning preferred
- `dotnet-openapi` - OpenAPI/Swagger: Microsoft.AspNetCore.OpenApi, Swashbuckle, NSwag. Built-in .NET 10 first-class support.
- `dotnet-api-security` - Authentication/authorization: ASP.NET Core Identity, OAuth/OIDC, JWT, passkeys (WebAuthn), CORS, CSP
- `dotnet-input-validation` - Input validation patterns: .NET 10 built-in validation (AddValidation/Microsoft.Extensions.Validation), FluentValidation, Data Annotations, custom validators, endpoint filter integration, ProblemDetails error responses, security-focused validation (ReDoS prevention, allowlist patterns)

## Scope Boundaries

| Concern | fn-11 owns (API development) | Other epic owns | Enforcement |
|---|---|---|---|
| Security validation | Security-focused validation tips (ReDoS, allowlists) — practical patterns for input handling | fn-8: OWASP A03/A05 Injection mitigation (security principles) | Cross-ref `[skill:dotnet-security-owasp]` |
| Architecture validation | N/A — cross-references `[skill:dotnet-architecture-patterns]` | fn-5: validation strategy (architectural patterns, FluentValidation overview) | Cross-ref presence validated by grep |
| Blazor form validation | Brief mention with cross-ref | fn-12: Blazor patterns including EditForm validation | Cross-ref `[skill:dotnet-blazor-patterns]` when it lands |
| Configuration validation | N/A | fn-3: `[skill:dotnet-csharp-configuration]` owns Options pattern ValidateDataAnnotations | Cross-ref presence |

## Key Context
- Minimal APIs are Microsoft's official recommendation for new projects (ASP.NET Core best practices)
- .NET 10 brings built-in validation (AddValidation() + Microsoft.Extensions.Validation), SSE, OpenAPI 3.1 to Minimal APIs
- Swashbuckle is no longer actively maintained; Microsoft.AspNetCore.OpenApi is the built-in replacement for .NET 9+ (existing projects can continue using Swashbuckle but should plan migration)
- .NET 10 adds passkey authentication (WebAuthn) support
- Vertical slice architecture increasingly mainstream for API organization
- FluentValidation auto-validation via ASP.NET pipeline is deprecated; manual validation or endpoint filters preferred
- .NET 10 validation uses source generators for AOT compatibility ([ValidatableType] attribute)
- Microsoft.Extensions.Validation package extracts validation APIs for use outside HTTP scenarios
- Validation decision tree: .NET 10 built-in (default for new projects) > FluentValidation (complex business rules) > Data Annotations (simple models) > MiniValidation (lightweight scenarios)

## Task Decomposition

### fn-11.1: Minimal APIs and versioning skills
**Delivers:** `dotnet-minimal-apis`, `dotnet-api-versioning`
- `skills/api/dotnet-minimal-apis/SKILL.md`
- `skills/api/dotnet-api-versioning/SKILL.md`
- Does NOT touch `plugin.json` (handled by integration task or combined)

### fn-11.2: OpenAPI and API security skills
**Delivers:** `dotnet-openapi`, `dotnet-api-security`
- `skills/api/dotnet-openapi/SKILL.md`
- `skills/api/dotnet-api-security/SKILL.md`

### fn-11.3: Input validation skill
**Delivers:** `dotnet-input-validation`
- `skills/api/dotnet-input-validation/SKILL.md`
- Covers: validation framework decision tree, .NET 10 built-in, FluentValidation, Data Annotations, endpoint filters for validation, ProblemDetails, security validation tips
- Cross-references: `[skill:dotnet-security-owasp]`, `[skill:dotnet-architecture-patterns]`, `[skill:dotnet-minimal-apis]`

## Quick Commands
```bash
# Smoke test: verify all 5 skills exist
for s in dotnet-minimal-apis dotnet-api-versioning dotnet-openapi dotnet-api-security dotnet-input-validation; do
  test -f "skills/api/$s/SKILL.md" && echo "OK: $s" || echo "MISSING: $s"
done

# Validate OpenAPI .NET 10 built-in support
grep -i "Microsoft.AspNetCore.OpenApi" skills/api/dotnet-openapi/SKILL.md

# Test API security coverage
grep -i "passkey\|WebAuthn" skills/api/dotnet-api-security/SKILL.md

# Validate .NET 10 built-in validation coverage
grep -i "AddValidation\|Microsoft.Extensions.Validation" skills/api/dotnet-input-validation/SKILL.md

# Verify FluentValidation coverage
grep -i "FluentValidation\|AbstractValidator" skills/api/dotnet-input-validation/SKILL.md

# Verify security validation patterns
grep -i "ReDoS\|allowlist\|denylist" skills/api/dotnet-input-validation/SKILL.md

# Verify cross-references
grep "skill:dotnet-security-owasp" skills/api/dotnet-input-validation/SKILL.md
grep "skill:dotnet-architecture-patterns" skills/api/dotnet-input-validation/SKILL.md

# Validate all skills registered
grep -c "skills/api/" .claude-plugin/plugin.json  # expect 5

# Run validation
./scripts/validate-skills.sh
```

## Acceptance Criteria
1. All 5 skills written at `skills/api/<name>/SKILL.md` with `name` and `description` frontmatter
2. Minimal APIs skill covers route groups, filters, endpoint filter pipeline, organization at scale; references `[skill:dotnet-input-validation]` for validation depth
3. API versioning skill documents URL versioning (preferred) and other strategies
4. OpenAPI skill emphasizes built-in .NET 10 support over third-party libraries
5. API security skill covers modern auth (passkeys, OAuth/OIDC) and security headers
6. Input validation skill covers: validation decision tree (.NET 10 built-in vs FluentValidation vs Data Annotations), .NET 10 AddValidation() with source generator support, FluentValidation with manual validation pattern, Data Annotations + IValidatableObject, endpoint filters for validation, ProblemDetails/ValidationProblem error responses, security-focused validation (ReDoS prevention, allowlist patterns, max lengths)
7. Input validation skill has explicit scope boundary: fn-8 OWASP (security principles), fn-5 architecture (architectural patterns), fn-11 validation (practical framework guidance)
8. Skills cross-reference architecture patterns (vertical slices, request pipeline)
9. ASP.NET Core best practices referenced throughout
10. All 5 skills registered in `.claude-plugin/plugin.json`
11. `./scripts/validate-skills.sh` passes

## Test Notes
- Verify minimal APIs skill recommends organization patterns for large projects
- Test OpenAPI skill recommends Microsoft.AspNetCore.OpenApi for new projects, notes Swashbuckle migration path
- Validate API security skill covers OWASP API security best practices
- Verify input validation skill provides clear decision tree for framework selection
- Test that .NET 10 AddValidation() is documented as the default for new projects
- Verify FluentValidation section recommends manual validation over deprecated auto-validation
- Confirm security validation tips cross-reference OWASP without duplicating fn-8 content

## References
- Minimal APIs: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis?view=aspnetcore-10.0
- ASP.NET Core Best Practices: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0
- OpenAPI in ASP.NET Core: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/overview?view=aspnetcore-10.0
- ASP.NET Core Security: https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-10.0
- Model Validation: https://learn.microsoft.com/en-us/aspnet/core/mvc/models/validation?view=aspnetcore-10.0
- FluentValidation: https://docs.fluentvalidation.net/en/latest/aspnet.html
- OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
