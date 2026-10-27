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
