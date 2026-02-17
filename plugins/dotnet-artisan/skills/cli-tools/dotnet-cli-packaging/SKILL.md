---
name: dotnet-cli-packaging
description: "Publishing to package managers. Homebrew, apt/deb, winget, Scoop, Chocolatey manifests."
---

# dotnet-cli-packaging

Multi-platform packaging for .NET CLI tools: Homebrew formula authoring (binary tap and cask), apt/deb packaging with `dpkg-deb`, winget manifest YAML schema and PR submission to `winget-pkgs`, Scoop manifest JSON, Chocolatey package creation, `dotnet tool` global/local packaging, and NuGet distribution.

**Version assumptions:** .NET 8.0+ baseline. Package manager formats are stable across .NET versions.

**Out of scope:** CLI distribution strategy (AOT vs framework-dependent vs dotnet tool decision) -- see [skill:dotnet-cli-distribution]. Release CI/CD pipeline that automates packaging -- see [skill:dotnet-cli-release-pipeline]. Native AOT compilation -- see [skill:dotnet-native-aot]. Container-based distribution -- see [skill:dotnet-containers]. General CI/CD patterns -- see [skill:dotnet-gha-patterns] and [skill:dotnet-ado-patterns].

Cross-references: [skill:dotnet-cli-distribution] for distribution strategy and RID matrix, [skill:dotnet-cli-release-pipeline] for automated package publishing, [skill:dotnet-native-aot] for AOT binary production, [skill:dotnet-containers] for container-based distribution, [skill:dotnet-tool-management] for consumer-side tool installation and manifest management.

---

## Homebrew (macOS / Linux)

Homebrew is the primary package manager for macOS and widely used on Linux. Two distribution formats exist for CLI tools.

### Binary Tap (Formula)

A formula downloads pre-built binaries per platform. This is the recommended approach for Native AOT CLI tools.

```ruby
# Formula/mytool.rb
class Mytool < Formula
  desc "A CLI tool for managing widgets"
  homepage "https://github.com/myorg/mytool"
  version "1.2.3"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/myorg/mytool/releases/download/v1.2.3/mytool-1.2.3-osx-arm64.tar.gz"
      sha256 "abc123..."
    end
    # Optional: remove on_intel block if not targeting Intel Macs
    on_intel do
      url "https://github.com/myorg/mytool/releases/download/v1.2.3/mytool-1.2.3-osx-x64.tar.gz"
      sha256 "def456..."
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/myorg/mytool/releases/download/v1.2.3/mytool-1.2.3-linux-arm64.tar.gz"
      sha256 "ghi789..."
    end
    on_intel do
      url "https://github.com/myorg/mytool/releases/download/v1.2.3/mytool-1.2.3-linux-x64.tar.gz"
      sha256 "jkl012..."
    end
  end

  def install
    bin.install "mytool"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/mytool --version")
  end
end
```

### Hosting a Tap

A tap is a Git repository containing formulae. Create a repo named `homebrew-tap`:

```
myorg/homebrew-tap/
  Formula/
    mytool.rb
```

Users install with:

```bash
brew tap myorg/tap
brew install mytool
```

### Homebrew Cask

Casks are for GUI applications or tools with an installer. For pure CLI tools, prefer formulae over casks.

```ruby
# Casks/mytool.rb -- only if the tool has a GUI component
cask "mytool" do
  version "1.2.3"
  sha256 "abc123..."

  url "https://github.com/myorg/mytool/releases/download/v#{version}/mytool-#{version}-osx-arm64.tar.gz"
  name "MyTool"
  homepage "https://github.com/myorg/mytool"

  binary "mytool"
end
```

---

## apt/deb (Debian/Ubuntu)

### Building a .deb Package with dpkg-deb

Create the package directory structure:

```
mytool_1.2.3_amd64/
  DEBIAN/
    control
  usr/
    bin/
      mytool
```

**Control file:**

```
Package: mytool
Version: 1.2.3
Section: utils
Priority: optional
Architecture: amd64
Maintainer: My Org <dev@myorg.com>
Description: A CLI tool for managing widgets
 MyTool provides fast widget management from the command line.
 Built with .NET Native AOT for zero-dependency execution.
Homepage: https://github.com/myorg/mytool
```

