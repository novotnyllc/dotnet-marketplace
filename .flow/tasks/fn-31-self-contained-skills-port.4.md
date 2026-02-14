# fn-31-self-contained-skills-port.4 Create SOLID/DRY/SRP architecture principles skill

## Description
Create skills/architecture/dotnet-solid-principles/SKILL.md deeply engraining SOLID, DRY, and SRP principles with concrete C# anti-patterns and fixes. Foundational skill that other architecture skills should cross-reference.

**Size:** M
**Files:** skills/architecture/dotnet-solid-principles/SKILL.md, .claude-plugin/plugin.json

## Approach
- Structure around each SOLID principle with C# anti-patterns and fixes
- SRP: Cover god classes, fat controllers, mixed abstractions (ref: https://stormwild.github.io/blog/post/srp-mistakes-csharp-dotnet/)
- OCP: Extension via interfaces/abstract classes, strategy pattern
- LSP: Behavioral subtypes, collection covariance pitfalls
- ISP: Interface segregation, role interfaces vs header interfaces
- DIP: Dependency inversion with M.E.DI, cross-ref to [skill:dotnet-dependency-injection]
- DRY: When to abstract vs when duplication is acceptable (rule of three)
- Include "describe in one sentence" test for SRP compliance
## Acceptance
- [ ] All SOLID principles with C# anti-patterns and fixes
- [ ] DRY with nuanced guidance (rule of three)
- [ ] Cross-refs to related skills
- [ ] No fn-N references
- [ ] Validation passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
