# Task 4: Minimize third-party deps, System.CommandLine version, and SOLID/DRY/SRP enforcement

## Scope

### FluentValidation positioning
- Ensure FluentValidation is positioned as opt-in for complex validation scenarios, not a default
- Verify all skills that mention FluentValidation also mention built-in alternatives first (DataAnnotations, IValidateOptions, .NET 10 AddValidation)
- Primary target: `skills/api-development/dotnet-input-validation/SKILL.md` — verify decision tree recommends built-in first
- Check any other skills mentioning FluentValidation

### System.CommandLine version
- System.CommandLine 2.0 has no stable release — it remains at `2.0.0-beta4.*` pre-release
- Verify references use latest `2.0.0-beta4.*` version
- Add note that no stable 2.0 release exists yet
- Remove any references to older beta versions (beta1, beta2, beta3)
- Primary target: `skills/cli-tools/dotnet-system-commandline/SKILL.md`

### SOLID/DRY/SRP enforcement
- Ensure architecture-related skills engrain SOLID, DRY, SRP principles
- Check: `dotnet-clean-architecture`, `dotnet-csharp-coding-standards`, `dotnet-architecture-patterns`
- This targets a different set of files from other scope items

## Verification
```bash
# FluentValidation should appear but not as primary recommendation
grep -r 'FluentValidation' skills/ --include='*.md' -l  # Review each manually

# System.CommandLine beta versions — should only be beta4
grep -r 'beta[123]' skills/ --include='*.md' | grep -i 'commandline' | wc -l  # Should be 0

# SOLID/DRY/SRP — should appear in architecture skills
grep -r 'SOLID\|DRY\|SRP\|Single Responsibility' skills/architecture/ --include='*.md' | wc -l  # Should be > 0

./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
python3 scripts/validate_cross_agent.py
```

## Acceptance
- [ ] FluentValidation positioned as opt-in, built-in recommended first
- [ ] System.CommandLine references use latest beta4, note pre-release status
- [ ] No references to older beta versions (beta1-3)
- [ ] Architecture skills reference SOLID/DRY/SRP principles
- [ ] All four validation commands pass

## Evidence
<!-- filled by flowctl done -->

## Done summary
<!-- filled by flowctl done -->
