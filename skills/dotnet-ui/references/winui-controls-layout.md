# WinUI Controls and Layout

WinUI 3 control selection by scenario, ScrollViewer ownership rules, and adaptive layout with VisualStateManager. Complements `references/winui.md` which covers project setup, XAML patterns, MVVM, packaging, and UWP migration.

**Version assumptions:** Windows App SDK 1.6+. TFM `net8.0-windows10.0.19041.0`. All controls are in `Microsoft.UI.Xaml.Controls`.

## Control Selection by Scenario

### Forms and Settings

| Control | When to use |
|---------|------------|
| `TextBox` | Single-line or multi-line plain text (names, free-form input) |
| `NumberBox` | Numeric input with optional spin buttons, validation, and inline equation evaluation |
| `PasswordBox` | Masked input for passwords, PINs, SSNs. Built-in reveal button via `PasswordRevealMode` |
| `ComboBox` | Pick one item from a long list (states, countries). Starts compact, expands on interaction |
| `ToggleSwitch` | Binary on/off setting with immediate effect. Use instead of a single checkbox for settings |
| `RadioButtons` | Pick one from 2-4 mutually exclusive options. Use the `RadioButtons` group control, not raw `RadioButton` |
| `CalendarDatePicker` | Pick a single date from a contextual dropdown calendar |
| `TimePicker` | Pick a single time value with hour/minute/AM-PM spinners |

```xml
<!-- Settings form example -->
<StackPanel Spacing="16" Padding="24">
    <TextBox Header="Display Name" Text="{x:Bind ViewModel.DisplayName, Mode=TwoWay}" />
    <NumberBox Header="Font Size" Value="{x:Bind ViewModel.FontSize, Mode=TwoWay}"
               Minimum="8" Maximum="72" SpinButtonPlacementMode="Inline" />
    <PasswordBox Header="API Key" Password="{x:Bind ViewModel.ApiKey, Mode=TwoWay}"
                 PasswordRevealMode="Peek" />
    <ComboBox Header="Region" ItemsSource="{x:Bind ViewModel.Regions}"
              SelectedItem="{x:Bind ViewModel.SelectedRegion, Mode=TwoWay}" />
    <ToggleSwitch Header="Dark Mode" IsOn="{x:Bind ViewModel.IsDarkMode, Mode=TwoWay}" />
    <RadioButtons Header="Update Frequency"
                  SelectedIndex="{x:Bind ViewModel.UpdateFrequencyIndex, Mode=TwoWay}">
        <x:String>Daily</x:String>
        <x:String>Weekly</x:String>
        <x:String>Monthly</x:String>
    </RadioButtons>
    <CalendarDatePicker Header="Start Date"
                        Date="{x:Bind ViewModel.StartDate, Mode=TwoWay}" />
    <TimePicker Header="Reminder Time"
                Time="{x:Bind ViewModel.ReminderTime, Mode=TwoWay}" />
</StackPanel>
```

### Command Surfaces

**CommandBar** provides layout for primary and secondary commands with automatic overflow handling.

```xml
<CommandBar DefaultLabelPosition="Right">
    <AppBarButton Icon="Add" Label="New" Command="{x:Bind ViewModel.NewCommand}" />
    <AppBarButton Icon="Save" Label="Save" Command="{x:Bind ViewModel.SaveCommand}" />
    <AppBarSeparator />
    <AppBarButton Icon="Delete" Label="Delete" Command="{x:Bind ViewModel.DeleteCommand}" />

    <CommandBar.SecondaryCommands>
        <AppBarButton Label="Export" Command="{x:Bind ViewModel.ExportCommand}" />
        <AppBarButton Label="Settings" Command="{x:Bind ViewModel.SettingsCommand}" />
    </CommandBar.SecondaryCommands>
</CommandBar>
```

Key properties: `PrimaryCommands` (always visible), `SecondaryCommands` (overflow menu), `IsOpen` (programmatic expand), `DefaultLabelPosition` (`Right`, `Bottom`, `Collapsed`).

**MenuBar** provides a traditional top-level menu for document-centric or productivity apps.

```xml
<MenuBar>
    <MenuBarItem Title="File">
        <MenuFlyoutItem Text="New" Command="{x:Bind ViewModel.NewCommand}" />
        <MenuFlyoutItem Text="Open" Command="{x:Bind ViewModel.OpenCommand}" />
        <MenuFlyoutSeparator />
        <MenuFlyoutItem Text="Exit" Command="{x:Bind ViewModel.ExitCommand}" />
    </MenuBarItem>
    <MenuBarItem Title="Edit">
        <MenuFlyoutItem Text="Undo" Command="{x:Bind ViewModel.UndoCommand}" />
        <MenuFlyoutItem Text="Redo" Command="{x:Bind ViewModel.RedoCommand}" />
    </MenuBarItem>
</MenuBar>
```

### Large Collections

| Control | Layout | Built-in features |
|---------|--------|-------------------|
| `ListView` | Vertical stack | Selection, reorder, incremental loading, built-in ScrollViewer |
| `GridView` | Horizontal wrap grid | Same as ListView but items flow left-to-right, then wrap |
| `ItemsRepeater` | Custom (StackLayout, UniformGridLayout, or custom) | None -- no selection, no built-in ScrollViewer. Must wrap in ScrollViewer manually |

