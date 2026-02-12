# fn-3-core-c-and-language-patterns-skills.1 Language patterns and coding standards skills

## Description
Create the `dotnet-csharp-modern-patterns` and `dotnet-csharp-coding-standards` skills under `skills/core-csharp/`.

**`dotnet-csharp-modern-patterns`**: Covers C# 14/15 features (primary constructors, collection expressions, pattern matching enhancements, records, `required` members), with TFM-specific sections for net8.0 through net11.0. Progressive disclosure: trigger description -> quick patterns -> deep reference.

**`dotnet-csharp-coding-standards`**: Microsoft Framework Design Guidelines and C# Coding Conventions. Naming conventions, file organization, code style rules. Cross-references `[skill:dotnet-csharp-modern-patterns]` for feature-specific conventions.

Both skills must:
- Use canonical frontmatter (`name`, `description`) per fn-2
- Include `[skill:name]` cross-references to other fn-3 skills
- Reference authoritative Microsoft docs
- Keep `description` field under 120 chars

## Acceptance
- [ ] `skills/core-csharp/dotnet-csharp-modern-patterns/SKILL.md` exists with valid frontmatter
- [ ] `skills/core-csharp/dotnet-csharp-coding-standards/SKILL.md` exists with valid frontmatter
- [ ] Both descriptions under 120 chars
- [ ] TFM-specific sections for net8.0, net9.0, net10.0, net11.0 in modern-patterns
- [ ] Cross-references use `[skill:name]` syntax
- [ ] Microsoft docs links included
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
Created two core C# skills under `skills/core-csharp/`:

1. **dotnet-csharp-modern-patterns** -- TFM-aware C# 12-15 language feature guidance covering records, primary constructors, collection expressions, pattern matching, `required` members, `field` keyword (C# 14), extension blocks (C# 14), `params` collections (C# 13), `Lock` type (C# 13), partial properties (C# 13), collection expression `with()` arguments (C# 15 preview), and polyfill guidance for multi-targeting.

2. **dotnet-csharp-coding-standards** -- Microsoft Framework Design Guidelines and C# Coding Conventions covering naming conventions, file organization, code style rules, access modifiers, type design (seal by default, composition over inheritance), CancellationToken conventions, XML documentation, and analyzer enforcement.

Both skills use canonical frontmatter, descriptions under 120 chars, `[skill:name]` cross-references, TFM-specific sections (net8.0-net11.0), and authoritative Microsoft docs links. Registered in plugin.json. Validation passes with 0 errors.
## Evidence
- Commits:
- Tests:
- PRs: