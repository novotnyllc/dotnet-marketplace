# fn-11-api-development-skills.2 OpenAPI and API security skills

## Description
Create the `dotnet-openapi` and `dotnet-api-security` skills covering OpenAPI/Swagger integration and API security patterns. Update existing advisor catalog/routing entries, register in plugin.json, and update OWASP skill scope text for auth ownership consistency.

**Size:** M
**Files:**
- `skills/api-development/dotnet-openapi/SKILL.md` (new)
- `skills/api-development/dotnet-api-security/SKILL.md` (new)
- `.claude-plugin/plugin.json` (modify — ensure 2 skill paths present)
- `skills/foundation/dotnet-advisor/SKILL.md` (modify — update 2 existing catalog entries + routing)
- `skills/security/dotnet-security-owasp/SKILL.md` (modify — update auth ownership in scope text)

## Approach
- Follow existing skill patterns at `skills/security/dotnet-security-owasp/SKILL.md` for structure and frontmatter conventions
- Use `[skill:...]` cross-reference syntax per fn-2 conventions
- OpenAPI skill: Microsoft.AspNetCore.OpenApi (built-in .NET 9+/10), Swashbuckle migration path, NSwag alternatives, schema customization, document transformers
- API security skill: ASP.NET Core Identity, OAuth 2.0/OIDC, JWT bearer tokens, passkeys (WebAuthn .NET 10), CORS policies, CSP headers, rate limiting. Cross-ref `[skill:dotnet-security-owasp]` for OWASP security principles.
- Update existing advisor catalog entries (lines 67-68) and routing (lines 185-186) — do not duplicate
- Update OWASP skill scope text (line 10): change "Authentication/authorization implementation (ASP.NET Core Identity, OAuth) -- owned by fn-12" to "Authentication/authorization implementation -- API-level auth patterns owned by fn-11 (`[skill:dotnet-api-security]`), Blazor auth UI owned by fn-12"
- Ensure both skills registered in plugin.json
- Verify no duplicate skill IDs in advisor

## Key context
- Swashbuckle is no longer actively maintained; Microsoft.AspNetCore.OpenApi is the recommended replacement for .NET 9+
- .NET 10 OpenAPI 3.1 support includes JSON Schema draft 2020-12 compliance
- Passkey (WebAuthn) support is new in .NET 10 — covers FIDO2 passwordless authentication
- Rate limiting via Microsoft.AspNetCore.RateLimiting (built-in .NET 7+): fixed window, sliding window, token bucket, concurrency
- CORS: prefer explicit policy names over global AllowAny; document common pitfalls (preflight caching, credentials with wildcards)
- Auth ownership split: fn-11 owns API-level auth patterns (Identity, OAuth/OIDC, JWT, passkeys, CORS). fn-8 owns OWASP security principles (cross-cutting). fn-12 owns Blazor-specific auth UI (AuthorizeView, CascadingAuthenticationState).
- OWASP skill scope text must be updated to reflect this split (currently says all auth implementation owned by fn-12)
- Existing advisor catalog entries at lines 67-68 and routing at lines 185-186 need content updates, not duplication
- Pitfall: Swashbuckle does not support OpenAPI 3.1; projects needing 3.1 must migrate to Microsoft.AspNetCore.OpenApi

## Acceptance
- [ ] Skill file exists at `skills/api-development/dotnet-openapi/SKILL.md`
- [ ] Skill file exists at `skills/api-development/dotnet-api-security/SKILL.md`
- [ ] Both have frontmatter with `name` and `description` (under 120 chars each)
- [ ] OpenAPI skill covers: Microsoft.AspNetCore.OpenApi (recommended), Swashbuckle migration, NSwag, document transformers, schema customization
- [ ] OpenAPI skill emphasizes built-in .NET 10 support over third-party libraries
- [ ] API security skill covers: ASP.NET Core Identity, OAuth/OIDC, JWT, passkeys (WebAuthn), CORS, CSP, rate limiting
- [ ] API security skill cross-references `[skill:dotnet-security-owasp]` for OWASP principles
- [ ] API security skill has explicit auth ownership note: fn-11 owns API-level auth, fn-12 owns Blazor auth UI
- [ ] OWASP skill scope text updated: auth implementation points to fn-11 (API auth) and fn-12 (Blazor auth UI)
- [ ] Both skills registered in `.claude-plugin/plugin.json` skills array
- [ ] Advisor catalog and routing entries updated (not duplicated); no duplicate skill IDs
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
Added dotnet-openapi skill (Microsoft.AspNetCore.OpenApi, Swashbuckle migration, NSwag, document/operation/schema transformers, OpenAPI 3.1) and dotnet-api-security skill (Identity, OAuth/OIDC, JWT bearer, passkeys/WebAuthn, CORS, CSP, rate limiting). Updated OWASP skill scope text for auth ownership split, advisor catalog/routing entries, and plugin.json registration.
## Evidence
- Commits: 084e790, 983b30a
- Tests: ./scripts/validate-skills.sh
- PRs: