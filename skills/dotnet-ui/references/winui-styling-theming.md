# WinUI Styling and Theming

WinUI 3 styling, theming, materials, typography, icons, and resource organization. Complements `references/winui.md` which covers project setup, XAML patterns, MVVM, and packaging, and `references/winui-controls-layout.md` which covers control selection and adaptive layout.

**Version assumptions:** Windows App SDK 1.6+. TFM `net8.0-windows10.0.19041.0`. Mica and Acrylic backdrops require Windows 11 (build 22000+).

## Theme Support

WinUI 3 supports Light, Dark, and HighContrast themes out of the box. All built-in controls automatically adjust their visuals when the theme changes.

### ThemeResource vs StaticResource

- **`{ThemeResource}`** -- Re-evaluated when the theme changes at runtime. Use for all color and brush references that should adapt to light/dark/high-contrast.
- **`{StaticResource}`** -- Evaluated once at load time. Use for non-theme-dependent values (font families, spacing constants, styles).

```xml
<!-- Correct: brush adapts when user switches theme -->
<Border Background="{ThemeResource CardBackgroundFillColorDefaultBrush}" />

<!-- Wrong: brush is locked to the value resolved at load time -->
<Border Background="{StaticResource CardBackgroundFillColorDefaultBrush}" />
```

### Setting the App Theme

Set `RequestedTheme` on `Application` in App.xaml to override the system default:

```xml
<Application RequestedTheme="Dark">
```

`RequestedTheme` on `Application` can only be set at startup -- setting it after launch throws `NotSupportedException`. To allow runtime theme switching, set `RequestedTheme` on individual `FrameworkElement` instances (Window root, Page, or specific containers):

```csharp
// Switch theme at runtime for the entire window content
(Content as FrameworkElement).RequestedTheme = ElementTheme.Dark;
```

### Detecting Theme Changes

Use `ActualThemeChanged` to react when the effective theme changes (user switches system theme, or `RequestedTheme` is set on an ancestor):

```csharp
rootElement.ActualThemeChanged += (sender, _) =>
{
    var currentTheme = ((FrameworkElement)sender).ActualTheme;
    // Update non-XAML visuals, analytics, or custom rendering
};
```

### Custom Theme Dictionaries

Define per-theme resources using `ThemeDictionaries` with keys `Default` (Dark), `Light`, and `HighContrast`:

```xml
<ResourceDictionary.ThemeDictionaries>
    <ResourceDictionary x:Key="Light">
        <SolidColorBrush x:Key="AppHeaderBrush" Color="#F3F3F3" />
    </ResourceDictionary>
    <ResourceDictionary x:Key="Default">
        <SolidColorBrush x:Key="AppHeaderBrush" Color="#2D2D2D" />
    </ResourceDictionary>
    <ResourceDictionary x:Key="HighContrast">
        <SolidColorBrush x:Key="AppHeaderBrush"
                         Color="{ThemeResource SystemColorWindowColor}" />
    </ResourceDictionary>
</ResourceDictionary.ThemeDictionaries>
```

Note: In `ThemeDictionaries`, use `{ThemeResource}` in the `HighContrast` dictionary (system colors update dynamically) and `{StaticResource}` in `Light`/`Default` dictionaries to avoid shared-brush pollution across theme sub-trees.


## Materials

Materials are visual effects that add depth and hierarchy to surfaces.

### Mica

An opaque material that incorporates the user's desktop wallpaper and theme. Use for **long-lived base surfaces** such as the main window background.

```xml
<!-- XAML: set Mica as window backdrop -->
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Window.SystemBackdrop>
        <MicaBackdrop />
    </Window.SystemBackdrop>
    <!-- Content here -- set Background="Transparent" on root to see Mica -->
</Window>
```

```csharp
// Code-behind: set Mica with MicaKind
SystemBackdrop = new MicaBackdrop { Kind = MicaKind.Base };
```

**MicaKind.Base** -- Standard Mica, slightly tinted by wallpaper. Best for the primary window surface.

**MicaKind.BaseAlt** -- Darker, more subdued variant. Use when the content layer on top needs stronger contrast (e.g., card pattern with `LayerFillColorDefaultBrush`).

### Acrylic

A semi-transparent frosted-glass material. Use for **transient, light-dismiss surfaces** such as flyouts, context menus, and dialog overlays.