**Build the package:**

```bash
#!/bin/bash
set -euo pipefail

VERSION="${1:?Usage: build-deb.sh <version>}"
ARCH="amd64"  # or arm64
PKG_DIR="mytool_${VERSION}_${ARCH}"

mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/usr/bin"

# Copy the published binary
cp "artifacts/linux-x64/mytool" "$PKG_DIR/usr/bin/mytool"
chmod 755 "$PKG_DIR/usr/bin/mytool"

# Write control file
cat > "$PKG_DIR/DEBIAN/control" << EOF
Package: mytool
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Maintainer: My Org <dev@myorg.com>
Description: A CLI tool for managing widgets
Homepage: https://github.com/myorg/mytool
EOF

# Build the .deb
dpkg-deb --build --root-owner-group "$PKG_DIR"
echo "Built: ${PKG_DIR}.deb"
```

**RID to Debian architecture mapping:**

| .NET RID | Debian Architecture |
|----------|-------------------|
| `linux-x64` | `amd64` |
| `linux-arm64` | `arm64` |

### Installing the .deb

```bash
sudo dpkg -i mytool_1.2.3_amd64.deb
```

---

## winget (Windows Package Manager)

### Manifest YAML Schema

winget manifests consist of multiple YAML files in a versioned directory structure within the `microsoft/winget-pkgs` repository.

**Directory structure:**

```
manifests/
  m/
    MyOrg/
      MyTool/
        1.2.3/
          MyOrg.MyTool.yaml              # Version manifest
          MyOrg.MyTool.installer.yaml    # Installer manifest
          MyOrg.MyTool.locale.en-US.yaml # Locale manifest
```

**Version manifest (MyOrg.MyTool.yaml):**

```yaml
PackageIdentifier: MyOrg.MyTool
PackageVersion: 1.2.3
DefaultLocale: en-US
ManifestType: version
ManifestVersion: 1.9.0
```

**Installer manifest (MyOrg.MyTool.installer.yaml):**

```yaml
PackageIdentifier: MyOrg.MyTool
PackageVersion: 1.2.3
InstallerType: zip
NestedInstallerType: portable
NestedInstallerFiles:
  - RelativeFilePath: mytool.exe
    PortableCommandAlias: mytool
Installers:
  - Architecture: x64
    InstallerUrl: https://github.com/myorg/mytool/releases/download/v1.2.3/mytool-1.2.3-win-x64.zip
    InstallerSha256: ABC123...
  - Architecture: arm64
    InstallerUrl: https://github.com/myorg/mytool/releases/download/v1.2.3/mytool-1.2.3-win-arm64.zip
    InstallerSha256: DEF456...
ManifestType: installer
ManifestVersion: 1.9.0
```

**Locale manifest (MyOrg.MyTool.locale.en-US.yaml):**

```yaml
PackageIdentifier: MyOrg.MyTool
PackageVersion: 1.2.3
PackageLocale: en-US
PackageName: MyTool
Publisher: My Org
ShortDescription: A CLI tool for managing widgets
License: MIT
PackageUrl: https://github.com/myorg/mytool
ManifestType: defaultLocale
ManifestVersion: 1.9.0
```

### Submitting to winget-pkgs

1. Fork `microsoft/winget-pkgs` on GitHub
2. Create the manifest files in the correct directory structure
3. Validate locally: `winget validate --manifest <path>`
4. Submit a PR -- automated checks run against the manifest
5. Microsoft team reviews and merges

See [skill:dotnet-cli-release-pipeline] for automating winget PR creation.

---

## Scoop (Windows)

Scoop is popular among Windows power users. Manifests are JSON files in a bucket repository.

### Scoop Manifest

```json
{
  "version": "1.2.3",
  "description": "A CLI tool for managing widgets",
  "homepage": "https://github.com/myorg/mytool",
  "license": "MIT",
  "architecture": {
    "64bit": {
      "url": "https://github.com/myorg/mytool/releases/download/v1.2.3/mytool-1.2.3-win-x64.zip",
      "hash": "abc123..."
    },
    "arm64": {
      "url": "https://github.com/myorg/mytool/releases/download/v1.2.3/mytool-1.2.3-win-arm64.zip",
      "hash": "def456..."
    }
  },
  "bin": "mytool.exe",
  "checkver": {
    "github": "https://github.com/myorg/mytool"
  },
  "autoupdate": {
    "architecture": {
      "64bit": {
        "url": "https://github.com/myorg/mytool/releases/download/v$version/mytool-$version-win-x64.zip"
      },
      "arm64": {
        "url": "https://github.com/myorg/mytool/releases/download/v$version/mytool-$version-win-arm64.zip"
      }
    }
  }
}
```

