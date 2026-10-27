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
