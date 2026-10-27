# Report package contract (public profile v1)

One JSON object (or an array of objects for batch import):

```json
{"id":"example_report","name":"Example report","version":1,"permissions":["datasets"],"html":"<div class=\"viewer\"></div>","css":".viewer { padding: 12px; }","js":"root.querySelector('.viewer').textContent = 'Ready';"}
```

Required: `id` (ASCII letters/digits/underscore/dash, 1-80 chars), `name` (1-140 chars), `html`, `css`, `js` strings. Optional: `version` (string or number), `permissions` (list of SDK capability strings). Keep serialized package under 500,000 characters. `html` is rendered beneath a host-provided root element; `css` styles the report; `js` is evaluated by the host with `root` and `reportAPI` bindings. Avoid global selectors, third-party scripts, and direct URL requests.

The current compatibility profile is based on an experimental runtime and is **not an official public API guarantee**. Consumers should verify against their installed runtime. The `permissions` field documents requested capabilities; actual authorization is controlled by the host.

## Versioned authoring profile (v0.4.0)

For new reports, prefer `"schemaVersion":1, "version":2, "reportVersion":"1.0.0"`; `version` remains a legacy compatibility marker while `reportVersion` describes human-visible revisions. On edits, keep the original `id` and existing schema/legacy versions. Refer to `references/report-iteration.md`.
