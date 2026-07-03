---
name: task-triage
description: >
  Analyze daily handwritten to-do checklists (PNG images) over time using GTD
  principles. Triggers on requests to triage, sync, or analyze task notes / to-do
  lists; generate daily, weekly, monthly, or annual execution analyses; extract text
  from handwritten checklist images; or summarize project codebases as context for
  task analysis (task_context.md / "triage").
---

# TaskTriage

Turns timestamped PNG images of daily handwritten checklists
(`YYYYMMDD_HHMMSS.png` in a notes directory) into a temporal hierarchy of execution
analyses: daily → weekly → monthly → annual, each saved as a `.triaged.txt` file.
You perform the OCR, analysis, and codebase summarization; `scripts/triage.py`
(stdlib-only) handles all date math, trigger conditions, and file bookkeeping —
never recompute those by hand. Other formats (`.jpg/.pdf/.txt`) are tolerated if
encountered, but PNG images are the expected input.

**Notes directory**: ask the user once if unknown (may pass several, e.g. a USB mount
plus a local folder; the first is where new analyses are written). All `triage.py`
commands below take `--notes-dir DIR` (repeatable).

## Workflow

**Step 0 — Sync/OCR** (the standard first step — every new PNG needs it):
`triage.py scan` lists notes needing analysis. Entries with `"reason": "needs_ocr"`
have no extracted text yet — read the image and transcribe it per the OCR rules in
`references/input-format.md`, save to the given `raw_notes_path`, and offer the user
a chance to fix OCR errors before analyzing.

**Step 1 — Daily analyses** (on explicit user request):
For each entry from `scan` (reason `new` or `edited`): read `content_file`, optionally
inject project context (Step 3), analyze per `references/daily-analysis.md`, and write
to `analysis_path` with the standard file header (overwriting on re-analysis). Report
a summary: N successful, N failed.

**Step 2 — Automatic cascade**: after dailies, run `triage.py pending`. For every
listed period, collect and analyze — repeat `pending` after each level since new
weeklies can unlock a monthly, etc.:
- weekly: `triage.py collect-week YYYY-MM-DD` (the week_start) → analyze per
  `references/weekly-analysis.md`
- monthly: `triage.py collect-month YYYY-MM` → `references/monthly-analysis.md`
- annual: `triage.py collect-year YYYY` → `references/annual-analysis.md`

Each collect command prints the output path on line 1, then the combined date-labeled
input. Write the result to that path with the standard header.

**Step 3 — Project context** (on request, or before dailies when `local_context/`
has summaries): see `references/project-context.md` for generating codebase summaries
from `task_context.md` (`context-scan` / `context-mark` for change detection) and for
selecting ≤2 relevant summaries to append to a day's notes.

## Reference files (read when performing that step)

- `references/input-format.md` — notes schema, task notation (✓ ✗ * ↳), filename and
  directory conventions, OCR transcription rules, edge cases. Read before Step 0/1.
- `references/daily-analysis.md`, `weekly-analysis.md`, `monthly-analysis.md`,
  `annual-analysis.md` — full methodology and output template per level.
- `references/project-context.md` — codebase summarization + context injection.
