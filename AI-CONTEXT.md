# AI Context: Portable Report Development Skill

> Consolidated single-file version of the Skill, contracts, field catalog, quality requirements and examples. Read this full document before generating any report. This is a review candidate requiring company approval for public disclosure.

**Source of truth:** this file is generated from the repository sources using `python scripts/generate_ai_context.py`; do not hand-edit the generated file. For Agent Skills installers, use `SKILL.md`.

**If a section is truncated or absent:** fetch the corresponding source link in `AI-ENTRY.md` or disclose the limitation; never fabricate missing contract details.


---

## Source: SKILL.md (Skill instructions)

Source URL: https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/SKILL.md

---
name: report-development
description: Produce a complete, immediately runnable report JSON for a compatible reportAPI host. Use verified query contracts, fieldName identifiers, honest aggregation and the bundled validator; never push API plumbing or field mapping to end users.
---
# Portable Report Development, v3 candidate (creation and iteration)

## Non-negotiable acceptance test
Create **one self-contained, importable JSON** report that opens and queries without asking its end user to paste request JSON, map API field names, choose SDK methods, or supply tokens. Normal *business filters* (date, brand, grouping) are welcome. Never confuse `showName` (display label) with `fieldName` (machine identifier).

Read in order:
1. `references/report-package.md` and `references/report-sdk.md` for runtime contracts.
2. `references/query-contracts.md` for **complete ready-to-call parameters**; do not substitute placeholders in final report code.
3. `references/field-catalog.md` and `references/quality-rules.md` for approved fields, semantics, completeness and nulls.
4. `examples/brand-advertising-efficiency.json` for an actual, complete report; adapt it rather than constructing request plumbing from scratch.
5. `references/report-requirements.md` for the user-facing release gate.
6. **For editing an existing report**, `references/report-iteration.md` for identity, versioning, regression and full-output rules.

## Choose the task mode first
- **CREATE:** No original report supplied. Generate a new stable `id`, a complete importable JSON object, `schemaVersion: 1`, and `reportVersion: "1.0.0"`. For this experimental runtime, keep the legacy `version` field at the already supported numeric value (typically `2` for SDK-enabled reports), never use it for the report revision.
- **UPDATE:** The user supplies an existing report JSON. **Treat that JSON as the baseline**. Keep its `id` byte-for-byte unchanged, preserve `schemaVersion` and legacy `version`, increment `reportVersion` (SemVer), and return the **whole JSON package**, not a patch. Preserve unrequested behavior, data selection, error states, style intent and permissions unless a new feature requires a documented permission. Read `references/report-iteration.md` before editing.
- **RESTORE:** Do not silently generate a new higher-version report just to roll back; use the host's History/Restore feature when available.

## Procedure
1. Map requested measures and dimensions to verified `fieldName` identifiers in the approved catalog. If the required field is absent, use host metadata discovery **inside the report**, or explicitly state it cannot be completed: do **not** show users a technical configuration form as a fallback.
2. Implement a full report package with `id,name,version,schemaVersion,reportVersion,permissions,html,css,js` in v0.4-compatible JSON. On UPDATE, preserve identity and pre-existing functions. Include default dates and controls usable by the end user.
3. Use only `reportAPI` for data access. No raw URLs, auth tokens, page DOM access or unrelated network calls. Ensure declared `permissions` cover SDK calls.
4. Use `queryTotal()` for scope-wide KPIs. For `queryTable()` multi-page stats, fetch all pages or label outputs clearly as page-only. ROAS = sum(sales)/sum(spend), never mean(row ROAS); null is not zero.
5. Make loading/empty/error states obvious, prevent duplicate concurrent submissions and ensure dates and charts display clearly.
6. Run `python scripts/validate_report.py YOUR_REPORT.json`; fix errors and investigate warnings. Verify in a permitted running host. Never assert live testing if it did not occur.

## Output
Provide **the finished JSON file**, not an HTML draft or an input form to configure SDK internals. For updates, summarize what changed and what was deliberately preserved; verify identity and version fields against the supplied baseline. Summarize metric scope and any assumptions. No need to show code unless requested.

## Publication boundary
This is a release candidate, not automatically authorized for public sharing. Verified product-facing identifiers and query shapes in these materials still need organizational disclosure review. Authentication, raw backend URLs and customer records are intentionally excluded. This Skill does not confer data-access permission or prove runtime code safe.

