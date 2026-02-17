# fn-45-add-net-tools-consumer-skill.2 Integrate dotnet-tool-management into plugin registry and routing

## Description
Register `dotnet-tool-management` in plugin.json, add routing entry in `dotnet-advisor`, and add cross-references.

**Size:** S
**Files:** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`, `skills/cli-tools/dotnet-cli-packaging/SKILL.md`, `skills/cli-tools/dotnet-cli-distribution/SKILL.md`, `scripts/validate-skills.sh`

## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor`
- Add `[skill:dotnet-tool-management]` cross-references in packaging and distribution skills
- Update `--projected-skills` in validate-skills.sh

## File contention warning

**plugin.json and dotnet-advisor SKILL.md are shared files.** Run integration tasks sequentially, not in parallel.
## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor`
- Add `[skill:dotnet-tool-management]` cross-references in packaging and distribution skills
- Update `--projected-skills` count in validation
## Acceptance
- [ ] plugin.json includes `skills/cli-tools/dotnet-tool-management`
- [ ] `dotnet-advisor` has routing entry for tool management
- [ ] Cross-references added in `dotnet-cli-packaging`, `dotnet-cli-distribution`
- [ ] `--projected-skills` incremented in validate-skills.sh
- [ ] All four validation scripts pass
## Done summary
Registered dotnet-tool-management in plugin.json, added catalog entry and routing rule in dotnet-advisor, added [skill:dotnet-tool-management] cross-references in dotnet-cli-packaging and dotnet-cli-distribution, incremented --projected-skills to 125, and fixed projected budget boundary check to use strict > for pessimistic estimates.
## Evidence
- Commits: 2bee08a4699d07e044f2c7258603100fabc863b1
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: