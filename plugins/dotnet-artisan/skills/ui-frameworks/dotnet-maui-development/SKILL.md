---
name: dotnet-maui-development
description: "Building .NET MAUI apps. Project structure, XAML/MVVM, platform services, current caveats."
---

# dotnet-maui-development

.NET MAUI cross-platform development: single-project structure with platform folders, XAML data binding with MVVM (CommunityToolkit.Mvvm), Shell navigation, platform services via partial classes and conditional compilation, dependency injection, Hot Reload per platform, and .NET 11 improvements (XAML source gen, CoreCLR for Android, `dotnet run` device selection). Includes honest current-state assessment and migration options.

**Version assumptions:** .NET 8.0+ baseline (MAUI ships with .NET 8+). .NET 11 Preview 1 content explicitly marked. Examples use the latest stable APIs.

**Scope boundary:** This skill owns MAUI project structure, XAML/MVVM patterns, platform services, current-state assessment, migration options, and .NET 11 improvements. MAUI Native AOT on iOS/Mac Catalyst is owned by [skill:dotnet-maui-aot].

**Out of scope:** MAUI testing (Appium, XHarness, platform-specific testing) -- see [skill:dotnet-maui-testing]. General Native AOT patterns -- see [skill:dotnet-native-aot]. UI framework selection decision tree -- see [skill:dotnet-ui-chooser].

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

## XAML Patterns

### Data Binding Fundamentals

MAUI XAML data binding connects UI elements to ViewModel properties. Use `{Binding}` with proper `BindingContext` setup.

```xml
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:vm="clr-namespace:MyApp.ViewModels"
             x:Class="MyApp.Views.ProductListPage"
             x:DataType="vm:ProductListViewModel">

    <VerticalStackLayout Padding="16" Spacing="12">
        <SearchBar Text="{Binding SearchTerm}"
                   SearchCommand="{Binding SearchCommand}" />

        <CollectionView ItemsSource="{Binding Products}"
                        SelectionMode="Single"
                        SelectionChangedCommand="{Binding SelectProductCommand}"
                        SelectionChangedCommandParameter="{Binding SelectedItem,
                            Source={RelativeSource Self}}">
            <CollectionView.ItemTemplate>
                <DataTemplate x:DataType="model:Product">
                    <Frame Padding="12" Margin="0,4">
                        <HorizontalStackLayout Spacing="12">
                            <Image Source="{Binding ImageUrl}"
                                   HeightRequest="60" WidthRequest="60" />
                            <VerticalStackLayout>
                                <Label Text="{Binding Name}"
                                       FontAttributes="Bold" />
                                <Label Text="{Binding Price, StringFormat='{0:C}'}"
                                       TextColor="Gray" />
                            </VerticalStackLayout>
                        </HorizontalStackLayout>
                    </Frame>
                </DataTemplate>
            </CollectionView.ItemTemplate>
        </CollectionView>
    </VerticalStackLayout>
</ContentPage>
```

**Compiled bindings:** Use `x:DataType` on pages and data templates to enable compiled bindings. Compiled bindings are type-checked at build time and faster at runtime than reflection-based bindings.

### MVVM with CommunityToolkit.Mvvm

CommunityToolkit.Mvvm (Microsoft MVVM Toolkit) is the recommended MVVM framework for MAUI. It uses source generators to eliminate boilerplate.

```csharp
// ViewModels/ProductListViewModel.cs
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class ProductListViewModel : ObservableObject
{
    private readonly IProductService _productService;
    private readonly INavigationService _navigationService;

    public ProductListViewModel(
        IProductService productService,
        INavigationService navigationService)
    {
        _productService = productService;
        _navigationService = navigationService;
    }

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(SearchCommand))]
    private string _searchTerm = "";

    [ObservableProperty]
    private ObservableCollection<Product> _products = [];

    [ObservableProperty]
    private bool _isLoading;

    [RelayCommand]
    private async Task LoadProductsAsync(CancellationToken ct)
    {
        IsLoading = true;
        try
        {
            var items = await _productService.GetProductsAsync(ct);
            Products = new ObservableCollection<Product>(items);
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand(CanExecute = nameof(CanSearch))]
    private async Task SearchAsync(CancellationToken ct)
    {
        var results = await _productService.SearchAsync(SearchTerm, ct);
        Products = new ObservableCollection<Product>(results);
    }

    private bool CanSearch() => !string.IsNullOrWhiteSpace(SearchTerm);

    [RelayCommand]
    private async Task SelectProductAsync(Product? product)
    {
        if (product is null) return;
        await _navigationService.GoToAsync(
            nameof(ProductDetailPage),
            new Dictionary<string, object> { ["Product"] = product });
    }
}
```

