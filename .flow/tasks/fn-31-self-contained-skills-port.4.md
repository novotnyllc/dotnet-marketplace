# fn-31-self-contained-skills-port.4 Create SOLID/DRY/SRP architecture principles skill

## Description
Create `skills/architecture/dotnet-solid-principles/SKILL.md` deeply engraining SOLID, DRY, and SRP principles with concrete C# anti-patterns and fixes. Cross-references `[skill:dotnet-architecture-patterns]` for clean arch/vertical slices.

**Size:** M
**Files:** skills/architecture/dotnet-solid-principles/SKILL.md, .claude-plugin/plugin.json

## Approach
- First check `skills/architecture/dotnet-architecture-patterns/SKILL.md` for overlap — that skill covers vertical slices and request pipelines; this skill covers foundational SOLID principles (complementary, not overlapping)
- Structure around each SOLID principle with C# anti-patterns and fixes
- SRP: Cover god classes, fat controllers, mixed abstractions (ref: https://stormwild.github.io/blog/post/srp-mistakes-csharp-dotnet/)
- OCP: Extension via interfaces/abstract classes, strategy pattern
- LSP: Behavioral subtypes, collection covariance pitfalls
- ISP: Interface segregation, role interfaces vs header interfaces
- DIP: Dependency inversion with M.E.DI, cross-ref to `[skill:dotnet-csharp-dependency-injection]`
- DRY: When to abstract vs when duplication is acceptable (rule of three)
- Include "describe in one sentence" test for SRP compliance
- Cross-ref `[skill:dotnet-architecture-patterns]` for clean architecture and vertical slices (explicitly note they are covered there, not here)
- Add `## Attribution` section crediting Aaronontheweb/dotnet-skills
- Register in plugin.json under `skills/architecture/dotnet-solid-principles`

## Acceptance
- [ ] All SOLID principles with C# anti-patterns and fixes
- [ ] DRY with nuanced guidance (rule of three)
- [ ] Cross-refs use correct skill names (`[skill:dotnet-csharp-dependency-injection]`, `[skill:dotnet-architecture-patterns]`)
- [ ] No fn-N references in skill content
- [ ] Attribution section present
- [ ] Registered in plugin.json
- [ ] Description under 120 chars
- [ ] Validation passes

## Done summary
Created dotnet-solid-principles skill covering all five SOLID principles (SRP, OCP, LSP, ISP, DIP) with concrete C# anti-patterns and fixes, plus DRY guidance with rule of three and acceptable-duplication scenarios. Registered in plugin.json (103 skills total).
## Evidence
- Commits: 5f7b8935751f9720a1731f717d80e12ac33e95e0
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: