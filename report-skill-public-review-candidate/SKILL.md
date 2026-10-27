---
name: report-development
description: Create and validate portable custom analytics reports using a host-provided reportAPI and an importable JSON report format.
---
# Portable Report Development

Use this skill to create **one JSON report artifact** compatible with the documented report host. It describes the **public development contract**, not any private company's backend or account access.

## Workflow
1. Read `references/report-package.md`, `references/report-sdk.md`, and `references/quality-rules.md`.
2. Discover available datasets, fields, and dimensions using `reportAPI.getDataSets()` **at report runtime**; do not guess private identifiers. The AI author must obtain an approved schema or use dynamic discovery before naming fields.
3. Produce an importable JSON object containing `id`, `name`, `version`, `permissions`, `html`, `css`, and `js`.
4. Render only in the host-provided `root` and access data only via `reportAPI`. Handle loading, empty, error, and partial states. Do not access parent page, browser credentials, raw HTTP endpoints, or unrelated websites.
5. Run `python scripts/validate_report.py PATH_TO_REPORT.json`. Correct errors; review warnings as heuristics.
6. Test the report in an **authorized** compatible host. Confirm calculations, pagination and expected results against authoritative sources.

## Output
Return a JSON file the host can import, plus a brief explanation of analytical scope, assumptions, permissions, and tests. Do not assume a model reading this URL has tools to execute tests or access a backend.

## Boundaries
This package does **not** provide a live data connector, credentials, secrets, deployment endpoints, or permission to access a service. The host enforces authorized data access. Static validation is not a security audit. Do not execute reports from untrusted parties without host-side isolation, policy checks and review.

## References
- `references/report-package.md`: portable import format
- `references/report-sdk.md`: abstract SDK methods and response shapes
- `references/quality-rules.md`: data correctness and visualization guidance
- `examples/dataset-discovery.json`: runnable metadata explorer with no hardcoded dataset names
- `scripts/validate_report.py`: static validator
