# Task Workspace Manifest Format

Use this format for `TASK-MANIFEST.md` when maintaining a durable task-analysis workspace.

```md
---
title: "Task Analysis Manifest"
tags: [tasks, productivity, manifest]
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Task Analysis Manifest

## Purpose

{One paragraph describing what task notes this workspace tracks, what analyses it produces, and whether it integrates with project context or Obsidian.}

## Workspace root

- Path: `{absolute or user-provided path}`
- Mode: `{one-off analysis | managed workspace | existing TaskTriage history | Obsidian-integrated}`
- Output format: `{markdown | existing .triaged.txt convention}`
- Last validation: YYYY-MM-DD

## Folder conventions

| folder | role | notes |
| --- | --- | --- |
| `raw/` | Optional managed copies of source notes. | {used or not used} |
| `daily/` | Daily execution analyses. | {filename convention} |
| `weekly/` | Weekly execution analyses. | {filename convention} |
| `monthly/` | Monthly execution reports. | {filename convention} |
| `annual/` | Annual execution reviews. | {filename convention} |
| `context/` | Project and knowledge-base summaries. | {refresh rule} |

## Source locations

| location | type | handling |
| --- | --- | --- |
| `{path}` | `{local folder | mounted device | user-provided file | Obsidian vault | project context}` | `{read in place | copy to raw | summarize only | write target}` |

## Task notation assumptions

- Completed marker: `✓`
- Abandoned marker: `✗` or `X`
- Incomplete marker: no status marker
- Subtask marker: `↳`
- Urgent marker: `*`
- Other observed notation: {none or mapping}

## Analysis cadence

- Daily analysis trigger: `{explicit user request | changed source | all new notes}`
- Weekly trigger: `5+ weekday analyses, elapsed week with at least 1 daily analysis, or explicit request`
- Monthly trigger: `4+ weekly analyses, elapsed month with at least 1 weekly analysis, or explicit request`
- Annual trigger: `12 monthly reports, elapsed year with at least 1 monthly report, or explicit request`
- Re-analysis rule: `{source newer than output | forced | manual only}`

## Project context

- `task_context.md` path: `{path or none}`
- Context output folder: `context/`
- Matching method: `{keyword | semantic if available | manual}`
- Context refresh rule: `{source changed | forced | manual}`
- Excluded folders: `.git`, `node_modules`, virtualenvs, build output, generated files, datasets, binaries, and other large irrelevant folders.

## Obsidian integration

- Target vault: `{path or none}`
- Obsidian settings inspected: `{yes | no | partial | not applicable}`
- Output placement in vault: `{folder or not applicable}`
- Link convention: `{WikiLinks | existing convention | not applicable}`
- Graph entry points: `{index, MOC, project note, source note, or none}`
- Integration status: `{not requested | planned | complete | partial | blocked}`

## Current source inventory

| source | date or period | type | status | output |
| --- | --- | --- | --- | --- |
| `{path}` | `{YYYY-MM-DD}` | `{text | image | PDF | daily analysis | weekly analysis | monthly report}` | `{queued | processed | reanalyze | skipped}` | `{path}` |

## Known issues

- {ambiguous dates, unreadable handwriting, stale project context, missing lower-level analyses, broken Obsidian links, duplicate outputs, or user decisions needed}
```

## Rules

- Keep the manifest factual and operational. Do not turn it into a retrospective.
- Update it when workspace paths, filename conventions, context sources, Obsidian integration, or re-analysis rules change.
- Do not list sensitive task-note content in the manifest. Use paths, dates, and statuses only.
