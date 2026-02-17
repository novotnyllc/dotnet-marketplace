---
name: dotnet-terminal-gui
description: "Building full TUI apps. Terminal.Gui v2: views, layout (Pos/Dim), menus, dialogs, bindings, themes."
---

# dotnet-terminal-gui

Terminal.Gui v2 for building full terminal user interfaces with windows, menus, dialogs, views, layout, event handling, color themes, and mouse support. Cross-platform across Windows, macOS, and Linux terminals.

**Version assumptions:** .NET 8.0+ baseline. Terminal.Gui 2.0.0-alpha (v2 Alpha is the active development line for new projects -- API is stable with comprehensive features; breaking changes possible before Beta but core architecture is solid). v1.x (1.19.0) is in maintenance mode with no new features.

**Scope boundary:** This skill owns full TUI application development with Terminal.Gui -- application lifecycle, layout, views, menus, dialogs, event handling, themes. Rich console output (tables, progress bars, prompts, markup) is owned by [skill:dotnet-spectre-console]. CLI command-line parsing is owned by [skill:dotnet-system-commandline]. CLI application architecture and distribution are owned by [skill:dotnet-cli-architecture] and [skill:dotnet-cli-distribution].

Cross-references: [skill:dotnet-spectre-console] for rich console output alternative, [skill:dotnet-csharp-async-patterns] for async TUI patterns, [skill:dotnet-native-aot] for AOT compilation considerations, [skill:dotnet-system-commandline] for CLI parsing, [skill:dotnet-csharp-dependency-injection] for DI in TUI apps, [skill:dotnet-accessibility] for TUI accessibility limitations and screen reader considerations.

---

## Package Reference

```xml
<ItemGroup>
  <!-- v2 Alpha -- recommended for new projects -->
  <PackageReference Include="Terminal.Gui" Version="2.0.0-alpha.*" />
</ItemGroup>
```

Terminal.Gui v2 targets .NET 8+ and .NET Standard 2.0/2.1. For v1 maintenance projects, use `Version="1.19.*"`.

---

## Application Lifecycle

Terminal.Gui v2 uses an instance-based model with `IApplication` and `IDisposable` for proper resource cleanup. This replaces v1's static `Application.Init()` / `Application.Run()` / `Application.Shutdown()` pattern.

### Basic Application

```csharp
using Terminal.Gui;

// Create and initialize the application (instance-based in v2)
using IApplication app = Application.Create().Init();

var window = new Window
{
    Title = "My TUI App",
    Width = Dim.Fill(),
    Height = Dim.Fill()
};

var label = new Label
{
    Text = "Hello, Terminal.Gui!",
    X = Pos.Center(),
    Y = Pos.Center()
};
window.Add(label);

app.Run(window);
```

### Application with Typed Result

```csharp
using IApplication app = Application.Create().Init();

// Run a dialog and get a typed result
app.Run<MyInputDialog>();
string? result = app.GetResult<string>();
```

### Lifecycle Events

```csharp
// IsRunningChanging -- cancellable, fires before state change
// IsRunningChanged  -- non-cancellable, fires after state change
window.IsRunningChanged += (sender, args) =>
{
    if (!args.NewValue)
    {
        // Window is closing -- clean up resources
    }
};
```

---

## Layout System

