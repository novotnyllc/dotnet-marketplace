# fn-64.6 Consolidate dotnet-tooling (~34 source skills)

## Description
Create consolidated `dotnet-tooling` skill directory. Merge ~34 build, performance, AOT, CLI, project setup, docs generation, and meta-skills into one skill with companion files. This is the largest consolidation group. Delete source skill directories. Do NOT edit `plugin.json` (deferred to task .9).

**Size:** M
**Files:** `skills/dotnet-tooling/SKILL.md` + `references/*.md` (new), ~34 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- Write SKILL.md: developer tooling overview, routing table with rich keyword hints, scope/out-of-scope, ToC (~4-5KB given breadth)
- Create `references/` dir. Expected companion files:
  - `references/project-setup.md` — project structure, scaffolding, artifacts output, add-analyzers, add-ci, add-testing, modernize
  - `references/msbuild.md` — MSBuild authoring, tasks, build optimization, build analysis, csproj reading
  - `references/performance.md` — patterns, profiling, GC/memory, LINQ optimization
  - `references/native-aot.md` — Native AOT, AOT architecture, trimming, WASM AOT
  - `references/cli-apps.md` — System.CommandLine, CLI architecture, distribution, packaging, release pipeline
  - `references/terminal-ui.md` — Spectre.Console, Terminal.Gui
  - `references/tool-management.md` — dotnet tool install, local tools, solution navigation
  - `references/documentation.md` — strategy, Mermaid diagrams, GitHub docs, XML docs, API docs
  - `references/version-management.md` — version detection, version upgrade, multi-targeting
  - `references/agent-meta.md` — agent gotchas, slopwatch, build-analysis tips
  - (exact list per task .1 output)
- Delete old skill directories after content is migrated
- **Do NOT edit plugin.json** — manifest update deferred to task .9

## Key context

- This is the broadest consolidation (~34 source skills) — intentionally a grab-bag per epic decision #9
- The SKILL.md routing table must have strong keyword differentiation since sub-topics are diverse
- Several source skills are user-invocable (scaffold-project, add-analyzers, add-ci, add-testing, modernize, slopwatch, version-upgrade) — decide per task .1 which user-invocable designation the consolidated skill gets
- `dotnet-version-detection` and `dotnet-project-analysis` are shared foundations used by 5 agents — companion file must be prominent in ToC
- If post-implementation this feels too broad, splitting into build/performance/cli is a single-task change (epic decision #9)

## Acceptance
- [ ] `skills/dotnet-tooling/SKILL.md` exists with overview, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-tooling/references/` contains ~10 companion files covering all sub-domains
- [ ] All ~34 source tooling skill directories deleted
- [ ] `plugin.json` NOT edited (deferred to task .9)
- [ ] Valid frontmatter
- [ ] No content lost from source skills
- [ ] User-invocable designation decided and set correctly

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
