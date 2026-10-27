# Portable Report Skill v4: Creation + Iteration + UI Kit (publication review candidate)

This release retains the Report Iteration Contract and adds **optional** ECharts + Native Table authoring for Custom Reports Lab v0.5.1.

For URL-based AI readers, share the full [AI-CONTEXT.md](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/AI-CONTEXT.md). For Agent Skills installations, use `SKILL.md`.

To update a report, give the AI **both** the online Skill URL and the **exported existing report JSON**, then describe the change. Keeping the report ID is essential to host versioning.

Checks: `python scripts/validate_report.py updated.json` and `python scripts/check_report_update.py old.json updated.json`. Refresh AI-CONTEXT via `python scripts/generate_ai_context.py` after changing source files.

The UI Kit spec is in `references/report-ui-kit.md`; a complete example is `examples/uikit-brand-sales.json`. Do not target UI Kit on older runtimes.

## One-link AI access (web-reading models)

- **Recommended single document:** [AI-CONTEXT.md](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/AI-CONTEXT.md)
- [AI-ENTRY.md](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/AI-ENTRY.md) gives explicit links to every required source.
- Agent Skills installations continue to use `SKILL.md`.

When changing any Skill reference/example, regenerate the consolidated context with `python scripts/generate_ai_context.py`, then commit both the source files and `AI-CONTEXT.md` together. A repository URL alone does not guarantee the AI crawls all files.

**Security notice:** The query and field catalog are implementation-facing release-candidate material. Obtain company disclosure approval before uploading these documents publicly.
