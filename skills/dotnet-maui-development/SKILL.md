---
name: dotnet-maui-development
description: Builds .NET MAUI mobile apps. Project structure, XAML/MVVM, platform services, caveats.
license: MIT
user-invocable: false
---

# dotnet-maui-development

.NET MAUI cross-platform development: single-project structure with platform folders, XAML data binding with MVVM (CommunityToolkit.Mvvm), Shell navigation, platform services via partial classes and conditional compilation, dependency injection, Hot Reload per platform, and .NET 11 improvements (XAML source gen, CoreCLR for Android, `dotnet run` device selection). Includes honest current-state assessment and migration options.

**Version assumptions:** .NET 8.0+ baseline (MAUI ships with .NET 8+). .NET 11 Preview 1 content explicitly marked. Examples use the latest stable APIs.

## Scope

- Single-project structure with platform folders
- XAML data binding with MVVM (CommunityToolkit.Mvvm)
- Shell navigation and platform services
- Dependency injection and Hot Reload
- Current-state assessment and migration options
- .NET 11 improvements (XAML source gen, CoreCLR for Android)

## Out of scope

- MAUI Native AOT on iOS/Mac Catalyst -- see [skill:dotnet-maui-aot]
- MAUI testing (Appium, XHarness) -- see [skill:dotnet-maui-testing]
- General Native AOT patterns -- see [skill:dotnet-native-aot]
- UI framework selection decision tree -- see [skill:dotnet-ui-chooser]

Cross-references: [skill:dotnet-maui-aot] for Native AOT on iOS/Mac Catalyst, [skill:dotnet-maui-testing] for testing patterns, [skill:dotnet-version-detection] for TFM detection, [skill:dotnet-native-aot] for general AOT patterns, [skill:dotnet-ui-chooser] for framework selection, [skill:dotnet-accessibility] for accessibility patterns (SemanticProperties, screen readers).

---

## Project Structure

MAUI uses a single-project architecture. One `.csproj` targets all platforms via multi-targeting, with platform-specific code in platform folders.

```xml
<!-- MyApp.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFrameworks>net8.0-android;net8.0-ios;net8.0-maccatalyst</TargetFrameworks>
    <TargetFrameworks Condition="$([MSBuild]::IsOSPlatform('windows'))">
      $(TargetFrameworks);net8.0-windows10.0.19041.0
    </TargetFrameworks>
    <OutputType>Exe</OutputType>
    <UseMaui>true</UseMaui>
    <SingleProject>true</SingleProject>
    <RootNamespace>MyApp</RootNamespace>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="CommunityToolkit.Mvvm" Version="8.*" />
    <PackageReference Include="CommunityToolkit.Maui" Version="9.*" />
  </ItemGroup>
</Project>
```

### Project Layout

```
MyApp/
  MyApp/
    App.xaml / App.xaml.cs            # Application entry, resource dictionaries
    AppShell.xaml / AppShell.xaml.cs  # Shell navigation definition
    MauiProgram.cs                   # Host builder, DI, service registration
    MainPage.xaml / MainPage.xaml.cs  # Initial page
    ViewModels/                      # MVVM ViewModels
    Views/                           # XAML pages
    Models/                          # Data models
    Services/                        # Service interfaces and implementations
    Resources/
      Fonts/                         # Custom fonts (.ttf/.otf)
      Images/                        # SVG/PNG images (auto-resized per platform)
      Styles/                        # Shared styles, colors, resource dictionaries
      Raw/                           # Raw assets (JSON, etc.)
      Splash/                        # Splash screen image
    Platforms/
      Android/                       # AndroidManifest.xml, MainActivity.cs
      iOS/                           # Info.plist, AppDelegate.cs
      MacCatalyst/                   # Info.plist, AppDelegate.cs
      Windows/                       # Package.appxmanifest, App.xaml
    Properties/
      launchSettings.json
  MyApp.Tests/                       # Unit tests
```

### Resource Management

MAUI handles resource files declaratively. Images are auto-resized per platform from a single source:

```xml
<!-- Resources are configured in .csproj ItemGroups -->
<ItemGroup>
  <!-- SVG/PNG images: MAUI resizes for each platform density -->
  <MauiImage Include="Resources\Images\*" />

  <!-- Fonts: registered automatically -->
  <MauiFont Include="Resources\Fonts\*" />

  <!-- Splash screen -->
  <MauiSplashScreen Include="Resources\Splash\splash.svg"
                    Color="#512BD4" BaseSize="128,128" />

  <!-- App icon -->
  <MauiIcon Include="Resources\AppIcon\appicon.svg"
            ForegroundFile="Resources\AppIcon\appiconfg.svg"
            Color="#512BD4" />
</ItemGroup>
```

---


For detailed code examples (XAML data binding, MVVM, Shell navigation, platform services, .NET 11 improvements, Hot Reload), see `examples.md` in this skill directory.

## Agent Gotchas

1. **Do not create separate platform projects.** MAUI uses a single-project structure. Platform-specific code goes in the `Platforms/` folder within the same project, not in separate Android/iOS projects (that was Xamarin.Forms).
2. **Do not mix MVVM Toolkit attributes with manual `INotifyPropertyChanged`.** Use `[ObservableProperty]` consistently. Mixing source-generated and hand-written property changed implementations causes subtle binding bugs.
3. **Do not call async methods in constructors.** Use `OnAppearing()` or a loaded command to trigger data loading. Constructor async calls cause unobserved exceptions and race conditions with binding context initialization.
4. **Do not use `Device.BeginInvokeOnMainThread`.** It is deprecated. Use `MainThread.BeginInvokeOnMainThread()` or `MainThread.InvokeOnMainThreadAsync()` from `Microsoft.Maui.ApplicationModel` instead.
5. **Do not hardcode platform checks with `RuntimeInformation`.** Use `DeviceInfo.Platform` comparisons (`DevicePlatform.Android`, `DevicePlatform.iOS`) which are MAUI's cross-platform abstraction for platform detection.
6. **Do not use `{Binding}` without `x:DataType`.** Always set `x:DataType` on the page and data templates to enable compiled bindings. Reflection-based bindings are slower and not caught at build time.
7. **Pages should generally be Transient, not Singleton.** Singleton pages cause stale data and memory leaks from retained bindings. If state preservation is needed (e.g., tabbed pages), use a Singleton ViewModel with a Transient page.
8. **Do not forget to register Shell routes for non-tab pages.** Pages pushed onto the navigation stack (via `GoToAsync`) must be registered with `Routing.RegisterRoute` in `AppShell` constructor, or navigation throws `RouteNotFoundException`.

---

## Prerequisites

- .NET 8.0+ (.NET MAUI ships with .NET 8+)
- MAUI workload: `dotnet workload install maui`
- Platform SDKs: Android SDK (API 21+), Xcode (macOS only, for iOS/Mac Catalyst), Windows App SDK (for Windows)
- Visual Studio 2022+ with MAUI workload, VS Code with .NET MAUI extension, or JetBrains Rider 2024.2+

---

## References

- [.NET MAUI Documentation](https://learn.microsoft.com/en-us/dotnet/maui/)
- [.NET 11 Preview 1 Announcement](https://devblogs.microsoft.com/dotnet/dotnet-11-preview-1/)
- [CommunityToolkit.Mvvm](https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/)
- [MAUI Shell Navigation](https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/shell/)
- [MAUI Single Project](https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/single-project)
- [MAUI Platform Integration](https://learn.microsoft.com/en-us/dotnet/maui/platform-integration/)
