# fn-7 Testing Cross-Reference Reconciliation

When fn-7 (Testing Foundation Skills) lands, replace all deferred placeholder comments
in fn-5 architecture skills with canonical `[skill:...]` cross-references.

## Affected Skills

The following skills contain `<!-- TODO: fn-7 reconciliation -->` placeholders:

1. `dotnet-architecture-patterns` -- replace with canonical testing strategy cross-ref
2. `dotnet-background-services` -- replace with canonical testing cross-ref
3. `dotnet-resilience` -- replace with canonical testing cross-ref
4. `dotnet-http-client` -- replace with canonical testing cross-ref
5. `dotnet-observability` -- replace with `[skill:dotnet-integration-testing]`
6. `dotnet-efcore-patterns` -- replace with `[skill:dotnet-integration-testing]`
7. `dotnet-efcore-architecture` -- replace with `[skill:dotnet-integration-testing]`
8. `dotnet-data-access-strategy` -- replace with `[skill:dotnet-integration-testing]`
9. `dotnet-containers` -- replace with canonical testing cross-ref
10. `dotnet-container-deployment` -- replace with canonical testing cross-ref

## Verification

After reconciliation, run:

```bash
# Confirm no placeholders remain
grep -rl "TODO.*fn-7" skills/architecture/*/SKILL.md  # expect empty

# Confirm canonical cross-refs are present
grep -rl "\[skill:dotnet-integration-testing\]" skills/architecture/*/SKILL.md  # expect >= 4
```
