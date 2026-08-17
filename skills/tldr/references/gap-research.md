# Gap Analysis and Research

Two sub-stages: (A) identify knowledge gaps in a document as a list of
questions, then (B) answer those questions via web search. Run both unless the
user only wants the question list.

## A. Identify gaps

Read the full document and flag concepts, terminology, methodologies,
background information, or logical connections that are:
- Insufficiently explained for a reader with general scientific literacy
- Ambiguous or open to multiple interpretations without clarification
- Assumed knowledge that is never defined or elaborated

Formulate one precise question per gap. Rules for questions:
- **Origin**: every question must arise directly from content present (or
  implied as missing) in the document.
- **Answerable by search**: ask questions that can be answered from scientific
  databases, textbooks, reputable encyclopedias, or research articles found
  through Google Scholar or PubMed. Do not ask for new experimental data,
  subjective opinions, or unpublished insights from the authors.
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
- Synthesize the findings into a comprehensive, accurate answer rather than a
  list of links.
- Cite all sources consistently (direct links or clear references).
- Output the answers with citations; no conversational filler.

If researched answers are added to a summary, append them in a clearly labeled
"Background Context" section rather than mixing them into source-derived
sections. Never present researched material as though it came from the source
document.
