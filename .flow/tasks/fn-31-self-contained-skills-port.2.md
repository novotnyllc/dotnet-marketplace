# fn-31-self-contained-skills-port.2 Create built-in validation patterns skill

## Description
Create `skills/core-csharp/dotnet-validation-patterns/SKILL.md` covering built-in .NET validation patterns. Minimize third-party deps. Prefer DataAnnotations, IValidatableObject, IValidateOptions<T>, MinimalApis.Extensions validation over FluentValidation.

**Size:** M
**Files:** skills/core-csharp/dotnet-validation-patterns/SKILL.md, .claude-plugin/plugin.json

## Approach
- First check existing skills for overlap (none expected — validation is not yet covered)
- DataAnnotations: [Required], [Range], [RegularExpression], custom attributes
- IValidatableObject for cross-property validation
- IValidateOptions<T> for options validation on startup (cross-ref [skill:dotnet-csharp-configuration])
- Minimal API validation with EndpointFilter
- FluentValidation mentioned only for complex domain rules, not as default
- Add `## Attribution` section crediting Aaronontheweb/dotnet-skills
- Register in plugin.json under `skills/core-csharp/dotnet-validation-patterns`

## Acceptance
- [ ] Built-in validation as default recommendation
- [ ] FluentValidation only for complex cases
- [ ] IValidateOptions<T> covered
- [ ] Frontmatter correct (name, description under 120 chars)
- [ ] Registered in plugin.json
- [ ] Attribution section present
- [ ] Validation passes

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
