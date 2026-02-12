# fn-8: Security Skills

## Overview
Delivers security skills covering OWASP top 10 for .NET, secrets management, modern cryptography (including post-quantum), and a security reviewer agent.

## Scope
**Skills:**
- `dotnet-security-owasp` - OWASP top 10 for .NET: injection prevention, XSS, CSRF, security headers, input validation
- `dotnet-secrets-management` - User secrets, environment variables, secure configuration patterns (cloud-agnostic)
- `dotnet-cryptography` - Modern .NET cryptography including post-quantum algorithms (ML-KEM, ML-DSA, SLH-DSA in .NET 10)

**Agents:**
- `dotnet-security-reviewer` - Analyzes code for security vulnerabilities, OWASP compliance

## Key Context
- .NET 10 introduces post-quantum cryptography (ML-KEM, ML-DSA, SLH-DSA)
- ASP.NET Core Security: https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-10.0
- Secure Coding Guidelines: https://learn.microsoft.com/en-us/dotnet/standard/security/secure-coding-guidelines
- User secrets for local development, environment variables for production
- Avoid deprecated patterns: CAS, APTCA, .NET Remoting, DCOM, binary formatters

## Quick Commands
```bash
# Smoke test: verify OWASP skill covers top 10
grep -i "OWASP" skills/security/dotnet-security-owasp.md

# Validate post-quantum crypto coverage
grep -i "ML-KEM\|ML-DSA\|SLH-DSA" skills/security/dotnet-cryptography.md

# Test security reviewer agent configuration
fd -e json dotnet-security-reviewer agents/
```

## Acceptance Criteria
1. All 3 skills written with standard depth and frontmatter
2. OWASP skill covers top 10 vulnerabilities with .NET-specific mitigation patterns
3. Secrets management skill documents user secrets, environment variables, managed identities
4. Cryptography skill covers post-quantum algorithms (ML-KEM, ML-DSA, SLH-DSA) for .NET 10+
5. Security reviewer agent configured with preloaded security skills
6. Skills warn against deprecated security patterns (CAS, binary formatters)
7. Cross-references to ASP.NET Core security documentation

## Test Notes
- Verify OWASP skill detects common vulnerabilities (SQL injection, XSS, CSRF)
- Test cryptography skill adapts guidance for .NET 10 vs earlier TFMs
- Validate security reviewer agent triggers on security-related keywords

## References
- ASP.NET Core Security: https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-10.0
- Secure Coding Guidelines: https://learn.microsoft.com/en-us/dotnet/standard/security/secure-coding-guidelines
- Security in .NET: https://learn.microsoft.com/en-us/dotnet/standard/security/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