### Hosting a Scoop Bucket

Create a GitHub repo named `scoop-mytool` (or `scoop-bucket`):

```
myorg/scoop-mytool/
  bucket/
    mytool.json
```

Users install with:

```powershell
scoop bucket add myorg https://github.com/myorg/scoop-mytool
scoop install mytool
```

---

## Chocolatey

Chocolatey is Windows' most established package manager for binary distribution.

### Package Structure

```
mytool/
  mytool.nuspec
  tools/
    chocolateyInstall.ps1
    LICENSE.txt
```

**mytool.nuspec:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.xmldata.org/2004/07/nuspec">
  <metadata>
    <id>mytool</id>
    <version>1.2.3</version>
    <title>MyTool</title>
    <authors>My Org</authors>
    <projectUrl>https://github.com/myorg/mytool</projectUrl>
    <license type="expression">MIT</license>
    <description>A CLI tool for managing widgets.</description>
    <tags>cli dotnet tools</tags>
  </metadata>
</package>
```

**tools/chocolateyInstall.ps1:**

```powershell
$ErrorActionPreference = 'Stop'

$packageArgs = @{
  packageName    = 'mytool'
  url64bit       = 'https://github.com/myorg/mytool/releases/download/v1.2.3/mytool-1.2.3-win-x64.zip'
  checksum64     = 'ABC123...'
  checksumType64 = 'sha256'
  unzipLocation  = "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"
}

Install-ChocolateyZipPackage @packageArgs
```

### Building and Publishing

```powershell
# Pack the .nupkg
choco pack mytool.nuspec

# Test locally
choco install mytool --source="." --force

# Push to Chocolatey Community Repository
choco push mytool.1.2.3.nupkg --source https://push.chocolatey.org/ --api-key $env:CHOCO_API_KEY
```

---

## dotnet tool (Global and Local)

`dotnet tool` is the simplest distribution for .NET developers. Tools are distributed as NuGet packages.

### Project Configuration for Tool Packaging

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>

    <!-- Tool packaging properties -->
    <PackAsTool>true</PackAsTool>
    <ToolCommandName>mytool</ToolCommandName>
    <PackageId>MyOrg.MyTool</PackageId>
    <Version>1.2.3</Version>
    <Description>A CLI tool for managing widgets</Description>
    <Authors>My Org</Authors>
    <PackageLicenseExpression>MIT</PackageLicenseExpression>
    <PackageProjectUrl>https://github.com/myorg/mytool</PackageProjectUrl>
    <PackageReadmeFile>README.md</PackageReadmeFile>
  </PropertyGroup>

  <ItemGroup>
    <None Include="../../README.md" Pack="true" PackagePath="/" />
  </ItemGroup>
</Project>
```

### Building and Publishing

```bash
# Pack the tool
dotnet pack -c Release

# Publish to NuGet.org
dotnet nuget push bin/Release/MyOrg.MyTool.1.2.3.nupkg \
  --source https://api.nuget.org/v3/index.json \
  --api-key "$NUGET_API_KEY"
```

### Installing dotnet Tools

```bash
# Global tool (available system-wide)
dotnet tool install -g MyOrg.MyTool

# Local tool (per-project, tracked in .config/dotnet-tools.json)
dotnet new tool-manifest  # first time only
dotnet tool install MyOrg.MyTool

# Update
dotnet tool update -g MyOrg.MyTool

# Run local tool
dotnet tool run mytool
# or just:
dotnet mytool
```

### Global vs Local Tools

| Aspect | Global Tool | Local Tool |
|--------|------------|------------|
| Scope | System-wide (per user) | Per-project directory |
| Install location | `~/.dotnet/tools` | `.config/dotnet-tools.json` |
| Version management | Manual update | Tracked in source control |
| CI/CD | Must install before use | `dotnet tool restore` restores all |
| Best for | Personal productivity tools | Project-specific build tools |