**Key source generator attributes:**
- `[ObservableProperty]` -- generates property with `INotifyPropertyChanged` from a backing field
- `[RelayCommand]` -- generates `ICommand` from a method (supports async, cancellation, `CanExecute`)
- `[NotifyPropertyChangedFor]` -- raises `PropertyChanged` for dependent properties
- `[NotifyCanExecuteChangedFor]` -- re-evaluates command `CanExecute` when property changes

### Shell Navigation

Shell defines the visual hierarchy and navigation structure. It supports flyout, tab, and URI-based navigation.

```xml
<!-- AppShell.xaml -->
<Shell xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
       xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
       xmlns:views="clr-namespace:MyApp.Views"
       x:Class="MyApp.AppShell">

    <!-- Tab-based navigation -->
    <TabBar>
        <ShellContent Title="Products"
                      Icon="products.png"
                      ContentTemplate="{DataTemplate views:ProductListPage}" />

        <ShellContent Title="Cart"
                      Icon="cart.png"
                      ContentTemplate="{DataTemplate views:CartPage}" />

        <ShellContent Title="Profile"
                      Icon="profile.png"
                      ContentTemplate="{DataTemplate views:ProfilePage}" />
    </TabBar>
</Shell>
```

```csharp
// Register routes for pages not in the Shell visual hierarchy
// (pushed onto the navigation stack, not direct Shell tabs)
public partial class AppShell : Shell
{
    public AppShell()
    {
        InitializeComponent();
        Routing.RegisterRoute(nameof(ProductDetailPage), typeof(ProductDetailPage));
        Routing.RegisterRoute(nameof(CheckoutPage), typeof(CheckoutPage));
    }
}
```

```csharp
// Navigate with parameters
await Shell.Current.GoToAsync(nameof(ProductDetailPage),
    new Dictionary<string, object>
    {
        ["Product"] = selectedProduct
    });

// Receive parameters via QueryProperty
[QueryProperty(nameof(Product), "Product")]
public partial class ProductDetailViewModel : ObservableObject
{
    [ObservableProperty]
    private Product _product = null!;
}
```

### ContentPage Lifecycle

```csharp
public partial class ProductListPage : ContentPage
{
    private readonly ProductListViewModel _viewModel;

    public ProductListPage(ProductListViewModel viewModel)
    {
        InitializeComponent();
        _viewModel = viewModel;
        BindingContext = viewModel;
    }

    protected override async void OnAppearing()
    {
        base.OnAppearing();
        // Load data when page appears (not in constructor)
        await _viewModel.LoadProductsCommand.ExecuteAsync(null);
    }

    protected override void OnDisappearing()
    {
        base.OnDisappearing();
        // Cancel pending operations, unsubscribe events
    }
}
```

---

## Platform Services

### Partial Classes for Platform-Specific Code

Use partial classes with platform-specific implementations in the Platforms folder. The build system compiles the correct implementation for each target.

```csharp
// Services/IDeviceService.cs (shared interface)
public interface IDeviceService
{
    string GetDeviceIdentifier();
    Task<bool> HasBiometricAsync();
}

// Services/DeviceService.cs (shared partial class)
public partial class DeviceService : IDeviceService
{
    public partial string GetDeviceIdentifier();
    public partial Task<bool> HasBiometricAsync();
}
```

```csharp
// Platforms/Android/Services/DeviceService.cs
public partial class DeviceService
{
    public partial string GetDeviceIdentifier()
    {
        return Android.Provider.Settings.Secure.GetString(
            Android.App.Application.Context.ContentResolver,
            Android.Provider.Settings.Secure.AndroidId) ?? "unknown";
    }

    public partial Task<bool> HasBiometricAsync()
    {
        var manager = BiometricManager.From(Android.App.Application.Context);
        var result = manager.CanAuthenticate(
            BiometricManager.Authenticators.BiometricStrong);
        return Task.FromResult(
            result == BiometricManager.BiometricSuccess);
    }
}
```

```csharp
// Platforms/iOS/Services/DeviceService.cs
public partial class DeviceService
{
    public partial string GetDeviceIdentifier()
    {
        return UIKit.UIDevice.CurrentDevice.IdentifierForVendor?.ToString()
            ?? "unknown";
    }

    public partial Task<bool> HasBiometricAsync()
    {
        var context = new LocalAuthentication.LAContext();
        return Task.FromResult(context.CanEvaluatePolicy(
            LocalAuthentication.LAPolicy.DeviceOwnerAuthenticationWithBiometrics,
            out _));
    }
}
```

### Conditional Compilation

For minor platform differences, use `#if` directives instead of partial classes:

