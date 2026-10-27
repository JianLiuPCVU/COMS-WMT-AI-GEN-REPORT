#!/usr/bin/env python3
"""Regenerate AI-CONTEXT.md from the canonical Skill sources."""
from pathlib import Path
repo=Path(__file__).resolve().parents[1]
paths=['SKILL.md', 'references/report-package.md', 'references/report-sdk.md', 'references/query-contracts.md', 'references/field-catalog.md', 'references/quality-rules.md', 'references/report-requirements.md', 'references/report-iteration.md', 'references/report-ui-kit.md', 'examples/uikit-brand-sales.json', 'examples/brand-advertising-efficiency.json', 'examples/dataset-discovery.json']
labels={'SKILL.md': 'Skill instructions', 'references/report-package.md': 'Report package contract', 'references/report-sdk.md': 'Report SDK', 'references/query-contracts.md': 'Full query contracts', 'references/field-catalog.md': 'Verified field catalog', 'references/quality-rules.md': 'Quality rules', 'references/report-requirements.md': 'Ready-to-run acceptance rules', 'references/report-iteration.md': 'Report iteration contract', 'references/report-ui-kit.md': 'Report UI Kit v1.1', 'examples/uikit-brand-sales.json': 'Complete UI Kit report', 'examples/brand-advertising-efficiency.json': 'Working report example', 'examples/dataset-discovery.json': 'Metadata discovery example'}
base="https://github.com/JianLiuPCVU/COMS-WMT-AI-GEN-REPORT"
parts=["# AI Context: Portable Report Development Skill", "", "> Consolidated single-file version of the Skill, contracts, field catalog, quality requirements and examples. Read this full document before generating any report. This is a review candidate requiring company approval for public disclosure.", "", "**Source of truth:** this file is generated from the repository sources using `python scripts/generate_ai_context.py`; do not hand-edit the generated file. For Agent Skills installers, use `SKILL.md`.", "", "**If a section is truncated or absent:** fetch the corresponding source link in `AI-ENTRY.md` or disclose the limitation; never fabricate missing contract details.", ""]
for path in paths:
    data=(repo/path).read_text(encoding="utf-8").rstrip()
    parts += ["", "---", "", f"## Source: {path} ({labels[path]})", "",f"Source URL: {base}/blob/main/{path}", ""]
    parts += (["```json",data,"```"] if path.endswith(".json") else [data])
parts += ["", "---", "", "## Final self-check", "", "Generate one complete, runnable JSON. No manual query JSON or developer field mapping input. Do not claim live host verification without actually running in a host. Mention any limitations or approval needs.", ""]
(repo/"AI-CONTEXT.md").write_text("\n".join(parts),encoding="utf-8")
print("Regenerated AI-CONTEXT.md")
