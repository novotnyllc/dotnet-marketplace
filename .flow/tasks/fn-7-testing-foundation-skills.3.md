# fn-7-testing-foundation-skills.3 Snapshot testing and test quality skills

## Description
Create two testing skills focused on test validation and quality measurement.

**Skills delivered:**
- `skills/testing/dotnet-snapshot-testing/SKILL.md` -- Verify (VerifyTests): API surfaces, HTTP responses, rendered emails, scrubbing/filtering, custom converters
- `skills/testing/dotnet-test-quality/SKILL.md` -- Code coverage (coverlet + ReportGenerator), CRAP analysis, mutation testing (Stryker.NET), flaky test detection

**File ownership:** This task exclusively owns `skills/testing/dotnet-snapshot-testing/` and `skills/testing/dotnet-test-quality/`. No other task creates or modifies these directories. This task does NOT modify `plugin.json` (Task 4 handles registration).

## Acceptance
- [ ] Two SKILL.md files created with required frontmatter (`name`, `description`)
- [ ] Each skill has: scope boundary, prerequisites, cross-references per matrix, >=2 code examples, gotchas section, references
- [ ] Snapshot testing covers Verify with scrubbing/filtering patterns for dates, GUIDs
- [ ] Snapshot testing includes custom converter examples
- [ ] Test quality covers coverlet + ReportGenerator, CRAP analysis, Stryker.NET
- [ ] Version assumptions stated: Verify 20.x+, Stryker.NET 4.x+, .NET 8.0+ baseline
- [ ] Cross-references match the epic cross-reference matrix
- [ ] Skill content complete and ready for registration by Task 4

## Done summary
Created two testing skills: dotnet-snapshot-testing covering Verify library with scrubbing/filtering for dates and GUIDs, custom converters, HTTP response verification, and rendered email testing; and dotnet-test-quality covering coverlet + ReportGenerator code coverage, CRAP analysis, Stryker.NET mutation testing, and flaky test detection.
## Evidence
- Commits: 11ea4125c4b66b0e21b7b06eba77e3b97e40f1dd, 1e0cd07c602f6d92449984bbb9c599023566757e
- Tests: grep -i Verify skills/testing/dotnet-snapshot-testing/SKILL.md, grep -i Stryker skills/testing/dotnet-test-quality/SKILL.md, grep skill: skills/testing/dotnet-snapshot-testing/SKILL.md, grep skill: skills/testing/dotnet-test-quality/SKILL.md
- PRs: