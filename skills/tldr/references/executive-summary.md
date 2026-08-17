# Executive Summary (Multi-Document Synthesis)

Synthesize summaries of multiple documents on a common topic into one executive
summary for informed non-specialists, including executives, funders, and
policymakers.

Input: a set of summaries (S1…Sn), each derived from a distinct document.
Prioritize completeness and coverage of unique topics over brevity, but keep
the result executive-length (roughly one page).

## Process

1. **Extract from each summary**: primary research question(s) or objectives;
   key methodologies; core findings and results; principal conclusions;
   significant limitations or caveats; novel contributions or unique aspects.
2. **Synthesize across summaries** by identifying relationships rather than
   merely aggregating their contents:
   - Overarching themes: common threads, concepts, or research directions
   - Areas of consensus: where findings or conclusions align
   - Areas of divergence: conflicting findings, differing interpretations, or
     contrasting methodologies worth noting
   - Knowledge gaps: unanswered questions or research avenues suggested by the
     collective work
   - Overall significance: broader importance or potential impact of the
     collective findings
3. **Write a cohesive narrative** that integrates the points instead of listing
   items from each summary.

## Output structure

- High-level overview: the general topic and the purpose of this synthesis
- Major themes and key consolidated takeaways
- Consensus and divergence, if significant
- Overall implications and significance in a broader context
- Forward-looking close: future directions or remaining questions

## Rules

- Tone: objective, balanced, authoritative. Explain necessary technical terms
  briefly.
- Faithfully represent all core information from the provided summaries; no
  outside information or opinions.
- Sections rendered as bullet points need at least 3 entries each.
- Output only the executive summary, with no preamble or postscript.
