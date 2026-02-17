---
name: dotnet-cli-distribution
description: "Choosing CLI output format. AOT vs framework-dependent, RID matrix, single-file, dotnet tool."
---

# dotnet-cli-distribution

CLI distribution strategy for .NET tools: choosing between Native AOT single-file publish, framework-dependent deployment, and `dotnet tool` packaging. Runtime Identifier (RID) matrix planning for cross-platform targets (linux-x64, osx-arm64, win-x64, linux-arm64), single-file publish configuration, and binary size optimization techniques for CLI applications.

**Version assumptions:** .NET 8.0+ baseline. Native AOT for console apps is fully supported since .NET 8. Single-file publish has been mature since .NET 6.

**Out of scope:** Native AOT MSBuild configuration (PublishAot, ILLink descriptors, EnableAotAnalyzer, trimming) -- see [skill:dotnet-native-aot]. AOT-first application design patterns (source gen over reflection, DI choices) -- see [skill:dotnet-aot-architecture]. Multi-platform packaging formats (Homebrew, apt/deb, winget, Scoop) -- see [skill:dotnet-cli-packaging]. Release CI/CD pipeline -- see [skill:dotnet-cli-release-pipeline]. Container-based distribution -- see [skill:dotnet-containers]. General CI/CD patterns -- see [skill:dotnet-gha-patterns] and [skill:dotnet-ado-patterns].

Cross-references: [skill:dotnet-native-aot] for AOT compilation pipeline, [skill:dotnet-aot-architecture] for AOT-safe design patterns, [skill:dotnet-cli-architecture] for CLI layered architecture, [skill:dotnet-cli-packaging] for platform-specific package formats, [skill:dotnet-cli-release-pipeline] for automated release workflows, [skill:dotnet-containers] for container-based distribution, [skill:dotnet-tool-management] for consumer-side tool installation and manifest management.

---

## Distribution Strategy Decision Matrix

Choose the distribution model based on target audience and deployment constraints.

| Strategy | Startup Time | Binary Size | Runtime Required | Best For |
|----------|-------------|-------------|-----------------|----------|
| Native AOT single-file | ~10ms | 10-30 MB | None | Performance-critical CLI tools, broad distribution |
| Framework-dependent single-file | ~100ms | 1-5 MB | .NET runtime | Internal tools where runtime is guaranteed |
| Self-contained single-file | ~100ms | 60-80 MB | None | Simple distribution without AOT complexity |
| `dotnet tool` (global/local) | ~200ms | < 1 MB (NuGet) | .NET SDK | Developer tools, .NET ecosystem users |

### When to Choose Each Strategy

**Native AOT single-file** -- the gold standard for CLI distribution:
- Zero dependencies on target machine (no .NET runtime needed)
- Fastest startup (~10ms vs ~100ms+ for JIT)
- Smallest binary when combined with trimming
- Trade-off: longer build times, no reflection unless preserved
- See [skill:dotnet-native-aot] for PublishAot MSBuild configuration

**Framework-dependent deployment:**
- Smallest artifact size (only app code, no runtime)
- Users must have .NET runtime installed
- Best for internal/enterprise tools where runtime is managed
- Can still use single-file publish for convenience

**Self-contained (non-AOT):**
- Includes .NET runtime in the artifact
- Larger binary than AOT but simpler build process
- Full reflection and dynamic code support
- Good compromise when AOT compat is difficult

**`dotnet tool` packaging:**
- Distributed via NuGet -- simplest publishing workflow
- Users install with `dotnet tool install -g mytool`
- Requires .NET SDK on target (not just runtime)
- Best for developer-facing tools in the .NET ecosystem
- See [skill:dotnet-cli-packaging] for NuGet distribution details

---

## Runtime Identifier (RID) Matrix

### Standard CLI RID Targets

Target the four primary RIDs for broad coverage:

| RID | Platform | Notes |
|-----|----------|-------|
| `linux-x64` | Linux x86_64 | Most Linux servers, CI runners, WSL |
| `linux-arm64` | Linux ARM64 | AWS Graviton, Raspberry Pi 4+, Apple Silicon VMs |
| `osx-arm64` | macOS Apple Silicon | M1/M2/M3+ Macs (primary macOS target) |
| `win-x64` | Windows x86_64 | Windows 10+, Windows Server |

### Optional Extended Targets

