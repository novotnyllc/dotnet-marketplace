# fn-10-version-detection-and-multi-targeting.2 Version upgrade guidance skill

## Description
Create `skills/multi-targeting/dotnet-version-upgrade/SKILL.md` — a comprehensive skill for .NET version upgrade guidance with defined upgrade lanes.

The skill consumes output from `dotnet-version-detection` (current TFM, SDK version, preview flags) and provides actionable upgrade guidance based on three upgrade lanes:
1. **Production (LTS→LTS):** net8.0 → net10.0 — direct upgrade for most apps
2. **Staged production:** net8.0 → net9.0 → net10.0 — when ecosystem dependencies require incremental migration
3. **Experimental:** net10.0 → net11.0 (preview) — non-production exploration of upcoming features

**Pattern reference:** Follow the structure of `skills/security/dotnet-secrets-management/SKILL.md` — frontmatter, overview with scope/out-of-scope/cross-references, detailed sections with code examples, gotchas, prerequisites, references.

### Files to Create
- `skills/multi-targeting/dotnet-version-upgrade/SKILL.md`

### Files NOT to Modify
- `skills/foundation/dotnet-version-detection/SKILL.md` (already has cross-references)

## Acceptance
- [ ] SKILL.md created at `skills/multi-targeting/dotnet-version-upgrade/SKILL.md`
- [ ] Frontmatter has `name: dotnet-version-upgrade` and `description` following WHEN/WHEN NOT pattern
- [ ] Three upgrade lanes documented with explicit guardrails:
  - Production: net8.0 → net10.0 (LTS-to-LTS, recommended default)
  - Staged: net8.0 → net9.0 → net10.0 (when ecosystem requires incremental steps)
  - Experimental: net10.0 → net11.0 preview (non-production only, explicit warnings)
- [ ] .NET 9 documented as valid staging option (STS, end-of-support May 2026), not skipped
- [ ] Upgrade checklist per lane: TFM update, package updates, breaking change review, deprecated API replacement, test validation
- [ ] `dotnet-outdated` or equivalent tooling documented for detecting stale packages
- [ ] .NET Upgrade Assistant coverage (when useful, limitations)
- [ ] Breaking change detection patterns: `dotnet build` warnings, analyzer diagnostics, API diff tools
- [ ] Preview feature opt-in guidance: `LangVersion=preview`, `EnablePreviewFeatures`, runtime-async flag
- [ ] Gotchas section with at least 5 agent-relevant gotchas (e.g., STS support windows, preview feature stability, TFM-conditional package references)
- [ ] Cross-references to `[skill:dotnet-version-detection]` and `[skill:dotnet-multi-targeting]`
- [ ] Prerequisites section
- [ ] References section with source URLs
- [ ] No TFM/SDK detection algorithm implemented — guidance consumes `dotnet-version-detection` output only
- [ ] "Last verified" date included in skill references/metadata

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
