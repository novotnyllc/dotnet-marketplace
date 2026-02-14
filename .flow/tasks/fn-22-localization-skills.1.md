# fn-22-localization-skills.1 Research current .NET localization best practices

## Description
Research the current state of .NET localization ecosystem (Feb 2026) to inform the comprehensive `dotnet-localization` skill. Cover resource formats (.resx, JSON-based, source generators), IStringLocalizer patterns, pluralization engines, date/number/currency formatting, RTL support, and per-framework localization mechanisms.

## Acceptance
- [ ] Research covers resource format options: .resx, JSON resources, source generator approaches (e.g., ResXResourceSourceGenerator, community SG libs) with AOT compatibility assessment
- [ ] Research covers IStringLocalizer<T> vs IViewLocalizer vs IHtmlLocalizer patterns and when to use each
- [ ] Research covers pluralization engines: MessageFormat.NET, SmartFormat, ICU-based options
- [ ] Research covers date/number/currency formatting via CultureInfo, DateTimeFormatInfo
- [ ] Research covers RTL layout support patterns per UI framework
- [ ] Research covers per-framework localization mechanisms: Blazor (CultureProvider, @inject IStringLocalizer), MAUI (AppResources, x:Static), Uno (.resw, x:Uid, UseLocalization()), WPF (LocBaml, resource dictionaries)
- [ ] Findings documented in done-summary with recommended approaches for each area

## Files Touched
None — research-only task. Output captured in done-summary.

## Done summary
## Research: .NET Localization Best Practices (Feb 2026)

### 1. Resource Format Options

**Traditional .resx files** remain the primary resource format in .NET. They compile into satellite assemblies via the ResourceManager/ResourceReader infrastructure. The default `.resx` file serves as the single source of truth; translation files should never contain keys absent from the default file. Culture fallback resolves resources in order of specificity (e.g., `sr-Cyrl-RS.resx` -> `sr-Cyrl.resx` -> `sr.resx` -> default `.resx`).

**JSON-based resources** are a lightweight alternative, especially for projects already using JSON for configuration. Libraries like `Senlin.Mo.Localization` and `Embedded.Json.Localization` provide `IStringLocalizer` implementations backed by JSON files. These are popular in ASP.NET Core projects but lack the built-in tooling support of .resx.

**Source generator approaches**: Several community source generators exist for compile-time strongly-typed resource access:
- **ResXGenerator** (ycanardeau/ResXGenerator): Generates strongly-typed resource classes with IStringLocalizer support and IServiceCollection registration methods. Fork of VocaDb/ResXFileCodeGenerator.
- **VocaDb.ResXFileCodeGenerator**: Original source generator for strongly-typed .resx access.
- **ResxCodeGenerator**: Another community option on NuGet.
- The built-in `ResXFileCodeGenerator` custom tool in Visual Studio generates static properties but is not a Roslyn source generator.

**AOT Compatibility Assessment**: Traditional .resx with ResourceManager uses reflection at runtime, which is problematic for Native AOT. Source generator approaches (ResXGenerator etc.) eliminate runtime reflection by generating static code at compile time, making them AOT-compatible. .NET 8+ introduced a configuration binding source generator as a model for AOT-friendly code generation. For localization, source generators that produce strongly-typed accessor classes are the recommended path for AOT/trimming scenarios.

### 2. IStringLocalizer<T> vs IViewLocalizer vs IHtmlLocalizer Patterns

**IStringLocalizer<T>**: The primary localization interface. Injectable via DI after calling `builder.Services.AddLocalization()`. Uses an indexer (`localizer["Key"]`) returning `LocalizedString` with implicit conversion to `string`. Best for services, controllers, and cross-cutting localization. Supports parameterized format strings via `localizer["Key", arg1, arg2]`. Preferred over IStringLocalizerFactory for most DI scenarios. Uses `RootNamespaceAttribute` to resolve namespace/assembly mismatches.

**IHtmlLocalizer<T>**: HTML-aware variant that HTML-encodes format arguments but preserves HTML markup in the resource string itself. ASP.NET Core MVC feature only. **Not supported in Blazor apps.**

**IViewLocalizer**: Razor view-specific localizer that automatically resolves resource files matching the view path/name. Most convenient for view-local strings. ASP.NET Core MVC feature only. **Not supported in Blazor apps.**

