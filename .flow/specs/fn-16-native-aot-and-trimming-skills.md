# fn-16: Native AOT and Trimming Skills

## Problem/Goal
Add comprehensive Native AOT and trimming skills covering full pipeline, AOT-friendly architecture patterns, and WebAssembly AOT compilation. Enable agents to architect applications for AOT from the start.

## Acceptance Checks
- [ ] `dotnet-native-aot` skill covers full AOT pipeline (trimming, RD.xml, reflection-free patterns, p/invoke, size optimization)
- [ ] `dotnet-aot-architecture` skill covers AOT-first design (source gen over reflection, DI patterns, serialization choices)
- [ ] `dotnet-trimming` skill covers trim-safe development (annotations, linker config, testing trimmed output, fixing warnings)
- [ ] `dotnet-aot-wasm` skill covers WebAssembly AOT for Blazor WASM and Uno WASM
- [ ] Cross-references to serialization, source generators, CLI tools, performance skills

## Key Context
- AOT-friendly patterns must be architecture-level decisions, not afterthoughts
- Source generators are foundational for AOT compatibility
- .NET 10 ASP.NET Core has major AOT improvements
- WASM AOT benefits from .NET 11 CoreCLR on WebAssembly