| RID | When to Include |
|-----|----------------|
| `osx-x64` | Legacy Intel Mac support (declining market share) |
| `linux-musl-x64` | Alpine Linux / Docker scratch images |
| `linux-musl-arm64` | Alpine on ARM64 |
| `win-arm64` | Windows on ARM (Surface Pro X, Snapdragon laptops) |

### RID Configuration in .csproj

```xml
<!-- Set per publish, not in csproj (avoids accidental RID lock-in) -->
<!-- Use dotnet publish -r <rid> instead -->

<!-- If you must set a default for local development -->
<PropertyGroup Condition="'$(RuntimeIdentifier)' == ''">
  <RuntimeIdentifier>osx-arm64</RuntimeIdentifier>
</PropertyGroup>
```

Publish per RID from the command line:

```bash
# Publish for each target RID
dotnet publish -c Release -r linux-x64
dotnet publish -c Release -r linux-arm64
dotnet publish -c Release -r osx-arm64
dotnet publish -c Release -r win-x64
```

---

## Single-File Publish

Single-file publish bundles the application and its dependencies into one executable.

### Configuration

```xml
<PropertyGroup>
  <PublishSingleFile>true</PublishSingleFile>
  <!-- Required for single-file -->
  <SelfContained>true</SelfContained>
  <!-- Embed PDB for stack traces (optional, adds ~2-5 MB) -->
  <DebugType>embedded</DebugType>
  <!-- Include native libraries in the single file -->
  <IncludeNativeLibrariesForSelfExtract>true</IncludeNativeLibrariesForSelfExtract>
</PropertyGroup>
```

### Single-File with Native AOT

When combined with Native AOT, single-file is implicit -- AOT always produces a single native binary:

```xml
<PropertyGroup>
  <PublishAot>true</PublishAot>
  <!-- PublishSingleFile is not needed -- AOT output is inherently single-file -->
  <!-- SelfContained is implied by PublishAot -->
</PropertyGroup>
```

See [skill:dotnet-native-aot] for the full AOT publish configuration including ILLink, type preservation, and analyzer setup.

### Publish Command

```bash
# Framework-dependent single-file (requires .NET runtime on target)
dotnet publish -c Release -r linux-x64 /p:PublishSingleFile=true --self-contained false

# Self-contained single-file (includes runtime, no AOT)
dotnet publish -c Release -r linux-x64 /p:PublishSingleFile=true --self-contained true

# Native AOT (inherently single-file, smallest and fastest)
dotnet publish -c Release -r linux-x64
# (when PublishAot=true is in csproj)
```

---

## Size Optimization for CLI Binaries

### Trimming (Non-AOT)

Trimming removes unused code from the published output. For self-contained non-AOT builds:

```xml
<PropertyGroup>
  <PublishTrimmed>true</PublishTrimmed>
  <TrimMode>link</TrimMode>
  <!-- Suppress known trim warnings for CLI scenarios -->
  <SuppressTrimAnalysisWarnings>false</SuppressTrimAnalysisWarnings>
</PropertyGroup>
```

### AOT Size Optimization

For Native AOT builds, size is controlled by AOT-specific MSBuild properties. See [skill:dotnet-native-aot] for the full configuration. Key CLI-relevant properties include `StripSymbols`, `OptimizationPreference`, `InvariantGlobalization`, and `StackTraceSupport`.

### Size Comparison (Typical CLI Tool)

| Configuration | Approximate Size |
|---------------|-----------------|
| Self-contained (no trim) | 60-80 MB |
| Self-contained + trimmed | 15-30 MB |
| Native AOT (default) | 15-25 MB |
| Native AOT + size optimized | 8-15 MB |
| Native AOT + invariant globalization + stripped | 5-10 MB |
| Framework-dependent | 1-5 MB |

### Practical Size Reduction Checklist

1. **Enable invariant globalization** if the tool does not need locale-specific formatting (`InvariantGlobalization=true`)
2. **Strip symbols** on Linux/macOS (`StripSymbols=true`) -- keep separate symbol files for crash analysis
3. **Optimize for size** (`OptimizationPreference=Size`) -- minimal runtime performance impact for I/O-bound CLI tools
4. **Disable reflection** where possible -- use source generators for JSON serialization ([skill:dotnet-aot-architecture])
5. **Audit NuGet dependencies** -- each dependency adds to the binary; remove unused packages

