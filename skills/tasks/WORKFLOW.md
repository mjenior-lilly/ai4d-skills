# Local Task Analysis Workflow

Use this workflow to analyze personal task notes and maintain a local task-analysis workspace. The local agent performs the work directly: it reads source notes, transcribes images/PDFs when tool support exists, writes analysis artifacts, determines whether re-analysis is needed, triggers higher-level reviews, and validates outputs.

## Objectives

- Convert raw daily task notes into evidence-based execution analyses.
- Preserve task markers, task order, subtask relationships, and priority intent.
- Identify completion patterns, priority alignment, workload realism, task design quality, and next-action priorities.
- Cascade daily analyses into weekly, monthly, and annual syntheses when enough lower-level artifacts exist.
- Enrich daily analysis with bounded project context and relevant local Obsidian knowledge-base context when available.
- Keep all generated artifacts discoverable, consistently named, source-grounded, and safe to re-run.

## Supported inputs

- Text notes: `.txt`, `.md`, `.raw_notes.txt`.
- Images: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, when the agent has image-reading support.
- PDFs: when the agent has PDF or image-frame extraction support.
- Existing analyses in `daily/`, `weekly/`, `monthly/`, or `annual/`.
- Project context paths listed in `task_context.md` or supplied by the user.
- Obsidian vaults supplied by the user or clearly present in the workspace.

## Task notation

Preserve and interpret these markers:

- `✓` on the left: completed during the day.
- `✗` or `X` on the left: removed or abandoned during the day.
- No status marker: planned but incomplete.
- `↳`: subtask directly related to the preceding parent task. Analyze independently while preserving the relationship.
- `*` on the right: urgent or high-priority intent.

If the source uses a similar notation, infer the mapping only when clear and record the assumption in `TASK-MANIFEST.md` or the analysis.

## Phase gates

| phase | gate |
| --- | --- |
| workspace scope | Workspace path, write target, source locations, and filename conventions are known or explicitly assumed. |
| source inventory | Candidate task notes and existing analyses are listed by date, type, status, and output path. |
| transcription | Image/PDF sources have editable text extracted, or the limitation is recorded. |
| context collection | Relevant project and Obsidian context has been searched or intentionally skipped with a reason. |
| daily analysis | Each changed daily source has a current analysis with task evidence, estimates, patterns, and next queue. |
| cascade | Eligible weekly, monthly, and annual periods have been generated or skipped with a reason. |
| validation | Changed artifacts have consistent names, dates, links, source references, and no obvious orphan outputs. |

## Workflow loop

### 0. Scope the workspace

1. Identify the task workspace, source notes, existing output folders, and any target Obsidian vault.
2. Inspect existing conventions before writing: file extensions, date format, folder names, frontmatter, and whether analyses are `.md` or `.txt`.
3. Create or update `TASK-MANIFEST.md` using [WORKSPACE-FORMAT.md](./WORKSPACE-FORMAT.md) when the task is more than a one-off analysis.
4. Use markdown output by default. Preserve `.triaged.txt` only when updating an existing TaskTriage-style history that already uses that convention.

### 1. Inventory and normalize sources

1. Find candidate raw notes using timestamp-style names such as `YYYYMMDD_HHMMSS.ext`, explicit user-provided dates, or surrounding folder context.
2. Record source type, source date, last modified time, expected output path, and whether an output already exists.
3. For duplicate timestamps across locations, choose the most authoritative source in this order unless the user says otherwise:
   1. user-specified file;
   2. editable `.raw_notes.txt`;
   3. plain text or markdown note;
   4. image/PDF source.
4. Re-analyze a daily note when the source was modified after the generated analysis, or when the user explicitly requests re-analysis.
5. Do not create duplicate analyses for the same date unless the user says the notes represent separate planning sessions.

### 2. Transcribe image and PDF notes

1. Extract text into a sibling `.raw_notes.txt` file when possible.
2. Preserve visible line order, indentation, status markers, priority markers, and subtasks.
3. Do not interpret or clean up task wording during transcription. Analysis happens later.
4. If text is unclear, make the best bounded transcription and mark uncertainty inline with `[unclear: ...]` only when necessary for correctness.
5. If transcription tooling is unavailable, record the source as skipped with the reason and continue with analyzable sources.

### 3. Collect project and Obsidian context

