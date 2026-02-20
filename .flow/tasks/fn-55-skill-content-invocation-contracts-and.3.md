# fn-55-skill-content-invocation-contracts-and.3 Update high-traffic skills with stronger invocation signals

## Description
Update the 14 skills in cases.json corpus with stronger invocation signals per the invocation contract spec.

**Size:** M
**Files:** Multiple SKILL.md files (14 skills), `skills/foundation/dotnet-advisor/SKILL.md`

## Approach

- Exact 14 skills from cases.json:
  1. `dotnet-version-detection` 2. `dotnet-xunit` 3. `dotnet-gha-build-test` 4. `dotnet-minimal-apis`
  5. `dotnet-architecture-patterns` 6. `dotnet-security-owasp` 7. `dotnet-benchmarkdotnet` 8. `dotnet-blazor-components`
  9. `dotnet-efcore-patterns` 10. `dotnet-msbuild-authoring` 11. `dotnet-trimming` 12. `dotnet-system-commandline`
  13. `dotnet-advisor` 14. `dotnet-uno-mcp`
- Strengthen Scope (≥1 `- ` bullet) and OOS (≥1 `- ` bullet with `[skill:name]`)
- dotnet-advisor: strengthen routing catalog
- Budget: BUDGET_STATUS != FAIL
- No agents/*.md, no plugin.json

## Key context

- T2 emits `INVOCATION_CONTRACT:` stable prefix per warning — use this for path-scoped verification
- Most skills have Scope/OOS from fn-53 — this strengthens existing content

## Acceptance
- [ ] All 14 skills have ≥1 `- ` bullet in Scope
- [ ] All 14 skills have ≥1 OOS `- ` bullet with `[skill:name]`
- [ ] Zero INVOCATION_CONTRACT warnings for the 14 target files — verifiable:
  ```
  ./scripts/validate-skills.sh 2>&1 | grep "INVOCATION_CONTRACT:" \
    | grep -E "(dotnet-version-detection|dotnet-xunit|dotnet-gha-build-test|dotnet-minimal-apis|dotnet-architecture-patterns|dotnet-security-owasp|dotnet-benchmarkdotnet|dotnet-blazor-components|dotnet-efcore-patterns|dotnet-msbuild-authoring|dotnet-trimming|dotnet-system-commandline|dotnet-advisor|dotnet-uno-mcp)" \
    | wc -l
  ```
  Must output `0`
- [ ] dotnet-advisor routing catalog strengthened
- [ ] `./scripts/validate-skills.sh` passes with 0 errors
- [ ] `BUDGET_STATUS != FAIL`
