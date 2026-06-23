# CLAIMS-MATRIX.md Format

`CLAIMS-MATRIX.md` is the evidence ledger for the research. It maps every material claim to verified source IDs and keeps weak, conflicting, or unsupported claims out of the final synthesis.

## Template

```md
# Claims Matrix: {Topic}

## Facet: {Research facet or sub-question}

### CLM-0001: {Short claim title}
- Claim: {One precise sentence.}
- Claim type: {fact | interpretation | estimate | normative | context}
- Source support:
  - `SRC-0001`: {quote, excerpt, table, figure, or paraphrase tied to a source location}
    - Location: {page, section, heading, timestamp, table, figure, line, etc.}
  - `SRC-0004`: {additional support, if any}
    - Location: {source location}
- Confidence: {high | medium | low}
- Why this confidence: {method quality, source agreement, primary status, recency, or limitations}
- Contradictions or tension: {conflicting source IDs and the nature of disagreement, or `none found`}
- Relevance to goal: {why this claim matters for the final answer}
- Synthesis use: {use | background | exclude}

## Unsupported or unresolved claims

### UNS-0001: {Claim that came up but is not ready to use}
- Claim: {claim text}
- Why unresolved: {no source, weak source, contradiction, access limit, unclear meaning}
- Needed check: {specific next search or source needed}
```

## Rules

- One claim per entry. Split compound claims so each can be verified or rejected independently.
- A source summary is not a claim. Extract only statements that help answer `RESEARCH-GOAL.md`.
- Use direct quotes or short excerpts for important or controversial claims when possible.
- Assign lower confidence to claims supported only by secondary, promotional, old, or methodologically weak sources.
- Do not promote unsupported claims into `SYNTHESIS.md` except in a clearly labeled uncertainty section.
- Capture contradictions. Research value often comes from explaining why credible sources disagree.