**When to use each**:
- `IStringLocalizer<T>` -- use everywhere: services, controllers, Blazor components, middleware. The universal choice.
- `IViewLocalizer` -- use in MVC Razor views when strings are view-specific. Auto-resolves resource file location.
- `IHtmlLocalizer<T>` -- use in MVC views when resource strings contain HTML markup that should not be encoded.

### 3. Pluralization Engines

**MessageFormat.NET** (jeffijoe/messageformat.net): ICU MessageFormat implementation for .NET. Since v5.0, ships CLDR-based pluralizers. Standards-compliant with the ICU specification. Built-in caching prevents reparsing. Pluralizers dictionary allows customization. Best for teams requiring ICU compliance and CLDR correctness.

**SmartFormat.NET** (axuno/SmartFormat, v3.6.1): Lightweight text templating library, drop-in replacement for `string.Format`. Supports pluralization via named branches with custom syntax: `{count:plural:one{# message}|other{# messages}}`. Extensible with custom source/formatter extensions. Good for teams wanting maximum flexibility without strict ICU adherence.

**ICU-based approaches**: Both libraries support ICU-style pluralization rules. MessageFormat.NET is more strictly ICU-compliant (CLDR plural categories: zero, one, two, few, many, other). SmartFormat offers a more flexible, .NET-idiomatic API.

**Recommendation**: MessageFormat.NET for internationalization-first projects needing CLDR correctness across many locales. SmartFormat.NET for projects wanting flexible templating with built-in pluralization. For simple cases (English-only dual forms), .NET's built-in `string.Format` with conditional logic may suffice.

### 4. Date/Number/Currency Formatting

**CultureInfo**: Central class providing access to `DateTimeFormatInfo`, `NumberFormatInfo`, `CompareInfo`, and `TextInfo`. `CultureInfo.CurrentCulture` controls formatting; `CultureInfo.CurrentUICulture` controls resource lookup. Always pass explicit `IFormatProvider`/`CultureInfo` to avoid server-locale-dependent formatting.

**DateTimeFormatInfo**: Provides culture-specific date/time patterns. Access via `CultureInfo.DateTimeFormat`. Supports standard format strings ("d", "D", "f", etc.) and custom patterns ("yyyy-MM-dd").

**NumberFormatInfo**: Defines culture-appropriate number, currency, and percentage display. Access via `CultureInfo.NumberFormat`. Currency formatting uses "C" format specifier. Customizable via `CurrencyPositivePattern`, `CurrencyNegativePattern`, `CurrencySymbol`.

**Best practices**:
- Always use explicit `CultureInfo` parameter, never rely on thread-current defaults in server code.
- Use `CultureInfo(string, false)` constructor to avoid user-override issues in server scenarios.
- Blazor WASM requires `BlazorWebAssemblyLoadAllGlobalizationData=true` for full ICU data; otherwise only a subset is loaded.
- ICU data files can be customized: `icudt.dat` (full), `icudt_EFIGS.dat`, `icudt_CJK.dat`, `icudt_no_CJK.dat`.
- `InvariantGlobalization=true` disables localization entirely for smaller WASM downloads.

### 5. RTL Layout Support Patterns

**General .NET pattern**: `CultureInfo.CurrentCulture.TextInfo.IsRightToLeft` detects RTL cultures. UI frameworks use `FlowDirection` enum: `LeftToRight`, `RightToLeft`, `MatchParent`.

**Per-framework RTL support**:

- **Blazor**: No native `FlowDirection` -- RTL is handled via CSS `dir="rtl"` on HTML elements. Set `document.documentElement.lang` and `dir` attribute dynamically via JS interop. Telerik (v4.2.0+) and Syncfusion offer built-in RTL support with `EnableRtl` property.

- **MAUI**: `FlowDirection` property on `VisualElement` and `Window`. Set on root layout or window level. MAUI auto-respects device flow direction based on locale. Android requires `android:supportsRtl="true"` in AndroidManifest.xml (set by default). Some controls (ScrollView, Frame, Border) had RTL issues fixed in .NET 8. Setting `FlowDirection` at runtime causes expensive re-layout.

- **WPF**: `FlowDirection` property on `FrameworkElement`. Set on `Window` or root element. Values: `LeftToRight`, `RightToLeft`. Well-supported since WPF inception.

- **Uno Platform**: Inherits UWP/WinUI `FlowDirection` model. `FrameworkElement.FlowDirection` property. `.resw` localization works with RTL cultures similarly to WinUI.

