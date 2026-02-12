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
