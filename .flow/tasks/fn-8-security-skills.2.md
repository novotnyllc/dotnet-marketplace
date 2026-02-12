# fn-8-security-skills.2 Cryptography skill and security reviewer agent

## Description
Create the `dotnet-cryptography` skill and `dotnet-security-reviewer` agent, then register all fn-8 deliverables in plugin.json.

**Depends on:** fn-8-security-skills.1 (OWASP and secrets skills must exist before plugin registration and agent preload validation).

**dotnet-cryptography:** Modern .NET cryptography covering hashing (SHA-256/384/512), symmetric encryption (AES-GCM), asymmetric (RSA, ECDSA), key derivation (PBKDF2, Argon2). Post-quantum algorithms (ML-KEM, ML-DSA, SLH-DSA) for .NET 10+ with TFM-aware guidance: what's available on net10.0 vs fallback for net8.0/net9.0. Include interoperability caveats. Warn against deprecated crypto APIs (MD5, SHA1, DES, RC2); cross-reference OWASP skill for the full deprecated security pattern list.

**dotnet-security-reviewer:** Agent at `agents/dotnet-security-reviewer.md` following existing agent template (see `agents/dotnet-architect.md`). Must include: frontmatter (name, description, model, capabilities, tools), preloaded skills ([skill:dotnet-security-owasp], [skill:dotnet-secrets-management], [skill:dotnet-cryptography], [skill:dotnet-advisor]), deterministic review workflow, and read-only constraints (no code modification).

**plugin.json registration:** Add all 3 security skills and the security reviewer agent to `.claude-plugin/plugin.json`. This is the final integration step — run after fn-8.1 skills exist.

**File ownership (this task):**
- `skills/security/dotnet-cryptography/SKILL.md` (create)
- `agents/dotnet-security-reviewer.md` (create)
- `.claude-plugin/plugin.json` (modify — add 3 skills + 1 agent)

**Files NOT owned by this task (fn-8.1 owns):**
- `skills/security/dotnet-security-owasp/SKILL.md`
- `skills/security/dotnet-secrets-management/SKILL.md`

## Acceptance
- [ ] `dotnet-cryptography` skill at `skills/security/dotnet-cryptography/SKILL.md` with frontmatter (`name`, `description`)
- [ ] Crypto skill covers: hashing, symmetric (AES-GCM), asymmetric (RSA, ECDSA), key derivation
- [ ] Crypto skill has TFM-aware post-quantum section: ML-KEM, ML-DSA, SLH-DSA for net10.0+, fallback strategy for net8.0/net9.0
- [ ] Crypto skill documents interoperability caveats for PQ algorithms
- [ ] Crypto skill warns against deprecated crypto APIs (MD5, SHA1, DES, RC2) and cross-references OWASP for full deprecated pattern list
- [ ] Crypto skill has: scope boundary, prerequisites, ≥2 code examples, gotchas/pitfalls, cross-references, references
- [ ] Crypto skill includes ASP.NET Core security documentation links in references
- [ ] Cross-references verified by grep:
  - `grep "skill:dotnet-security-owasp" skills/security/dotnet-cryptography/SKILL.md` -- match
  - `grep "skill:dotnet-secrets-management" skills/security/dotnet-cryptography/SKILL.md` -- match
- [ ] `dotnet-security-reviewer` agent at `agents/dotnet-security-reviewer.md` with complete frontmatter (name, description, model, capabilities, tools)
- [ ] Agent preloads verified by grep:
  - `grep "skill:dotnet-security-owasp" agents/dotnet-security-reviewer.md` -- match
  - `grep "skill:dotnet-secrets-management" agents/dotnet-security-reviewer.md` -- match
  - `grep "skill:dotnet-cryptography" agents/dotnet-security-reviewer.md` -- match
  - `grep "skill:dotnet-advisor" agents/dotnet-security-reviewer.md` -- match
- [ ] Agent has deterministic review workflow and read-only constraints
- [ ] Agent follows existing pattern from `agents/dotnet-architect.md`
- [ ] 3 skills registered: `grep -c "skills/security/" .claude-plugin/plugin.json` returns 3
- [ ] Agent registered: `grep -c "dotnet-security-reviewer" .claude-plugin/plugin.json` returns 1

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
