# fn-34-msbuild-and-build-system-skills.3 Build optimization skill + integration (plugin registration, docs update)

## Description
Create `skills/build-system/dotnet-build-optimization/SKILL.md` covering build optimization and diagnostics. Key focus: diagnosing incremental build failures, binary log analysis, parallel builds, and common build performance pitfalls. Also serves as the **integration task**: registers all 3 fn-34 skills in `plugin.json`, updates README.md and CLAUDE.md with new category/skill counts.

**Size:** M
**Files:** `skills/build-system/dotnet-build-optimization/SKILL.md`, `.claude-plugin/plugin.json` (sole owner), `README.md`, `CLAUDE.md`
**Depends on:** fn-34.1 and fn-34.2 (cross-references their skills)

## Approach
- Incremental build diagnostics: warning → `/bl` binary log → MSBuild Structured Log Viewer → root cause → fix
- Common failures: targets without Inputs/Outputs, file copy timestamps, generators writing mid-build
- Binary log analysis: `dotnet build /bl`, MSBuild Structured Log Viewer, `msbuild -pp` preprocessed project
- Parallel build: `/m`, `/graph` mode, `BuildInParallel` property
- Build caching: SDK artifact caching, restore optimization
- Scope boundary: NoWarn/TreatWarningsAsErrors configuration strategy only; detecting misuse → cross-ref `[skill:dotnet-build-analysis]`
- Scope boundary: NuGet restore optimization patterns only; lock files and CPM → cross-ref `[skill:dotnet-project-structure]`
- Cross-ref to `[skill:dotnet-msbuild-authoring]` and `[skill:dotnet-msbuild-tasks]` (soft — same epic)
- Cross-ref to `[skill:dotnet-build-analysis]` (hard — exists)
- Each section uses explicit `##` headers
- Include Agent Gotchas section (build optimization pitfalls)
- Include References section with Microsoft Learn links

**Integration responsibilities:**
- Register all 3 skill paths in `.claude-plugin/plugin.json` skills array
- Update README.md: add `build-system` category, update total skill count (101 → 104), update category count (19 → 20)
- Update CLAUDE.md: update skill/category counts
- Run all four validation commands

## Acceptance
- [ ] Incremental build failure diagnosis workflow (warning → `/bl` → root cause → fix)
- [ ] Common incremental build failure patterns listed with fixes
- [ ] Binary log analysis (`dotnet build /bl`, Structured Log Viewer) documented
- [ ] Preprocessed project (`-pp`) documented
- [ ] Parallel builds (`/m`, `/graph`, BuildInParallel) documented
- [ ] Build caching and restore optimization documented
- [ ] Scope boundary: error interpretation → `[skill:dotnet-build-analysis]`
- [ ] Scope boundary: lock files/CPM → `[skill:dotnet-project-structure]`
- [ ] Cross-refs to `[skill:dotnet-msbuild-authoring]` and `[skill:dotnet-msbuild-tasks]` present
- [ ] Agent Gotchas section with build optimization pitfalls
- [ ] References section with Microsoft Learn links
- [ ] All cross-references use `[skill:name]` syntax
- [ ] SKILL.md frontmatter has `name` and `description` only
- [ ] Description under 120 characters
- [ ] All 3 skills registered in `plugin.json`
- [ ] README.md updated with new category and counts
- [ ] CLAUDE.md updated with new counts
- [ ] All four validation commands pass

## Validation
```bash
# Verify skill file exists and has required frontmatter
grep -q '^name: dotnet-build-optimization' skills/build-system/dotnet-build-optimization/SKILL.md
grep -q '^description:' skills/build-system/dotnet-build-optimization/SKILL.md

# Verify scope boundary cross-refs
grep -c '\[skill:dotnet-build-analysis\]' skills/build-system/dotnet-build-optimization/SKILL.md
grep -c '\[skill:dotnet-project-structure\]' skills/build-system/dotnet-build-optimization/SKILL.md

# Verify Agent Gotchas section exists
grep -q '## .*Gotcha' skills/build-system/dotnet-build-optimization/SKILL.md

# Verify References section exists
grep -q '## References' skills/build-system/dotnet-build-optimization/SKILL.md

# Verify plugin.json registration (all 3 skills)
grep -c 'build-system/dotnet-msbuild-authoring' .claude-plugin/plugin.json
grep -c 'build-system/dotnet-msbuild-tasks' .claude-plugin/plugin.json
grep -c 'build-system/dotnet-build-optimization' .claude-plugin/plugin.json

# Run all four validation commands
./scripts/validate-skills.sh && \
./scripts/validate-marketplace.sh && \
python3 scripts/generate_dist.py --strict && \
python3 scripts/validate_cross_agent.py
```

## Done summary
Created dotnet-build-optimization skill covering incremental build diagnosis workflow, binary log analysis, parallel builds, build caching, and restore optimization. Registered all 3 build-system skills in plugin.json and updated README.md/CLAUDE.md counts (101->104 skills, 19->20 categories).
## Evidence
- Commits: 936b69d, b5cc96c
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: