# Report UI Kit v1.1 contract (Custom Reports Lab extension v0.5.1)

This is an **optional UI convenience layer** in the report sandbox. It does not change the `reportAPI` query contracts. In a compatible v0.5.1 host the report JS receives `root`, `reportAPI`, and `reportUI`. Before relying on UI Kit, target that host version; do not assume it is available on v0.4.0 and earlier. Preserve old report presentation on UPDATE unless specifically requested to migrate it.

## Source-verified API

- `reportUI.version` is `'1.1.0'`.
- `reportUI.features`: `{echarts: boolean, nativeTable: true}`. ECharts must be installed locally in the extension `vendor` directory. If ECharts is absent, `chart()` throws.
- `reportUI.chart(elementOrSelector, {type, data, x, y, horizontal?, rotateLabels?, smooth?, option?})`. `type` is `bar`, `line`, `area`, `pie` or `donut`. `data` is an array of records; `x` selects the category/label field; `y` can be one field name or an array of field names (multiple series for cartesian charts). `option` merges a supplied ECharts option object shallowly over defaults, so replacing a nested object requires providing the complete nested setting.
- `reportUI.table(elementOrSelector, {data, columns, compact?, label?, emptyText?})` renders exactly the provided rows. `columns` can be field-name strings or objects `{field,title,format?,decimals?,visual?,align?,width?,visible?}`. `format`: `number`, `currency`, `percent`, `ratio`; `visual:'dataBar'` creates an inline bar normalized to the maximum **within the supplied rows**. Nulls show `—`. `percent` appends `%` without multiplying by 100; ensure source units are appropriate. Values are placed via `textContent`, not HTML.
- `chart()` and `table()` return controllers with `.update(rows)` and `.dispose()`; `reportUI.dispose(elementOrSelector)` and `reportUI.disposeAll()` also exist. `chart().update(rows)` rebuilds that chart and disposes the old one; do not retain the earlier controller for later operations after updating.

## AI authoring requirements

1. Create `<div id="chart" class="cr-chart"></div>` and `<div id="table" class="cr-table"></div>` inside the package's `html`. The provided host stylesheet styles these classes. Use scoped selectors with `root.querySelector` for report-owned elements. Note that `reportUI` accepts CSS selectors and resolves them against the sandbox document; unique IDs are preferred.
2. Query business data with `reportAPI`, then pass data rows into `reportUI`. UI Kit does not fetch data and does not implicitly grant permissions. Keep `permissions` appropriate to the SDK methods used.
3. **No built-in table sorting, filtering or pagination**. If user requests these, create separate business controls and issue supported backend `reportAPI.queryTable()` calls. Do not sort only the first backend page and label it a global ranking.
4. Scope KPI totals correctly. A table page is not a full population; use `queryTotal()` where appropriate, or label returned-row-only results explicitly. Never infer total row counts from `hasNextPage`.
5. No reliance on Tabulator or Grid.js. Tabulator-specific options (`headerFilter`, `sorter`, `pagination`, custom `formatter` callbacks) are not implemented.
6. Handle loading, empty/error states, date changes and chart/table redraw. For update of an existing report, keep its ID and all unrelated functionality unchanged. Validate the exported JSON before delivery.
7. Do not insert ECharts scripts, vendor assets, remote CDN URLs, authentication tokens or raw API endpoints into a report JSON. The host owns the locally installed ECharts library and table renderer.

## Ready-to-copy JavaScript pattern

```js
const $ = selector => root.querySelector(selector);
async function refresh() {
  const response = await reportAPI.queryTable({
    /* Paste a complete request following references/query-contracts.md; no placeholders in delivered JSON */
  });
  const rows = response.list || [];
  reportUI.chart($('#chart'), { type: 'bar', data: rows, x: 'brandName', y: 'adSalesAmount' });
  reportUI.table($('#table'), { data: rows, columns: [
    { field:'brandName', title:'Brand' },
    { field:'adSalesAmount', title:'Ad Sales', format:'currency', visual:'dataBar' },
    { field:'adRoas', title:'ROAS', format:'ratio' }
  ] });
}
```

The code above is a usage snippet, **not** a full importable report; use `examples/uikit-brand-sales.json` as the complete reference package. The sample's KPI explicitly covers returned rows rather than whole-population totals.

## Runtime availability check

If the target host does not provide `reportUI` or `reportUI.features.nativeTable`, do not generate a report that requires UI Kit. Ask for a compatible runtime or use the older plain HTML/SVG approach. For reports that require ECharts, check `reportUI.features.echarts` and display a clear diagnostic instead of silently failing.

## Compatibility and performance

Native table generates DOM for all rows passed and does not offer virtual scrolling. Fetch only the rows needed for the current display. Use host data paging at query level for large datasets. The present UI Kit profile has no backend-paged table adapter; do not invent one.