**When to use ItemsRepeater:** Building a custom collection control where you need full layout control. It provides virtualization but no interaction policy. You must provide your own ScrollViewer, selection logic, and visual states.

```xml
<!-- ItemsRepeater with explicit ScrollViewer -->
<ScrollViewer>
    <ItemsRepeater ItemsSource="{x:Bind ViewModel.Items}"
                   Layout="{StaticResource MyUniformGridLayout}">
        <ItemsRepeater.ItemTemplate>
            <DataTemplate x:DataType="models:Item">
                <Grid Padding="8">
                    <TextBlock Text="{x:Bind Name}" />
                </Grid>
            </DataTemplate>
        </ItemsRepeater.ItemTemplate>
    </ItemsRepeater>
</ScrollViewer>
```

### Filtering and Search

| Control | Purpose |
|---------|---------|
| `AutoSuggestBox` | Text input with a dropdown suggestion list that filters as the user types. Handle `TextChanged`, `SuggestionChosen`, and `QuerySubmitted` events |
| `SelectorBar` | Switch between a small fixed set of views (e.g., Recent / Shared / Favorites). One item selected at a time. Handle `SelectionChanged` |
| `BreadcrumbBar` | Show the navigation path to the current location. Items collapse into an ellipsis flyout when space is limited |

```xml
<AutoSuggestBox QueryIcon="Find" PlaceholderText="Search products..."
                TextChanged="SearchBox_TextChanged"
                QuerySubmitted="SearchBox_QuerySubmitted" />
```

### Dialogs and Notifications

| Control | Purpose | Lifetime |
|---------|---------|----------|
| `ContentDialog` | Modal dialog requiring user decision. Use for confirmations, destructive actions, or blocking inputs | Until user dismisses |
| `InfoBar` | Persistent inline status notification. Use for connectivity loss, update availability, or background task completion | Until user closes or condition resolves |
| `TeachingTip` | Contextual onboarding tip anchored to a UI element. Supports light-dismiss. Use for first-run hints | Transient |

```xml
<InfoBar x:Name="UpdateBar" Title="Update available"
         Message="Restart to apply the latest update."
         Severity="Informational" IsOpen="True" IsClosable="True" />

<TeachingTip x:Name="SaveTip" Target="{x:Bind SaveButton}"
             Title="Auto-save enabled"
             Subtitle="Changes are saved automatically."
             IsLightDismissEnabled="True" />
```

### Navigation

| Control | Purpose |
|---------|---------|
| `NavigationView` | Primary app navigation with left pane or top bar. Supports Compact and Minimal display modes. Adapts to window width automatically |
| `TabView` | Tabbed document interface. Users can open, close, reorder, and tear off tabs |

**Pivot is deprecated.** It was removed from WinUI 3 starting with Project Reunion 0.5 Preview. Use `TabView` for tabbed content or `NavigationView` with top pane for section switching.


## ScrollViewer Ownership

**Rule:** Only one scroll owner per direction in the visual tree. Nesting a `ListView` or `GridView` inside a `ScrollViewer` in the same scroll direction causes conflicts -- the inner control's built-in ScrollViewer fights the outer one for scroll input.

### Symptoms of Nested ScrollViewer Conflicts

- Items render but do not scroll
- Scroll jumps or stutters as two scrollers compete
- Virtualization breaks because the inner control expands to full height (no viewport constraint)

### Fixes

**Option 1 -- Remove the outer ScrollViewer.** Let the collection control manage its own scrolling.

**Option 2 -- Use ItemsRepeater.** It has no built-in ScrollViewer, so you provide exactly one:

```xml
<!-- Correct: single scroll owner -->
<ScrollViewer>
    <StackPanel>
        <TextBlock Text="Header" Style="{StaticResource TitleTextBlockStyle}" />
        <ItemsRepeater ItemsSource="{x:Bind ViewModel.Items}" />
    </StackPanel>
</ScrollViewer>
```

**Option 3 -- Constrain the inner control height.** Give the ListView/GridView a fixed `Height` or `MaxHeight` so it scrolls independently within a bounded region:

```xml
<ScrollViewer>
    <StackPanel>
        <TextBlock Text="Other content" />
        <ListView ItemsSource="{x:Bind ViewModel.Items}" MaxHeight="400" />
        <TextBlock Text="More content below" />
    </StackPanel>
</ScrollViewer>
```


## Adaptive Layout

### Effective Pixels and Resolution Independence

WinUI uses effective pixels (epx), not physical pixels. The system scales UI automatically based on display DPI so that a 24 epx font is legible on both a phone screen at arm's length and a large monitor across the room. Design in effective pixels and let the platform handle scaling.

### VisualStateManager with AdaptiveTrigger

`AdaptiveTrigger` applies visual states declaratively based on window dimensions. No need to handle `SizeChanged` manually.