---

## NuGet Distribution

For tools distributed as NuGet packages (either as `dotnet tool` or standalone):

### Package Metadata

```xml
<PropertyGroup>
  <PackageId>MyOrg.MyTool</PackageId>
  <Version>1.2.3</Version>
  <Description>A CLI tool for managing widgets</Description>
  <Authors>My Org</Authors>
  <PackageLicenseExpression>MIT</PackageLicenseExpression>
  <PackageProjectUrl>https://github.com/myorg/mytool</PackageProjectUrl>
  <PackageReadmeFile>README.md</PackageReadmeFile>
  <PackageTags>cli;tools;widgets</PackageTags>
  <RepositoryUrl>https://github.com/myorg/mytool</RepositoryUrl>
  <RepositoryType>git</RepositoryType>
</PropertyGroup>
```

### Publishing to NuGet.org

```bash
# Pack
dotnet pack -c Release -o ./nupkgs

# Push (use env var for API key -- never hardcode)
dotnet nuget push ./nupkgs/MyOrg.MyTool.1.2.3.nupkg \
  --source https://api.nuget.org/v3/index.json \
  --api-key "$NUGET_API_KEY"
```

### Private Feed Distribution

```bash
# Push to a private feed (Azure Artifacts, GitHub Packages, etc.)
dotnet nuget push ./nupkgs/MyOrg.MyTool.1.2.3.nupkg \
  --source https://pkgs.dev.azure.com/myorg/_packaging/myfeed/nuget/v3/index.json \
  --api-key "$AZURE_ARTIFACTS_PAT"
```

---

## Package Format Comparison

| Format | Platform | Requires .NET | Auto-Update | Difficulty |
|--------|----------|--------------|-------------|------------|
| Homebrew formula | macOS, Linux | No (binary tap) | `brew upgrade` | Medium |
| apt/deb | Debian/Ubuntu | No (AOT binary) | Via apt repo | Medium |
| winget | Windows 10+ | No (portable) | `winget upgrade` | Medium |
| Scoop | Windows | No (portable) | `scoop update` | Low |
| Chocolatey | Windows | No | `choco upgrade` | Medium |
| dotnet tool | Cross-platform | Yes (SDK) | `dotnet tool update` | Low |
| NuGet (library) | Cross-platform | Yes (SDK) | NuGet restore | Low |

---

## Agent Gotchas

1. **Do not hardcode SHA-256 hashes in package manifests.** Generate checksums from actual release artifacts, not placeholder values. All package managers validate checksums against downloaded files.
2. **Do not use `InstallerType: exe` for portable CLI tools in winget.** Use `InstallerType: zip` with `NestedInstallerType: portable` for standalone executables. The `exe` type implies an installer with silent flags.
3. **Do not forget `PackAsTool` for dotnet tool projects.** Without `<PackAsTool>true</PackAsTool>`, `dotnet pack` produces a library package, not an installable tool.
4. **Do not hardcode API keys in packaging scripts.** Use environment variable references (`$NUGET_API_KEY`, `$env:CHOCO_API_KEY`) with a comment noting CI secret configuration.
5. **Do not mix Homebrew formula and cask for the same CLI tool.** Pure CLI tools should use formulae. Casks are for GUI applications with macOS app bundles.
6. **Do not skip the `test` block in Homebrew formulae.** Homebrew CI runs formula tests. A missing test block causes review rejection. At minimum, test `--version` output.

---

## References

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Homebrew Taps](https://docs.brew.sh/Taps)
- [dpkg-deb manual](https://man7.org/linux/man-pages/man1/dpkg-deb.1.html)
- [winget manifest schema](https://learn.microsoft.com/en-us/windows/package-manager/package/manifest)
- [winget-pkgs repository](https://github.com/microsoft/winget-pkgs)
- [Scoop Wiki](https://github.com/ScoopInstaller/Scoop/wiki)
- [Chocolatey package creation](https://docs.chocolatey.org/en-us/create/create-packages)
- [.NET tool packaging](https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools-how-to-create)
- [NuGet publishing](https://learn.microsoft.com/en-us/nuget/nuget-org/publish-a-package)
