# fn-17: CLI Tool Development Skills

## Problem/Goal
Add comprehensive CLI tool development skills covering System.CommandLine, architecture patterns (avoiding "one big bash script"), Native AOT distribution, and multi-platform package manager publishing (Homebrew, apt, winget).

## Acceptance Checks
- [ ] `dotnet-system-commandline` skill covers full System.CommandLine API (commands, options, arguments, middleware, hosting, tab completion)
- [ ] `dotnet-cli-architecture` skill covers layered CLI design patterns (reference: clig.dev) for maintainability
- [ ] `dotnet-cli-aot-distribution` skill covers Native AOT for CLI tools plus cross-platform distribution
- [ ] `dotnet-cli-homebrew`, `dotnet-cli-apt`, `dotnet-cli-winget` skills cover platform-specific packaging + CI/CD
- [ ] `dotnet-cli-unified-pipeline` skill covers unified CI/CD producing all package formats from single build
- [ ] Cross-references to dotnet-native-aot, CI/CD skills

## Key Context
- System.CommandLine is the modern standard (not CommandLineParser)
- CLI apps benefit significantly from Native AOT (fast startup, no runtime dependency)
- clig.dev principles for good CLI design
- Unified CI/CD pipeline maximizes maintainability across package managers
