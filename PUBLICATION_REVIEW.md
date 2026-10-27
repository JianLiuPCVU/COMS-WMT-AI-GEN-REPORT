# Public release gate (owner/company review required)

**Current state: draft for review. Do not publish without written authorization.**

## Must confirm before creating the public repository
- [ ] Company approves public use of the project / product name and trademark.
- [ ] Company approves disclosing the `reportAPI` method names, JSON package shape, metadata model and compatibility details.
- [ ] No internal network URLs, authentication interception details, tokens, cookies, private config or screenshots are present.
- [ ] No customer account information, customer numbers, or production datasets appear in examples or tests.
- [ ] All included code is authorized to redistribute and has been reviewed for unsafe operations and dependencies.
- [ ] Maintainer has selected an appropriate LICENSE, or explicitly keeps rights reserved.
- [ ] An appropriate company security/product owner has signed off on sharing implementation-facing material.
- [ ] Repository initialized from this reviewed clean folder, without importing internal git history, old ZIP files, or logs.

## Security assumptions
The public Skill does not supply data access. Hosts must independently authenticate, authorize, rate-limit, validate input, and isolate untrusted report JS. Static validator warnings are heuristics, not security certification. Limit distribution of unsafe executable reports even if source documentation is public.

## Review notes
- Dataset identifiers and internal endpoints were removed in favor of runtime metadata discovery.
- Example queries with real commercial figures were replaced with a metadata-only example.
- Only abstract methods and return shapes remain, and these **still require disclosure approval**.
- Priority ordering for label IDs is unspecified; no ordering assumption was published.
- Compatibility target: experimental JSON report hosts exposing the documented `reportAPI`. Verify compatibility with each implementation.

## No-approval fallback
If public disclosure is not approved, use a private repository or publish a fully generic skill with no organization name or proprietary runtime method signatures.