---

## Framework-Dependent vs Self-Contained Trade-offs

### Framework-Dependent

```bash
dotnet publish -c Release -r linux-x64 --self-contained false
```

**Advantages:**
- Smallest artifact (1-5 MB)
- Serviced by runtime updates (security patches applied by runtime, not app rebuild)
- Faster publish times

**Disadvantages:**
- Requires matching .NET runtime on target
- Runtime version mismatch causes startup failures
- Users must manage runtime installation

### Self-Contained

```bash
dotnet publish -c Release -r linux-x64 --self-contained true
```

**Advantages:**
- No runtime dependency on target
- App controls exact runtime version
- Side-by-side deployment (multiple apps, different runtimes)

**Disadvantages:**
- Larger artifact (60-80 MB without trimming)
- Must rebuild and redistribute for runtime security patches
- One artifact per target RID

---

## Publishing Workflow

### Local Development

```bash
# Quick local publish for testing
dotnet publish -c Release -r osx-arm64

# Verify the binary
./bin/Release/net8.0/osx-arm64/publish/mytool --version
```

### Producing Release Artifacts

```bash
#!/bin/bash
# build-all.sh -- Produce artifacts for all target RIDs
set -euo pipefail

VERSION="${1:?Usage: build-all.sh <version>}"
PROJECT="src/MyCli/MyCli.csproj"
OUTPUT_DIR="artifacts"

RIDS=("linux-x64" "linux-arm64" "osx-arm64" "win-x64")
# Note: Native AOT cross-compilation for ARM64 on x64 requires platform toolchain
# See [skill:dotnet-cli-release-pipeline] for CI-based cross-compilation setup

for rid in "${RIDS[@]}"; do
  echo "Publishing for $rid..."
  dotnet publish "$PROJECT" \
    -c Release \
    -r "$rid" \
    -o "$OUTPUT_DIR/$rid" \
    /p:Version="$VERSION"
done

# Create archives
for rid in "${RIDS[@]}"; do
  if [[ "$rid" == win-* ]]; then
    (cd "$OUTPUT_DIR/$rid" && zip -q "../mytool-$VERSION-$rid.zip" *)
  else
    tar -czf "$OUTPUT_DIR/mytool-$VERSION-$rid.tar.gz" -C "$OUTPUT_DIR/$rid" .
  fi
done

echo "Artifacts in $OUTPUT_DIR/"
```

### Checksum Generation

Always produce checksums for release artifacts:

```bash
# Generate SHA-256 checksums
cd artifacts
shasum -a 256 *.tar.gz *.zip > checksums-sha256.txt
```

See [skill:dotnet-cli-release-pipeline] for automating this in GitHub Actions.

---

## Agent Gotchas

1. **Do not set RuntimeIdentifier in the .csproj for multi-platform CLI tools.** Hardcoding a RID in the project file prevents building for other platforms. Pass `-r <rid>` at publish time instead.
2. **Do not use PublishSingleFile with PublishAot.** Native AOT output is inherently single-file. Setting both is redundant and may cause confusing build warnings.
3. **Do not skip InvariantGlobalization for size-sensitive CLI tools.** Globalization data adds ~25 MB to AOT binaries. Most CLI tools that do not format locale-specific dates/currencies should enable `InvariantGlobalization=true`.
4. **Do not distribute self-contained non-trimmed binaries.** A 60-80 MB CLI tool is unacceptable for end users. Either trim (PublishTrimmed), use AOT, or distribute as framework-dependent.
5. **Do not forget to produce checksums for release artifacts.** Users and package managers need SHA-256 checksums to verify download integrity. See [skill:dotnet-cli-release-pipeline] for automated checksum generation.
6. **Do not hardcode secrets in publish scripts.** Use environment variable placeholders (`${SIGNING_KEY}`) with a comment about CI secret storage for any signing or upload credentials.

---

## References

- [.NET application publishing overview](https://learn.microsoft.com/en-us/dotnet/core/deploying/)
- [Single-file deployment](https://learn.microsoft.com/en-us/dotnet/core/deploying/single-file/overview)
- [Native AOT deployment](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/)
- [Runtime Identifier (RID) catalog](https://learn.microsoft.com/en-us/dotnet/core/rid-catalog)
- [Trimming options](https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/trimming-options)