```xml
<Window.SystemBackdrop>
    <DesktopAcrylicBackdrop />
</Window.SystemBackdrop>
```

For in-app acrylic on specific UI elements (not the window background), use `AcrylicBrush` theme resources directly on panels or controls.

### Fallback Behavior

On Windows 10 or systems that do not support composition effects, Mica and Acrylic fall back to a solid color automatically. No special handling is needed, but test on Windows 10 to verify the fallback appearance is acceptable.

**Rules:**
- Apply backdrop material only once per window. Do not layer multiple backdrop materials.
- Set `Background="Transparent"` on all layers between the window and the content area where Mica should show through.
- Mica should be visible in the title bar -- extend content into the non-client area for a seamless look.


## System Brushes

Use system brushes instead of hard-coded colors. They adapt to Light, Dark, and HighContrast themes automatically.

### Surface Brushes

| Brush | Purpose |
|-------|---------|
| `CardBackgroundFillColorDefaultBrush` | Card surface backgrounds |
| `CardStrokeColorDefaultBrush` | Card border/outline |
| `LayerFillColorDefaultBrush` | Content layer on top of Mica (standard pattern) |
| `LayerOnMicaBaseAltFillColorDefaultBrush` | Content layer on Mica BaseAlt |
| `SolidBackgroundFillColorBaseBrush` | Solid opaque background when transparency is not desired |

### Text Brushes

| Brush | Purpose |
|-------|---------|
| `TextFillColorPrimaryBrush` | Primary text (titles, body) |
| `TextFillColorSecondaryBrush` | Secondary text (subtitles, descriptions) |
| `TextFillColorTertiaryBrush` | Tertiary text (hints, placeholders, disabled labels) |

### Usage Example

```xml
<Border Background="{ThemeResource CardBackgroundFillColorDefaultBrush}"
        BorderBrush="{ThemeResource CardStrokeColorDefaultBrush}"
        BorderThickness="1" CornerRadius="8" Padding="16">
    <StackPanel Spacing="4">
        <TextBlock Text="Product Name"
                   Foreground="{ThemeResource TextFillColorPrimaryBrush}"
                   Style="{StaticResource BodyStrongTextBlockStyle}" />
        <TextBlock Text="$49.99"
                   Foreground="{ThemeResource TextFillColorSecondaryBrush}"
                   Style="{StaticResource CaptionTextBlockStyle}" />
    </StackPanel>
</Border>
```


## Typography

### Default Font

**Segoe UI Variable** is the default WinUI 3 system font. It is a variable font that adjusts weight and optical size dynamically for optimal legibility across all display sizes. Do not override the font family unless the app has specific branding requirements.

### Type Ramp

WinUI provides predefined TextBlock styles that align with the Windows type ramp:

| Style | Weight | Size (epx) |
|-------|--------|-----------|
| `CaptionTextBlockStyle` | Regular | 12 |
| `BodyTextBlockStyle` | Regular | 14 |
| `BodyStrongTextBlockStyle` | Semibold | 14 |
| `BodyLargeTextBlockStyle` | Regular | 18 |
| `SubtitleTextBlockStyle` | Semibold | 20 |
| `TitleTextBlockStyle` | Semibold | 28 |
| `TitleLargeTextBlockStyle` | Semibold | 40 |
| `DisplayTextBlockStyle` | Semibold | 68 |

```xml
<StackPanel Spacing="8">
    <TextBlock Text="Page Title" Style="{StaticResource TitleTextBlockStyle}" />
    <TextBlock Text="Section heading" Style="{StaticResource SubtitleTextBlockStyle}" />
    <TextBlock Text="Body content" Style="{StaticResource BodyTextBlockStyle}" />
    <TextBlock Text="Metadata" Style="{StaticResource CaptionTextBlockStyle}" />
</StackPanel>
```

### Typography Rules

- Use sentence casing for all UI text, including titles.
- Minimum legible size: 14 epx Regular or 12 epx Semibold. Text below these thresholds is illegible in some languages.
- Do not hard-code font sizes -- always use the type ramp styles. This ensures consistency and respects system accessibility scaling.


## Icons

### Segoe Fluent Icons

**Segoe Fluent Icons** is the icon font for WinUI 3 apps. Use it for consistency with the Windows shell.

```xml
<!-- FontIcon with unicode glyph -->
<FontIcon FontFamily="{StaticResource SymbolThemeFontFamily}" Glyph="&#xE721;" />

<!-- SymbolIcon for common symbols -->
<SymbolIcon Symbol="Save" />

<!-- In AppBarButton -->
<AppBarButton Icon="Add" Label="New Item" />
```

