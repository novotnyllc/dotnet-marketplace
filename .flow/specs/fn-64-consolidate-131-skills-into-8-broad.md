# Consolidate 131 Skills into 8 Broad Skills

## Overview

The plugin has 131 individual skills consuming 75% of the 15,600-char routing description budget. Research shows Tier 1 plugin repos converge on 5-16 skills (Vercel: 6, kepano/obsidian: 5, anthropics/skills: 16). RAG-MCP research shows routing accuracy drops from 43% to 13% with many tools. This epic consolidates 131 skills into 8 broad skills (6 content + debugging + advisor) with companion files for depth. With 8 skills, each description gets 400+ chars (vs 120 today) for dramatically better routing signal while using only ~20% of the budget.

**The 8 skills:**

| # | Skill | Source skills | What merges in |
|---|-------|:---:|---|
| 1 | **dotnet-csharp** | ~22 | Language patterns, async, DI, config, generators, standards, nullable types, serialization, channels, LINQ, domain modeling, SOLID, concurrency, analyzers, editorconfig, file I/O, native interop, validation |
| 2 | **dotnet-api** | ~28 | ASP.NET Core, minimal APIs, middleware, EF Core, data access, gRPC, SignalR, resilience, HTTP client, API versioning, OpenAPI, security (OWASP, secrets, crypto), background services, Aspire, Semantic Kernel, architecture patterns |
| 3 | **dotnet-ui** | ~18 | Blazor (patterns, components, auth, testing), MAUI (dev, AOT, testing), Uno (platform, targets, MCP, testing), WPF, WinUI, WinForms, accessibility, localization, UI chooser |
| 4 | **dotnet-testing** | ~11 | Strategy, xUnit, integration, snapshot, Playwright, UI testing core, BenchmarkDotNet, test quality, CI benchmarking |
| 5 | **dotnet-devops** | ~18 | CI/CD (GHA 4 + ADO 4), containers (2), NuGet, MSIX, GitHub Releases, release management, observability, structured logging |
| 6 | **dotnet-tooling** | ~34 | Project setup, MSBuild, build, perf patterns, profiling, AOT/trimming, GC/memory, CLI apps, terminal UI, docs generation, tool management, version detection/upgrade, solution nav |
| 7 | **dotnet-debugging** | 1 | Standalone (user requirement). WinDbg debugging (single source skill: `dotnet-windbg-debugging`) |
| 8 | **dotnet-advisor** | 1 | Router/dispatcher (rewritten for 8 skills) |

