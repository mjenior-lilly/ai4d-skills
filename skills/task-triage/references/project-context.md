# Project Context: Summarization and Injection

Project-context summaries give daily analyses technical background about what the
user is actually working on. Weekly/monthly/annual analyses never receive context
injection — daily only.

## task_context.md

Lives in the working directory (override with `--context-file`). One project
directory per line; `#` comments; optional `label: /path` syntax; `~` expansion:

```markdown
# Auto-labeled by directory name
/home/user/repos/my-api
# Custom label
frontend: ~/repos/react-app
```

Summaries and manifests are stored in `local_context/` (override `--context-dir`):
`{label}.context.md` (the summary) and `{label}.context.meta.json` (mtime manifest
for change detection). Labels are sanitized for filesystem safety by the script.

## Generating / refreshing summaries

1. `triage.py context-scan` lists each project with a `stale` flag (true when no
   summary exists or eligible file mtimes changed; `--force` marks all stale).
   Only re-summarize stale projects — this is the cost-control mechanism.
2. For each stale project, read the codebase yourself (README and config first, then
   key source; skip build artifacts, vendored deps, and generated files — the script's
   exclusion list is the guide; stay within roughly 150K characters of source).
3. Write the summary as a senior software architect reviewing the codebase, with
   exactly these sections, each 3-8 bullets or a short paragraph, specific and
   evidence-based with real file paths:
   - **Purpose and Overview** — what it does, who it's for, problem solved
   - **Technology Stack** — languages, frameworks, runtimes, key libraries
   - **Architecture Overview** — components, interactions, data flow, deployment model
   - **Key Patterns and Conventions** — style, naming, design patterns, idioms
   - **Important Files and Entry Points** — where to start reading; CLI/API/main; config
   - **External Dependencies and Integrations** — services, APIs, databases, third parties
   - **Current State and Notable Concerns** — tech debt, incomplete features, known issues
4. Save to `local_context/{label}.context.md` with this header:

```
<!-- Context Summary: {label} -->
<!-- Source: {source_path} -->
<!-- Generated: {ISO timestamp} -->

# Project Context: {label}
```

5. Run `triage.py context-mark LABEL SOURCE_PATH` to record the mtime manifest so
   unchanged projects are skipped next time.

## Injecting context into a daily analysis

Before analyzing a day's notes, if `local_context/` contains summaries:

1. Read the task notes and judge which projects they plausibly relate to — match on
   project names, technologies, task vocabulary, and conceptual overlap, not just
   literal keywords.
2. Select at most **2** clearly relevant projects; when nothing is clearly relevant,
   inject nothing.
3. Append the selected summaries (body only — skip the HTML-comment header and the
   `# Project Context:` title line) to the task notes before analysis:

```
## Relevant Project Context

The following project contexts are relevant to today's tasks:

### Project: {label}
{summary body}
```

Context injection is optional enrichment — if summaries are missing or unreadable,
proceed with the analysis without them.
