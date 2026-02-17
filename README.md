# dotnet-marketplace

> A Claude Code plugin marketplace for .NET development

[![CI](https://github.com/novotnyllc/dotnet-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/novotnyllc/dotnet-marketplace/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Overview

**dotnet-marketplace** hosts Claude Code plugins for .NET development. It follows the [marketplace pattern](https://github.com/anthropics/claude-plugins-official) established by `anthropics/claude-plugins-official`, with each plugin self-contained in its own subdirectory under `plugins/`.

## Available Plugins

| Plugin | Description | Skills | Agents |
|---|---|---|---|
| [**dotnet-artisan**](plugins/dotnet-artisan/) | Comprehensive .NET development skills for modern C#, ASP.NET, MAUI, Blazor, and cloud-native applications | 122 | 14 |

## Installation

Install a plugin from this marketplace using the Claude Code CLI:

```bash
claude plugin add novotnyllc/dotnet-marketplace
claude plugin install dotnet-artisan
```

Installation syntax may change as the Claude Code plugin system evolves.

## Repository Structure

```
/
+-- .claude-plugin/
|   +-- marketplace.json          # Root marketplace listing
+-- plugins/
|   +-- dotnet-artisan/           # Self-contained plugin
|       +-- .claude-plugin/       # Plugin manifest and metadata
|       +-- skills/               # 122 skills (22 categories)
|       +-- agents/               # 14 specialist agents
|       +-- hooks/                # Session hooks
|       +-- scripts/              # Validation scripts
|       +-- ...
+-- .github/workflows/            # CI/CD
+-- CONTRIBUTING.md               # Contribution guide
+-- CHANGELOG.md                  # Release history
+-- LICENSE                       # MIT
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution guide, PR process, and validation requirements.

For plugin-specific skill authoring guidance, see [plugins/dotnet-artisan/CONTRIBUTING-SKILLS.md](plugins/dotnet-artisan/CONTRIBUTING-SKILLS.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
