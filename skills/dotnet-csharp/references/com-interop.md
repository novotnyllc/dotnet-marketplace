# COM Interop

Component Object Model (COM) interop for .NET: modern `ComWrappers`-based source generation (.NET 8+), legacy `[ComImport]` RCW/CCW patterns, COM activation, Office COM automation, and threading considerations. Prefer Open XML SDK over COM for document manipulation — COM requires the Office application installed and is Windows-only.

**Version assumptions:** .NET 8+ for `[GeneratedComInterface]` source generation. `[ComImport]` available in all .NET versions but generates runtime marshalling code incompatible with AOT.

## ComWrappers Source Generation (.NET 8+)

The modern approach uses `[GeneratedComInterface]` to produce COM interop code at compile time via source generators. This is AOT-compatible and eliminates runtime RCW/CCW generation.

```csharp
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.Marshalling;

// Define the COM interface with source generation
[GeneratedComInterface]
[Guid("00000000-0000-0000-C000-000000000046")]
public partial interface IUnknownExample
{
    void QueryInterface(in Guid riid, out nint ppvObject);
}

// A more practical example — automating a COM server
[GeneratedComInterface]
[Guid("000209FF-0000-0000-C000-000000000046")]
public partial interface IWordApplication
{
    [return: MarshalAs(UnmanagedType.Interface)]
    object Documents { get; }

    [MarshalAs(UnmanagedType.BStr)]
    string Version { get; }

    void Quit();
}
```

### Key Requirements

- Interface must be `partial`
- `[Guid]` attribute is required on every COM interface
- `[GeneratedComInterface]` generates the marshalling code at compile time
- String parameters use `[MarshalAs(UnmanagedType.BStr)]` for COM `BSTR` strings
- Works with Native AOT (no runtime codegen needed)

### StringMarshalling for COM

```csharp
// Default: BSTR (most COM APIs)
[GeneratedComInterface(StringMarshalling = StringMarshalling.Custom,
    StringMarshallingCustomType = typeof(BStrStringMarshaller))]
[Guid("...")]
public partial interface IMyComObject
{
    void SetName([MarshalAs(UnmanagedType.BStr)] string name);
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetName();
}

// UTF-8 (rare in COM, but used by some custom servers)
[GeneratedComInterface(StringMarshalling = StringMarshalling.Utf8)]
[Guid("...")]
public partial interface IMyUtf8ComObject
{
    void Process(string input);
}
```

## Legacy ComImport (Pre-.NET 8)

The older approach using `[ComImport]` relies on runtime-generated Runtime Callable Wrappers (RCW) and COM Callable Wrappers (CCW). Not AOT-compatible.

```csharp
using System.Runtime.InteropServices;

[ComImport]
[Guid("000209FF-0000-0000-C000-000000000046")]
[InterfaceType(ComInterfaceType.InterfaceIsIDispatch)]
public interface IWordApplication
{
    object Documents { get; }
    string Version { get; }
    void Quit();
}
```

### Migration Path

| Pattern | Legacy | Modern (.NET 8+) |
|---------|--------|-------------------|
| Interface attribute | `[ComImport]` | `[GeneratedComInterface]` |
| Interface modifier | none | `partial` |
| Wrapper generation | Runtime (RCW/CCW) | Compile-time (source gen) |
| AOT compatible | No | Yes |
| Analyzer | None | SYSLIB1096-SYSLIB1100 |

The `SYSLIB1096` analyzer suggests converting `[ComImport]` interfaces to `[GeneratedComInterface]`.

## COM Activation

### Creating COM Objects

```csharp
using System.Runtime.InteropServices;

// By CLSID (class ID)
var clsid = new Guid("000209FF-0000-0000-C000-000000000046"); // Word.Application
var type = Type.GetTypeFromCLSID(clsid, throwOnError: true)!;
var wordApp = Activator.CreateInstance(type)!;

// By ProgID (programmatic identifier)
var type2 = Type.GetTypeFromProgID("Word.Application", throwOnError: true)!;
var wordApp2 = Activator.CreateInstance(type2)!;

// With GeneratedComInterface, cast to the typed interface
var app = (IWordApplication)Activator.CreateInstance(
    Type.GetTypeFromProgID("Word.Application")!)!;
try
{
    Console.WriteLine($"Word version: {app.Version}");
}
finally
{
    app.Quit();
    Marshal.FinalReleaseComObject(app);
}
```

### IDispatch Late Binding (dynamic)

For quick scripting without defining interfaces, use `dynamic`:

