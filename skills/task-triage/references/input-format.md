# Input Formats, Directory Layout, and OCR Rules

## Directory layout

Raw notes live at the top level of the notes directory; analyses in subdirectories
(created on demand):

```
Notes/
├── 20251226_094500.png              # daily checklist (PNG image — the expected input)
├── 20251226_094500.raw_notes.txt    # extracted text (auto-generated, user-editable)
├── 20251227_120000_Page_1.png       # multi-page checklist (one timestamp, one analysis)
├── 20251227_120000_Page_2.png
├── daily/26_12_2025.triaged.txt     # daily analysis   (DD_MM_YYYY)
├── weekly/22_12_2025.triaged.txt    # weekly analysis  (DD_MM_YYYY of the week's Monday)
├── monthly/12_2025.triaged.txt      # monthly analysis (MM_YYYY)
└── annual/2025.triaged.txt          # annual analysis  (YYYY)
```

- Checklist filenames: `YYYYMMDD_HHMMSS.png` (expected). Multi-page scans use
  `YYYYMMDD_HHMMSS_Page_N.png`; all pages share one timestamp and one analysis.
  Other formats (`.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, plain `.txt`) are
  handled the same way if present, but PNG is the norm. Files without a valid
  timestamp prefix are ignored.
- Analysis files always end in `.triaged.txt` and begin with the header block:

```
Triaged Tasks
========================================

<analysis body>
```

(40 `=` characters, blank line, then the body. Reproduce this exactly when saving.)

## Task notation (inside daily notes)

- Date header on the first line: two-digit numbers separated by spaces (e.g. `12  11  25`).
- One task per line, no categorical organization required.
- Left-side status markers: `✓` completed, `✗` (or X) removed/abandoned, no marker = planned but not completed.
- `↳` marks a subtask of the task on the preceding line (often indented). Subtasks
  have independent completion status but are analyzed with their parent relationship in mind.
- Right-side `*` marks an urgent/high-priority task.

## OCR: extracting text from checklist images

Every new checklist image must be transcribed before it can be analyzed. Read the
PNG (or each page/PDF page) directly and transcribe the handwriting:

1. Preserve every marker (`✓`, `✗`, `*`, `↳`) in its original position relative to the task.
2. One task per line, flat list, original order preserved; keep subtask indentation.
3. Transcribe exactly — do not add, remove, interpret, or flag uncertainty; make a
   best attempt at unclear handwriting.
4. For multi-page checklists (`_Page_N.png` siblings sharing the timestamp, or
   multi-page PDFs), transcribe every page in order and join pages with a line
   containing only `---`. `scan` reports one entry per timestamp — find the sibling
   pages yourself.
5. Save the result to the `raw_notes_path` given by `scan` (`YYYYMMDD_HHMMSS.raw_notes.txt`,
   top level, no header). The user may edit this file to fix OCR errors; edits after
   analysis trigger automatic re-analysis on the next run.

If a PDF cannot be read directly, convert pages to images first
(`pdftoppm -png file.pdf out` or python pdf2image if available).

## Edge cases

- **Missing days**: weekly analysis proceeds with whatever daily analyses exist
  (as few as 1) once the work week has passed.
- **Malformed filenames / dates**: skipped silently by the script.
- **Empty or near-empty checklist**: still analyze; note the absence of recorded
  tasks and what that implies (untracked day vs. rest day).
- **Duplicate notes in multiple directories**: deduplicated by timestamp — first
  directory listed wins.
- **Edited notes**: a `.raw_notes.txt` (or replaced image) modified after its
  analysis is re-analyzed; the new analysis overwrites the old file (same name,
  no duplicates).
- **Unconverted images**: cannot be analyzed until their `.raw_notes.txt` exists
  (scan reports these as `needs_ocr`) — run the OCR step first.
