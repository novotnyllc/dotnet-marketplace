# Conventions

Project patterns discovered during work. Not in CLAUDE.md but important.

<!-- Entries added manually via `flowctl memory add` -->

## 2026-02-12 manual [convention]
Agent .md frontmatter requires name field in addition to description, capabilities, and tools

## 2026-02-12 manual [convention]
Always validate JSON field types with jq predicates (type=="string" and length>0), not just emptiness checks

## 2026-02-12 manual [convention]
When an epic's skills overlap with other epics, add an explicit scope boundary table mapping which epic owns scaffolding vs depth for each concern

## 2026-02-12 manual [convention]
When multiple tasks touch a shared file (e.g., plugin.json), assign registration to one dedicated task or final consolidation step — keeps skill-authoring tasks file-disjoint and parallelizable

## 2026-02-12 manual [convention]
When adding skills, validate name uniqueness both repo-wide AND against marketplace catalog metadata to prevent cross-plugin skill ID collisions

## 2026-02-12 manual [convention]
When epic acceptance criteria reference validation (e.g. cross-ref matrix, deprecated patterns), task specs must include executable grep commands that verify each requirement — not just intent statements

## 2026-02-12 manual [convention]
When multiple skills share a concern (e.g. deprecated patterns), designate a canonical owner in the epic spec and have other skills cross-reference it — avoids scope ambiguity and duplication

## 2026-02-12 manual [convention]
Agent workflow steps must be executable with the agent declared toolset -- do not reference CLI commands if Bash is not in tools list

## 2026-02-12 manual [convention]
Per-subsection acceptance: when skill definition says 'each section MUST include X', the AC and task checkboxes must enforce X per subsection, not just globally