```csharp
// Late-bound COM — no interface definition needed
// Requires <LangVersion>latest</LangVersion> and System.Runtime.InteropServices
dynamic word = Activator.CreateInstance(
    Type.GetTypeFromProgID("Word.Application")!)!;
word.Visible = true;

dynamic doc = word.Documents.Add();
dynamic para = doc.Paragraphs.Add();
para.Range.Text = "Hello from .NET";
para.Range.Font.Size = 16;
para.Range.Font.Bold = 1;

doc.SaveAs2(@"C:\temp\test.docx");
doc.Close();
word.Quit();

Marshal.FinalReleaseComObject(word);
```

Late binding is convenient but has no compile-time safety, no IntelliSense, and poor performance compared to typed interfaces.

## COM Threading

COM has threading models that .NET must respect:

| Thread Model | Description | .NET Impact |
|---|---|---|
| STA (Single-Threaded Apartment) | COM object runs on one thread | Must call from `[STAThread]` or STA `SynchronizationContext` |
| MTA (Multi-Threaded Apartment) | COM object callable from any thread | Default for .NET threads |
| Free-threaded | No apartment restrictions | No special handling needed |

Most Office COM objects require STA:

```csharp
// Console app using Office COM — must be STA
[STAThread]
static void Main(string[] args)
{
    // COM calls work on the STA thread
    var type = Type.GetTypeFromProgID("Excel.Application")!;
    dynamic excel = Activator.CreateInstance(type)!;
    // ...
    Marshal.FinalReleaseComObject(excel);
}

// In ASP.NET or background services, create a dedicated STA thread
var staThread = new Thread(() =>
{
    // COM operations here
});
staThread.SetApartmentState(ApartmentState.STA);
staThread.Start();
staThread.Join();
```

## Office COM vs Open XML SDK

| Concern | COM Automation | Open XML SDK |
|---------|---------------|-------------|
| Requires Office installed | Yes | No |
| Platform | Windows only | Cross-platform |
| Server/headless use | Not supported by Microsoft | Fully supported |
| Performance | Slow (out-of-process COM) | Fast (in-process, direct XML) |
| AOT compatible | No (COM runtime) | Yes |
| Feature coverage | 100% of Office features | OOXML file format only |
| Charts, macros, VBA | Full support | Read/modify only |
| Pivot tables | Full support | Full support |
| Print/export to PDF | Yes (via Office engine) | No (use QuestPDF) |
| Licensing | Office license required | MIT (free) |

**Recommendation:** Use Open XML SDK for document generation, manipulation, and server-side processing. Use COM only when you need features that require the Office rendering engine (print layout, PDF export via Office, macro execution) and Windows desktop deployment is acceptable.

## Resource Cleanup

COM objects hold unmanaged resources. Always release them explicitly:

```csharp
// Release a single COM object
Marshal.ReleaseComObject(comObject);

// Release all references (when done with the object entirely)
Marshal.FinalReleaseComObject(comObject);

// Pattern for multiple COM objects — release in reverse order
object? workbook = null;
object? worksheet = null;
try
{
    workbook = excel.Workbooks.Open(path);
    worksheet = ((dynamic)workbook).Sheets[1];
    // ... work with worksheet
}
finally
{
    if (worksheet is not null) Marshal.ReleaseComObject(worksheet);
    if (workbook is not null) Marshal.ReleaseComObject(workbook);
}
```

**Two-dot rule:** Avoid chaining COM property access (`excel.Workbooks.Open(...)`) because intermediate COM objects are not released. Assign each level to a variable and release in reverse order. In practice, `dynamic` + `FinalReleaseComObject` on the top-level object is acceptable for scripts.

## Agent Gotchas

1. **Don't use COM for server-side document generation.** Microsoft explicitly does not support Office COM automation in server/headless environments (ASP.NET, Azure, containers). Use Open XML SDK instead.
2. **Don't forget `[STAThread]` for Office COM.** Office COM objects require STA threading. Without it, calls may deadlock or throw `InvalidOperationException`.
3. **Don't use COM in AOT builds.** COM RCW/CCW require runtime code generation. Use `[GeneratedComInterface]` (.NET 8+) for AOT-compatible COM, or avoid COM entirely.
4. **Don't leak COM references.** Always call `Marshal.ReleaseComObject` or `Marshal.FinalReleaseComObject`. Leaked COM references keep Office processes running after your app exits.
5. **Don't assume COM works cross-platform.** COM is Windows-only. For cross-platform interop, use P/Invoke or Open XML SDK.
6. **Don't use `[ComImport]` in new .NET 8+ code.** Use `[GeneratedComInterface]` for source-generated, AOT-compatible COM interop.
