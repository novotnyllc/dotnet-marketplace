# fn-31-self-contained-skills-port.2 Create built-in validation patterns skill

## Description
Create skills/core-csharp/dotnet-validation-patterns/SKILL.md covering built-in .NET validation patterns. Minimize third-party deps. Prefer DataAnnotations, IValidatableObject, IValidateOptions<T>, MinimalApis.Extensions validation over FluentValidation.

**Size:** M
**Files:** skills/core-csharp/dotnet-validation-patterns/SKILL.md, .claude-plugin/plugin.json

## Approach
- DataAnnotations: [Required], [Range], [RegularExpression], custom attributes
- IValidatableObject for cross-property validation
- IValidateOptions<T> for options validation on startup
- Minimal API validation with EndpointFilter
- FluentValidation mentioned only for complex domain rules, not as default
## Acceptance
- [ ] Built-in validation as default recommendation
- [ ] FluentValidation only for complex cases
- [ ] IValidateOptions<T> covered
- [ ] Frontmatter and registration correct
- [ ] Validation passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