### 6. Per-Framework Localization Mechanisms

#### Blazor
- **Supported**: `IStringLocalizer` and `IStringLocalizer<T>` only.
- **Not supported**: `IHtmlLocalizer`, `IViewLocalizer` (MVC-only features).
- **Injection**: `@inject IStringLocalizer<MyComponent> Loc` in Razor components.
- **Culture setting**: Blazor Web App (.NET 8+) supports culture via `RequestLocalizationMiddleware` (server-side), `applicationCulture` Blazor start option (WASM), browser local storage, or localization cookies.
- **Render modes**: Culture must be configured per render mode -- Server uses middleware, WebAssembly uses `CultureInfo.DefaultThreadCurrentCulture`, Auto requires both.
- **WASM ICU**: `BlazorWebAssemblyLoadAllGlobalizationData=true` for full globalization data.
- **Dynamic culture**: CultureSelector component pattern using JS interop with local storage + controller redirect for server-side cookie.

#### MAUI
- **Resource files**: `AppResources.resx` (default), `AppResources.{culture}.resx` per locale. Build action: `EmbeddedResource`.
- **XAML binding**: `{x:Static strings:AppResources.PropertyName}` via `clr-namespace` import.
- **Code access**: `AppResources.PropertyName` (generated strongly-typed static properties).
- **Platform setup**: iOS/Mac Catalyst require `CFBundleLocalizations` in Info.plist; Windows requires `<Resource Language="...">` entries in Package.appxmanifest.
- **Neutral language**: `<NeutralLanguage>en-US</NeutralLanguage>` in csproj required.
- **RTL**: `FlowDirection` property on Window/VisualElement.
- **VS Code**: Requires manual MSBuild `EmbeddedResource` + `Compile` items for resource code generation.

#### Uno Platform
- **Resource format**: `.resw` files (Windows resource format), organized in culture-named folders (e.g., `en-US/Resources.resw`, `fr-FR/Resources.resw`).
- **x:Uid pattern**: `<TextBlock x:Uid="MyTextBlock" />` maps to `MyTextBlock.Text` key in `.resw`.
- **UseLocalization()**: Extension method on `IHostBuilder` that registers `ResourceLoaderStringLocalizer` as `IStringLocalizer`.
- **ILocalizationService**: Changes current culture/locale at runtime (requires app restart for x:Uid updates).
- **Known limitation**: XAML localization via x:Uid keeps old culture until app restart, even after `ILocalizationService.SetCurrentCultureAsync`.

#### WPF
- **LocBaml**: Legacy tool for localizing BAML streams into satellite assemblies. **Only works with .NET Framework, not modern .NET.** Not production-ready (sample tool).
- **Resource dictionaries**: `ResourceDictionary` with `{DynamicResource}` binding for runtime locale switching. Create per-culture XAML resource dictionaries.
- **ResX approach**: Standard .resx files with strongly-typed generated classes. Works on all .NET versions. Better Visual Studio tooling.
- **WPF Localization Extensions** (community): Uses RESX files with XAML markup extensions for declarative localization.
- **LocBamlCore** (community, h3xds1nz): Unofficial port supporting .NET 9 -- provides BAML localization for modern .NET WPF apps.
- **Recommendation for modern .NET**: Use .resx files with DynamicResource binding or WPF Localization Extensions. Avoid LocBaml unless targeting .NET Framework.

### Key Recommendations Summary

| Area | Recommended Approach |
|------|---------------------|
| Resource format | .resx (standard) + source generator (AOT); JSON for lightweight/config-heavy projects |
| String localization | IStringLocalizer<T> everywhere; IViewLocalizer for MVC views only |
| Pluralization | MessageFormat.NET (ICU/CLDR) or SmartFormat.NET (flexible) |
| Date/number formatting | Explicit CultureInfo parameter; never rely on thread defaults in server code |
| RTL support | Framework-specific FlowDirection; CSS dir attribute for Blazor |
| Blazor | @inject IStringLocalizer, RequestLocalizationMiddleware, culture cookies |
| MAUI | AppResources.resx + x:Static, NeutralLanguage in csproj |
| Uno | .resw + x:Uid + UseLocalization(), ILocalizationService for runtime changes |
| WPF (.NET 8+) | .resx + DynamicResource or WPF Localization Extensions; avoid LocBaml |
## Evidence
- Commits:
- Tests:
- PRs: