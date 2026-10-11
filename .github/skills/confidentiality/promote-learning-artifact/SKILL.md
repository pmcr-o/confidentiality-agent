---
name: promote-learning-artifact
description: "Promote a sanitized operational record into a reusable learning artifact only when explicit consent, grants, policy, and retention rules allow it."
---
# promote-learning-artifact
Route: `@confidentiality-agent /confidentiality:promote-learning-artifact`.

Use `scripts/promote.py`. Default is DENY. Raw trails are never promoted directly. INTERNAL and CONFIDENTIAL material require explicit learning consent; RESTRICTED material requires a separate declassification capability first.

The output is a new sanitized learning artifact with only explicitly allowed fields, its own digest, purpose, retention period, policy refs, grant refs, and consent ref.
