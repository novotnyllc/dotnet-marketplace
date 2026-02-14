# Library API Compatibility Skills

## Overview
Create skills focused on managing public API surface area for .NET libraries. Covers binary vs source compatibility, type forwarders, API surface validation, and versioning strategy. This extends beyond the existing `dotnet-api-versioning` (HTTP API versioning) into library/NuGet package API management.

## Scope
- **Library API Compatibility skill** — Binary compatibility rules (field layout, virtual dispatch, default interface members), source compatibility (overload resolution, extension method conflicts), SemVer for NuGet packages
- **Type forwarders** — `[TypeForwardedTo]`, `[TypeForwardedFrom]`, migrating types between assemblies without breaking consumers
- **API surface validation** — Using Microsoft.CodeAnalysis.PublicApiAnalyzers (`PublicAPI.Shipped.txt`/`PublicAPI.Unshipped.txt`), Verify for snapshot testing API surfaces, ApiCompat tool
- **Package version strategy** — When to bump major/minor/patch, pre-release version conventions, multi-TFM packaging strategy

**Relation to existing skills**: `dotnet-api-versioning` covers HTTP API versioning (Asp.Versioning). This epic covers library/NuGet package API compatibility — complementary, not overlapping.

## Quick commands
```bash
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
```

## Acceptance
- [ ] Binary vs source compatibility rules documented with concrete examples
- [ ] Type forwarder patterns covered (migration between assemblies)
- [ ] API surface validation with PublicApiAnalyzers and/or Verify
- [ ] Package versioning strategy (SemVer for NuGet)
- [ ] Cross-refs to `[skill:dotnet-api-versioning]` for HTTP API versioning
- [ ] Cross-refs to `[skill:dotnet-roslyn-analyzers]` for analyzer-based validation
- [ ] No fn-N spec references
- [ ] Budget constraint respected
- [ ] All validation commands pass

## References
- Microsoft.CodeAnalysis.PublicApiAnalyzers — API surface tracking
- `skills/api/dotnet-api-versioning/SKILL.md` — HTTP API versioning (complementary)
- `skills/testing/dotnet-snapshot-testing/SKILL.md` — Verify for API surface snapshots
