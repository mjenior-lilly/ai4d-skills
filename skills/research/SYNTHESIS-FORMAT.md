# SYNTHESIS.md Format

`SYNTHESIS.md` is the final research brief. It answers the research goal from the claims matrix rather than summarizing sources one by one.

## Template

```md
# Synthesis: {Topic or question}

## Research goal
{Restate the core question, intended use, and desired level of understanding from `RESEARCH-GOAL.md`.}

## Bottom line
{3-6 sentences answering the question directly. Use source IDs for material claims.}

## What the evidence shows

### {Facet or sub-question}
{Synthesize the strongest relevant claims. Cite source IDs inline, e.g. `(SRC-0001, SRC-0004)`.}

### {Facet or sub-question}
{Repeat as needed.}

## Points of disagreement or uncertainty
- {Contradiction, uncertainty, or evidence gap, with source IDs when applicable}

## Practical implications
- {What the user can infer, decide, try, or watch next based on the evidence}

## What not to conclude
- {Overclaims, tempting but unsupported conclusions, or scope boundaries}

## Source coverage
- Verified sources used: {n}
- Source types represented: {types}
- Important source gaps: {gaps or `none identified within scope`}

## Methodology
{Briefly describe search facets, verification approach, extraction process, skeptic review, and stopping criteria.}
```

## Rules

- Answer the user's question before explaining the research process.
- Synthesize by idea, facet, or decision need, not by source order.
- Cite source IDs for every material claim.
- Separate evidence from interpretation.
- Preserve uncertainty and disagreement. Do not smooth over real contradictions.
- Include `What not to conclude` to prevent plausible hallucinations or overextensions.
- Do not include a source that exists only as a search snippet or unverified citation.
