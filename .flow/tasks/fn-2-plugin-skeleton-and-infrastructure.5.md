## Description
Create the `plugin-self-publish` skill documenting how this plugin itself is versioned and published, plus validation scripts for SKILL.md frontmatter and cross-references.

**Size:** M
**Files:**
- `skills/foundation/plugin-self-publish/SKILL.md`
- `scripts/validate-skills.sh`
- `scripts/validate-marketplace.sh`

## Approach

1. `plugin-self-publish` skill covers:
   - SemVer versioning strategy for the plugin
   - CHANGELOG.md format (keep-a-changelog)
   - GitHub Releases workflow
   - Marketplace publishing steps
2. `validate-skills.sh` script:
   - Single-pass scan of all `SKILL.md` files (no subprocess spawning, no network)
   - Checks required frontmatter: `name`, `description` (canonical set from epic, nothing more)
   - Validates YAML frontmatter is well-formed
   - Checks `[skill:name]` cross-references point to existing skill directories
   - Budget validation with coherent thresholds:
     - Constants: PROJECTED_SKILLS_COUNT=95, MAX_DESC_CHARS=120
     - Reports current combined description char count
     - Reports projected: 95 x 120 = 11,400
     - WARN at 12,000 chars (current or projected)
     - FAIL at 15,000 chars (hard platform limit)
   - Outputs stable keys for CI parsing:
     ```
     CURRENT_DESC_CHARS=<N>
     PROJECTED_DESC_CHARS=<N>
     BUDGET_STATUS=OK|WARN|FAIL
     ```
   - Exits non-zero on: missing required frontmatter, broken cross-references, BUDGET_STATUS=FAIL
3. `validate-marketplace.sh` script:
   - Validates plugin.json against canonical schema: skills=array of dir paths, agents=array of file paths, hooks=string path, mcpServers=string path
   - Validates marketplace.json completeness
   - Checks all referenced skill dirs contain SKILL.md
   - Checks all referenced agent files exist
   - Exits non-zero on validation failures

## Key context

- Reference dotnet-skills `marketplace-publishing` and `validate-marketplace.sh` patterns
- Budget validation thresholds must be coherent: WARN at 12,000, FAIL at 15,000
- Projected: 95 x 120 = 11,400 (safely under 12,000 warn)
- Scripts must be fast (<5s): single-pass scan, no subprocess spawning, no network
- Use `disable-model-invocation: true` in self-publish frontmatter (side-effect command)
- Cross-reference syntax: `[skill:skill-name]` (machine-parseable, canonical format)
- Required frontmatter is exactly: `name`, `description`. Do not enforce optional fields.
- Both scripts are used identically in local dev and CI (same commands)
- Stable output keys (CURRENT_DESC_CHARS, PROJECTED_DESC_CHARS, BUDGET_STATUS) enable CI parsing

## Acceptance
- [ ] plugin-self-publish skill documents versioning and publishing workflow
- [ ] validate-skills.sh checks all SKILL.md files for required frontmatter (name, description only)
- [ ] validate-skills.sh reports CURRENT_DESC_CHARS and PROJECTED_DESC_CHARS via stable output keys
- [ ] validate-skills.sh reports BUDGET_STATUS=OK|WARN|FAIL
- [ ] validate-skills.sh WARNs at 12,000 chars, FAILs at 15,000 chars
- [ ] validate-skills.sh validates `[skill:name]` cross-references against existing skill dirs
- [ ] validate-marketplace.sh validates plugin.json against canonical schema
- [ ] validate-marketplace.sh checks all referenced paths exist
- [ ] Both scripts run in <5 seconds (single-pass, no subprocesses, no network)
- [ ] Both scripts exit non-zero on FAIL conditions
