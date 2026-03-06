# Razor Pages

Razor Pages is ASP.NET Core's page-focused programming model for server-rendered UI. It uses a convention-based folder structure where each page is a `.cshtml` file paired with a `PageModel` code-behind class. Best suited for CRUD forms, admin dashboards, and server-rendered content pages.

## When to Use Razor Pages

| Scenario | Razor Pages | MVC | Blazor SSR |
|----------|-------------|-----|------------|
| Simple CRUD forms | Best fit | Viable | Viable |
| Page-focused server UI | Best fit | Overengineered | Viable |
| Complex shared layouts with partial views | Good | Good | Limited |
| Rich interactivity without JS | No | No | Best fit |
| API endpoints | No -- use Minimal APIs or controllers | Yes | No |

## Page Model Pattern

```csharp
// Pages/Products/Index.cshtml.cs
public class IndexModel : PageModel
{
    private readonly AppDbContext _db;

    public IndexModel(AppDbContext db) => _db = db;

    public List<Product> Products { get; set; } = [];

    public async Task OnGetAsync()
    {
        Products = await _db.Products.OrderBy(p => p.Name).ToListAsync();
    }
}
```

```cshtml
@* Pages/Products/Index.cshtml *@
@page
@model IndexModel

<h1>Products</h1>

<table>
    @foreach (var product in Model.Products)
    {
        <tr>
            <td>@product.Name</td>
            <td>@product.Price.ToString("C")</td>
            <td><a asp-page="./Edit" asp-route-id="@product.Id">Edit</a></td>
        </tr>
    }
</table>

<a asp-page="./Create">Create New</a>
```

### Handler Methods

Handlers follow the `On{Verb}[Async]` convention:

```csharp
public class CreateModel : PageModel
{
    private readonly AppDbContext _db;
    public CreateModel(AppDbContext db) => _db = db;

    [BindProperty]
    public ProductInput Input { get; set; } = default!;

    public void OnGet() { }  // Display the form

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
            return Page();  // Re-display with validation errors

        var product = new Product { Name = Input.Name, Price = Input.Price };
        _db.Products.Add(product);
        await _db.SaveChangesAsync();

        return RedirectToPage("./Index");
    }
}
```

### Named Handlers

Use named handlers for multiple submit buttons on the same page:

```csharp
public async Task<IActionResult> OnPostDeleteAsync(int id)
{
    var product = await _db.Products.FindAsync(id);
    if (product is null) return NotFound();

    _db.Products.Remove(product);
    await _db.SaveChangesAsync();
    return RedirectToPage();
}
```

```cshtml
<button type="submit" asp-page-handler="delete" asp-route-id="@product.Id">Delete</button>
```

The form generates `formaction="?handler=delete&id=42"` and dispatches to `OnPostDeleteAsync`.

## Model Binding and Validation

```csharp
[BindProperty]
public ProductInput Input { get; set; } = default!;

// BindProperty binds on POST by default. For GET binding:
[BindProperty(SupportsGet = true)]
public string? SearchTerm { get; set; }
```

**Warning:** `[BindProperty]` should not be applied to properties containing fields the client should not modify (overposting). Use a view model/DTO instead of binding directly to your entity.

```csharp
// AVOID: binding the entity directly
[BindProperty]
public Product Product { get; set; }  // Overposting risk -- client can set Id, IsAdmin, etc.

// PREFER: bind a restricted DTO
[BindProperty]
public ProductInput Input { get; set; }

public record ProductInput(
    [Required, StringLength(100)] string Name,
    [Range(0.01, 10000)] decimal Price);
```

## Routing Conventions

Folder structure maps directly to URL paths:

```
Pages/
  Index.cshtml          -> /
  Privacy.cshtml        -> /Privacy
  Products/
    Index.cshtml        -> /Products
    Create.cshtml       -> /Products/Create
    Edit.cshtml         -> /Products/Edit
```

Custom route templates in `@page`:

```cshtml
@page "{id:int}"          @* /Products/Edit/42 *@
@page "{id:int?}"         @* Optional parameter *@
@page "/custom-path"      @* Override convention *@
```

## Layouts, Partials, and View Components

