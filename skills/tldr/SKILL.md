---
name: tldr
description: >
  Summarize technical documents into structured, audience-ready summaries.
  Triggers on requests to summarize or "tldr" a scientific publication, internal
  technical document, repository README, or general document; synthesize multiple
  summaries into an executive summary; identify knowledge gaps and research them;
  reorganize or stylistically polish technical text; or score summary quality.
---

# TLDR

Turns technical source documents into structured summaries using a fixed
per-document-type template, with optional downstream stages (executive synthesis,
gap research, polishing, quality evaluation). Each stage has its own reference
file — read only the file for the stage and document type you are executing.

## Core workflow

**Step 1 — Ingest.** Read the provided source completely and thoroughly interpret
it before doing anything else. Accept file paths, pasted text, PDFs, or URLs. For
multiple documents, run Steps 2–4 per document, then offer Step 5.

**Step 2 — Classify the document type.** Pick exactly one:

| Type | Definition | Template |
|---|---|---|
| `publication` | Formal scientific literature: journal articles, conference papers, preprints, theses | `references/summary-publication.md` |
| `document` | Internal technical communications: internal reports, design documents | `references/summary-document.md` |
| `readme` | README from a code repository: project overview, setup, usage | `references/summary-readme.md` |
| `other` | Anything else: memos, emails, meeting transcripts, etc. | `references/summary-other.md` |

**Step 3 — Summarize.** Read the matching template file (only that one) and
produce the summary following its exact section structure, plus the shared
guardrails below.

**Step 4 — Title and save.** Generate a concise, descriptive title of no more
than 5 words. When saving to a file, derive the filename from the title
(kebab-case, `.md`) and write it beside the source unless the user specifies a
destination. If the user only wants the summary inline, don't write a file.

**Step 5 — Optional stages** (on user request, or offer when clearly relevant):

- **Executive summary** — synthesize the summaries of 2+ documents on a common
  topic into a single high-level overview: `references/executive-summary.md`
- **Gap research** — identify under-explained concepts in the source and answer
  them via web search: `references/gap-research.md`
- **Polishing** — reorganize poorly structured technical text, optionally with a
  stylistic rewrite: `references/polishing.md`
- **Evaluation** — score a summary against its source with a weighted rubric,
  and consolidate multiple score reports: `references/evaluation.md`

## Shared guardrails (apply to every summary)

- **Completeness over brevity**: prioritize coverage of every unique topic over
  shortness; but within each section, be concise and avoid verbosity.
- **All sections present**: include every section of the template even when the
  source has no matching content — state "None" or "Not specified".
- **Objectivity**: do not add interpretation, assumptions, or outside
  information beyond the source text.
- **Tone**: technical and concise, suitable for internal biotech/biopharma
  staff and cross-functional technical readers.
- **Jargon**: define acronyms and jargon only when uncommon or ambiguous to
  cross-functional readers; avoid unexplained abbreviations.
- **Formatting**: use headers, bullet points, and short paragraphs to maximize
  scannability.