---

## Source: references/report-package.md (Report package contract)

Source URL: https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/report-package.md

# Report package contract (public profile v1)

One JSON object (or an array of objects for batch import):

```json
{"id":"example_report","name":"Example report","version":1,"permissions":["datasets"],"html":"<div class=\"viewer\"></div>","css":".viewer { padding: 12px; }","js":"root.querySelector('.viewer').textContent = 'Ready';"}
```

Required: `id` (ASCII letters/digits/underscore/dash, 1-80 chars), `name` (1-140 chars), `html`, `css`, `js` strings. Optional: `version` (string or number), `permissions` (list of SDK capability strings). Keep serialized package under 500,000 characters. `html` is rendered beneath a host-provided root element; `css` styles the report; `js` is evaluated by the host with `root` and `reportAPI` bindings. Avoid global selectors, third-party scripts, and direct URL requests.

The current compatibility profile is based on an experimental runtime and is **not an official public API guarantee**. Consumers should verify against their installed runtime. The `permissions` field documents requested capabilities; actual authorization is controlled by the host.

## Versioned authoring profile (v0.4.0)

For new reports, prefer `"schemaVersion":1, "version":2, "reportVersion":"1.0.0"`; `version` remains a legacy compatibility marker while `reportVersion` describes human-visible revisions. On edits, keep the original `id` and existing schema/legacy versions. Refer to `references/report-iteration.md`.

---

## Source: references/report-sdk.md (Report SDK)

Source URL: https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/report-sdk.md

# Report SDK (abstract host interface)

The host injects an asynchronous `reportAPI` object into report JavaScript. A report must not implement authentication, fetch raw endpoints or read credentials.

| Method | Resolution payload | Capability |
|---|---|---|
| `queryTable(params)` | `{list: [...], hasNextPage, ...}` | `table` |
| `queryChart(params)` | `{xAxis: [...], data: {metric: [...]}}` | `chart` |
| `queryTotal(params)` | `{metric: value, metricCompare, metricRate, ...}` | `total` |
| `getDataSets()` | array of metadata objects | `datasets` |
| `getBrands()` | array of strings | `brands` |
| `getAlertLabels()` | array of `{labelId, labelName, labelDesc, sentiment}` | `alertLabels` |
| `query(source, params)` | source-dependent | corresponding source |

These methods return the payload data, not a transport envelope. Supported dataset IDs, parameters, field names and permissions depend on the **deployed host**. Consult host-authorized metadata at runtime; do not infer field names from documentation examples. For queries requiring dates, dimensions, filters or paging, use the host's approved parameter contract. An API field being listed in metadata does not prove every query combination is supported.

## Safe use example

```js
const datasets = await reportAPI.getDataSets();
const names = datasets.map(x => String(x.dataSet ?? 'Unnamed'));
root.querySelector('[data-datasets]').textContent = names.join(', ');
```

Private URLs, header names, token acquisition, account identifiers, backend service details and real customer data are intentionally absent.

---

## Source: references/query-contracts.md (Full query contracts)

Source URL: https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/query-contracts.md

# Verified query patterns for the experimental v0.3 reportAPI host

The host SDK returns the **data payload**, not the `{code,data,msg}` envelope. Full query parameters below are observed from authorized Data Center query examples and one functioning sample. Query support varies by dataset and deployment. These values are not secret but **must be approved for public disclosure**.

## Full base context (copy this, then override values)

```js
const base = {
  dataSet: 'OmniMetrics',
  startDate: '2026-10-01', endDate: '2026-10-24',
  dateDimension: 'Period',
  aggregations: ['brandName'], groupBys: [],
  filters: {
    customBrandName: [], customCategory: [], brandName: [], category: [],
    promotionStatus: [], currentBadges: [], labels: [], historyLabels: []
  },
  columnGroupTypes: ['Advertising','ChannelSales','Inventory','OnlineOrganicSales','OnlineSales','OverallSales','StoreSales'],
  uniqueTimeZone: 8,
  isShowCompare: false
};
```

Date literals are examples only; set dates from real report controls. `uniqueTimeZone` is an environment-specific example (do **not** assume 8 applies worldwide). Only request dataset/aggregation/filters that the host authorizes.

