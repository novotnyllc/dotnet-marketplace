# fn-8: Security Skills

## Overview
Delivers security skills covering OWASP top 10 for .NET, secrets management, modern cryptography (including post-quantum), and a security reviewer agent.

## Scope Boundary
**In scope:** Security guidance for .NET applications: OWASP vulnerability mitigation, secrets management patterns, cryptographic best practices, and automated security review.

**Out of scope / Owned by other skills:**
- Authentication/authorization implementation (ASP.NET Core Identity, OAuth) -- owned by fn-12
- Cloud-specific security services (Azure Key Vault, AWS Secrets Manager details) -- cloud epics
- Network security and firewall configuration -- infrastructure concerns

The boundary is: fn-8 skills cover "how to write secure .NET code"; cloud-specific and auth implementation details belong to other epics.

## Skills
Each skill lives at `skills/security/<skill-name>/SKILL.md` (folder-per-skill convention).

- `dotnet-security-owasp` -- OWASP Top 10 for .NET with mitigation patterns for each category:
  1. A01 Broken Access Control
  2. A02 Cryptographic Failures
  3. A03 Injection (SQL, command, LDAP, XSS)
  4. A04 Insecure Design
  5. A05 Security Misconfiguration
  6. A06 Vulnerable and Outdated Components
  7. A07 Identification and Authentication Failures
  8. A08 Software and Data Integrity Failures
  9. A09 Security Logging and Monitoring Failures
  10. A10 Server-Side Request Forgery (SSRF)
- `dotnet-secrets-management` -- Cloud-agnostic first: user secrets for local development, environment variables for production, IConfiguration binding patterns, secret rotation guidance; mentions managed identity as a production best practice without deep cloud-provider specifics; anti-patterns (secrets in source, appsettings.json, hardcoded connection strings)
- `dotnet-cryptography` -- Modern .NET cryptography: hashing (SHA-256/384/512), symmetric encryption (AES-GCM), asymmetric (RSA, ECDSA), key derivation (PBKDF2, Argon2); post-quantum algorithms (ML-KEM, ML-DSA, SLH-DSA) for .NET 10+ with fallback strategy for earlier TFMs; interoperability caveats

## Deprecated Pattern Ownership
The `dotnet-security-owasp` skill is the **canonical owner** of deprecated security pattern warnings (CAS, APTCA, .NET Remoting, DCOM, BinaryFormatter). Other security skills cross-reference OWASP for the full list rather than duplicating it. The crypto skill warns only about deprecated cryptographic APIs (MD5, SHA1, DES, RC2) relevant to its domain.

## Agent
- `dotnet-security-reviewer` -- Agent at `agents/dotnet-security-reviewer.md`. Analyzes code for security vulnerabilities using OWASP compliance patterns. Read-only analysis agent (no code modification).

## Minimum Supported Versions
- .NET: 8.0+ (LTS baseline); note when features require 10.0+ (post-quantum crypto)
- ASP.NET Core: 8.0+ for security middleware and anti-forgery patterns

## Cross-Reference Matrix
Each skill MUST include outbound `[skill:...]` cross-references as follows:

| Skill | Required Outbound Refs |
|---|---|
| `dotnet-security-owasp` | `dotnet-secrets-management`, `dotnet-cryptography`, `dotnet-csharp-coding-standards` |
| `dotnet-secrets-management` | `dotnet-security-owasp`, `dotnet-csharp-configuration` |
| `dotnet-cryptography` | `dotnet-security-owasp`, `dotnet-secrets-management` |

The `dotnet-security-reviewer` agent preloads all 3 security skills plus `dotnet-advisor`.

## Quick Commands
```bash
# Smoke test: verify OWASP skill covers top 10
grep -c "^##.*A0[1-9]\|^##.*A10" skills/security/dotnet-security-owasp/SKILL.md  # expect 10

# Validate post-quantum crypto coverage
grep -i "ML-KEM\|ML-DSA\|SLH-DSA" skills/security/dotnet-cryptography/SKILL.md

# Verify security reviewer agent exists
test -f agents/dotnet-security-reviewer.md && echo "OK" || echo "MISSING"

# Verify all 3 skills registered in plugin.json
grep -c "skills/security/" .claude-plugin/plugin.json  # expect 3

# Verify agent registered in plugin.json
grep -c "dotnet-security-reviewer" .claude-plugin/plugin.json  # expect 1

# Verify deprecated patterns in OWASP skill (canonical owner)
grep -i "CAS\|APTCA\|\.NET Remoting\|DCOM\|BinaryFormatter" skills/security/dotnet-security-owasp/SKILL.md

# Verify cross-references per matrix
grep "skill:dotnet-secrets-management" skills/security/dotnet-security-owasp/SKILL.md
grep "skill:dotnet-cryptography" skills/security/dotnet-security-owasp/SKILL.md
grep "skill:dotnet-csharp-coding-standards" skills/security/dotnet-security-owasp/SKILL.md
grep "skill:dotnet-security-owasp" skills/security/dotnet-secrets-management/SKILL.md
grep "skill:dotnet-csharp-configuration" skills/security/dotnet-secrets-management/SKILL.md
grep "skill:dotnet-security-owasp" skills/security/dotnet-cryptography/SKILL.md
grep "skill:dotnet-secrets-management" skills/security/dotnet-cryptography/SKILL.md
```

## Acceptance Criteria
1. All 3 skills written at `skills/security/<name>/SKILL.md` with required frontmatter (`name`, `description`)
2. Each skill has: description, scope boundary, prerequisites, cross-references, ≥2 practical code examples, gotchas/pitfalls section, references
3. OWASP skill covers all 10 OWASP Top 10 (2021) categories with .NET-specific mitigation patterns for each
4. Secrets management skill documents user secrets (local dev), environment variables (production), IConfiguration binding, secret rotation, managed identity mention, and anti-patterns (no secrets in source/appsettings)
5. Cryptography skill covers modern algorithms with TFM-aware guidance: post-quantum (ML-KEM, ML-DSA, SLH-DSA) for .NET 10+, fallback strategy for .NET 8/9, interoperability caveats
6. OWASP skill (canonical owner) warns against ALL deprecated security patterns: CAS, APTCA, .NET Remoting, DCOM, BinaryFormatter; crypto skill warns against deprecated crypto APIs (MD5, SHA1, DES, RC2)
7. Cross-references validated per matrix above using grep-based checks (each `[skill:...]` ref verified)
8. Security reviewer agent at `agents/dotnet-security-reviewer.md` with frontmatter (name, description, model, capabilities, tools), preloaded skills list, deterministic review workflow, and read-only constraints
9. All 3 skills registered in `.claude-plugin/plugin.json` skills array
10. Security reviewer agent registered in `.claude-plugin/plugin.json` agents array
11. Cross-references to ASP.NET Core security documentation in relevant skills

## Test Notes
- Validate OWASP skill has a section for each of the 10 categories
- Test cryptography skill provides version-gated guidance (net10.0 PQ vs earlier TFM fallback)
- Verify secrets management skill covers local-dev vs production lifecycle
- Confirm security reviewer agent follows existing agent pattern (see `agents/dotnet-architect.md`)
- Confirm no overlap with auth/identity epics -- fn-8 references them, not duplicates

## References
- ASP.NET Core Security: https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-10.0
- Secure Coding Guidelines: https://learn.microsoft.com/en-us/dotnet/standard/security/secure-coding-guidelines
- Security in .NET: https://learn.microsoft.com/en-us/dotnet/standard/security/
- OWASP Top 10 (2021): https://owasp.org/www-project-top-ten/
- Post-Quantum Cryptography in .NET 10: https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/overview
