# dotnet-terminal-gui -- Detailed Examples

Extended code examples for Terminal.Gui v2 views, layout, menus, dialogs, event handling, themes, and complete application patterns.

---

## Core Views

### Container Views

```csharp
var window = new Window
{
    Title = "Main Window",
    Width = Dim.Fill(),
    Height = Dim.Fill()
};

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
var label = new Label
{
    Text = "Username:",
    X = 1, Y = 1
};

var textField = new TextField
{
    X = Pos.Right(label) + 1,
    Y = Pos.Top(label),
    Width = 30,
    Text = ""
};

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

button.Accepting += (sender, args) =>
{
    MessageBox.Query(button.App!, "Info", $"You entered: {textField.Text}", "OK");
    args.Handled = true;
};
```

### ListView and TableView

```csharp
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
```

### Additional v2 Views

```csharp
var datePicker = new DatePicker
{
    X = 1, Y = 1,
    Date = DateTime.Today
};

var spinner = new NumericUpDown<int>
{
    X = 1, Y = 3,
    Value = 42
};

var colorPicker = new ColorPicker
{
    X = 1, Y = 5,
    SelectedColor = new Color(0, 120, 215)
};
```

---

## Menus and Status Bar

### MenuBar

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

```csharp
int result = MessageBox.Query(app, "Confirm Delete",
    "Delete this file permanently?",
    "Yes", "No");

if (result == 0)
{
    // User clicked "Yes"
}

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
}
```

---

## Event Handling and Key Bindings

### Key Bindings with Commands

```csharp
view.AddCommand(Command.Accept, (args) =>
{
    return true;
});
view.KeyBindings.Add(Key.Enter, Command.Accept);

view.KeyBindings.Add(Key.S.WithCtrl, Command.Save);
view.AddCommand(Command.Save, (args) =>
{
    SaveDocument();
    return true;
});
```

### Key Event Handling

```csharp
view.KeyDown += (sender, args) =>
{
    if (args.KeyCode == Key.F5)
    {
        RefreshData();
        args.Handled = true;
    }
};
```

### Mouse Events

```csharp
view.MouseClick += (sender, args) =>
{
    int col = args.Position.X;
    int row = args.Position.Y;
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

```csharp
var customColor = new Color(0xFF, 0x99, 0x00);

var attr = new Attribute(
    new Color(255, 255, 255),
    new Color(0, 0, 128)
);

view.ColorScheme = new ColorScheme
{
    Normal = attr,
    Focus = new Attribute(Color.Black, Color.BrightCyan),
    HotNormal = new Attribute(Color.Red, Color.Blue),
    HotFocus = new Attribute(Color.BrightRed, Color.BrightCyan)
};
```

### Theme Configuration

```csharp
ConfigurationManager.RuntimeConfig = """{ "Theme": "Amber Phosphor" }""";
ConfigurationManager.Enable(ConfigLocations.All);
IApplication app = Application.Create().Init();
```

---

## Adornments (Borders, Margins, Padding)

```csharp
var view = new View
{
    X = 1, Y = 1,
    Width = 40, Height = 10
};

view.Border.LineStyle = LineStyle.Rounded;
view.Border.Thickness = new Thickness(1);
view.Margin.Thickness = new Thickness(1);
view.Padding.Thickness = new Thickness(1, 0);
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

var textView = new TextView
{
    X = 0, Y = 1,
    Width = Dim.Fill(),
    Height = Dim.Fill(1),
    Text = ""
};

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
