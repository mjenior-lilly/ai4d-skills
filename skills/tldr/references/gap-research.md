# Gap Analysis and Research

Two sub-stages: (A) identify knowledge gaps in a document as a list of
questions, then (B) answer those questions via web search. Run both unless the
user only wants the question list.

## A. Identify gaps

Read the document meticulously and flag concepts, terminology, methodologies,
background information, or logical connections that are:
- Insufficiently explained for a reader with general scientific literacy
- Ambiguous or open to multiple interpretations without clarification
- Assumed knowledge that is never defined or elaborated

Formulate one precise question per gap. Rules for questions:
- **Origin**: every question must arise directly from content present (or
  implied as missing) in the document.
- **Answerable by search**: target information commonly available in scientific
  databases, textbooks, reputable encyclopedias, or standard research articles
  (Google Scholar, PubMed). Never ask for new experimental data, subjective
  opinions, or unpublished insights from the authors.
- **Specific and clear**: pinpoint the exact aspect needing clarification,
  using the document's own terminology where appropriate.
- **Explanatory focus**: what something is, how it works, why an approach was
  taken (if unexplained), or what background context is missing.
- **No critique**: do not challenge the validity of the findings or design
  unless the document itself flags the uncertainty.

Output: a bulleted list of questions only, one per line. If the document is
exceptionally clear and self-contained, say so explicitly instead of forcing
questions.

## B. Research answers

For each question, conduct targeted web searches:
- Prioritize authoritative, peer-reviewed sources: academic journals,
  university research, reputable scientific organizations.
- Synthesize into a comprehensive, accurate answer — not a link dump.
- Cite all sources consistently (direct links or clear references).
- Output the answers with citations; no conversational filler.

When the results feed back into a summary, append them as a clearly labeled
"Background Context" section rather than mixing them into source-derived
sections (objectivity guardrail: never present researched material as if it
came from the source document).
