# Copilot CLI v0.0.412 Skill Loading Verification

> **Historical document (fn-56; pre-consolidation).** Test results below reflect the 131-skill catalog prior to fn-64 consolidation. The current canonical skill count is **8**.

**Date:** 2026-02-20
**Epic:** fn-56-copilot-structural-compatibility (Task 4)
**CLI version:** GitHub Copilot CLI 0.0.412
**Environment:** macOS (Darwin 25.3.0), installed via Homebrew at /opt/homebrew/bin/copilot

## Test 1: Skill discovery (flat layout)

**Command:** `copilot -p "List all available skills" --allow-all-tools --log-level debug`

**Observed:**
- CLI used `Glob "skills/*/SKILL.md"` to discover skills
- Found **131 files** (matches canonical count)
- Skills listed in **alphabetical order** (when model uses filesystem glob)

## Test 2: Skill count and ordering (manifest)

**Command:** `copilot -p "How many skills are available? List every skill name, one per line." --allow-all-tools --log-level info`

**Observed:**
- CLI reported **131 skills** available
- Model read from `.claude-plugin/plugin.json` to enumerate skills
- Skills listed in **manifest order** (plugin.json array order), not alphabetical
- **ALL 131 skills visible** -- no truncation at 32 or any other threshold
- `dotnet-advisor` listed first (as intended by manifest positioning)

## 32-Skill Limit Findings

- **No truncation observed.** All 131 skills (11 user-invocable, 120 non-user-invocable) were accessible to the model.
- The upstream ~32-skill limit reported in copilot-cli#1464 and #1130 may be:
  - Version-dependent (not reproduced in v0.0.412)
  - Context-dependent (may apply only when total description tokens exceed a threshold)
  - Resolved in a more recent version
- **Ordering:** Manifest order (plugin.json) when model reads the manifest; alphabetical when model uses filesystem glob.

## Frontmatter Parsing

- No errors during skill loading (all 131 parsed successfully)
- Unquoted descriptions loaded correctly
- `license: MIT` present on all skills (no loading failures)
- `user-invocable: false` skills loaded alongside `user-invocable: true` skills

## metadata-last Key Verification (copilot-cli#951)

### Test 3: metadata: as last frontmatter key

**Setup:** Created temporary test skill `skills/test-metadata-last/SKILL.md` with frontmatter:

```yaml
---
name: test-metadata-last
description: Temporary test skill for metadata-last key verification
license: MIT
user-invocable: false
metadata: test-value
---
```

**Command:** `copilot -p "Does a skill called 'test-metadata-last' exist? What is its description?" --allow-all-tools --log-level info`

**Observed:**
- Copilot CLI discovered the skill via `Glob "**/test-metadata-last/SKILL.md"` (1 file found)
- Successfully read `skills/test-metadata-last/SKILL.md` (19 lines)
- Correctly extracted description: "Temporary test skill for metadata-last key verification"
- **No silent drop.** The skill loaded and was accessible despite `metadata:` being the last frontmatter key.

### metadata-last Findings

- **copilot-cli#951 behavior NOT reproduced in v0.0.412.** The skill loaded successfully.
- No dotnet-artisan skills use a `metadata:` frontmatter key (verified via `grep` across all 131 SKILL.md files).
- The conservative validator guard (ERROR if `metadata:` is the last key) is retained as a preventive measure against older or future Copilot versions, with zero false-positive risk on the current catalog.

## Conclusion

The flat layout is fully compatible with Copilot CLI v0.0.412. The 32-skill truncation limit was NOT reproduced in this version, making the advisor meta-routing strategy a beneficial redundancy rather than a critical requirement. All frontmatter constraints (unquoted descriptions, license: MIT, user-invocable explicit) are validated by the skill validator and confirmed compatible with Copilot CLI loading.
