---
name: classify-context
description: "Classify an artifact or trail reference from explicit caller-supplied labels and policy references without inferring undisclosed sensitive facts."
---
# classify-context
Route: `@confidentiality-agent /confidentiality:classify-context`.

Use `scripts/classify.py`. The classifier never guesses whether content is sensitive; it maps declared labels to PUBLIC, INTERNAL, CONFIDENTIAL, or RESTRICTED according to `assets/policy.json`.

Raw/private intent may remain operational evidence without becoming learning data. Classification changes handling policy, not the truth of the underlying intent.
