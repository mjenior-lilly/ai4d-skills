# Polishing (Reorganization and Stylistic Rewrite)

Both modes use the same reorganization process. Use **formal** mode by default;
use **stylized** mode when the user asks for an engaging, accessible, or
narrative rewrite.

## Reorganization core (both modes)

Analyze the technical text and diagnose structural flaws: illogical topic
sequencing, scattered or fragmented information, redundant presentation across
sections, prematurely introduced concepts, abrupt or missing transitions,
inconsistent logical flow. Then rebuild:

1. **Semantic analysis**: read the entire text; catalog every distinct concept,
   topic, methodology, result, discussion point, and background item.
2. **Diagnosis**: identify the specific organizational flaws.
3. **Outline**: design a clear hierarchical outline suited to the content:
   general to specific, foundational to advanced, or problem to solution.
4. **Mapping and relocation**: assign every original text block to its new
   location, then reassemble the text without losing any content.
5. **Transitions**: add concise transitions between relocated blocks, using only
   information already present in the source.
6. **Verification**: confirm that all original content remains, the new structure
   is more coherent, technical accuracy is intact, and the text has no abrupt
   shifts.

Hard constraints:
- **Absolute completeness**: include every topic, concept, fact, and data
  point. Do not omit or summarize content; relocate out-of-place material
  instead of discarding it.
- **Technical accuracy preserved**: never alter, misinterpret, or diminish the
  precision or nuance of the original.
- **Citations**: keep citations attached to their text when the input has them.
- **Headings**: build a clear Markdown heading hierarchy (#, ##, ###); adapt
  existing headings or create new ones. Bulleted sections need at least 2
  entries each.
- **Formal mode only**: reorganize the text without stylistic sentence rewrites
  or new information, explanations, or examples beyond minimal transitions.

## Stylized mode (adds a rewrite pass after reorganization)

Rewrite the reorganized content by blending the styles of a pair of expert
science/nonfiction communicators, chosen by topic:

- **Scientific topics**: one science communicator (Carl Sagan, Neil deGrasse
  Tyson, or Mary Roach) + one narrative expert (Malcolm Gladwell or Bill Bryson)
- **Economic/social topics**: one analytical author (Michael Lewis,
  Levitt & Dubner) + one big-picture thinker (Yuval Noah Harari, Jared Diamond)
- **Technical/medical topics**: Siddhartha Mukherjee or Elizabeth Kolbert +
  Bryson or Roach
- **Historical/cultural analysis**: Diamond or Harari + Gladwell or Lewis

Rewrite rules:
- Maintain factual accuracy and clarity. Do not change or omit any information.
- Adapt complexity to the specified audience; keep a consistent voice.
- Include relevant examples or case studies only when present in the source.
- Never mention which authors' styles are being used.

Stylized output structure: clear introduction of the topic → ideas developed
logically with supporting evidence → accessible yet sophisticated language →
relevant examples or data where appropriate → conclusion with key insights or
implications.