```cshtml
@* Pages/Shared/_Layout.cshtml -- shared layout *@
<html>
<body>
    <nav>@await Component.InvokeAsync("Navigation")</nav>
    @RenderBody()
    @await RenderSectionAsync("Scripts", required: false)
</body>
</html>
```

```cshtml
@* Partial view usage *@
<partial name="_ProductCard" model="product" />
```

```cshtml
@* Tag Helper form with anti-forgery (automatic in Razor Pages) *@
<form method="post">
    <input asp-for="Input.Name" />
    <span asp-validation-for="Input.Name"></span>
    <input type="submit" value="Save" />
</form>
```

Anti-forgery tokens are included automatically in Razor Pages forms. No manual `@Html.AntiForgeryToken()` required.

## Page Filters

```csharp
public class AuditPageFilter : IAsyncPageFilter
{
    public Task OnPageHandlerSelectionAsync(PageHandlerSelectedContext context)
        => Task.CompletedTask;

    public async Task OnPageHandlerExecutionAsync(
        PageHandlerExecutingContext context,
        PageHandlerExecutionDelegate next)
    {
        var logger = context.HttpContext.RequestServices
            .GetRequiredService<ILogger<AuditPageFilter>>();
        logger.LogInformation("Executing {Page}", context.ActionDescriptor.DisplayName);

        await next();
    }
}

// Register globally
builder.Services.AddRazorPages(options =>
{
    options.Conventions.ConfigureFilter(new AuditPageFilter());
});
```

Note: MVC Action Filters are **ignored** by Razor Pages. Use `IPageFilter` / `IAsyncPageFilter` instead.

## Areas

```
Areas/
  Admin/
    Pages/
      Dashboard.cshtml    -> /Admin/Dashboard
      Users/
        Index.cshtml      -> /Admin/Users
```

```csharp
builder.Services.AddRazorPages();
// Areas are auto-discovered; no explicit registration needed
```

## Authorization on Pages

```csharp
builder.Services.AddRazorPages(options =>
{
    options.Conventions.AuthorizePage("/Products/Create");
    options.Conventions.AuthorizeFolder("/Admin");
    options.Conventions.AllowAnonymousToPage("/Public/About");
});
```

Or per-page with the attribute:

```csharp
[Authorize(Policy = "AdminOnly")]
public class DashboardModel : PageModel { }
```

**Note:** You cannot declare a folder as anonymous and then require auth on a specific page inside it -- `AllowAnonymousFilter` takes precedence over `AuthorizeFilter` when both are applied.

---

## Agent Gotchas

1. **Do not use `[BindProperty]` on entity types** -- this enables overposting. Always bind to a restricted input DTO and map to the entity in the handler.
2. **Do not forget that `[BindProperty]` does not bind on GET by default** -- set `SupportsGet = true` explicitly if you need query string binding on GET requests.
3. **Do not use MVC Action Filters on Razor Pages** -- they are silently ignored. Use `IPageFilter` or `IAsyncPageFilter` instead.
4. **Do not call `RedirectToPage` with a relative path missing `./`** -- `RedirectToPage("Index")` resolves against the root, not the current folder. Use `RedirectToPage("./Index")` for same-folder redirects.
5. **Do not omit `@page` at the top of `.cshtml` files** -- without `@page`, the file is treated as a partial view, not a routable Razor Page. Requests will 404.
6. **Do not combine `AllowAnonymousToFolder` with `AuthorizePage` inside that folder** -- `AllowAnonymous` always wins, silently bypassing the per-page authorization.

---

## References

- [Razor Pages introduction](https://learn.microsoft.com/aspnet/core/razor-pages/?view=aspnetcore-10.0)
- [Model binding](https://learn.microsoft.com/aspnet/core/mvc/models/model-binding?view=aspnetcore-10.0)
- [Authorization conventions](https://learn.microsoft.com/aspnet/core/security/authorization/razor-pages-authorization?view=aspnetcore-10.0)
- [Page filters](https://learn.microsoft.com/aspnet/core/razor-pages/filter?view=aspnetcore-10.0)
- [Route conventions](https://learn.microsoft.com/aspnet/core/razor-pages/razor-pages-conventions?view=aspnetcore-10.0)
