# fn-11-api-development-skills.3 Input validation skill

## Description
Create the `dotnet-input-validation` skill covering comprehensive input validation patterns for .NET APIs: framework decision tree, .NET 10 built-in validation, FluentValidation, Data Annotations, endpoint filters, error responses, and security-focused validation. Register skill in plugin.json and dotnet-advisor catalog.

**Size:** M
**Files:**
- `skills/api-development/dotnet-input-validation/SKILL.md` (new)
- `.claude-plugin/plugin.json` (modify — add skill path)
- `skills/foundation/dotnet-advisor/SKILL.md` (modify — add catalog entry + routing)

## Approach
- Follow existing skill patterns at `skills/security/dotnet-security-owasp/SKILL.md` for structure and frontmatter conventions
- Use `[skill:...]` cross-reference syntax per fn-2 conventions
- Cross-reference `[skill:dotnet-security-owasp]` for OWASP injection prevention (don't duplicate fn-8 security principles)
- Cross-reference `[skill:dotnet-architecture-patterns]` for architectural validation strategy (fn-5 has FluentValidation overview at lines 269-314)
- Cross-reference `[skill:dotnet-minimal-apis]` for Minimal API pipeline integration
- Reference `[skill:dotnet-csharp-configuration]` for Options pattern ValidateDataAnnotations
- Register skill in plugin.json and add to dotnet-advisor catalog (category 6) and routing logic

## Key context
- .NET 10 built-in validation: `builder.Services.AddValidation()` auto-discovers types from Minimal API handlers, adds endpoint filter. Uses source generators (`[ValidatableType]`) for AOT compatibility. Lives in `Microsoft.Extensions.Validation` package.
- FluentValidation: manual validation is preferred (auto-validation via ASP.NET pipeline deprecated). Use `FluentValidation.DependencyInjectionExtensions` for assembly scanning. Endpoint filters for Minimal API integration.
- Data Annotations: `[Required]`, `[Range]`, `[RegularExpression]`, `[StringLength]`, custom `ValidationAttribute`. `IValidatableObject` for cross-property validation.
- MiniValidation: lightweight alternative for simple scenarios (mention briefly, cross-ref architecture-patterns for details).
- ProblemDetails: `TypedResults.ValidationProblem()` for standard error responses. Customizable via `IProblemDetailsService`.
- Security validation: ReDoS prevention (use `Regex()` with timeout, or `[GeneratedRegex]` for .NET 7+), allowlist vs denylist (always prefer allowlist), max length enforcement, file upload content type validation. Defer OWASP category semantics to `[skill:dotnet-security-owasp]`.
- Decision tree: .NET 10 AddValidation (default new projects) > FluentValidation (complex rules) > Data Annotations (simple) > MiniValidation (micro)
- Pitfall from memory: ConfigureHttpJsonOptions applies to Minimal APIs only, not MVC controllers — validation error formatting may differ
- Pitfall from memory: options pattern classes must use { get; set; } not { get; init; } for binder compatibility — relevant for validation attributes on options

## Acceptance
- [ ] Skill file exists at `skills/api-development/dotnet-input-validation/SKILL.md`
- [ ] Frontmatter has `name: dotnet-input-validation` and `description` (under 120 chars)
- [ ] Covers validation framework decision tree: when to use .NET 10 built-in vs FluentValidation vs Data Annotations vs MiniValidation
- [ ] Covers .NET 10 built-in validation: AddValidation(), [ValidatableType], source generator integration, Microsoft.Extensions.Validation
- [ ] Covers FluentValidation: AbstractValidator<T>, DependencyInjectionExtensions, assembly scanning, manual validation pattern (NOT deprecated auto-validation)
- [ ] Covers Data Annotations: standard attributes ([Required], [Range], [RegularExpression], [StringLength]), custom ValidationAttribute, IValidatableObject
- [ ] Covers endpoint filters for validation in Minimal APIs
- [ ] Covers error responses: ProblemDetails, ValidationProblem, IProblemDetailsService customization
- [ ] Covers security-focused validation: ReDoS prevention (Regex timeout, [GeneratedRegex]), allowlist patterns, max length enforcement, file upload validation
- [ ] Cross-references `[skill:dotnet-security-owasp]` for OWASP injection prevention
- [ ] Cross-references `[skill:dotnet-architecture-patterns]` for architectural validation strategy
- [ ] Cross-references `[skill:dotnet-minimal-apis]` for API pipeline integration
- [ ] Cross-references `[skill:dotnet-csharp-configuration]` for Options pattern validation
- [ ] Explicit scope boundary: fn-8 owns security principles, fn-5 owns architectural patterns, fn-11 owns practical validation framework guidance
- [ ] Skill registered in `.claude-plugin/plugin.json` skills array
- [ ] Skill added to `dotnet-advisor` catalog (category 6: API Development) and routing logic
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