## Table: brand ranking, paginated
```js
const result = await reportAPI.queryTable({
  ...base, pageNum: 1, pageSize: 100,
  orderBys: { orderBy: 'adSalesAmount', orderType: 'descending' }
});
const rows = result.list || [];
const more = result.hasNextPage === true;
```
If more is true, either request further pages or make the UI explicit that rankings/totals are partial. Do not silently sum the first page as an all-brand total. The example report demonstrates **page-scoped** computation.

## Total: comprehensive KPI under filter context
```js
const totals = await reportAPI.queryTotal({
  ...base, aggregations: ['productId']
});
const sales = totals.adSalesAmount;
const spend = totals.adSpend;
const roas = totals.adRoas;
```
`queryTotal` produces a metric object. Some comparison metrics are null.

## Chart: dated series
```js
const chart = await reportAPI.queryChart({
  ...base, aggregations: ['productId'], dimension: 'Daily'
});
const points = (chart.xAxis || []).map((date,i)=>({
  date, value: chart.data?.adSalesAmount?.[i] ?? null
}));
```
Preserve gaps; label date and numeric axes. `dimension` is chart timescale distinct from `dateDimension`.

## Metadata and lists
```js
const datasets = await reportAPI.getDataSets();
const options = await reportAPI.getBrands();
const labels = await reportAPI.getAlertLabels();
```
`getDataSets` exposes entries with `dataSet`, `aggregations`, `columns`, `filters`, `dateAggregation`, `summaryAggregations`, and `summaryColumns`. Each column object carries `fieldName` (for queries) and `showName` (for labels). Brand list is string[]. Alert label objects have `labelId`, `labelName`, `labelDesc`, `sentiment`. Label IDs can encode **display priority**, but priority direction must be supplied by the host, not guessed.

## Failure states
Try/catch SDK requests and show an understandable error. Keep permissions explicit: table/chart/total/datasets/brands/alertLabels. Do not expose raw request bodies as user-editable UI.

---

## Source: references/field-catalog.md (Verified field catalog)

Source URL: https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/field-catalog.md

# Minimum verified field catalog (requires public disclosure approval)

This is an **experimental host contract**, not a guarantee for every tenant. For `OmniMetrics` the authorized metadata and observed responses support:

| fieldName | Display label | Usage / semantic note |
|---|---|---|
| `brandName` | Brand | grouping dimension, filtering |
| `productId` | Product | grouping dimension |
| `customBrandName` | Custom Brand | grouping dimension/filter |
| `categoryName` | Category | grouping dimension |
| `overallSalesAmount` | Overall Sales Amount | additive amount across disjoint groups |
| `adSalesAmount` | Ad Sales Amount | additive monetary amount |
| `adSpend` | Ad Spend | additive monetary amount |
| `adRoas` | Ad ROAS | ratio, recompute as adSalesAmount / adSpend for group totals |
| `adAcos` | Ad ACOS | percent ratio, recompute with numerator/denominator as appropriate |
| `adClicks` | Ad Clicks | additive count |
| `adImpressions` | Ad Impressions | additive count |

Use `fieldName` in objects and property lookups. **Do not use** `Brand`, `Ad Sales Amount`, `Ad Spend` as object keys. Use the human-friendly form for screen labels only. Check current runtime's `getDataSets()` before using a dataset outside this verified subset. Access remains scoped to the authorized user and host.

---

## Source: references/quality-rules.md (Quality rules)

Source URL: https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/quality-rules.md

# Analytics and presentation quality

- Whole-range totals: use `queryTotal()` when appropriate, or retrieve **all** pages before claiming an exhaustive aggregate. If using just one page, mark the metric as page-level.
- Do not sum or take an unweighted average of ratios (e.g. ROAS, CTR). Recompute from appropriate numerator and denominator across a valid, complete scope.
- Preserve `null`/missing values; they are not equivalent to numeric `0`. Undefined denominators yield not-available output.
- Chart series: align metric arrays with `xAxis` by index. Show date labels, numeric axis units and hover details. Preserve null gaps.
- Treat comparison rate units as **host-specific** until confirmed by schema. Do not blindly multiply by 100.
- Labels: `sentiment` may represent negative (-1), neutral (0), positive (+1), unknown/null. A label ID may also encode display priority in some hosts; no universal priority direction is defined. Do not guess ordering from the ID.
- Implement loading, empty, permission-denied, request-failed and partial-result states.
- Limit request volume and return sizes. Do not log customer records or credentials.
- Validate both static contract and runtime calculations; static checks will miss business errors and cannot prove security.

