# fn-65-skill-quality-fine-tuning-eliminate.2 Clean up 145 reference files: normalize titles, remove Scope/OOS, fix stale refs

## Description
Clean up all 145 reference files across the 8 skills: normalize titles, remove Scope/OOS sections, and fix stale cross-references.

**Size:** M (mechanical changes per file, high file count — land this task first to establish clean baseline before other tasks)
**Files:** All `skills/*/references/*.md` files (~145 total)

## Approach

### 1. Normalize titles to human-readable Title Case

Change all 107 slug-style titles from `# dotnet-*` to human-readable Title Case. The `dotnet-csharp` and `dotnet-debugging` skills already use human-readable titles — follow their convention.

**Title casing convention:**
- Use Title Case (capitalize first letter of each significant word)
- Preserve known acronyms: EF, MSBuild, gRPC, WinUI, MAUI, AOT, WPF, WinForms, TUI, LINQ, DI, XML, API, HTTP, CLI, NuGet, MSIX, CI, CD, ADO, GHA, TFM, BOM, SSR, WASM, OIDC, JWT, XAML, MVVM, P/Invoke, etc.
- Prefer short, descriptive titles: `# Minimal APIs`, `# EF Core Patterns`, `# GitHub Actions Patterns`
- Do NOT prefix with "dotnet-" or ".NET" unless the title would be ambiguous without it

**Mapping examples:** `# dotnet-minimal-apis` → `# Minimal APIs`, `# dotnet-efcore-patterns` → `# EF Core Patterns`, `# dotnet-gha-patterns` → `# GitHub Actions Patterns`, `# dotnet-msbuild-authoring` → `# MSBuild Authoring`.

**Files with code fences before the H1 title** (e.g., `skills/dotnet-tooling/references/version-detection.md`, `project-analysis.md`, `solution-navigation.md`): Move the code fence below the H1 title so the title is always the first non-blank line. This simplifies validation and gives Claude immediate context when previewing.

### 2. Remove Scope/OOS sections from reference files

Remove `## Scope` and `## Out of scope` sections from the ~121 reference files that have them. These are holdovers from the standalone skill era and contain 372 stale `[skill:]` refs pointing to 63 deleted skill names.

**Also remove legacy `Cross-references:` lines** that accompanied Scope/OOS blocks (typically the line immediately after OOS). These are the lines formatted as `Cross-references: [skill:dotnet-foo], [skill:dotnet-bar]`.

**Preserve modern standalone cross-reference lines** in files that are already in the modern format (e.g., `dotnet-csharp/references/coding-standards.md` has a `Cross-references:` line without Scope/OOS — leave it as-is).

The 16 `dotnet-debugging` reference files don't have Scope/OOS — skip those.

### 3. Fix remaining stale `[skill:]` refs in body text

After removing Scope/OOS sections, check for any remaining stale `[skill:]` refs in body text (outside code fences). For each:
- If it's a "See also" pointer within the same skill domain, convert to a relative markdown link: `See [Minimal APIs](minimal-apis.md)` or remove if redundant.
- If it crosses skill domains, convert to the current broad skill name: `[skill:dotnet-api]`.

**Important:** Do not flag `[skill:]` refs inside code fences or markdown examples — those are illustrative and should be left alone.

### 4. Verify with grep

After all changes, verify zero stale refs remain (fence-naive quick check — validator will do fence-aware check in Task 4):
```bash
grep -r '\[skill:' skills/*/references/ | grep -v -E '\[skill:(dotnet-advisor|dotnet-api|dotnet-csharp|dotnet-debugging|dotnet-devops|dotnet-testing|dotnet-tooling|dotnet-ui)\]'
```

Note: This quick check may flag legitimate agent refs. The full validator (Task 4) resolves against `known_ids` (skills + agents) for authoritative checking.

## Key context

- Reference files are loaded on-demand by Claude, not at startup. Removing Scope/OOS saves ~10-15 lines per file loaded.
- The validator (`scripts/_validate_skills.py`) does NOT check reference files — so there's no automated gate currently. Task 4 will add one.
- Some reference files have both a title and a `> brief description` line below it. Keep description lines — they serve as a quick summary when Claude previews the file.
- Valid `[skill:]` targets include both skill directory names AND agent file stems (e.g., `[skill:dotnet-architect]` is valid).

## Acceptance
- [ ] All 145 reference files have human-readable Title Case H1 titles (no `# dotnet-*` slugs)
- [ ] Title casing follows convention: Title Case with known acronyms preserved (EF, MSBuild, gRPC, etc.)
- [ ] No reference file is missing an H1 title
- [ ] No reference file has a code fence before its H1 title (moved below)
- [ ] No reference file has a `## Scope` section
- [ ] No reference file has a `## Out of scope` section
- [ ] Legacy `Cross-references:` lines (accompanying Scope/OOS blocks) removed
- [ ] Modern standalone cross-reference lines in already-compliant files preserved
- [ ] Zero stale `[skill:]` refs in reference file body text (only current skill names and agent stems allowed)
- [ ] `grep -r '^\# dotnet-' skills/*/references/*.md` returns zero matches

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