```csharp
public void ConfigurePlatformDefaults()
{
#if ANDROID
    // Android-specific: request permissions
    Platform.CurrentActivity?.RequestPermissions(
        [Android.Manifest.Permission.Camera]);
#elif IOS || MACCATALYST
    // iOS/Mac Catalyst: no runtime permission request needed for camera
    // (handled via Info.plist NSCameraUsageDescription)
#elif WINDOWS
    // Windows: WinUI-specific configuration
#endif
}
```

**When to use each approach:**
- **Partial classes:** large platform implementations, multiple methods, complex logic
- **Conditional compilation:** single-line differences, minor branching, constants

### Dependency Injection

MAUI uses Microsoft.Extensions.DependencyInjection. Register services, ViewModels, and pages in `MauiProgram.cs`.

```csharp
// MauiProgram.cs
public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        builder
            .UseMauiApp<App>()
            .UseMauiCommunityToolkit()
            .ConfigureFonts(fonts =>
            {
                fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
            });

        // Services
        builder.Services.AddSingleton<IProductService, ProductService>();
        builder.Services.AddSingleton<INavigationService, NavigationService>();
        builder.Services.AddTransient<IDeviceService, DeviceService>();

        // HTTP client
        builder.Services.AddHttpClient("api", client =>
        {
            client.BaseAddress = new Uri("https://api.example.com");
        });

        // ViewModels (transient so each page gets a fresh instance)
        builder.Services.AddTransient<ProductListViewModel>();
        builder.Services.AddTransient<ProductDetailViewModel>();

        // Pages (transient, resolved with DI-injected ViewModels)
        builder.Services.AddTransient<ProductListPage>();
        builder.Services.AddTransient<ProductDetailPage>();

        // For DI patterns beyond MAUI-specific registration, see [skill:dotnet-csharp-dependency-injection]

#if DEBUG
        builder.Logging.AddDebug();
#endif

        return builder.Build();
    }
}
```

---

## Current State Assessment (Feb 2026)

> **Last verified: 2026-02-13**

### Production Readiness

.NET MAUI is **production-ready with caveats**. The framework has strong enterprise traction and active community investment, but developers should be aware of known tooling and platform gaps.

**Growth metrics:**
- 36% year-over-year user growth
- 557% increase in community pull requests
- Strong enterprise adoption for line-of-business apps

### Known Issues

**Visual Studio 2026 tooling bugs:**
- Android toolchain occasionally fails on first build after IDE update; clean and rebuild resolves most issues
- Hot Reload intermittently fails to connect on some Android emulator configurations
- XAML IntelliSense may show false errors for valid compiled bindings; build succeeds despite red squiggles

**iOS platform gaps:**
- iOS 26.x compatibility requires testing with latest MAUI servicing patches
- Some iOS-specific controls (e.g., `DatePicker` with custom formatting) have rendering inconsistencies
- Xcode updates can break the build toolchain until MAUI releases a servicing update

### Honest Assessment

MAUI is the right choice when you need a single C#/.NET codebase targeting Android, iOS, macOS (Catalyst), and Windows with native UI rendering. It excels at line-of-business apps, enterprise scenarios, and teams with existing .NET expertise.

MAUI is **not the best choice** when:
- You need web browser targets (consider Blazor or Uno Platform)
- You need Linux desktop support (consider Uno Platform or Avalonia)
- You need pixel-perfect custom rendering across platforms (consider a game engine or Skia-based framework)
- Your team has no .NET experience (evaluate native or React Native alternatives)

---

## Migration Options

When MAUI is not the optimal fit, consider these .NET alternatives:

### WinUI 3 (Windows-Only)

If your application targets only Windows, WinUI 3 provides a richer Windows-native experience without the cross-platform abstraction layer.

```xml
<!-- WinUI 3 project -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0-windows10.0.19041.0</TargetFramework>
    <UseWinUI>true</UseWinUI>
  </PropertyGroup>
</Project>
```

**When to choose WinUI over MAUI:**
- Windows-only app with no mobile/macOS requirements
- Need deep Windows integration (taskbar, notifications, widgets)
- Need WinAppSDK features not exposed through MAUI
- Migrating from UWP

### Uno Platform (Web + Linux + All Platforms)

If you need web (WASM) or Linux desktop support in addition to mobile and Windows, Uno Platform provides broader target coverage with a WinUI-compatible API surface.

**When to choose Uno over MAUI:**
- Need web browser deployment (WASM)
- Need Linux desktop support (GTK/Framebuffer)
- Need embedded device targets
- Team prefers WinUI API surface with MVUX reactive pattern
- Need Figma-to-XAML design workflow

See [skill:dotnet-uno-platform] for Uno Platform development patterns and [skill:dotnet-uno-targets] for per-target deployment.

### Decision Summary

