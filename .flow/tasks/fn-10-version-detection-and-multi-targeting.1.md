# fn-10-version-detection-and-multi-targeting.1 Multi-targeting with polyfills skill

## Description
Create `skills/multi-targeting/dotnet-multi-targeting/SKILL.md` — a comprehensive skill for .NET multi-targeting strategies with a polyfill-first approach.

The skill consumes output from `dotnet-version-detection` (TFM, C# version, preview flags) and provides actionable guidance on:
1. When and how to use PolySharp and SimonCropp/Polyfill for language feature backporting
2. When conditional compilation (`#if`) is necessary (runtime/API behavior gaps)
3. API compatibility validation with `EnablePackageValidation` and `ApiCompat`
4. Multi-targeting `.csproj` setup patterns

**Pattern reference:** Follow the structure of `skills/security/dotnet-secrets-management/SKILL.md` — frontmatter, overview with scope/out-of-scope/cross-references, detailed sections with code examples, gotchas, prerequisites, references.

### Files to Create
- `skills/multi-targeting/dotnet-multi-targeting/SKILL.md`

### Files NOT to Modify
- `skills/foundation/dotnet-version-detection/SKILL.md` (already has cross-references)

## Acceptance
- [ ] SKILL.md created at `skills/multi-targeting/dotnet-multi-targeting/SKILL.md`
- [ ] Frontmatter has `name: dotnet-multi-targeting` and `description` following WHEN/WHEN NOT pattern
- [ ] Decision matrix: polyfill vs conditional compilation vs adapter pattern for each gap type (language, BCL API, runtime behavior, platform API)
- [ ] PolySharp section: package reference, what it provides (compiler-synthesized polyfills for `required`, `init`, `SetsRequiredMembers`, etc.), setup in .csproj
- [ ] SimonCropp/Polyfill section: package reference, what it provides (BCL API polyfills like `System.Threading.Lock`), setup in .csproj
- [ ] Conditional compilation section: when `#if` is correct (runtime gaps), patterns for TFM-specific code
- [ ] API compatibility section: `EnablePackageValidation` setup, `ApiCompat` baseline workflow, pass/fail interpretation
- [ ] Multi-targeting .csproj patterns: `<TargetFrameworks>`, conditional `<PackageReference>`, TFM-specific source files
- [ ] Gotchas section with at least 5 agent-relevant gotchas
- [ ] Cross-references to `[skill:dotnet-version-detection]` and `[skill:dotnet-version-upgrade]`
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