Terminal.Gui v2 unifies layout into a single model (v1's Absolute/Computed distinction is removed). Position is controlled by `Pos` (X, Y) and size by `Dim` (Width, Height), both relative to the SuperView's content area.

### Pos Types (Positioning)

```csharp
// Absolute -- fixed coordinate
view.X = 5;                          // Pos.Absolute(5)

// Percent -- percentage of parent
view.X = Pos.Percent(25);            // 25% from left

// Center -- centered in parent
view.X = Pos.Center();

// AnchorEnd -- anchored from right/bottom edge
view.X = Pos.AnchorEnd(10);          // 10 from right edge

// Relative to another view
view.X = Pos.Right(otherView) + 1;   // 1 right of otherView
view.Y = Pos.Bottom(otherView) + 1;  // 1 below otherView
view.X = Pos.Left(otherView);        // aligned left with otherView
view.Y = Pos.Top(otherView);         // aligned top with otherView

// Align -- align groups of views
view.X = Pos.Align(Alignment.End);   // right-align (e.g., dialog buttons)

// Func -- custom function
view.X = Pos.Func(() => CalculateX());

// Arithmetic
view.X = Pos.Center() - 10;
view.Y = Pos.Bottom(label) + 2;
```

### Dim Types (Sizing)

```csharp
// Absolute -- fixed size
view.Width = 40;                       // Dim.Absolute(40)

// Percent -- percentage of parent
view.Width = Dim.Percent(50);          // 50% of parent width

// Fill -- fill remaining space
view.Width = Dim.Fill();               // fill to right edge
view.Width = Dim.Fill(2);              // fill minus 2 (margin)

// Auto -- size based on content (replaces v1's AutoSize)
view.Width = Dim.Auto();
view.Width = Dim.Auto(minimumContentDim: 20);

// Relative to another view
view.Width = Dim.Width(otherView);
view.Height = Dim.Height(otherView);

// Func -- custom function
view.Width = Dim.Func(() => CalculateWidth());

// Arithmetic
view.Width = Dim.Fill() - 10;
view.Height = Dim.Height(label) + 2;
```

### Frame vs. Viewport

- **Frame** -- outermost rectangle: location and size relative to SuperView
- **Viewport** -- visible portion of content area: acts as a scrollable portal into the view's content

```csharp
// Set content size larger than viewport to enable scrolling
view.SetContentSize(new Size(200, 100));
// Viewport automatically provides scroll behavior
```

---

## Core Views

### Container Views

```csharp
// Window -- top-level container with title bar and border
var window = new Window
{
    Title = "Main Window",
    Width = Dim.Fill(),
    Height = Dim.Fill()
};

// FrameView -- bordered container without title bar behavior
var frame = new FrameView
{
    Title = "Settings",
    X = 1, Y = 1,
    Width = Dim.Fill(1),
    Height = 10
};
window.Add(frame);
```

### Text and Input Views

```csharp
// Label -- static text display
var label = new Label
{
    Text = "Username:",
    X = 1, Y = 1
};

// TextField -- single-line text input
var textField = new TextField
{
    X = Pos.Right(label) + 1,
    Y = Pos.Top(label),
    Width = 30,
    Text = ""
};

// TextView -- multi-line text editor
var textView = new TextView
{
    X = 1, Y = 3,
    Width = Dim.Fill(1),
    Height = Dim.Fill(1),
    Text = "Multi-line\nediting area"
};
```

### Button

```csharp
var button = new Button
{
    Text = "OK",
    X = Pos.Center(),
    Y = Pos.Bottom(textField) + 1
};

// Accept event (v2 replaces v1's Clicked)
button.Accepting += (sender, args) =>
{
    MessageBox.Query(button.App!, "Info", $"You entered: {textField.Text}", "OK");
    args.Handled = true; // prevent event bubbling
};
```

### ListView and TableView

```csharp
// ListView -- scrollable list
var items = new List<string> { "Item 1", "Item 2", "Item 3" };
var listView = new ListView
{
    X = 1, Y = 1,
    Width = Dim.Fill(1),
    Height = Dim.Fill(1),
    Source = new ListWrapper<string>(new ObservableCollection<string>(items))
};

listView.SelectedItemChanged += (sender, args) =>
{
    // args.Value is the selected item index
};
```

### CheckBox and RadioGroup

```csharp
var checkbox = new CheckBox
{
    Text = "Enable notifications",
    X = 1, Y = 1
};

checkbox.CheckedStateChanging += (sender, args) =>
{
    // args.NewValue is the new CheckState
};

var radioGroup = new RadioGroup
{
    X = 1, Y = 3,
    RadioLabels = ["Option A", "Option B", "Option C"]
};

radioGroup.SelectedItemChanged += (sender, args) =>
{
    // args.SelectedItem is the selected index
};
```

### Additional v2 Views

```csharp
// DatePicker -- calendar-based date input
var datePicker = new DatePicker
{
    X = 1, Y = 1,
    Date = DateTime.Today
};

// NumericUpDown -- numeric spinner
var spinner = new NumericUpDown<int>
{
    X = 1, Y = 3,
    Value = 42
};

// ColorPicker -- TrueColor selection
var colorPicker = new ColorPicker
{
    X = 1, Y = 5,
    SelectedColor = new Color(0, 120, 215)
};
```

---

## Menus and Status Bar

### MenuBar

In v2, `MenuBar` takes a `MenuBarItem[]` constructor parameter. `MenuItem` supports both positional constructors and object initializer syntax.

```csharp
var menuBar = new MenuBar([
    new MenuBarItem("_File",
    [
        new MenuItem("_New", "Create new file", () => NewFile()),
        new MenuItem("_Open", "Open existing file", () => OpenFile()),
        new MenuBarItem("_Recent",
        [
            new MenuItem("file1.txt", "", () => Open("file1.txt")),
            new MenuItem("file2.txt", "", () => Open("file2.txt"))
        ]),
        null,  // separator
        new MenuItem
        {
            Title = "_Quit",
            HelpText = "Exit application",
            Key = Application.QuitKey,
            Command = Command.Quit
        }
    ]),
    new MenuBarItem("_Edit",
    [
        new MenuItem("_Copy", "", () => Copy(), Key.C.WithCtrl),
        new MenuItem("_Paste", "", () => Paste(), Key.V.WithCtrl)
    ]),
    new MenuBarItem("_Help",
    [
        new MenuItem("_About", "About this app", () =>
            MessageBox.Query(app, "", "My TUI App v1.0", "OK"))
    ])
]);
window.Add(menuBar);
```

### StatusBar

In v2, `StatusBar` uses `Shortcut` objects instead of v1's `StatusItem` (which was removed). Add shortcuts via `statusBar.Add()`.

```csharp
var statusBar = new StatusBar();

var helpShortcut = new Shortcut
{
    Title = "Help",
    Key = Key.F1,
    CanFocus = false
};
helpShortcut.Accepting += (sender, args) =>
{
    ShowHelp();
    args.Handled = true;
};

var saveShortcut = new Shortcut
{
    Title = "Save",
    Key = Key.F2,
    CanFocus = false
};
saveShortcut.Accepting += (sender, args) =>
{
    Save();
    args.Handled = true;
};

var quitShortcut = new Shortcut
{
    Title = "Quit",
    Key = Application.QuitKey,
    CanFocus = false
};

statusBar.Add(helpShortcut, saveShortcut, quitShortcut);
window.Add(statusBar);
```

---

## Dialogs and MessageBox

### Dialog

```csharp
// Dialog with buttons
var dialog = new Dialog
{
    Title = "Confirm",
    Width = 50,
    Height = 10
};

var label = new Label
{
    Text = "Are you sure?",
    X = Pos.Center(),
    Y = 1
};
dialog.Add(label);

var okButton = new Button { Text = "OK" };
okButton.Accepting += (sender, args) =>
{
    dialog.RequestStop();
    args.Handled = true;
};

var cancelButton = new Button { Text = "Cancel" };
cancelButton.Accepting += (sender, args) =>
{
    dialog.RequestStop();
    args.Handled = true;
};

dialog.AddButton(okButton);
dialog.AddButton(cancelButton);

app.Run(dialog);
```

### MessageBox

In v2, `MessageBox.Query` and `MessageBox.ErrorQuery` take an `IApplication` parameter first.

```csharp
// Simple query dialog (returns button index)
// In v2, pass the app instance as first parameter
int result = MessageBox.Query(app, "Confirm Delete",
    "Delete this file permanently?",
    "Yes", "No");

if (result == 0)
{
    // User clicked "Yes"
}

// Error message
MessageBox.ErrorQuery(app, "Error",
    "Failed to save file.\nCheck permissions.",
    "OK");
```

### FileDialog

```csharp
var fileDialog = new FileDialog
{
    Title = "Open File",
    AllowedTypes = [new AllowedType("C# Files", ".cs", ".csx")],
    MustExist = true
};

app.Run(fileDialog);

if (!fileDialog.Canceled)
{
    string selectedPath = fileDialog.FilePath;
    // Process the selected file
}
```

---

## Event Handling and Key Bindings

### Key Bindings with Commands

Terminal.Gui v2 uses a command pattern for key bindings. Views declare supported commands, then map keys to those commands.

```csharp
// Add a custom command and bind a key to it
view.AddCommand(Command.Accept, (args) =>
{
    // Handle the accept command
    return true; // handled
});
view.KeyBindings.Add(Key.Enter, Command.Accept);

// Bind Ctrl+S to a save action
view.KeyBindings.Add(Key.S.WithCtrl, Command.Save);
view.AddCommand(Command.Save, (args) =>
{
    SaveDocument();
    return true;
});
```

### Key Event Handling

```csharp
// KeyDown -- fires when a key is pressed
view.KeyDown += (sender, args) =>
{
    if (args.KeyCode == Key.F5)
    {
        RefreshData();
        args.Handled = true;
    }
};

// KeyUp -- fires when a key is released
view.KeyUp += (sender, args) =>
{
    // Handle key release
};
```

### Application-Level Keys

Although v2 uses instance-based `IApplication`, `Application.QuitKey` remains a static configuration property set before `Init()`. These are framework-level settings, not per-instance state.

```csharp
// Configure global quit key before Init (default: Esc)
Application.QuitKey = Key.Q.WithCtrl;

IApplication app = Application.Create().Init();
// Application.QuitKey is now in effect for this app instance
```

### Mouse Events

```csharp
// Mouse events provide viewport-relative coordinates
view.MouseClick += (sender, args) =>
{
    int col = args.Position.X;
    int row = args.Position.Y;
    // Handle click at viewport-relative position
};

view.MouseEvent += (sender, args) =>
{
    if (args.Flags.HasFlag(MouseFlags.Button1DoubleClicked))
    {
        // Handle double-click
    }
};
```

---

## Color Themes and Styling

Terminal.Gui v2 defaults to 24-bit TrueColor with automatic fallback to 16-color mode for limited terminals.

### Color and Attribute

```csharp
// TrueColor via RGB values
var customColor = new Color(0xFF, 0x99, 0x00); // orange

// Create an attribute (foreground + background + style)
var attr = new Attribute(
    new Color(255, 255, 255),  // foreground: white
    new Color(0, 0, 128)       // background: dark blue
);

// Apply to a view
view.ColorScheme = new ColorScheme
{
    Normal = attr,
    Focus = new Attribute(Color.Black, Color.BrightCyan),
    HotNormal = new Attribute(Color.Red, Color.Blue),
    HotFocus = new Attribute(Color.BrightRed, Color.BrightCyan)
};
```

### Text Styles

```csharp
// v2 supports text effects (terminal-dependent)
// Bold, Italic, Underline, Strikethrough, Blink, Reverse, Faint
```

### Theme Configuration

Terminal.Gui v2 supports JSON-based theme persistence via `ConfigurationManager`. Users can customize themes, key bindings, and view properties without code changes.

```csharp
// Set a built-in theme via runtime config before Init
ConfigurationManager.RuntimeConfig = """{ "Theme": "Amber Phosphor" }""";
ConfigurationManager.Enable(ConfigLocations.All);

IApplication app = Application.Create().Init();
// Theme is now applied
```

---

## Adornments (Borders, Margins, Padding)

Terminal.Gui v2 provides an adornment system for visual spacing and borders.

```csharp
var view = new View
{
    X = 1, Y = 1,
    Width = 40, Height = 10
};

// Border styles: Single, Double, Heavy, Rounded, Dashed, Dotted
view.Border.LineStyle = LineStyle.Rounded;
view.Border.Thickness = new Thickness(1);

// Margin -- transparent spacing outside the border
view.Margin.Thickness = new Thickness(1);

// Padding -- internal spacing inside the border
view.Padding.Thickness = new Thickness(1, 0); // top/bottom=1, left/right=0
```

---

## Cross-Platform Considerations

Terminal.Gui supports Windows, macOS, and Linux terminals with automatic driver selection.

### Terminal Compatibility

| Feature | Windows Terminal | macOS Terminal.app | Linux (xterm/gnome) |
|---|---|---|---|
| TrueColor (24-bit) | Yes | Yes | Yes (most) |
| Mouse support | Yes | Yes | Yes |
| Unicode/emoji | Yes | Yes | Varies |
| Sixel images | Some | No | Some |
| Key modifiers | Full | Limited | Full |

### Platform-Specific Gotchas

- **macOS Terminal.app** -- limited modifier key support; Alt-key combinations may be intercepted by the terminal. iTerm2 and WezTerm provide better modifier support.
- **SSH sessions** -- terminal capabilities depend on the client terminal, not the server. Test TUI apps over SSH to verify rendering.
- **Windows Console Host** -- legacy conhost has limited Unicode support. Windows Terminal provides full support.
- **tmux/screen** -- may intercept certain key combinations. Set `TERM=xterm-256color` for best color support.

### Logging Integration

```csharp
// Terminal.Gui v2 supports Microsoft.Extensions.Logging
// Useful for debugging rendering and event issues without
// interfering with the TUI display
```

---

## Complete Example: Simple Editor

```csharp
using Terminal.Gui;

using IApplication app = Application.Create().Init();

var window = new Window
{
    Title = $"Simple Editor ({Application.QuitKey} to quit)",
    Width = Dim.Fill(),
    Height = Dim.Fill()
};

// Declare textView first so menu lambda can capture it
var textView = new TextView
{
    X = 0, Y = 1,  // below menu bar
    Width = Dim.Fill(),
    Height = Dim.Fill(1),  // leave room for status bar
    Text = ""
};

// Menu bar
var menuBar = new MenuBar([
    new MenuBarItem("_File",
    [
        new MenuItem("_New", "Clear editor", () => textView.Text = ""),
        null,
        new MenuItem
        {
            Title = "_Quit",
            HelpText = "Exit",
            Key = Application.QuitKey,
            Command = Command.Quit
        }
    ])
]);

// Status bar with Shortcut objects (v2 API)
var statusBar = new StatusBar();
var helpShortcut = new Shortcut { Title = "Help", Key = Key.F1, CanFocus = false };
helpShortcut.Accepting += (s, e) =>
{
    MessageBox.Query(app, "Help", "Simple text editor.", "OK");
    e.Handled = true;
};
statusBar.Add(helpShortcut);

window.Add(menuBar, textView, statusBar);
app.Run(window);
```

---

## Agent Gotchas

1. **Do not use v1 static lifecycle pattern.** v2 uses instance-based `Application.Create().Init()` with `IDisposable`. The v1 pattern of `Application.Init()` / `Application.Run()` / `Application.Shutdown()` is obsolete. Always wrap the application in a `using` statement.
2. **Do not use `View.AutoSize`.** It was removed in v2. Use `Dim.Auto()` for content-based sizing instead.
3. **Do not confuse Frame with Viewport.** Frame is the outer rectangle (position/size relative to SuperView). Viewport is the visible content area (supports scrolling). Use Viewport for content-relative coordinates.
4. **Do not use `Button.Clicked`.** It was replaced by `Button.Accepting` in v2. The semantic change reflects the command pattern -- `Accepting` fires when the button's accept action triggers.
5. **Do not call UI operations from background threads.** Terminal.Gui is single-threaded. Use `Application.Invoke()` to marshal calls back to the UI thread from async code. See [skill:dotnet-csharp-async-patterns] for async patterns.
6. **Do not forget `RequestStop()` to close windows.** Calling `Dispose()` directly on a running window corrupts terminal state. Use `RequestStop()` to cleanly exit the run loop, which triggers proper cleanup.
7. **Do not hardcode terminal dimensions.** Use `Dim.Fill()`, `Dim.Percent()`, and `Pos.Center()` for responsive layouts that adapt to terminal resizing. Absolute coordinates break on different terminal sizes.
8. **Do not ignore terminal state on crash.** If the application crashes without proper disposal, the terminal may be left in raw mode. Wrap `app.Run()` in try/catch and ensure the `using` block disposes the application to restore terminal state.
9. **Do not use `ScrollView`.** It was removed in v2. All views now support scrolling natively via `SetContentSize()` and the `Viewport` property.
10. **Do not use `NStack.ustring`.** It was removed in v2. Use standard `System.String` throughout.
11. **Do not use `StatusItem`.** It was removed in v2. Use `Shortcut` objects with `StatusBar.Add()` instead. Set `CanFocus = false` on status bar shortcuts and handle `Accepting` with `args.Handled = true`.

---

## Prerequisites

- **NuGet package:** `Terminal.Gui` 2.0.0-alpha (v2) or 1.19.x (v1 maintenance)
- **Target framework:** net8.0 or later (also supports netstandard2.0/2.1)
- **Terminal:** Any terminal emulator supporting ANSI escape sequences. Windows Terminal, iTerm2, or modern Linux terminal recommended for best experience (TrueColor, mouse, Unicode).
- **No GUI runtime required:** Terminal.Gui runs in any terminal -- no X11, Wayland, or desktop environment needed.

---

## References

- [Terminal.Gui GitHub](https://github.com/gui-cs/Terminal.Gui) -- source code, issues, v2 development branch
- [Terminal.Gui v2 Documentation](https://gui-cs.github.io/Terminal.Gui/) -- API reference and guides for v2
- [Terminal.Gui NuGet](https://www.nuget.org/packages/Terminal.Gui) -- package downloads and version history
- [Terminal.Gui v2 What's New](https://gui-cs.github.io/Terminal.Gui/docs/newinv2) -- comprehensive v2 feature overview
- [v1 to v2 Migration Guide](https://github.com/gui-cs/Terminal.Gui/blob/v2_develop/docfx/docs/migratingfromv1.md) -- breaking changes and migration patterns
