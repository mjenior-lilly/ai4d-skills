---
name: tasks
description: Analyze handwritten or digital task notes with GTD-style execution review, daily/weekly/monthly/annual synthesis, project context awareness, and optional Obsidian vault integration. Use this skill when the user asks to triage task notes, assess what got done, extract planning patterns, or maintain a local task-analysis workspace.
argument-hint: "What task notes, analysis workspace, project context, or Obsidian vault should be processed?"
---

Use this skill to perform TaskTriage-style analysis directly as the local agent. Do not assume the TaskTriage CLI, LangChain app, Streamlit UI, Google Drive integration, or external Claude API workflow is available. The agent owns ingestion, analysis, artifact writing, re-analysis decisions, higher-level cascade, and validation.

Use the workflow in [WORKFLOW.md](./WORKFLOW.md). It defines workspace setup, note ingestion, OCR/transcription expectations, daily analysis, weekly/monthly/annual cascade, project context collection, Obsidian knowledge-base awareness, and validation.

Use [ANALYSIS-FORMATS.md](./ANALYSIS-FORMATS.md) for daily, weekly, monthly, annual, and project-context output structures.
Use [WORKSPACE-FORMAT.md](./WORKSPACE-FORMAT.md) for the task workspace manifest.

## Task workspace

Treat the user-provided task directory as the workspace. If the user has not provided one, use the current directory when it already contains task notes or task-analysis folders. Ask one focused question only when choosing the wrong workspace could misplace files, overwrite existing analyses, or mix unrelated personal task histories.

Default structure:

- `raw/`: optional copied source notes when the user wants a managed workspace.
- `daily/`: daily execution analyses.
- `weekly/`: weekly execution analyses.
- `monthly/`: monthly execution reports.
- `annual/`: annual execution reviews.
- `context/`: project and knowledge-base context summaries used to enrich daily analysis.
- `TASK-MANIFEST.md`: workspace conventions, paths, analysis cadence, context sources, and validation status.

When operating inside an existing TaskTriage-style directory, preserve its folder and filename conventions unless the user asks to migrate them.

## Default posture

- Analyze execution, planning realism, and task-system quality, not personal worth.
- Be candid and non-judgmental. Prefer clarity over motivation.
- Ground every observation in the supplied notes, prior analyses, project context, or Obsidian notes.
- Distinguish completed, abandoned, incomplete, vague, and inferred tasks.
- Use the notes' priority markers as evidence of intent, not proof of true priority.
- Treat repeated behavior as stronger evidence than labels or aspirations.
- Keep generated analyses as markdown artifacts on disk unless the user asks for chat-only output.

## Obsidian awareness

If the user provides an Obsidian vault or the current workspace has an obvious vault nearby, inspect relevant vault conventions and notes before analysis. Use Obsidian content only as context for project names, goals, prior decisions, recurring commitments, and terminology. Do not let vault notes override the task-note evidence.

When the user wants analyses captured in an Obsidian knowledge base, follow the `obsidian` skill's conventions: write notes inside the target vault, use vault-relative paths, add valid frontmatter, prefer WikiLinks, update relevant index/project/source links, and avoid orphan notes.

## Safety rules

- Do not delete or move raw task notes, images, PDFs, existing analyses, project repositories, or Obsidian notes without explicit approval.
- Re-analysis may replace a prior generated analysis for the same date or period only when the source note or lower-level input changed; preserve the existing filename convention.
- If handwriting, OCR, or transcription is uncertain, mark uncertainty instead of inventing task text.
- Do not ingest large code repositories, dependency folders, generated data, or whole Obsidian vaults indiscriminately. Search and summarize only the relevant bounded context.