| Requirement | MAUI | WinUI 3 | Uno Platform |
|-------------|------|---------|-------------|
| Android + iOS | Yes | No | Yes |
| Windows desktop | Yes | Yes (best) | Yes |
| macOS (Catalyst) | Yes | No | Yes |
| Web (WASM) | No | No | Yes |
| Linux desktop | No | No | Yes |
| Native UI rendering | Yes | Yes | Skia + Native |
| MVVM Toolkit | Yes | Yes | Yes |
| MVUX reactive | No | No | Yes |

For the full framework decision tree, see [skill:dotnet-ui-chooser].

---

## .NET 11 Improvements

> **Last verified: 2026-02-13**

### XAML Source Gen (Default in .NET 11 Preview 1)

.NET 11 Preview 1 makes XAML source generation the default XAML compilation mode, replacing the traditional XAMLC (XamlCompilationAttribute) approach. Source-generated XAML is AOT-friendly, produces better diagnostics, and enables faster startup.

```xml
<!-- .NET 11: XAML source gen is ON by default -->
<!-- To revert to legacy XAMLC (if source gen causes issues): -->
<PropertyGroup>
  <MauiXamlInflator>XamlC</MauiXamlInflator>
</PropertyGroup>
```

**What changes:** XAML pages are converted to C# source code at build time instead of being compiled to IL via XamlCompilationAttribute. This produces type-safe initialization code that works with Native AOT.

**When to revert:** Revert to XamlC if you encounter source gen issues with custom markup extensions, third-party controls that rely on runtime XAML loading, or legacy `LoadFromXaml` usage.

### CoreCLR for Android (Default in .NET 11 Preview 1)

.NET 11 Preview 1 replaces Mono with CoreCLR as the default runtime for Android Release builds. CoreCLR provides better performance, improved diagnostics, and alignment with the server/desktop runtime.

```xml
<!-- .NET 11: CoreCLR is the default for Android Release builds -->
<!-- To opt out and continue using Mono: -->
<PropertyGroup>
  <UseMonoRuntime>true</UseMonoRuntime>
</PropertyGroup>
```

**What changes:** Release builds use CoreCLR (same runtime as ASP.NET Core and desktop apps) instead of Mono. Debug builds continue to use Mono for Hot Reload support.

**When to opt out:** Opt out if you depend on Mono-specific behavior, encounter compatibility issues with CoreCLR on older Android devices (API < 26), or use libraries that specifically target Mono internals.

### `dotnet run` Device Selection

.NET 11 Preview 1 adds interactive target framework and device selection to `dotnet run` for MAUI projects.

```bash
# .NET 11: interactive device selection
dotnet run --project MyApp/MyApp.csproj
# Prompts: Select target framework:
#   1. net11.0-android
#   2. net11.0-ios
#   3. net11.0-maccatalyst
# Then: Select device:
#   1. Pixel 7 API 34 (emulator)
#   2. Samsung Galaxy S24 (physical)

# Skip interactive selection with explicit TFM
dotnet run --project MyApp/MyApp.csproj -f net11.0-android
```

This replaces the need to manually specify `-f` with exact TFM strings and simplifies the developer inner loop.

---

## Hot Reload

MAUI supports both XAML Hot Reload and C# Hot Reload, but capabilities vary by platform.

### Support Matrix

| Change Type | Android | iOS | macOS | Windows |
|-------------|---------|-----|-------|---------|
| XAML layout/styling | Yes | Yes | Yes | Yes |
| C# method bodies | Yes | Yes | Yes | Yes |
| New instance methods (non-generic classes) | Partial (.NET 9+) | Partial (.NET 9+) | Partial (.NET 9+) | Partial (.NET 9+) |
| New static methods / generic type members | Rebuild | Rebuild | Rebuild | Rebuild |
| Resource dictionary | Yes | Yes | Yes | Yes |
| Add new XAML page | Rebuild | Rebuild | Rebuild | Rebuild |
| CSS changes | Yes | Yes | Yes | Yes |

### Enabling Hot Reload

```bash
# CLI: Hot Reload is enabled automatically in Debug configuration
dotnet run --project MyApp/MyApp.csproj -f net8.0-android

# Visual Studio: Hot Reload is on by default (fire icon in toolbar)
# VS Code: Use MAUI extension with Hot Reload enabled
```

**Gotchas:**
- Hot Reload requires a Debug build configuration; Release builds do not support it
- XAML Hot Reload may not reflect changes to custom renderers or handlers until rebuild
- On Android, Hot Reload uses the `MetadataUpdateHandler` mechanism; changes to static fields or constructors require restart
- On iOS simulator, Hot Reload works but physical device Hot Reload requires a stable USB/WiFi connection

---

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
