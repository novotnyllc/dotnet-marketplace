# Batch B Findings: Architecture, Serialization, Security, Multi-Targeting

## Summary

| Metric | Count |
|--------|-------|
| Skills reviewed | 19 |
| Clean | 6 |
| Needs Work | 7 |
| Critical | 6 |
| Total issues | 19 |
| Critical issues | 8 |
| High issues | 4 |
| Low issues | 7 |

## Current Description Budget Impact

| Metric | Value |
|--------|-------|
| Total description chars (this batch) | 2,576 |
| Skills over 120 chars | 12 |
| Projected savings if all trimmed to 120 | 322 chars |

Skills over 120 chars (FAIL, >140): dotnet-version-upgrade (197), dotnet-multi-targeting (196), dotnet-cryptography (154), dotnet-service-communication (145), dotnet-grpc (142), dotnet-secrets-management (141).

Skills over 120 chars (WARN, 121-140): dotnet-realtime-communication (139), dotnet-serialization (135), dotnet-containers (134), dotnet-data-access-strategy (128), dotnet-efcore-architecture (126), dotnet-security-owasp (125).

Character counts measured using Python regex extraction from YAML frontmatter (strips quotes, trims whitespace).

## Findings by Skill

### architecture

### dotnet-architecture-patterns

**Category:** architecture
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 116 chars -- under limit, follows formula |
| 2 | Description Triggering | pass | Good trigger phrases (vertical slices, minimal API, caching, idempotency) |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 1,869 words -- under threshold |
| 5 | Cross-References | pass | 7 refs, all resolve correctly |
| 6 | Error Handling | warn | No Agent Gotchas section -- 9 of 10 architecture peers have one; domain has common pitfalls (idempotency race conditions, caching invalidation) |
| 7 | Examples | pass | 16 code blocks with real C# examples |
| 8 | Composability | pass | Out-of-scope marker present |
| 9 | Consistency | warn | Missing Agent Gotchas section that all 9 architecture peers have |
| 10 | Registration & Budget | pass | 116 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,869 words |

**Issues:**
- [High] No Agent Gotchas section -- all 9 architecture category peers have one (6-7 items each). Domain covers idempotency, caching, and outbox patterns where agent mistakes are common. Add an Agent Gotchas section covering at minimum: idempotency three-state handling, cache invalidation patterns, outbox message ordering.
- [Low] Missing Anti-Patterns section that would complement the pattern guidance (peer skills also lack this, so not a consistency issue)

---

### dotnet-background-services

**Category:** architecture
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 116 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 1,690 words |
| 5 | Cross-References | pass | 5 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 6 items |
| 7 | Examples | pass | 14 code blocks |
| 8 | Composability | pass | Out-of-scope marker present |
| 9 | Consistency | pass | Matches architecture category structure |
| 10 | Registration & Budget | pass | 116 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,690 words |

**Issues:**
(none)

---

### dotnet-resilience

**Category:** architecture
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 120 chars -- exactly at limit |
| 2 | Description Triggering | pass | Good trigger phrases (Polly, retry, circuit breaker) |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 1,587 words |
| 5 | Cross-References | pass | 6 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 6 items |
| 7 | Examples | pass | 16 code blocks |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 120 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,587 words |

**Issues:**
(none)

---

### dotnet-http-client

**Category:** architecture
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 117 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 1,813 words |
| 5 | Cross-References | pass | 4 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 6 items |
| 7 | Examples | pass | 19 code blocks |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 117 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,813 words |

**Issues:**
(none)

---

### dotnet-observability

**Category:** architecture
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 112 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 2,071 words |
| 5 | Cross-References | pass | 6 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 6 items |
| 7 | Examples | pass | 18 code blocks |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 112 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 2,071 words |

**Issues:**
(none)

---

### dotnet-efcore-patterns

**Category:** architecture
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 115 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 1,995 words |
| 5 | Cross-References | pass | 5 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 7 items |
| 7 | Examples | pass | 22 code blocks |
| 8 | Composability | pass | Clear scope boundary with dotnet-efcore-architecture |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 115 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,995 words |

**Issues:**
(none)

---

### dotnet-efcore-architecture

**Category:** architecture
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 126 chars (121-140 = warn) |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 2,366 words |
| 5 | Cross-References | pass | 5 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 7 items |
| 7 | Examples | pass | 14 code blocks |
| 8 | Composability | pass | Clear scope boundary with dotnet-efcore-patterns |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | warn | 126 chars -- 6 chars over 120 limit |
| 11 | Progressive Disclosure Compliance | pass | 2,366 words |

**Issues:**
- [Low] Description at 126 chars is 6 over the 120-char target -- trim "row limits" or condense phrasing

**Proposed description (119 chars):** `"WHEN designing data layer architecture. Read/write split, aggregate boundaries, repository policy, N+1 governance."`