---

## Source: references/report-requirements.md (Ready-to-run acceptance rules)

Source URL: https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/report-requirements.md

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

---

## Source: references/report-iteration.md (Report iteration contract)

Source URL: https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/report-iteration.md

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

---

## Source: examples/brand-advertising-efficiency.json (Working report example)

Source URL: https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/examples/brand-advertising-efficiency.json

```json
{
  "id": "brand-roas-comparison",
  "name": "Brand Advertising Efficiency",
  "version": 1,
  "permissions": [
    "table"
  ],
  "html": "<main class=\"report\"><header><h1>Brand Advertising Efficiency</h1><p>Independent report powered by Pacvue Data Bridge</p></header><section class=\"controls\"><label>From <input id=\"start\" type=\"date\" value=\"2026-09-27\"></label><label>To <input id=\"end\" type=\"date\" value=\"2026-10-24\"></label><button id=\"run\">Refresh</button></section><p id=\"status\" role=\"status\">Ready to query.</p><section class=\"cards\" id=\"cards\"></section><section class=\"chart\"><h2>ROAS by Brand</h2><p>Computed using the sum of Ad Sales divided by the sum of Ad Spend for the returned brand-level rows.</p><div id=\"bars\"></div></section><section><h2>Brand details</h2><div id=\"table\"></div></section><small id=\"notice\">This table shows the current query page only, not all matching brands if pagination continues.</small></main>",
  "css": "*{box-sizing:border-box}body{font:14px system-ui,Arial,sans-serif;color:#17233b;margin:0;background:#fff}.report{max-width:1200px;padding:24px;margin:auto}h1{font-size:23px;margin:0 0 5px}header p,.chart p{color:#64748b;font-size:12px}.controls{display:flex;gap:12px;flex-wrap:wrap;align-items:end;margin:20px 0}.controls label{font-size:12px;display:flex;flex-direction:column;gap:5px}input{border:1px solid #cbd5e1;border-radius:5px;padding:8px;max-width:150px}button{border:0;border-radius:5px;background:#2563eb;color:white;padding:10px 16px;cursor:pointer}button:disabled{opacity:.55}#status{color:#64748b;min-height:22px}.cards{display:flex;flex-wrap:wrap;gap:12px}.card{background:#f1f5f9;border-radius:8px;padding:14px;min-width:170px}.card strong{display:block;font-size:20px;margin-top:5px}.chart{margin-top:28px}.bar{display:grid;grid-template-columns:110px minmax(60px,1fr) 75px;gap:8px;align-items:center;padding:6px 0}.track{background:#eef2ff;height:21px;border-radius:4px;overflow:hidden}.fill{height:100%;background:#3b74e5}h2{font-size:17px;margin:24px 0 8px}.scroll{max-width:100%;overflow:auto}table{border-collapse:collapse;min-width:560px;width:100%}td,th{padding:10px;text-align:left;border-bottom:1px solid #e2e8f0}th{background:#f8fafc}small{display:block;margin-top:14px;color:#64748b}",
  "js": "const $=sel=>root.querySelector(sel);\nconst BASE={dataSet:'OmniMetrics',dateDimension:'Period',aggregations:['brandName'],groupBys:[],filters:{customBrandName:[],customCategory:[],brandName:[],category:[],promotionStatus:[],currentBadges:[],labels:[],historyLabels:[]},columnGroupTypes:['Advertising','ChannelSales','Inventory','OnlineOrganicSales','OnlineSales','OverallSales','StoreSales'],isShowCompare:false,uniqueTimeZone:8};\nconst money=x=>x==null?'—':Number(x).toLocaleString('en-US',{maximumFractionDigits:2});\nconst el=(tag,cl,txt)=>{const n=document.createElement(tag);if(cl)n.className=cl;if(txt!=null)n.textContent=String(txt);return n};\nfunction card(label,value){const d=el('div','card');d.append(el('span','',label),el('strong','',value));return d}\nfunction paint(rows,hasNext){\n const cards=$('#cards');cards.replaceChildren();\n const sales=rows.reduce((s,r)=>s+(Number(r.adSalesAmount)||0),0);\n const spend=rows.reduce((s,r)=>s+(Number(r.adSpend)||0),0);\n cards.append(card('Ad Sales (page)',money(sales)),card('Ad Spend (page)',money(spend)),card('Weighted ROAS (page)',spend>0?(sales/spend).toFixed(2)+'x':'—'),card('Brands (page)',String(rows.length)));\n const barRoot=$('#bars');barRoot.replaceChildren();\n const entries=rows.map(r=>({name:r.brandName||'Unspecified',roas:Number(r.adSpend)>0?Number(r.adSalesAmount||0)/Number(r.adSpend):null}));\n const max=Math.max(1,...entries.map(x=>x.roas??0));\n for(const item of entries){const line=el('div','bar');const name=el('span','',item.name);name.title=item.name;const track=el('div','track');const fill=el('div','fill');fill.style.width=(item.roas==null?0:item.roas/max*100)+'%';track.append(fill);line.append(name,track,el('span','',item.roas==null?'—':item.roas.toFixed(2)+'x'));barRoot.append(line)}\n const table=el('table');const head=table.insertRow();for(const h of ['Brand','Ad Sales','Ad Spend','ROAS']){const th=el('th','',h);head.append(th)}\n for(const r of rows){const tr=table.insertRow();for(const v of [r.brandName||'Unspecified',money(r.adSalesAmount),money(r.adSpend),r.adRoas==null?'—':Number(r.adRoas).toFixed(2)+'x']){tr.append(el('td','',v))}}\n const scroll=el('div','scroll');scroll.append(table);$('#table').replaceChildren(scroll);\n $('#notice').textContent=hasNext?'More rows exist. Results and KPI cards show the first 100 returned rows only.':'All rows returned for this query page; check data completeness against Pacvue.';\n}\nasync function run(){const start=$('#start').value,end=$('#end').value;if(!start||!end||start>end){$('#status').textContent='Please choose a valid date range.';return}\n const button=$('#run');button.disabled=true;$('#status').textContent='Loading…';\n try{const result=await reportAPI.queryTable({...BASE,startDate:start,endDate:end,pageNum:1,pageSize:100,orderBys:{orderBy:'adSalesAmount',orderType:'descending'}});\n const rows=Array.isArray(result?.list)?result.list:[];paint(rows,!!result?.hasNextPage);$('#status').textContent=rows.length?'Loaded '+rows.length+' brand rows':'No brands matched this date range.';\n }catch(e){$('#status').textContent='Query failed: '+e.message;$('#cards').replaceChildren();$('#bars').replaceChildren();$('#table').replaceChildren()}finally{button.disabled=false}}\n$('#run').addEventListener('click',run);run();"
}
```

