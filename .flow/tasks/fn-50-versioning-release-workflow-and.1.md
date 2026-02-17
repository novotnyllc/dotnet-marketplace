# fn-50-versioning-release-workflow-and.1 Optimize marketplace.json and plugin.json metadata

## Description
Restructure root marketplace.json and per-plugin marketplace.json to match the official Anthropic schema. Enrich plugin.json with missing discoverability fields.

**Size:** M
**Files:**
- `.claude-plugin/marketplace.json` (root)
- `plugins/dotnet-artisan/.claude-plugin/marketplace.json` (per-plugin)
- `plugins/dotnet-artisan/.claude-plugin/plugin.json`

## Approach

**Root marketplace.json** — Replace current structure with official pattern:
- Add `$schema: "https://anthropic.com/claude-code/marketplace.schema.json"`
- Replace `schema_version` with top-level `name: "dotnet-marketplace"`
- Add `owner: { name: "Claire Novotny LLC", url: "..." }`
- Add `metadata: { description: "...", version: "0.1.0" }`
- Per plugin entry: add `version`, `homepage`, singular `category: "development"`, keep `keywords`
- Remove `categories` array, replace with `category` string
- Follow pattern at `anthropics/claude-plugins-official/.claude-plugin/marketplace.json`

**Per-plugin marketplace.json** — Add `homepage` field. Keep existing structure.

**plugin.json** — Add fields: `author` (object with name/url), `homepage`, `repository`, `license`, `keywords`. Follow gmickel pattern at `plugins/flow-next/.claude-plugin/plugin.json`.

## Key context

- Official schema uses `owner` at root level, `author` at plugin entry level
- `category` is singular string (not array) in official schema — observed values: `development`, `productivity`, `security`, `learning`
- plugin.json version takes priority over marketplace entry version per Claude Code docs
- Keep per-plugin marketplace.json (removing breaks validate-marketplace.sh lines 248-281 and validate.yml line 52)
## Acceptance
- [ ] Root marketplace.json has `$schema`, `name`, `owner`, `metadata.description`, `metadata.version`
- [ ] Root marketplace.json plugin entry has `version`, `category` (string), `homepage`, `keywords`
- [ ] Root marketplace.json no longer has `schema_version` or `categories` (array)
- [ ] plugin.json has `author`, `homepage`, `repository`, `license`, `keywords`
- [ ] Per-plugin marketplace.json has `homepage` field
- [ ] All three JSON files are valid JSON (no syntax errors)
- [ ] Existing `validate-marketplace.sh` still passes (may need updates in task 3)
## Done summary
Restructured root marketplace.json to match official Anthropic schema ($schema, name, owner, metadata fields; singular category instead of categories array). Added homepage to per-plugin marketplace.json. Enriched plugin.json with author, homepage, repository, license, and keywords fields.
## Evidence
- Commits: 530c7ed93894cfe22d1e0f64f3a0ef014a3999fc
- Tests: cd plugins/dotnet-artisan && ./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
- PRs: