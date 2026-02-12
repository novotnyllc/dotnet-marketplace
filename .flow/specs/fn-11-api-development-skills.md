# fn-11: API Development Skills

## Overview
Delivers modern API development skills covering minimal APIs, API versioning, OpenAPI/Swagger integration, and API security patterns.

## Scope
**Skills:**
- `dotnet-minimal-apis` - Minimal APIs as the modern default: route groups, filters, validation, OpenAPI 3.1, organization patterns for scale
- `dotnet-api-versioning` - API versioning with Microsoft.AspNetCore.Mvc.Versioning, URL versioning preferred
- `dotnet-openapi` - OpenAPI/Swagger: Microsoft.AspNetCore.OpenApi, Swashbuckle, NSwag. Built-in .NET 10 first-class support.
- `dotnet-api-security` - Authentication/authorization: ASP.NET Core Identity, OAuth/OIDC, JWT, passkeys (WebAuthn), CORS, CSP

## Key Context
- Minimal APIs are Microsoft's official recommendation for new projects (ASP.NET Core best practices)
- .NET 10 brings built-in validation, SSE, OpenAPI 3.1 to Minimal APIs
- Swashbuckle deprecated in favor of built-in Microsoft.AspNetCore.OpenApi
- .NET 10 adds passkey authentication (WebAuthn) support
- Vertical slice architecture increasingly mainstream for API organization

## Quick Commands
```bash
# Smoke test: verify minimal APIs skill exists
fd -e md dotnet-minimal-apis skills/

# Validate OpenAPI .NET 10 built-in support
grep -i "Microsoft.AspNetCore.OpenApi" skills/api/dotnet-openapi.md

# Test API security coverage
grep -i "passkey\|WebAuthn" skills/api/dotnet-api-security.md
```

## Acceptance Criteria
1. All 4 skills written with standard depth and frontmatter
2. Minimal APIs skill covers route groups, filters, validation, organization at scale
3. API versioning skill documents URL versioning (preferred) and other strategies
4. OpenAPI skill emphasizes built-in .NET 10 support over third-party libraries
5. API security skill covers modern auth (passkeys, OAuth/OIDC) and security headers
6. Skills cross-reference architecture patterns (vertical slices, request pipeline)
7. ASP.NET Core best practices referenced throughout

## Test Notes
- Verify minimal APIs skill recommends organization patterns for large projects
- Test OpenAPI skill warns against deprecated Swashbuckle patterns
- Validate API security skill covers OWASP API security best practices

## References
- Minimal APIs: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis?view=aspnetcore-10.0
- ASP.NET Core Best Practices: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0
- OpenAPI in ASP.NET Core: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/overview?view=aspnetcore-10.0
- ASP.NET Core Security: https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-10.0
