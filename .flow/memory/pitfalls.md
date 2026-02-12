# Pitfalls

Lessons learned from NEEDS_WORK feedback. Things models tend to miss.

<!-- Entries added automatically by hooks or manually via `flowctl memory add` -->

## 2026-02-12 manual [pitfall]
When spec requires [skill:name] cross-reference syntax, use it for ALL skill references (catalog entries, routing targets, etc.) -- not just the first few. Bare text skill names are not machine-parseable.

## 2026-02-12 manual [pitfall]
.NET STS lifecycle is 18 months from GA (not 12). If GA Nov 2026, STS end is ~May 2028. Always calculate from actual GA date, not release year.

## 2026-02-12 manual [pitfall]
NuGet/MSBuild config files (Directory.Packages.props, nuget.config) resolve hierarchically upward, not just at solution root. Always instruct upward search for monorepo compatibility.

## 2026-02-12 manual [pitfall]
When documenting TFM patterns for platform detection (MAUI, Uno), use version-agnostic globs (net*-android) not hardcoded versions (net10.0-android) to avoid false negatives on older/newer TFMs.
