# Recommended .NET Libraries

Permissively licensed (MIT, Apache 2.0, BSD) .NET libraries for common tasks. Several high-profile .NET OSS libraries changed to restrictive licenses in 2023-2025 — this reference tracks the current state and provides safe alternatives.

**Why this matters for agents:** Agents must not introduce restrictive license dependencies into projects without explicit user consent. Always prefer the permissive alternatives listed here.

## Licensing Alert: Libraries That Changed

These were once permissively licensed but switched to dual-license or commercial models. Do not recommend them as default choices — note the license change if a user specifically asks about them.

| Library | Old License | New License | Version Affected | Permissive Alternative |
|---------|-------------|-------------|-----------------|----------------------|
| AutoMapper | MIT | Custom (paid > threshold) | v13+ | **Mapperly** (source-gen, zero-cost) |
| MediatR | Apache 2.0 | Custom (paid > threshold) | v12+ | **Mediator** by martinothamar (source-gen) |
| MassTransit | Apache 2.0 | Custom (free < 1M msg/mo) | v9+ | **Wolverine**, **Rebus** |
| ImageSharp | Apache 2.0 | Six Labors Split License | v3+ | **SkiaSharp**, **Magick.NET** |
| FluentAssertions | Apache 2.0 | Custom (paid > threshold) | v8+ | **Shouldly**, **TUnit** built-in assertions |
| EPPlus | LGPL → Polyform | Polyform (free < $1M rev) | v5+ | **ClosedXML**, **Open XML SDK** |
| QuestPDF | MIT | Community License (paid > $1M) | 2024+ | **PDFsharp/MigraDoc** |
| Duende IdentityServer | Apache 2.0 | Duende License (paid > $1M) | v6+ | **OpenIddict** |

