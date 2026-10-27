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