1. If `task_context.md` exists, read project paths and optional labels. Lines may be raw paths or `label: path`; `#` starts a comment.
2. Summarize only bounded, relevant project files. Prefer README, configuration, entry points, docs, tests, and shallow source files. Exclude dependency folders, build output, generated files, binaries, virtualenvs, and large files.
3. Write project summaries to `context/<label>.context.md` and record enough metadata to detect whether the summary is stale.
4. Match context to daily notes by project labels, distinctive keywords, technologies, task terms, and semantic similarity when available. Inject only the top relevant summaries.
5. If an Obsidian vault is available, search relevant note titles, aliases, tags, project notes, daily notes, and indexes for task terms. Use narrow searches. Do not read the whole vault unless it is small and the user asks for full integration.
6. Use context to clarify terminology and project significance. Do not use context to mark tasks complete or incomplete.

### 4. Generate daily analyses

For each changed daily source:

1. Parse all tasks and subtasks, preserving source wording.
2. Assess task definition quality:
   - infer reasonable scope for brief but clear tasks;
   - analyze adequately specific tasks as written;
   - flag fundamentally vague tasks and suggest 1-2 clearer alternatives.
3. For every analyzable task, determine status, inferred outcome, urgency marker, theme, energy level, estimated time, and completion rationale.
4. Estimate total planned time and completed time. Compare against a healthy 6-7 hour focused-work guardrail.
5. Group tasks into themes such as Communication, Planning, Implementation, Administrative, Research/Learning, Meetings/Collaboration, Health/Wellness, Personal/Home, or System/Meta.
6. Identify execution patterns, priority alignment, workload realism, task design quality, and tomorrow's priority queue.
7. Write the analysis using the daily format in [ANALYSIS-FORMATS.md](./ANALYSIS-FORMATS.md).

### 5. Cascade weekly, monthly, and annual analyses

After daily analyses are current, check higher-level periods.

Weekly analysis is eligible when:

- 5 or more weekday daily analyses exist for a Monday-Friday work week; or
- the work week has passed and at least 1 daily analysis exists for that week; or
- the user explicitly requests that week.

Monthly analysis is eligible when:

- 4 or more weekly analyses exist for the calendar month; or
- the calendar month has ended and at least 1 weekly analysis exists; or
- the user explicitly requests that month.

Annual analysis is eligible when:

- 12 monthly analyses exist for the year; or
- the calendar year has ended and at least 1 monthly analysis exists; or
- the user explicitly requests that year.

For each eligible period:

1. Collect lower-level analyses with date or period labels.
2. Skip periods whose output exists and is newer than all inputs unless forced.
3. Generate the synthesis using [ANALYSIS-FORMATS.md](./ANALYSIS-FORMATS.md).
4. Focus weekly reviews on behavior-driven priority correction.
5. Focus monthly reviews on strategic patterns, system evolution, persistent challenges, and next-month guidance.
6. Focus annual reviews on accomplishments, learning, highest-ROI improvements, and year-ahead direction.

### 6. Integrate with Obsidian when requested

1. If the user provides a target vault for outputs, write analyses inside the vault using the vault's conventions.
2. Add valid frontmatter, source links, and WikiLinks according to the `obsidian` skill.
3. Link task analyses from relevant project notes, daily notes, MOCs, source registers, or index notes when they exist.
4. Avoid dumping raw task histories into permanent notes. Use project or time-bound folders unless the analysis contains durable concepts worth evergreen notes.
5. Record any Obsidian integration assumptions or unresolved link issues in the task summary or vault audit.

### 7. Validate changed artifacts

Run the narrowest useful checks:

1. Generated files are inside the intended task workspace or target vault.
2. Daily analysis dates match source dates.
3. Higher-level analyses are based on the correct lower-level files.
4. Re-analysis replaced the intended output instead of creating duplicates.
5. Markdown headings match the required format.
6. Project context paths are bounded and do not include excluded folders.
7. Obsidian outputs, when requested, have valid frontmatter and non-broken internal links where practical.

## Output to the user

Return a concise summary with:

- workspace path or vault path;
- raw sources processed, skipped, and re-analyzed;
- daily, weekly, monthly, and annual files created or updated;
- project or Obsidian context used;
- validation performed and results;
- unresolved transcription gaps, ambiguous tasks, stale context, or integration issues.
