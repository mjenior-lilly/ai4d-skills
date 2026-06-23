---
name: research
description: Deeply research a new topic or question using goal-setting, parallel source discovery, source existence verification, evidence extraction, skeptic review, and synthesis.
argument-hint: "What topic or question should be researched?"
---

The user has asked you to research something deeply. Treat this as an evidence-building workflow, not as a request to answer from memory.

Use the workflow in [WORKFLOW.md](./WORKFLOW.md). It defines the goal decision phase, subagent topology, model and thinking tiers, parallelization limits, verification gates, skeptic review points, and final synthesis requirements.

## Research workspace

When the research needs durable state, use the current directory as the research workspace. Create files lazily as they become useful:

- `RESEARCH-GOAL.md`: the target question, desired level of understanding, audience, scope, exclusions, success criteria, and stopping criteria. Use [GOAL-FORMAT.md](./GOAL-FORMAT.md).
- `SOURCE-REGISTER.md`: the canonical register of candidate, verified, rejected, and used sources. Use [SOURCE-REGISTER-FORMAT.md](./SOURCE-REGISTER-FORMAT.md).
- `CLAIMS-MATRIX.md`: the evidence ledger that maps extracted claims to verified source IDs, quotes or excerpts, confidence, contradictions, and synthesis use. Use [CLAIMS-MATRIX-FORMAT.md](./CLAIMS-MATRIX-FORMAT.md).
- `SYNTHESIS.md`: the final answer or research brief. Use [SYNTHESIS-FORMAT.md](./SYNTHESIS-FORMAT.md).
- `NOTES.md`: scratchpad for user preferences, search dead ends, tool limits, and decisions not worth promoting into the formal artifacts.

## Default posture

- Do not answer from parametric memory when a source can be checked.
- A search result snippet is not a source. Fetch or otherwise inspect the source before using it.
- Every material claim in the synthesis must trace to at least one verified source in `CLAIMS-MATRIX.md`.
- Prefer primary sources, authoritative documentation, peer-reviewed work, standards, official datasets, original interviews, and reputable domain experts.
- Preserve uncertainty. If sources conflict, present the conflict and explain what would resolve it.
- Keep the research goal visible. Interesting tangents are rejected unless they improve the user's target understanding.

## When to ask before proceeding

Ask one focused question when the user's target outcome, audience, time horizon, or required depth would materially change what sources count as sufficient. Otherwise state the assumption in `RESEARCH-GOAL.md` and proceed.
