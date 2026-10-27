# Definition of Done: immediately runnable report

Block release when:
- user must paste `queryTable` / `queryChart` request JSON or API endpoint;
- user must type machine field identifiers, SDK method names, page numbers or authorization values to run;
- report uses `showName` strings as data property keys;
- report asks for a token or reads browser auth data;
- only one page is used to assert an unqualified grand total;
- an API response error leaves the screen blank with no explanation.

Allowed user controls are meaningful domain interactions, such as date range, brand, product, metric selector, visualization preferences and an optional page-size setting for an *explicitly* page-scoped table. Avoid magic default values such as a fixed historical date range in a long-lived report; initialize a recent valid range.

SDK specs in `query-contracts.md` are **developer-side** inputs. The user never needs to see or edit them. Prefer simple, conventional UI, legible labels, horizontal responsive layout and visible date axes/tooltips.

A validator's success only checks basic compatibility, not business accuracy, CORS, permissions, dynamic code safety or comprehensive datasets.

## Additional acceptance requirements for report updates

- Source report JSON supplied and read in full; preserve same stable `id`.
- Preserve all existing features unless explicitly changed, including filters and metric scope.
- Keep legacy `version`/`schemaVersion` separate from `reportVersion`.
- Output complete updated JSON; summarize the diff, tests and any unverified behavior.


## UI Kit report acceptance (only when host supports UI Kit 1.1)
- Charts and tables use the runtime-provided `reportUI`, not embedded third-party scripts or CDNs.
- A native table never implies sorting, filtering or paging; business controls, if needed, must query the backend.
- A visible incomplete-page warning is required whenever a result is partial and derived totals only cover those returned rows.
- ECharts dependency state is surfaced when unavailable.