```xml
<Page>
    <VisualStateManager.VisualStateGroups>
        <VisualStateGroup>
            <!-- Wide: side-by-side layout -->
            <VisualState x:Name="WideState">
                <VisualState.StateTriggers>
                    <AdaptiveTrigger MinWindowWidth="1008" />
                </VisualState.StateTriggers>
                <VisualState.Setters>
                    <Setter Target="ContentGrid.Orientation" Value="Horizontal" />
                    <Setter Target="SidePanel.Visibility" Value="Visible" />
                    <Setter Target="ContentGrid.Padding" Value="48,24" />
                </VisualState.Setters>
            </VisualState>

            <!-- Medium: reduced padding, side panel visible -->
            <VisualState x:Name="MediumState">
                <VisualState.StateTriggers>
                    <AdaptiveTrigger MinWindowWidth="641" />
                </VisualState.StateTriggers>
                <VisualState.Setters>
                    <Setter Target="ContentGrid.Orientation" Value="Vertical" />
                    <Setter Target="SidePanel.Visibility" Value="Visible" />
                    <Setter Target="ContentGrid.Padding" Value="24,16" />
                </VisualState.Setters>
            </VisualState>

            <!-- Narrow: stacked, minimal padding -->
            <VisualState x:Name="NarrowState">
                <VisualState.StateTriggers>
                    <AdaptiveTrigger MinWindowWidth="0" />
                </VisualState.StateTriggers>
                <VisualState.Setters>
                    <Setter Target="ContentGrid.Orientation" Value="Vertical" />
                    <Setter Target="SidePanel.Visibility" Value="Collapsed" />
                    <Setter Target="ContentGrid.Padding" Value="16,8" />
                </VisualState.Setters>
            </VisualState>
        </VisualStateGroup>
    </VisualStateManager.VisualStateGroups>

    <StackPanel x:Name="ContentGrid" Orientation="Horizontal" Padding="48,24">
        <StackPanel x:Name="SidePanel" Width="300">
            <!-- Sidebar content -->
        </StackPanel>
        <Grid>
            <!-- Main content -->
        </Grid>
    </StackPanel>
</Page>
```

### Breakpoint Planning

| Breakpoint | MinWindowWidth | Typical layout |
|-----------|----------------|----------------|
| Wide | 1008 epx | Side-by-side panels, full padding, expanded navigation |
| Medium | 641 epx | Single column, reduced padding, navigation pane visible |
| Narrow | 0 epx | Stacked content, minimal padding, hide secondary controls |

### Responsive NavigationView

`NavigationView` adapts automatically via `CompactModeThresholdWidth` and `ExpandedModeThresholdWidth`. At narrow widths it switches to `LeftMinimal` (hamburger button only). You can also switch between `Top` and `LeftMinimal` using AdaptiveTrigger:

```xml
<NavigationView x:Name="NavView" PaneDisplayMode="Auto">
    <!-- PaneDisplayMode="Auto" enables automatic adaptation -->
    <!-- CompactModeThresholdWidth defaults to 641 -->
    <!-- ExpandedModeThresholdWidth defaults to 1008 -->
</NavigationView>
```


## Anti-patterns

1. **Do not build custom button rows when CommandBar handles the same layout.** CommandBar provides overflow, keyboard shortcuts, and accessibility for free.
2. **Do not nest ScrollViewers in the same scroll direction.** This breaks virtualization and causes erratic scrolling. Use ItemsRepeater with a single ScrollViewer or constrain inner control height.
3. **Do not use Pivot.** It is deprecated and removed from WinUI 3. Use `TabView` for tabbed content or `NavigationView` with top pane mode.
4. **Do not hard-code pixel widths for responsive layouts.** Use `AdaptiveTrigger` with `MinWindowWidth` and flexible layout panels (`Grid` with proportional columns, `StackPanel`). Hard-coded widths break on different screen sizes and DPI settings.
5. **Do not put interactive content inside ListView items without careful focus management.** Nested interactive elements (buttons, text boxes) inside list items cause tab-order and focus conflicts. Set `IsItemClickEnabled` appropriately and follow the nested UI guidance.
6. **Do not use ItemsControl when you need virtualization.** `ItemsControl` does not virtualize. Use `ItemsRepeater` for custom virtualizing layouts or `ListView`/`GridView` for standard collection display.


## References

- [Controls for Windows apps](https://learn.microsoft.com/windows/apps/develop/ui/controls/)
- [Forms](https://learn.microsoft.com/windows/apps/develop/ui/controls/forms)
- [ListView and GridView](https://learn.microsoft.com/windows/apps/develop/ui/controls/listview-and-gridview)
- [ItemsRepeater](https://learn.microsoft.com/windows/apps/develop/ui/controls/items-repeater)
- [CommandBar](https://learn.microsoft.com/windows/apps/design/controls/command-bar)
- [Responsive layouts with XAML](https://learn.microsoft.com/windows/apps/develop/ui/layouts-with-xaml)
- [AdaptiveTrigger class](https://learn.microsoft.com/windows/windows-app-sdk/api/winrt/microsoft.ui.xaml.adaptivetrigger)
- [NavigationView](https://learn.microsoft.com/windows/apps/develop/ui/controls/navigationview)
