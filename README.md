# Portable Report Skill v2 (public release candidate)

**Not approved for public distribution until company review.** This edition focuses on zero-setup report generation by AI tools. Unlike the earlier generic edition, it provides a fully specified, experimentally verified SDK query pattern, field catalog, and real-code example, **without** publishing internal backend URLs, tokens or customer data.

## AI entry point
`SKILL.md` → `references/query-contracts.md`, `references/field-catalog.md`, `references/report-requirements.md` → `examples/brand-advertising-efficiency.json`.

Paste a repository URL into an AI with web-reading capabilities and ask it to read `SKILL.md` and linked files. Or install using a supported Agent Skills implementation. Reading a URL is not universal auto-install.

## Quick local checks
`python scripts/validate_report.py examples/brand-advertising-efficiency.json`

## Repository update
Upload the *contents* of this reviewed folder to the repository root, replacing existing versions. Keep existing company license and policies where applicable. Review PUBLICATION_REVIEW.md before exposing newly added field names and query semantics. Do not push any unapproved content merely because the repo is already Public.

## Known limits
This version documents one verified runtime profile (`OmniMetrics`) rather than every data source or grouping combination. It cannot guarantee the sample works in arbitrary hosts or that field-level metadata is safe to publish.
