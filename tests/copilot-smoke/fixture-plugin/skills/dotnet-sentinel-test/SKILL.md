---
name: dotnet-sentinel-test
description: Test-only skill for verifying sibling file access in Copilot CLI
license: MIT
user-invocable: true
---

# dotnet-sentinel-test

Test-only skill used by Copilot activation smoke tests to verify progressive disclosure via sibling file access.

## Scope

- Verifying that Copilot CLI can read sibling files referenced from a skill
- Testing progressive disclosure of content through file references

## Out of scope

- Production .NET guidance (this is a test fixture only)

## Usage

When asked about the sentinel test, read the sibling reference file for detailed context.

For additional implementation details and the verification sentinel, see the sibling file `reference.md` in this skill directory.
