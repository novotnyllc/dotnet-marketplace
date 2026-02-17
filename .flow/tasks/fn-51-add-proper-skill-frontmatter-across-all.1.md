## Description

Update the validation script and all documentation to support the expanded set of SKILL.md frontmatter fields. Remove `plugin-self-publish` from the plugin and move its content to repo-level instructions. This must complete before T2 and T3 modify skills.

**Size:** M
**Files:**
- `plugins/dotnet-artisan/scripts/_validate_skills.py` (~line 30)
- `plugins/dotnet-artisan/CONTRIBUTING-SKILLS.md` (~lines 82-90)
- `plugins/dotnet-artisan/CLAUDE.md` (~lines 7-20)
- `CLAUDE.md` (root, validation section)
- `plugins/dotnet-artisan/skills/foundation/plugin-self-publish/SKILL.md` (delete)
- `plugins/dotnet-artisan/.claude-plugin/plugin.json` (remove plugin-self-publish entry from skills array)
- Repo-level location for publishing instructions (e.g., section in `CONTRIBUTING.md` or root `CLAUDE.md`)

## Approach

- **Remove `plugin-self-publish`**: Delete the skill directory, remove from `plugin.json` skills array, move its publishing guidance to a repo-level doc (CONTRIBUTING.md "Publishing to Marketplace" section is the natural home)
- Expand `ALLOWED_FRONTMATTER_FIELDS` at `_validate_skills.py:30` to include: `user-invocable`, `disable-model-invocation`, `context`, `model`
- Add a `FIELD_TYPES` dict for type validation — boolean fields (`user-invocable`, `disable-model-invocation`) and string fields (`context`, `model`) — to catch quoted-string booleans like `user-invocable: "false"`
- Update `CONTRIBUTING-SKILLS.md` frontmatter spec section (currently says "No other frontmatter fields are recognized") with a table of all recognized fields
- Update plugin `CLAUDE.md` which says "Every skill requires exactly two frontmatter fields" to reflect expanded spec
- Update root `CLAUDE.md` validation section to list all recognized fields
- Update projected skill count references from 127 to 126 where applicable
- Maintain backwards compatibility — `name` and `description` remain the only REQUIRED fields

## Key context

- Official frontmatter reference: https://code.claude.com/docs/en/skills#frontmatter-reference
- Current allowed set: `{"name", "description"}` — anything else causes validation failure
- The existing parser at `_validate_skills.py:~108` already converts `true`/`false` to Python `bool`, but there is no type checking beyond name/description being strings
- `plugin-self-publish` is the only skill with `disable-model-invocation: true`; it's a meta-skill about publishing to this marketplace, not .NET guidance
- `validate-skills.sh` has `--projected-skills 127` — update to 126 after removal
- Must pass: `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh`

## Acceptance

- [ ] `plugin-self-publish` skill directory deleted
- [ ] `plugin-self-publish` removed from `plugin.json` skills array
- [ ] Publishing guidance moved to repo-level docs (e.g., CONTRIBUTING.md)
- [ ] `_validate_skills.py` `ALLOWED_FRONTMATTER_FIELDS` includes: `user-invocable`, `disable-model-invocation`, `context`, `model`
- [ ] `_validate_skills.py` has `FIELD_TYPES` dict with type validation for boolean and string fields
- [ ] Type errors (e.g., `user-invocable: "false"`) emit warnings
- [ ] `CONTRIBUTING-SKILLS.md` documents each frontmatter field with description and usage guidance
- [ ] Plugin `CLAUDE.md` no longer says "exactly two frontmatter fields"
- [ ] Root `CLAUDE.md` lists recognized frontmatter fields
- [ ] `validate-skills.sh && validate-marketplace.sh` pass clean (now 126 skills)

## Done summary

_To be filled on completion._

## Evidence

_To be filled on completion._
