# fn-7 Testing Cross-Reference Reconciliation

Reconciliation of fn-7 (Testing Foundation Skills) placeholder comments across
architecture and serialization skills. All deferred placeholder comments referencing
fn-7 testing skills have been replaced with canonical `[skill:...]` cross-references.

## Affected Skills

### Architecture

The following architecture skills contained fn-7 placeholders (now reconciled):

1. `dotnet-architecture-patterns` -- replaced with `[skill:dotnet-testing-strategy]`, `[skill:dotnet-integration-testing]`
2. `dotnet-background-services` -- replaced with `[skill:dotnet-testing-strategy]`, `[skill:dotnet-integration-testing]`
3. `dotnet-resilience` -- replaced with `[skill:dotnet-integration-testing]`, `[skill:dotnet-xunit]`
4. `dotnet-http-client` -- replaced with `[skill:dotnet-integration-testing]` (scope boundary + inline code comment)
5. `dotnet-observability` -- replaced with `[skill:dotnet-integration-testing]`
6. `dotnet-efcore-patterns` -- replaced with `[skill:dotnet-integration-testing]`
7. `dotnet-efcore-architecture` -- replaced with `[skill:dotnet-integration-testing]`
8. `dotnet-data-access-strategy` -- replaced with `[skill:dotnet-integration-testing]`
9. `dotnet-containers` -- replaced with `[skill:dotnet-integration-testing]`
10. `dotnet-container-deployment` -- replaced with `[skill:dotnet-integration-testing]`, `[skill:dotnet-playwright]`

### Serialization

The following serialization skills contained fn-7 placeholders (now reconciled):

1. `dotnet-grpc` -- replaced with `[skill:dotnet-integration-testing]`
2. `dotnet-serialization` -- replaced with `[skill:dotnet-integration-testing]`
3. `dotnet-realtime-communication` -- replaced with `[skill:dotnet-integration-testing]`
4. `dotnet-service-communication` -- replaced with `[skill:dotnet-integration-testing]`

### Project Structure

1. `dotnet-add-testing` -- replaced fn-7 references with `[skill:dotnet-xunit]`, `[skill:dotnet-integration-testing]`, `[skill:dotnet-blazor-testing]`, `[skill:dotnet-maui-testing]`, `[skill:dotnet-uno-testing]`, `[skill:dotnet-snapshot-testing]`, `[skill:dotnet-test-quality]`, `[skill:dotnet-testing-strategy]`

## Verification

After reconciliation, run:

```bash
# Confirm no deferred testing placeholders remain in skills/
HITS=$(grep -rl 'TODO' skills/ --include='*.md')
echo "$HITS" | xargs grep -l 'fn-7'  # expect empty

# Confirm canonical cross-refs are present in architecture skills
grep -rl "\[skill:dotnet-integration-testing\]" skills/architecture/*/SKILL.md  # expect >= 4

# Confirm canonical cross-refs are present in serialization skills
grep -rl "\[skill:dotnet-integration-testing\]" skills/serialization/*/SKILL.md  # expect >= 4

# Confirm all 10 testing skills registered in plugin.json
grep -c "skills/testing/" .claude-plugin/plugin.json  # expect 10
```
