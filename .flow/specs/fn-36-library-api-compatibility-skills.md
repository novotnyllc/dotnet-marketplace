# Library API Compatibility Skills

## Overview
Create skills focused on managing public API surface area for .NET libraries. Covers binary vs source compatibility, type forwarders, API surface validation, and versioning strategy. This extends beyond the existing `dotnet-api-versioning` (HTTP API versioning) into library/NuGet package API management.

## Scope
- **Library API Compatibility skill** — Binary compatibility rules (field layout, virtual dispatch, default interface members), source compatibility (overload resolution, extension method conflicts), type forwarders
- **API surface validation** — PublicApiAnalyzers (`PublicAPI.Shipped.txt`/`PublicAPI.Unshipped.txt`), Verify for snapshot testing API surfaces, CI enforcement workflow

### Scope Boundary Table

| Concern | This Epic Owns | Cross-Refs To |
|---------|---------------|---------------|
| Binary/source compat rules | Full ownership | — |
| Type forwarders | Full ownership | — |
| SemVer for NuGet | Summary + cross-ref | `[skill:dotnet-nuget-authoring]` |
| Multi-TFM packaging | How TFM choices affect binary compat only | `[skill:dotnet-multi-targeting]`, `[skill:dotnet-nuget-authoring]` |
| EnablePackageValidation / ApiCompat basics | Brief mention + cross-ref | `[skill:dotnet-nuget-authoring]`, `[skill:dotnet-multi-targeting]` |
| PublicApiAnalyzers (RS0016/RS0017 lifecycle) | Full ownership | `[skill:dotnet-roslyn-analyzers]` for general analyzer config |
| Verify for API surface snapshots | API surface snapshot pattern | `[skill:dotnet-snapshot-testing]` for Verify fundamentals |
| ApiCompat CI enforcement workflow | Unique CI gating workflow | `[skill:dotnet-multi-targeting]` for tool basics |
| HTTP API versioning | Out of scope | `[skill:dotnet-api-versioning]` |

## Out of Scope
- HTTP API versioning (covered by `[skill:dotnet-api-versioning]`)
- NuGet feed configuration and publish workflows
- CI/CD publish pipelines
- Detailed SemVer rules (covered by `[skill:dotnet-nuget-authoring]`)
- Multi-TFM packaging mechanics (covered by `[skill:dotnet-multi-targeting]`)
- Verify fundamentals — setup, scrubbing, converters (covered by `[skill:dotnet-snapshot-testing]`)
- General analyzer configuration (covered by `[skill:dotnet-roslyn-analyzers]`)

## Dependencies
- **Hard:** fn-2 (Plugin Skeleton — plugin.json infrastructure, already complete)
- **Soft:** None — all referenced skills already exist

## .NET Version Policy
- Baseline: .NET 8.0+
- No version-gated content

## Task Decomposition

| Task | Skill Path | Size | Depends On |
|------|-----------|------|------------|
| 1 | `skills/api-development/dotnet-library-api-compat/SKILL.md` | M | — |
| 2 | `skills/api-development/dotnet-api-surface-validation/SKILL.md` | M | Task 1 |
| 3 | `plugin.json` registration, `dotnet-advisor` catalog, `AGENTS.md` counts, trigger-corpus | S | Tasks 1, 2 |

## Conventions
- Category: `api-development` (matches existing `dotnet-api-versioning`)
- Cross-refs use `[skill:skill-name]` syntax
- Description under 120 characters per skill
- Each skill must include Agent Gotchas, Prerequisites, and References sections
- Skills follow CONTRIBUTING-SKILLS.md patterns

## Quick commands
```bash
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
```

## Acceptance
- [ ] Binary vs source compatibility rules documented with concrete examples
- [ ] Type forwarder patterns covered (migration between assemblies)
- [ ] PublicApiAnalyzers workflow documented (RS0016/RS0017 shipped/unshipped lifecycle)
- [ ] Verify API surface snapshot pattern documented (cross-ref to `[skill:dotnet-snapshot-testing]` for fundamentals)
- [ ] ApiCompat CI enforcement workflow (cross-ref to `[skill:dotnet-multi-targeting]` for tool basics)
- [ ] Cross-refs to `[skill:dotnet-api-versioning]` for HTTP API versioning
- [ ] Cross-refs to `[skill:dotnet-roslyn-analyzers]` for analyzer-based validation
- [ ] Both skills added to `dotnet-advisor` catalog under API Development section
- [ ] No fn-N epic references in SKILL.md body text (verified with `grep -r 'fn-[0-9]' skills/api-development/dotnet-library-api-compat/ skills/api-development/dotnet-api-surface-validation/`)
- [ ] Budget constraint respected (descriptions under 120 chars each)
- [ ] All validation commands pass

## References
- Microsoft.CodeAnalysis.PublicApiAnalyzers — API surface tracking
- `skills/api-development/dotnet-api-versioning/SKILL.md` — HTTP API versioning (complementary)
- `skills/testing/dotnet-snapshot-testing/SKILL.md` — Verify for API surface snapshots
- `skills/packaging/dotnet-nuget-authoring/SKILL.md` — SemVer, EnablePackageValidation
- `skills/multi-targeting/dotnet-multi-targeting/SKILL.md` — Multi-TFM, ApiCompat tool
