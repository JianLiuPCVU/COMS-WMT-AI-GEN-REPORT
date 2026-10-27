# Portable Report Skill (Public Edition, release candidate)

A model-neutral, Agent Skills-style instruction set for producing importable analytics report JSON for a compatible host-provided `reportAPI`.

**Status: NOT APPROVED FOR PUBLICATION.** This directory is a **review candidate**. Publish only after the owner confirms company authorization, project branding, report SDK redistribution rights, and code license.

## Read from an AI
Give the AI the URL to this repository's `SKILL.md` and ask it to read referenced files. Reading a public URL is **not the same as installing a skill**; support depends on the AI product. Supported tools may install from a repository by their own procedure.

Example prompt:
> Read the SKILL.md and relevant references at https://github.com/OWNER/REPOSITORY/blob/main/SKILL.md . Create a report compatible with this contract. Use only approved dataset metadata, no guessed API fields. Provide an importable JSON and validation results.

## Local static test
```bash
python scripts/validate_report.py examples/dataset-discovery.json
```

## Files
- `SKILL.md` instructions
- `references/` public contracts and correctness rules
- `examples/dataset-discovery.json` synthetic, live metadata-driven sample; no real customer data
- `scripts/validate_report.py` heuristic static validation
- `PUBLICATION_REVIEW.md` authorization and content checklist

## Publishing and versioning
Create a **new clean GitHub repository**, upload these files via the GitHub web interface only **after approval**, and tag approved releases (e.g. `v0.1.0-public`). Version in `SKILL.md` and the runtime compatibility profile independently of the repository tag. Do not upload the previous internal Skill package or original request dumps.

## License
No open-source license is included until the copyright holder chooses and approves one. **Public GitHub visibility by itself does not grant a license to reuse or redistribute.**
