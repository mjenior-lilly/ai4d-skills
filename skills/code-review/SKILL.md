---
name: code-review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

## Process

### 1. Pin the fixed point

Use whatever the user specified as the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask.

Run `git rev-parse <fixed-point>`. If it exits non-zero, stop and tell the user the ref does not resolve — do not proceed.

Capture the diff command: `git diff <fixed-point>...HEAD` (three-dot, merge-base comparison). Also capture `git log <fixed-point>..HEAD --oneline`.

If the diff output is empty (zero bytes), stop and tell the user there are no changes to review — do not proceed.

### 2. Identify the spec source

Search for the originating spec in this order. At each step, if not found, proceed to the next:

1. **Issue references in commit messages** (`#123`, `Closes #45`, GitLab `!67`, etc.) — detect the tracker and fetch:
   - Check `git remote -v`:
     - Contains `github.com` → use the workflow in [ISSUE-TRACKER-GITHUB.md](ISSUE-TRACKER-GITHUB.md).
     - Contains `gitlab.com` or `gitlab` in the hostname → use [ISSUE-TRACKER-GITLAB.md](ISSUE-TRACKER-GITLAB.md).
   - If no remote matches but `.scratch/` exists with spec/issue files → use [ISSUE-TRACKER-LOCAL.md](ISSUE-TRACKER-LOCAL.md).
   - If detection fails, ask the user which tracker to use.
2. **A path the user passed as an argument.**
3. **A PRD/spec file in the repo** — search for markdown files whose name or path matches the branch name or feature keyword (common locations: project root or `.scratch/`).
4. **Ask the user.** If they confirm no spec exists, skip the Spec sub-agent entirely and record in the final report: `## Spec\n\nNo spec source identified. Spec axis skipped.`

### 3. Identify the standards sources

Find anything in the repo that documents how code should be written — `CODING_STANDARDS.md`, `CONTRIBUTING.md`, style guides, etc.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** from [SMELL-BASELINE.md](SMELL-BASELINE.md). Read that file and include its full content in the Standards sub-agent prompt — the sub-agent has no other access to it.

### 4. Spawn both sub-agents in parallel

Send a single message with two `Agent` tool calls. Use the `general-purpose` subagent type for both.

If the diff exceeds ~200 KB when inlined, pass only the diff command (not the inline diff) and instruct the sub-agent to run it — it has shell access.

**Standards sub-agent prompt:**

```
You are reviewing a diff for coding-standards compliance.

Diff command: `{{diff_command}}`
Commits:
{{commit_list}}

Standards sources (read these files for the repo's rules): {{standards_file_paths}}

Smell baseline (apply as judgement calls — never hard violations):
{{full content of SMELL-BASELINE.md}}

Brief: Report — per file/hunk where relevant —
(a) every place the diff violates a documented standard: cite the standard (file + the rule);
(b) any baseline smell you spot: name it and quote the hunk.

Distinguish hard violations from judgement calls. Documented-standard breaches are hard violations; baseline smells are always judgement calls. A documented repo standard overrides the baseline — suppress any smell it endorses. Skip anything tooling already enforces (linters, formatters, type checks).

Budget: under 400 words.
```

**Spec sub-agent prompt:**

```
You are reviewing a diff for spec compliance.

Diff command: `{{diff_command}}`
Commits:
{{commit_list}}

Spec content:
{{spec_body or path to spec file}}

Brief: Report —
(a) requirements the spec asked for that are missing or partial in the diff;
(b) behaviour in the diff that the spec did not ask for (scope creep);
(c) requirements that look implemented but where the implementation appears incorrect.

Quote the spec line for each finding. Budget: under 400 words.
```

If the spec is unavailable (step 2 terminal state), do not spawn the Spec sub-agent.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings. Do **not** merge or rerank findings — the two axes are deliberately separate (see _Why two axes_ below).

Allowed edits to sub-agent output: remove duplicate blank lines, prepend a finding count (`N findings`). Do not reword, reorder, or merge findings across axes.

End with a one-line summary: total findings per axis, and the single worst finding _within each axis_ (if any). Do not pick a winner across axes — that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