---

### dotnet-data-access-strategy

**Category:** architecture
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 128 chars (121-140 = warn) |
| 2 | Description Triggering | pass | Good trigger (choosing data access approach) |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 2,165 words |
| 5 | Cross-References | pass | 5 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 7 items |
| 7 | Examples | pass | 11 code blocks |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | warn | 128 chars -- 8 over limit |
| 11 | Progressive Disclosure Compliance | pass | 2,165 words |

**Issues:**
- [Low] Description at 128 chars is 8 over target -- trim "AOT compatibility" or condense

**Proposed description (118 chars):** `"WHEN choosing a data access approach. EF Core vs Dapper vs ADO.NET decision framework, performance tradeoffs."`

---

### dotnet-containers

**Category:** architecture
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 134 chars (121-140 = warn) |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 1,553 words |
| 5 | Cross-References | pass | 6 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 7 items |
| 7 | Examples | pass | 16 code blocks |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | warn | 134 chars -- 14 over limit |
| 11 | Progressive Disclosure Compliance | pass | 1,553 words |

**Issues:**
- [Low] Description at 134 chars is 14 over target -- remove "health checks" (covered by dotnet-observability) or condense

**Proposed description (119 chars):** `"WHEN containerizing .NET apps. Multi-stage Dockerfiles, dotnet publish container images (.NET 8+), rootless containers."`

---

### dotnet-container-deployment

**Category:** architecture
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 118 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 1,495 words |
| 5 | Cross-References | pass | 10 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 7 items |
| 7 | Examples | pass | 15 code blocks |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 118 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,495 words |

**Issues:**
(none)

---

### serialization

### dotnet-grpc

**Category:** serialization
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 142 chars (>140 = fail) |
| 2 | Description Triggering | pass | Good trigger phrases |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 2,312 words |
| 5 | Cross-References | pass | 8 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 7 items |
| 7 | Examples | pass | 26 code blocks -- comprehensive |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | fail | 142 chars exceeds 140-char fail threshold |
| 11 | Progressive Disclosure Compliance | pass | 2,312 words |

**Issues:**
- [Critical] Description at 142 chars exceeds 140-char fail threshold -- trim "health checks" (covered by dotnet-observability) and condense

**Proposed description (119 chars):** `"WHEN building gRPC services. Proto definition, code-gen, ASP.NET Core server, Grpc.Net.Client, streaming, auth."`

---

### dotnet-realtime-communication

**Category:** serialization
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 139 chars (121-140 = warn) |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 1,615 words |
| 5 | Cross-References | pass | 8 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 7 items |
| 7 | Examples | pass | 14 code blocks |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | warn | 139 chars -- 19 over limit |
| 11 | Progressive Disclosure Compliance | pass | 1,615 words |

**Issues:**
- [Low] Description at 139 chars is 19 over target -- condense protocol list

**Proposed description (117 chars):** `"WHEN choosing real-time protocols. SignalR, SSE (.NET 10), JSON-RPC 2.0, gRPC streaming -- decision guidance."`

---

### dotnet-serialization

**Category:** serialization
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 135 chars (121-140 = warn) |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 1,574 words |
| 5 | Cross-References | pass | 7 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 6 items |
| 7 | Examples | pass | 16 code blocks |
| 8 | Composability | pass | Anti-patterns section present |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | warn | 135 chars -- 15 over limit |
| 11 | Progressive Disclosure Compliance | pass | 1,574 words |

**Issues:**
- [Low] Description at 135 chars is 15 over target -- trim "Performance tradeoffs and anti-patterns"

**Proposed description (116 chars):** `"WHEN serializing data. AOT-friendly System.Text.Json source generators, Protobuf, MessagePack anti-patterns."`

---

### dotnet-service-communication

**Category:** serialization
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 145 chars (>140 = fail) -- over limit |
| 2 | Description Triggering | pass | Good trigger (choosing communication protocol) |
| 3 | Instruction Clarity | pass | Decision matrix is clear and actionable |
| 4 | Progressive Disclosure | pass | 1,254 words -- well under threshold |
| 5 | Cross-References | pass | 9 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 7 items |
| 7 | Examples | warn | Only 4 code blocks -- router skill but could benefit from more concrete routing examples |
| 8 | Composability | pass | Routes to deeper skills appropriately |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | fail | 145 chars exceeds 140-char fail threshold |
| 11 | Progressive Disclosure Compliance | pass | 1,254 words |