Each consolidated skill gets:
- **SKILL.md** (auto-loaded on activation): overview, routing table, scope/out-of-scope, ToC pointing to companion files (~2-5KB)
- **references/** directory: topic-named companion files with deep content from merged source skills (read on demand)

## Execution model

**Single PR, big-bang migration.** All tasks land in one PR. CI only needs to pass on the final combined diff — intermediate states (after tasks 2-6 delete source dirs but before task .9 updates plugin.json and task .10 updates CI gates) are not independently mergeable. This is required because CI count gates make partial states unmergeable.

Tasks 2-6 run in parallel within a single worktree/branch, creating new dirs and deleting old ones. Task .9 then updates the manifest, agents, and advisor atomically. Task .10 updates CI gates and docs last. The final commit(s) must pass all validators.

## Scope

- Consolidate all 131 skill directories into 8 new skill directories
- Create companion `references/` files preserving all source skill content
- Rewrite `dotnet-advisor` routing catalog for 8 skills (replace mandatory first-action "dotnet-csharp-coding-standards" with "dotnet-csharp")
- Update all 14 agent preloaded skill references
- Update hooks, CI gates, validators
- Update validator thresholds: `--projected-skills 8`, `--max-desc-chars` raised to 600, warn/fail budget stays at 15,600
- Update `.agents/openai.yaml` discovery metadata for 8 skills
- Delete complex eval harness (`tests/evals/`) — structural validators only
- Simplify copilot smoke tests for 8 skills
- Update all documentation for new skill count and description policy

## Out of scope

- Redirect stubs for old skill names (no external consumers)
- New skill content (consolidation only, not enhancement)
- Agent restructuring (agents stay as-is, just update references)
- New eval framework (structural validators are sufficient)

## Key decisions

1. **8 skills, not ~20** — Tier 1 repos converge on 5-16 skills. With 8 skills at 400 chars each, routing signal per skill is 3x better than 20 skills at 120 chars. Companion files handle depth.
2. **dotnet-advisor survives** — hooks inject it as mandatory first action; rewrite routing catalog for 8 skills. Replace "invoke dotnet-csharp-coding-standards" with "invoke dotnet-csharp (read references/coding-standards.md)".
3. **Big-bang migration in a single PR** — CI count gates prevent incremental merging. All tasks land in one PR; CI passes only on final diff.
4. **Framework testing → UI framework group** — `dotnet-blazor-testing` → `dotnet-ui`, etc.
5. **Companion file convention** — `references/` directory (plural) with topic-named `.md` files. Rename existing `reference/` (singular) in dotnet-windbg-debugging.
6. **SKILL.md includes explicit ToC** — directs model to read specific companion files on demand.
7. **debugging stays standalone** — user requirement. Single source skill (`dotnet-windbg-debugging`).
8. **Delete eval harness, keep structural validators** — 8,100-line Python eval harness never ran in CI. Structural validators catch the top bug classes deterministically in <5 seconds. With 8 skills, routing confusion drops dramatically.
9. **dotnet-tooling as intentional grab-bag** — at 34 source skills it's the broadest group. Companion files (`references/msbuild.md`, `references/native-aot.md`, `references/cli-apps.md`, etc.) organize the depth. If it proves too broad post-implementation, splitting into build/performance/cli is a single-task change.
10. **plugin.json updated once in task .9** — tasks 2-6 only create new directories/files and delete old ones; they do NOT edit plugin.json. Task .9 updates plugin.json, agents, advisor, and hooks atomically to avoid merge conflicts.
11. **Validator thresholds updated in task .10** — `--projected-skills 8`, per-skill description cap raised from 120 to 600 chars. Global budget stays at 15,600. Documentation updated to match.
12. **Smoke test strategy: preserve case IDs, remap expected_skills** — existing `--case-id` filter in CI stays unchanged. Only `expected_skill` fields in `cases.jsonl` are remapped to new 8-skill names. Then optionally prune cases not referenced by CI.

## Quick commands

```bash
# Validate after changes (only passes on final combined diff)
STRICT_REFS=1 ./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Acceptance

- [ ] 8 consolidated skill directories replace 131 individual directories
- [ ] All source skill content preserved in SKILL.md + references/ companion files
- [ ] All 14 agents updated with correct [skill:new-name] references
- [ ] dotnet-advisor rewritten for 8 skills (dramatically simpler routing catalog)
- [ ] Hooks reference valid skill names
- [ ] CI gates updated (EXPECTED=8, --projected-skills 8)
- [ ] Validator per-skill description cap raised from 120 to 600 chars
- [ ] `.agents/openai.yaml` updated for 8 skills
- [ ] `tests/evals/` directory deleted (eval harness removed)
- [ ] `validate-skills.sh && validate-marketplace.sh` both pass (after threshold updates)
- [ ] `validate-marketplace.sh` passes specifically after legacy directory deletion (manifest/filesystem consistency)
- [ ] `reference/` (singular) renamed to `references/` (plural) everywhere; grep confirms no stale `/reference/` assumptions
- [ ] Similarity baseline regenerated for 8 skills
- [ ] Copilot smoke tests: existing case IDs preserved, `expected_skills` remapped to 8-skill names
- [ ] Total description budget under 3,900 chars (~25% of 15,600 cap)
- [ ] README.md, AGENTS.md, CONTRIBUTING-SKILLS.md, CONTRIBUTING.md updated with correct skill count and description policy
- [ ] All changes land in a single PR; CI passes on the final combined diff

## Dependencies

- fn-56 (flat layout) — DONE
- fn-51 (frontmatter schema) — DONE
- fn-53 (routing language) — DONE
- fn-55 (invocation contracts) — DONE
- fn-58/fn-60/fn-62/fn-63 (eval framework) — DONE, being deleted as too complex

## References

- Agent-skills spec: agentskills.io
- Research: BiasBusters, RAG-MCP (accuracy drops with many tools)
- Tier 1 repos: anthropics/skills (16), vercel-labs (6), kepano/obsidian (5)
- Companion file patterns: anthropics/skills PDF skill, Vercel rules/
- OpenAI eval-skills guide: deterministic checks > LLM evals
- anthropics/claude-plugins-official: minimal frontmatter validator in CI
