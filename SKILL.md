---
name: report-development
description: Produce a complete, immediately runnable report JSON for a compatible reportAPI host. Use verified query contracts, fieldName identifiers, honest aggregation and the bundled validator; never push API plumbing or field mapping to end users.
---
# Portable Report Development, v4 candidate (creation, iteration and UI Kit)

## Non-negotiable acceptance test
Create **one self-contained, importable JSON** report that opens and queries without asking its end user to paste request JSON, map API field names, choose SDK methods, or supply tokens. Normal *business filters* (date, brand, grouping) are welcome. Never confuse `showName` (display label) with `fieldName` (machine identifier).

Read in order:
1. `references/report-package.md` and `references/report-sdk.md` for runtime contracts.
2. `references/query-contracts.md` for **complete ready-to-call parameters**; do not substitute placeholders in final report code.
3. `references/field-catalog.md` and `references/quality-rules.md` for approved fields, semantics, completeness and nulls.
4. `examples/brand-advertising-efficiency.json` for an actual, complete report; adapt it rather than constructing request plumbing from scratch.
5. `references/report-requirements.md` for the user-facing release gate.
6. **For a v0.5.1+ UI Kit target**, read `references/report-ui-kit.md` and its complete working example `examples/uikit-brand-sales.json`. Do not use UI Kit on older hosts.
7. **For editing an existing report**, `references/report-iteration.md` for identity, versioning, regression and full-output rules.

## Choose the task mode first
- **CREATE:** No original report supplied. Generate a new stable `id`, a complete importable JSON object, `schemaVersion: 1`, and `reportVersion: "1.0.0"`. For this experimental runtime, keep the legacy `version` field at the already supported numeric value (typically `2` for SDK-enabled reports), never use it for the report revision.
- **UPDATE:** The user supplies an existing report JSON. **Treat that JSON as the baseline**. Keep its `id` byte-for-byte unchanged, preserve `schemaVersion` and legacy `version`, increment `reportVersion` (SemVer), and return the **whole JSON package**, not a patch. Preserve unrequested behavior, data selection, error states, style intent and permissions unless a new feature requires a documented permission. Read `references/report-iteration.md` before editing.
- **RESTORE:** Do not silently generate a new higher-version report just to roll back; use the host's History/Restore feature when available.

## Procedure
1. Map requested measures and dimensions to verified `fieldName` identifiers in the approved catalog. If the required field is absent, use host metadata discovery **inside the report**, or explicitly state it cannot be completed: do **not** show users a technical configuration form as a fallback.
2. Implement a full report package with `id,name,version,schemaVersion,reportVersion,permissions,html,css,js` in v0.4-compatible JSON. On UPDATE, preserve identity and pre-existing functions. Include default dates and controls usable by the end user.
3. Prefer `reportUI.chart()` and `reportUI.table()` for visualizations when target runtime supports UI Kit 1.1; retain flexibility to use standalone HTML/CSS and SVG. Table is presentation-only with no built-in sorting/filtering/pagination. Use only `reportAPI` for data access. No raw URLs, auth tokens, page DOM access or unrelated network calls. Ensure declared `permissions` cover SDK calls.
4. The UI Kit `dataBar` scales to supplied rows only, not to the total dataset; do not imply otherwise. Use `queryTotal()` for scope-wide KPIs. For `queryTable()` multi-page stats, fetch all pages or label outputs clearly as page-only. ROAS = sum(sales)/sum(spend), never mean(row ROAS); null is not zero.
5. Make loading/empty/error states obvious, prevent duplicate concurrent submissions and ensure dates and charts display clearly.
6. Run `python scripts/validate_report.py YOUR_REPORT.json`; fix errors and investigate warnings. Verify in a permitted running host. Never assert live testing if it did not occur.

## Output
Provide **the finished JSON file**, not an HTML draft or an input form to configure SDK internals. For updates, summarize what changed and what was deliberately preserved; verify identity and version fields against the supplied baseline. Summarize metric scope and any assumptions. No need to show code unless requested.

## Publication boundary
This is a release candidate, not automatically authorized for public sharing. Verified product-facing identifiers and query shapes in these materials still need organizational disclosure review. Authentication, raw backend URLs and customer records are intentionally excluded. This Skill does not confer data-access permission or prove runtime code safe.
