# Conventions

Project patterns discovered during work. Not in CLAUDE.md but important.

<!-- Entries added manually via `flowctl memory add` -->

## 2026-02-12 manual [convention]
Agent .md frontmatter requires name field in addition to description, capabilities, and tools

## 2026-02-12 manual [convention]
Always validate JSON field types with jq predicates (type=="string" and length>0), not just emptiness checks

## 2026-02-12 manual [convention]
When an epic's skills overlap with other epics, add an explicit scope boundary table mapping which epic owns scaffolding vs depth for each concern
