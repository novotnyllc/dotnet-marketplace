# fn-17.1 Create System.CommandLine and CLI architecture skills

## Description
Create the two foundational CLI skills covering System.CommandLine 2.0 API usage and CLI application architecture patterns. These are reference skills for .NET developers building command-line tools.

## Delivers
- `skills/cli-tools/dotnet-system-commandline/SKILL.md`
- `skills/cli-tools/dotnet-cli-architecture/SKILL.md`

## Acceptance
- [ ] `dotnet-system-commandline` covers: RootCommand, Command, Option<T>, Argument<T>, middleware pipeline, hosting integration (`UseCommandHandler`), tab completion, `--version`/`--help` auto-generation, dependency injection via hosting, `IConsole` abstraction
- [ ] `dotnet-system-commandline` documents System.CommandLine 2.0 pre-release status with production readiness assessment (battle-tested in `dotnet` CLI)
- [ ] `dotnet-cli-architecture` covers: clig.dev principles, layered command → handler → service architecture, configuration precedence (appsettings + env vars + CLI args), structured logging in CLI context, exit code conventions, stdin/stdout/stderr patterns
- [ ] `dotnet-cli-architecture` covers CLI testing: in-process invocation via `CommandLineBuilder`, stdout/stderr capture, exit code assertion
- [ ] Both skills have `name` and `description` frontmatter (< 120 chars each)
- [ ] Both skills contain out-of-scope boundary statements for fn-16 (AOT), fn-19 (CI/CD), fn-3 (DI)
- [ ] Cross-references use canonical `[skill:skill-name]` syntax
- [ ] Does NOT modify `plugin.json` (handled by fn-17.3)

## Dependencies
- None (foundation skills, no cross-skill file edits)

## Done summary
Created two foundational CLI skills for fn-17:

1. **dotnet-system-commandline** (`skills/cli-tools/dotnet-system-commandline/SKILL.md`): Covers System.CommandLine 2.0 API including RootCommand, Command hierarchy, Option<T>, Argument<T>, middleware pipeline with custom middleware, hosting integration with UseCommandHandler and DI, tab completion for Bash/Zsh/Fish/PowerShell, automatic --version/--help generation, IConsole abstraction with TestConsole for testing, validation, global options, and response files. Documents beta status with production readiness assessment (battle-tested in dotnet CLI).

2. **dotnet-cli-architecture** (`skills/cli-tools/dotnet-cli-architecture/SKILL.md`): Covers clig.dev principles (stdout for data, stderr for diagnostics, NO_COLOR), layered command/handler/service architecture with full example, configuration precedence (appsettings → env vars → CLI args), structured logging with verbosity mapping, exit code conventions (0-125 range), stdin/stdout/stderr patterns including piped input and machine-readable --json output, and comprehensive CLI testing via in-process CommandLineBuilder invocation with TestConsole, service mocks, exit code assertion, and output format verification.

Both skills have name/description frontmatter (≤120 chars), out-of-scope boundary statements for fn-16 (AOT), fn-19 (CI/CD), fn-3 (DI), fn-7 (testing), and use canonical [skill:skill-name] cross-reference syntax. plugin.json not modified (deferred to fn-17.3).
## Evidence
- Commits:
- Tests:
- PRs: