---
name: prepare-disclosure
description: "Create a minimum-disclosure handoff from explicit allowed fields, recipient scope, grants, and agreement references."
---
# prepare-disclosure
Route: `@confidentiality-agent /confidentiality:prepare-disclosure`.

Use `scripts/prepare.py`. Only explicitly allowed fields are emitted. Protected fields are rejected. CONFIDENTIAL or RESTRICTED disclosure requires an agreement reference; every disclosure requires a grant reference.

This skill does not widen access and does not mutate the source artifact.
