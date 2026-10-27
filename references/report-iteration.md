# Report iteration contract (Runtime v0.4.0 profile)

This file governs **modification of an existing report**, rather than creating a new report from a prompt. The baseline is the **complete previously exported report JSON**, provided to the AI by the user; the public Skill does not have access to the user's locally saved reports.

## Identity and versions

| Property | Purpose | On UPDATE |
|---|---|---|
| `id` | Stable report identity and host lookup key | **Preserve exactly**. The host uses matching IDs to offer Update vs Save as new. |
| `schemaVersion` | Package schema compatibility | Preserve the existing value, if present. The v0.4 validator supports `1`. |
| `version` | Legacy host compatibility marker | **Preserve its value**, commonly numeric `2`. Never use it to indicate feature revisions. |
| `reportVersion` | Human-readable SemVer revision | Increment, e.g. `1.0.0` → `1.1.0`. Introduce it when missing. |
| `name` | Visible report title | Preserve unless user requests a rename. |

When introducing `reportVersion` into a legacy report with only numeric `version`, select an initial SemVer baseline such as `1.0.0` and explain the choice. Never silently overwrite the original `id`. No implicit guarantee that the host enforces SemVer ordering: it currently prompts for an action when IDs match, and keeps a local history.

Suggested SemVer convention: patch for fixes or polish; minor for additive backwards-compatible features; major for intentional breaking changes. The choice is report-author metadata and does not alter runtime SDK compatibility.

## Edit workflow (must follow in order)

1. Read the provided source JSON in full and validate/parse it. If only a screenshot is supplied, **request the exported JSON** or explicitly say accurate preservation cannot be guaranteed.
2. Produce an inventory of its controls, fields, query methods, permissions, data semantics, loading/empty/error behavior, layout and chart behavior.
3. Translate the user's change request into a bounded edit plan. Keep unrelated behavior unchanged; never invent new business metrics or change date/brand defaults without a request.
4. Implement edits within `html`, `css` and `js`, while preserving working SDK contracts. Ensure new controls are wired to real state, and avoid accidental duplicate event handlers, queries, or altered query scope.
5. Keep data access exclusively through `reportAPI`. Check new permissions against documented methods. Do not embed a token, raw backend URL, or auth logic.
6. Validate the resulting JSON and compare it against the baseline with the bundled iteration check (command below). Fix errors. Review warnings, including lost controls, missing SDK methods and unexpected permission changes.
7. Output the **entire updated JSON** as a downloadable/importable artifact. Describe changed features, retained features, new permissions and tests performed; distinguish static validation from live browser verification.

## Validation

```bash
python scripts/validate_report.py edited.json
python scripts/check_report_update.py previous.json edited.json
```

The second tool checks stable ID, schema/legacy version compatibility, reportVersion progression, and surfaces potential regressions. It is a **heuristic check**, not semantic equivalence proof. Never claim that static validation proves unchanged UX.

## Runtime import lifecycle

On matching `id`, the v0.4.0 host offers **Update current (save previous to History)**, **Save as new report**, or **Skip**. History retains up to 10 prior full snapshots for each ID. Updating a report is not the same as loading it into the page: the user may need to click Load again. Backup export may not include version history. Do not assume a host will always select Update or automatically deploy the new version.

## Never do this

- Generate a new `id` while describing the output as an update.
- Change `version` to `"1.1.0"` when legacy numeric `2` is expected; use `reportVersion` instead.
- Return only the edited `js` string, code fragments, unified diff, or an unimportable object.
- Drop a pre-existing brand filter, table, KPI or tooltip as collateral damage.
- Treat a changed test account's missing advertising data as a regression without verifying the data scope.
