# Decisions

Architectural choices with rationale. Why we chose X over Y.

<!-- Entries added manually via `flowctl memory add` -->

## 2026-02-17 manual [decision]
Hand-authored YAML configuration files require CI validation rules (parse checks) added to workflows; acceptance criteria must specify WHERE validation occurs, not just WHAT to validate

## 2026-02-20 manual [decision]
CI baseline regression gates must handle schema evolution: new entries absent from the baseline ref should be treated as 'new coverage' (no regression comparison), not hard failures, to avoid deadlocking normal case addition.
