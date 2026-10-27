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
