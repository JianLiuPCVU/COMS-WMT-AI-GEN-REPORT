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
