# AI entry point: Report Development Skill

**For AI assistants that read URLs rather than install skills.** Read the complete single-file manual below first. The folder listing on GitHub is NOT guaranteed to be recursively read by an AI browser.

## One URL (recommended)

**[AI-CONTEXT.md](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/AI-CONTEXT.md)**

Raw Markdown URL: https://raw.githubusercontent.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/main/AI-CONTEXT.md

This file combines the Skill, required reference docs and complete working JSON examples. If your AI has a page-reading size limit, use the individual links below.

## Individual source files (read in this order)

- [Skill instructions](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/SKILL.md) (`SKILL.md`)
- [Report package contract](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/report-package.md) (`references/report-package.md`)
- [Report SDK](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/report-sdk.md) (`references/report-sdk.md`)
- [Full query contracts](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/query-contracts.md) (`references/query-contracts.md`)
- [Verified field catalog](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/field-catalog.md) (`references/field-catalog.md`)
- [Quality rules](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/quality-rules.md) (`references/quality-rules.md`)
- [Ready-to-run acceptance rules](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/references/report-requirements.md) (`references/report-requirements.md`)
- [Working report example](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/examples/brand-advertising-efficiency.json) (`examples/brand-advertising-efficiency.json`)
- [Metadata discovery example](https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/blob/main/examples/dataset-discovery.json) (`examples/dataset-discovery.json`)

## Ready-to-copy AI request

> Read the complete instructions at https://raw.githubusercontent.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT/main/AI-CONTEXT.md and create a self-contained, importable report JSON for my analytics requirements. Follow its SDK contract and finished example. Do not ask end users to supply field mappings, API tokens or query JSON. If you cannot access the URL or a required section, tell me exactly what is missing instead of guessing. Validate as far as your tools permit, and identify any tests you could not run.

## Standard Agent Skills installation

For compatible tools, `SKILL.md` plus the adjacent `references/`, `examples/`, and `scripts/` are the standard project files. Use the tool-specific install workflow; a web URL is not automatically a Skill installation.

## Publication note

**Review candidate only.** The v2 references include implementation-facing query field names and schemas. Obtain company approval before publishing them on a Public repository. Do not publish credentials or real customer data.