---

## Source: examples/dataset-discovery.json (Metadata discovery example)

Source URL: https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/examples/dataset-discovery.json

```json
{
  "id": "dataset_discovery_sample",
  "name": "Available Dataset Explorer",
  "version": 1,
  "permissions": [
    "datasets"
  ],
  "html": "<main class=\"report\"><h1>Available datasets</h1><p class=\"hint\">Names are loaded from the authorized report host.</p><p data-status>Loading...</p><ul data-items></ul></main>",
  "css": ".report{max-width:760px;margin:24px auto;padding:20px;font:14px system-ui;color:#202938}.report h1{font-size:22px}.hint{color:#64748b}.report li{padding:8px 0;border-bottom:1px solid #e2e8f0}",
  "js": "(async () => {\n  const status = root.querySelector('[data-status]');\n  const items = root.querySelector('[data-items]');\n  try {\n    const result = await reportAPI.getDataSets();\n    if (!Array.isArray(result)) throw new Error('Dataset metadata must be an array');\n    items.replaceChildren();\n    for (const item of result) {\n      const li = document.createElement('li');\n      li.textContent = String(item && item.dataSet != null ? item.dataSet : '(unnamed)');\n      items.appendChild(li);\n    }\n    status.textContent = result.length ? `${result.length} datasets available` : 'No datasets available for this account.';\n  } catch (e) {\n    status.textContent = 'Unable to load datasets: ' + (e && e.message ? e.message : 'Unknown error');\n  }\n})();"
}
```

---

## Final self-check

Generate one complete, runnable JSON. No manual query JSON or developer field mapping input. Do not claim live host verification without actually running in a host. Mention any limitations or approval needs.