`SymbolIcon` provides a simplified API for common icons (Save, Delete, Add, Edit, etc.). Use `FontIcon` with the Glyph property when you need access to the full Segoe Fluent Icons set.

### Icon Consistency

- Keep visual weight consistent across all icons in a surface. Do not mix filled and outline variants randomly.
- Use a single icon font throughout the app. Do not mix Segoe Fluent Icons with Segoe MDL2 Assets unless migrating from an older codebase.
- For custom icons, use `PathIcon` or `BitmapIcon` and ensure they match the visual weight of Segoe Fluent Icons.


## Resource Organization

### Centralize Custom Resources

Group custom brushes, typography overrides, and spacing values into dedicated resource dictionary files under a `Styles/` directory:

```
MyWinUIApp/
  Styles/
    Colors.xaml         # Custom brush definitions with ThemeDictionaries
    Typography.xaml     # Any type-ramp extensions or overrides
    Spacing.xaml        # Consistent margin/padding values
  App.xaml              # Merges all resource dictionaries
```

### Merge into App.xaml

```xml
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <XamlControlsResources xmlns="using:Microsoft.UI.Xaml.Controls" />
            <ResourceDictionary Source="Styles/Colors.xaml" />
            <ResourceDictionary Source="Styles/Typography.xaml" />
            <ResourceDictionary Source="Styles/Spacing.xaml" />
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application.Resources>
```

### Rules

- Always include `<XamlControlsResources />` first in `MergedDictionaries`. It contains the WinUI 3 control styles and theme resources.
- Do not scatter theme overrides across page-level resource dictionaries. Centralize in `Styles/` for single-source-of-truth maintenance.
- Use `x:Key` names that follow the WinUI naming convention (`[Category][Property][State]Brush`) for discoverability.


## Anti-patterns

1. **Do not hard-code colors.** Hard-coded hex values break Dark mode and HighContrast accessibility. Use `{ThemeResource}` system brushes.
2. **Do not wrap cards inside cards.** Nesting elements that both use `CardBackgroundFillColorDefaultBrush` and `CardStrokeColorDefaultBrush` creates a double-border, double-background effect that looks cluttered and muddles visual hierarchy.
3. **Do not add redundant Border wrappers** when the parent control template already provides the visual boundary (e.g., wrapping a `ListView` item in an extra Border when the ItemContainer already has one).
4. **Do not use bright colored oval pills for metadata tags.** They clash with the Fluent Design system's subtle aesthetic. Use `TextFillColorSecondaryBrush` on a plain `TextBlock` or a lightly styled `Border` with `SubtleFillColorSecondaryBrush`.
5. **Do not mix Segoe UI and Segoe Fluent Icons inconsistently.** Stick to the system defaults: Segoe UI Variable for text, Segoe Fluent Icons for icons.
6. **Do not hard-code font sizes.** Use the type ramp styles (`BodyTextBlockStyle`, `CaptionTextBlockStyle`, etc.) to maintain visual hierarchy and support accessibility text scaling.
7. **Do not use `{StaticResource}` for theme-dependent brushes.** The brush value will not update when the user switches between Light and Dark mode at runtime.
8. **Do not set `Application.RequestedTheme` after app launch.** It throws `NotSupportedException`. Use `FrameworkElement.RequestedTheme` on individual elements for runtime theme changes.


## References

- [Theming in Windows apps](https://learn.microsoft.com/windows/apps/develop/ui/theming)
- [XAML theme resources](https://learn.microsoft.com/windows/apps/develop/platform/xaml/xaml-theme-resources)
- [Materials in Windows apps](https://learn.microsoft.com/windows/apps/develop/ui/materials)
- [Apply Mica or Acrylic](https://learn.microsoft.com/windows/apps/develop/ui/system-backdrops)
- [Typography in Windows](https://learn.microsoft.com/windows/apps/design/signature-experiences/typography)
- [Segoe Fluent Icons font](https://learn.microsoft.com/windows/apps/design/style/segoe-fluent-icons-font)
- [Color in Windows apps](https://learn.microsoft.com/windows/apps/design/signature-experiences/color)
- [Contrast themes](https://learn.microsoft.com/windows/apps/design/accessibility/high-contrast-themes)