## Object Mapping

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **Mapperly** | Apache 2.0 | [Mapperly](https://www.nuget.org/packages/Riok.Mapperly) | Source-generated, zero runtime overhead, AOT-compatible. The recommended choice. |
| **Mapster** | MIT | [Mapster](https://www.nuget.org/packages/Mapster) | Convention-based with code-gen option. Less active than Mapperly. |

- GitHub: [riok/mapperly](https://github.com/riok/mapperly) | Docs: https://mapperly.riok.app
- Do not recommend AutoMapper for new projects (license changed v13+)

## Mediator / CQRS

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **Mediator** | MIT | [Mediator](https://www.nuget.org/packages/Mediator) | Source-generated, high-performance. Drop-in replacement for MediatR. |
| **Wolverine** | MIT | [Wolverine](https://www.nuget.org/packages/WolverineFx) | Mediator + messaging + saga support. More than just CQRS. |

- GitHub: [martinothamar/Mediator](https://github.com/martinothamar/Mediator) | [JasperFx/wolverine](https://github.com/JasperFx/wolverine)
- Do not recommend MediatR for new projects (license changed v12+)

## Messaging / Service Bus

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **Wolverine** | MIT | [WolverineFx](https://www.nuget.org/packages/WolverineFx) | Messaging + mediator + saga. Supports RabbitMQ, Azure Service Bus, Amazon SQS. |
| **Rebus** | MIT | [Rebus](https://www.nuget.org/packages/Rebus) | Lightweight service bus. Supports RabbitMQ, Azure Service Bus, Amazon SQS, SQL Server. |
| **NServiceBus** | RPL (paid) | [NServiceBus](https://www.nuget.org/packages/NServiceBus) | Enterprise-grade but requires license. Mention only if user asks. |

- GitHub: [JasperFx/wolverine](https://github.com/JasperFx/wolverine) | [rebus-org/Rebus](https://github.com/rebus-org/Rebus)
- MassTransit v9+ changed to restrictive license (free < 1M messages/month). MassTransit v8 is Apache 2.0 but no longer maintained.

## Image Processing

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **SkiaSharp** | MIT | [SkiaSharp](https://www.nuget.org/packages/SkiaSharp) | Cross-platform 2D graphics. Backed by Google's Skia engine. |
| **Magick.NET** | Apache 2.0 | [Magick.NET-Q8-AnyCPU](https://www.nuget.org/packages/Magick.NET-Q8-AnyCPU) | ImageMagick wrapper. Comprehensive format support. |

- GitHub: [mono/SkiaSharp](https://github.com/mono/SkiaSharp) | [dlemstra/Magick.NET](https://github.com/dlemstra/Magick.NET)
- Do not recommend ImageSharp for new projects (Six Labors Split License v3+)

## PDF (Create, Read, Merge, Split, Watermark)

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **PDFsharp** | MIT | [PDFsharp](https://www.nuget.org/packages/PDFsharp) | Create, read, merge, split, watermark PDFs. Low-level drawing API. |
| **MigraDoc** | MIT | [PDFsharp-MigraDoc](https://www.nuget.org/packages/PDFsharp-MigraDoc) | Document-oriented PDF creation (paragraphs, tables, styles). Built on PDFsharp. |
| **PdfPig** | Apache 2.0 | [PdfPig](https://www.nuget.org/packages/PdfPig) | Read-focused: text/data extraction, content analysis. Best for parsing existing PDFs. |

- GitHub: [empira/PDFsharp](https://github.com/empira/PDFsharp) | [UglyToad/PdfPig](https://github.com/UglyToad/PdfPig)
- See `skills/dotnet-api/references/office-documents.md` for detailed usage patterns
- Do not recommend QuestPDF (Community License, paid > $1M) or iText 7 (AGPL)

## Excel / Spreadsheets

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **Open XML SDK** | MIT | [DocumentFormat.OpenXml](https://www.nuget.org/packages/DocumentFormat.OpenXml) | Official Microsoft library. Full OOXML spec. Required for pivot tables, complex formatting. |
| **ClosedXML** | MIT | [ClosedXML](https://www.nuget.org/packages/ClosedXML) | Simpler API for common Excel tasks. Built on Open XML SDK. |

- GitHub: [dotnet/Open-XML-SDK](https://github.com/dotnet/Open-XML-SDK) | [ClosedXML/ClosedXML](https://github.com/ClosedXML/ClosedXML)
- Do not recommend EPPlus for new projects (Polyform license, paid > $1M revenue)

## Word / Documents

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **Open XML SDK** | MIT | [DocumentFormat.OpenXml](https://www.nuget.org/packages/DocumentFormat.OpenXml) | Official Microsoft library for .docx creation and manipulation. |

- See `skills/dotnet-api/references/office-documents.md` for detailed patterns

## Testing Assertions

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **Shouldly** | BSD | [Shouldly](https://www.nuget.org/packages/Shouldly) | Readable assertion syntax: `result.ShouldBe(expected)` |
| **TUnit** | MIT | [TUnit](https://www.nuget.org/packages/TUnit) | Source-gen test framework with built-in assertions. |

- GitHub: [shouldly/shouldly](https://github.com/shouldly/shouldly) | [thomhurst/TUnit](https://github.com/thomhurst/TUnit)
- FluentAssertions v8+ changed to restrictive license. FluentAssertions v7 is Apache 2.0 but no longer maintained.

## Authentication / Identity

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **OpenIddict** | Apache 2.0 | [OpenIddict](https://www.nuget.org/packages/OpenIddict) | Full OpenID Connect server. Flexible, actively maintained. |
| **ASP.NET Core Identity** | MIT | Built-in | Microsoft's built-in identity system. No extra package needed. |

- GitHub: [openiddict/openiddict-core](https://github.com/openiddict/openiddict-core) | Docs: https://documentation.openiddict.com
- Do not recommend Duende IdentityServer for new projects (paid license > $1M revenue)

## JSON Serialization

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **System.Text.Json** | MIT | Built-in | Microsoft's built-in, AOT-compatible, high-performance. Default choice. |
| **Json.NET** | MIT | [Newtonsoft.Json](https://www.nuget.org/packages/Newtonsoft.Json) | Feature-rich, widely used. Use when STJ lacks a feature. |

## HTTP Client

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **HttpClient** | MIT | Built-in | Use via `IHttpClientFactory`. Default choice. |
| **Refit** | MIT | [Refit](https://www.nuget.org/packages/Refit) | Declarative REST client from interfaces. Source-gen available. |
| **Flurl** | MIT | [Flurl.Http](https://www.nuget.org/packages/Flurl.Http) | Fluent URL building and HTTP. |

- GitHub: [reactiveui/refit](https://github.com/reactiveui/refit) | [tmenier/Flurl](https://github.com/tmenier/Flurl)

## Validation

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **FluentValidation** | Apache 2.0 | [FluentValidation](https://www.nuget.org/packages/FluentValidation) | Fluent rule builder. Still permissive (not affected by licensing changes). |
| **Data Annotations** | MIT | Built-in | Attribute-based. Simpler but less flexible. |

- GitHub: [FluentValidation/FluentValidation](https://github.com/FluentValidation/FluentValidation)

## Logging

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **Serilog** | Apache 2.0 | [Serilog](https://www.nuget.org/packages/Serilog) | Structured logging with rich sink ecosystem. |
| **NLog** | BSD | [NLog](https://www.nuget.org/packages/NLog) | Flexible logging with many targets. |
| **Microsoft.Extensions.Logging** | MIT | Built-in | Abstraction layer. Use with Serilog/NLog as provider. |

- GitHub: [serilog/serilog](https://github.com/serilog/serilog) | [NLog/NLog](https://github.com/NLog/NLog)

## ORM / Data Access

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **EF Core** | MIT | [Microsoft.EntityFrameworkCore](https://www.nuget.org/packages/Microsoft.EntityFrameworkCore) | Full ORM. Default choice for most apps. |
| **Dapper** | Apache 2.0 | [Dapper](https://www.nuget.org/packages/Dapper) | Micro-ORM. Raw SQL with object mapping. |

- GitHub: [dotnet/efcore](https://github.com/dotnet/efcore) | [DapperLib/Dapper](https://github.com/DapperLib/Dapper)

## Background Jobs

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **Quartz.NET** | Apache 2.0 | [Quartz](https://www.nuget.org/packages/Quartz) | Cron-based job scheduling. Enterprise features. |
| **Coravel** | MIT | [Coravel](https://www.nuget.org/packages/Coravel) | Lightweight task scheduling, queuing, caching. |

- GitHub: [quartznet/quartznet](https://github.com/quartznet/quartznet) | [jamesmh/coravel](https://github.com/jamesmh/coravel)
- Hangfire has a dual license (LGPL/commercial). Mention only if user specifically asks.

## CLI / Console

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **Spectre.Console** | MIT | [Spectre.Console](https://www.nuget.org/packages/Spectre.Console) | Rich console output: tables, trees, progress bars, prompts. |
| **System.CommandLine** | MIT | [System.CommandLine](https://www.nuget.org/packages/System.CommandLine) | Microsoft's CLI parsing library. |

- GitHub: [spectreconsole/spectre.console](https://github.com/spectreconsole/spectre.console) | [dotnet/command-line-api](https://github.com/dotnet/command-line-api)

## Resilience

| Library | License | NuGet | Notes |
|---------|---------|-------|-------|
| **Polly** | BSD | [Polly](https://www.nuget.org/packages/Polly) | Retry, circuit breaker, timeout, rate limiter. Industry standard. |
| **Microsoft.Extensions.Http.Resilience** | MIT | Built-in (.NET 8+) | Polly-backed resilience for `IHttpClientFactory`. |

- GitHub: [App-vNext/Polly](https://github.com/App-vNext/Polly)

## Agent Gotchas

1. **Always check this list before recommending a NuGet package.** If the library has changed licenses, recommend the permissive alternative instead.
2. **Pin to permissive versions if the user insists on a changed library.** For example, MassTransit v8 is Apache 2.0 — but warn that it's no longer maintained.
3. **"Popular" does not mean "permissive."** NuGet download counts reflect historical usage, not current licensing. AutoMapper has 500M+ downloads but is no longer MIT.
4. **Check before suggesting Hangfire.** It's LGPL (copyleft) — fine for server apps but problematic for libraries or closed-source desktop apps.