**Issues:**
- [Critical] Description at 145 chars exceeds 140-char fail threshold -- condense; remove "with routing to deeper skills" (that is implied by the skill's role)

**Proposed description (116 chars):** `"WHEN choosing a communication protocol. Decision matrix mapping requirements to gRPC, SignalR, SSE, JSON-RPC, REST."`

---

### security

### dotnet-security-owasp

**Category:** security
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 125 chars (121-140 = warn) |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 2,437 words |
| 5 | Cross-References | pass | 5 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 8 items |
| 7 | Examples | pass | 20 code blocks |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | warn | 125 chars -- 5 over limit |
| 11 | Progressive Disclosure Compliance | pass | 2,437 words |

**Issues:**
- [Low] Description at 125 chars is 5 over target -- remove "(2021)" year reference (will become stale)

**Proposed description (118 chars):** `"WHEN writing secure .NET code or reviewing for vulnerabilities. OWASP Top 10 mitigations, deprecated pattern warnings."`

---

### dotnet-secrets-management

**Category:** security
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 141 chars (>140 = fail) |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 1,755 words |
| 5 | Cross-References | pass | 3 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 8 items |
| 7 | Examples | pass | 20 code blocks |
| 8 | Composability | pass | Anti-patterns section present |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | fail | 141 chars exceeds 140-char fail threshold |
| 11 | Progressive Disclosure Compliance | pass | 1,755 words |

**Issues:**
- [Critical] Description at 141 chars exceeds 140-char fail threshold -- trim "IConfiguration binding, rotation" or condense

**Proposed description (119 chars):** `"WHEN handling secrets, connection strings, or sensitive configuration. User secrets, environment variables, rotation."`

---

### dotnet-cryptography

**Category:** security
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 154 chars (>140 = fail) -- lists too many algorithms |
| 2 | Description Triggering | pass | Good trigger phrases |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 2,152 words |
| 5 | Cross-References | pass | 2 refs, all resolve |
| 6 | Error Handling | warn | No Agent Gotchas section -- security/crypto is one of the most error-prone domains; peer skill dotnet-secrets-management has 8 gotchas |
| 7 | Examples | pass | 11 code blocks |
| 8 | Composability | pass | Out-of-scope markers present |
| 9 | Consistency | warn | Missing Agent Gotchas section that peer security skills have (dotnet-security-owasp: 8 items, dotnet-secrets-management: 8 items) |
| 10 | Registration & Budget | fail | 154 chars exceeds 140-char fail threshold |
| 11 | Progressive Disclosure Compliance | pass | 2,152 words |

**Issues:**
- [Critical] Description at 154 chars exceeds 140-char fail threshold -- remove individual algorithm names (ML-KEM, ML-DSA, SLH-DSA) and condense
- [High] No Agent Gotchas section in the most error-prone security domain. Cryptographic pitfalls are abundant: using ECB mode, hardcoded IVs, incorrect key derivation iteration counts, using SHA-1 for security, not using constant-time comparison for HMAC validation. Add Agent Gotchas with at minimum 6-8 items.

**Proposed description (114 chars):** `"WHEN choosing cryptographic algorithms, hashing, encryption, or key derivation in .NET. AES-GCM, RSA, ECDSA, PQC."`

---

### multi-targeting

### dotnet-multi-targeting

**Category:** multi-targeting
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 196 chars (>140 = fail) -- includes WHEN NOT clause which wastes budget |
| 2 | Description Triggering | warn | Overly specific WHEN clause limits activation; WHEN NOT clause is unconventional |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 2,254 words |
| 5 | Cross-References | pass | 2 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 10 items |
| 7 | Examples | pass | 20 code blocks |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | Consistent with dotnet-version-upgrade peer |
| 10 | Registration & Budget | fail | NOT registered in plugin.json -- skill is invisible to the plugin system |
| 11 | Progressive Disclosure Compliance | pass | 2,254 words |

**Issues:**
- [Critical] NOT registered in plugin.json `skills` array -- skill files exist on disk but are invisible to the plugin system
- [Critical] Description at 196 chars massively exceeds 140-char fail threshold -- WHEN NOT clause adds 76 chars of negative space
- [High] WHEN NOT clause is unconventional and wastes budget -- remove it

**Proposed description (115 chars):** `"WHEN project targets multiple TFMs or needs newer C# features on older TFMs. Polyfill strategy, API compat."`

---

### dotnet-version-upgrade

**Category:** multi-targeting
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 197 chars (>140 = fail) -- includes WHEN NOT clause which wastes budget |
| 2 | Description Triggering | warn | WHEN NOT clause adds no discrimination value |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | 2,325 words |
| 5 | Cross-References | pass | 2 refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas section with 10 items |
| 7 | Examples | pass | 18 code blocks |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | Consistent with dotnet-multi-targeting peer |
| 10 | Registration & Budget | fail | NOT registered in plugin.json -- skill is invisible to the plugin system |
| 11 | Progressive Disclosure Compliance | pass | 2,325 words |

**Issues:**
- [Critical] NOT registered in plugin.json `skills` array -- skill files exist on disk but are invisible to the plugin system
- [Critical] Description at 197 chars massively exceeds 140-char fail threshold -- WHEN NOT clause adds significant waste
- [High] WHEN NOT clause is unconventional and adds no value -- remove it

**Proposed description (118 chars):** `"WHEN upgrading a .NET project to a newer TFM or evaluating upgrade paths. LTS-to-LTS, staged through STS, preview."`

---

## Cross-Cutting Observations

1. **Unregistered multi-targeting skills:** Both `dotnet-multi-targeting` and `dotnet-version-upgrade` exist on disk but are NOT registered in `plugin.json`. This means they are invisible to the plugin system despite having complete, high-quality content (10 Agent Gotchas each, 18-20 code blocks). This is the highest-priority fix in this batch.

2. **Description budget pressure is severe in this batch:** 12 of 19 skills (63%) exceed the 120-char target. Six exceed the 140-char fail threshold. The multi-targeting skills are the worst offenders at 196 and 197 chars respectively. Trimming all to 120 chars would save 322 chars from the aggregate budget (currently at 12,458).

3. **WHEN NOT clauses in descriptions:** Both multi-targeting skills use "WHEN NOT" negative clauses in their descriptions. This pattern was also flagged in Batch A (3 foundation skills). The WHEN NOT information adds no discrimination value and wastes budget characters. This appears to be a systematic pattern in skills authored during the same period.

4. **Agent Gotchas coverage is strong but has two gaps:** 17 of 19 skills have Agent Gotchas sections (89%). The two missing skills are `dotnet-architecture-patterns` and `dotnet-cryptography`. The cryptography gap is more concerning because cryptographic errors are among the most dangerous security mistakes an agent can make.

5. **Cross-reference quality is excellent:** All 38 unique cross-reference targets across the batch resolve to existing skills. No broken references. No bare-text skill name references to other skills (only self-references in headings, which is expected).

6. **Consistent architecture category quality:** 6 of 10 architecture skills are Clean. The remaining 4 have only description-length warnings. The category has consistent structure: all have Agent Gotchas (except dotnet-architecture-patterns), out-of-scope markers, and proper cross-references.

7. **No details.md companions needed:** All 19 skills are under the 5,000-word limit. The highest is `dotnet-security-owasp` at 2,437 words, which is approaching the 3,000-word suggestion threshold but does not yet require extraction.

8. **Serialization category has the most Critical issues:** 2 of 4 serialization skills are Critical due to description length (dotnet-grpc at 142, dotnet-service-communication at 145). The other 2 are Needs Work for description warnings.

9. **Anti-Patterns sections are rare:** Only `dotnet-serialization` and `dotnet-secrets-management` have anti-pattern content. This is not a consistency issue since no category mandates anti-patterns sections, but the absence is notable in architecture skills where anti-patterns are common (e.g., service locator, ambient context).

## Recommended Changes

### Critical (must fix)
- Register `dotnet-multi-targeting` in `.claude-plugin/plugin.json` `skills` array -- skill is invisible without registration
- Register `dotnet-version-upgrade` in `.claude-plugin/plugin.json` `skills` array -- skill is invisible without registration
- Trim `dotnet-multi-targeting` description from 196 to under 120 chars -- remove WHEN NOT clause
- Trim `dotnet-version-upgrade` description from 197 to under 120 chars -- remove WHEN NOT clause
- Trim `dotnet-cryptography` description from 154 to under 120 chars -- remove individual PQC algorithm names
- Trim `dotnet-grpc` description from 142 to under 120 chars -- remove "health checks"
- Trim `dotnet-service-communication` description from 145 to under 120 chars -- remove "with routing to deeper skills"
- Trim `dotnet-secrets-management` description from 141 to under 120 chars -- condense

### High (should fix)
- Add Agent Gotchas section to `dotnet-cryptography` -- most error-prone security domain lacks agent pitfall guidance
- Add Agent Gotchas section to `dotnet-architecture-patterns` -- all 9 architecture peers have one; covers idempotency, caching, outbox where agent errors are common
- Remove WHEN NOT clause from `dotnet-multi-targeting` description
- Remove WHEN NOT clause from `dotnet-version-upgrade` description
- Trim `dotnet-realtime-communication` description from 139 to under 120 chars
- Trim `dotnet-serialization` description from 135 to under 120 chars
- Trim `dotnet-containers` description from 134 to under 120 chars

### Low (nice to have)
- Trim `dotnet-data-access-strategy` description from 128 to under 120 chars
- Trim `dotnet-efcore-architecture` description from 126 to under 120 chars
- Trim `dotnet-security-owasp` description from 125 to under 120 chars -- remove "(2021)" year reference
- Monitor `dotnet-security-owasp` (2,437 words) and `dotnet-efcore-architecture` (2,366 words) for details.md extraction if content grows
- Consider adding Anti-Patterns sections to architecture skills where anti-patterns are well-established (service locator, ambient context, god DbContext)
