# dotnet-marketplace -- Marketplace Instructions

This repository is a Claude Code plugin marketplace hosting .NET development plugins. It follows the [marketplace pattern](https://github.com/anthropics/claude-plugins-official) with plugins in `plugins/<name>/`.

## Repository Layout

- **`plugins/dotnet-artisan/`** -- The dotnet-artisan plugin (122 skills, 14 agents). See [plugins/dotnet-artisan/CLAUDE.md](plugins/dotnet-artisan/CLAUDE.md) for plugin-specific instructions.
- **`.claude-plugin/marketplace.json`** -- Root marketplace listing (lists available plugins)
- **`.github/workflows/`** -- CI/CD workflows
- **`scripts/ralph/`** -- Dev tooling (repo-level)
- **`.flow/`** -- Task planning (repo-level)

## Validation

Plugin validation runs from within the plugin directory:

```bash
cd plugins/dotnet-artisan
./scripts/validate-skills.sh
./scripts/validate-marketplace.sh
```

Root marketplace validation (JSON valid, source paths resolve):

```bash
jq empty .claude-plugin/marketplace.json
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution guide. For plugin-specific skill authoring, see [plugins/dotnet-artisan/CONTRIBUTING-SKILLS.md](plugins/dotnet-artisan/CONTRIBUTING-SKILLS.md).
