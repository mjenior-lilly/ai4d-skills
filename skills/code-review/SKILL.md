---
name: code-review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes. Standards asks whether the code follows the repo's documented coding standards; Spec asks whether the code matches the originating issue or PRD. Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue, PRD, or spec?

Run both axes as **parallel sub-agents** with separate contexts, then aggregate their findings.

## Process

### 1. Pin the fixed point

Use the fixed point the user specified, such as a commit SHA, branch name, tag, `main`, or `HEAD~5`. If they did not specify one, ask.

Run `git rev-parse <fixed-point>`. If it exits non-zero, stop and tell the user the ref does not resolve.

Capture the diff command: `git diff <fixed-point>...HEAD` (three-dot, merge-base comparison). Also capture `git log <fixed-point>..HEAD --oneline`.

If the diff output is empty (zero bytes), stop and tell the user there are no changes to review.

### 2. Identify the spec source

Search for the originating spec in this order. At each step, if not found, proceed to the next:

1. **Issue references in commit messages** (`#123`, `Closes #45`, GitLab `!67`, etc.). Detect the tracker and fetch the issue:
   - Check `git remote -v`:
     - Contains `github.com` → use the workflow in [ISSUE-TRACKER-GITHUB.md](ISSUE-TRACKER-GITHUB.md).
     - Contains `gitlab.com` or `gitlab` in the hostname → use [ISSUE-TRACKER-GITLAB.md](ISSUE-TRACKER-GITLAB.md).
   - If no remote matches but `.scratch/` exists with spec or issue files, use [ISSUE-TRACKER-LOCAL.md](ISSUE-TRACKER-LOCAL.md).
   - If detection fails, ask the user which tracker to use.
2. **A path the user passed as an argument.**
3. **A PRD or spec file in the repo.** Search for Markdown files whose name or path matches the branch name or feature keyword, commonly in the project root or `.scratch/`.
4. **Ask the user.** If they confirm no spec exists, skip the Spec sub-agent entirely and record in the final report: `## Spec\n\nNo spec source identified. Spec axis skipped.`

### 3. Identify the standards sources

Find the repo's coding guidance, such as `CODING_STANDARDS.md`, `CONTRIBUTING.md`, and style guides.

Always apply the **smell baseline** from [SMELL-BASELINE.md](SMELL-BASELINE.md) alongside the repo's documented standards. Read the file and include its full content in the Standards sub-agent prompt because the sub-agent cannot access it directly.

### 4. Spawn both sub-agents in parallel

Send a single message with two `Agent` tool calls. Use the `general-purpose` subagent type for both.

If the inlined diff exceeds ~200 KB, pass only the diff command and tell the sub-agent to run it with its shell access.

**Standards sub-agent prompt:**

```
You are reviewing a diff for coding-standards compliance.

Diff command: `{{diff_command}}`
Commits:
{{commit_list}}

Standards sources (read these files for the repo's rules): {{standards_file_paths}}

Smell baseline (apply as judgement calls, never hard violations):
{{full content of SMELL-BASELINE.md}}

Brief: For each relevant file or hunk, report:
(a) every place the diff violates a documented standard: cite the standard (file + the rule);
(b) any baseline smell you spot: name it and quote the hunk.

Classify documented-standard breaches as hard violations and baseline smells as judgement calls. If a documented repo standard endorses something the baseline would flag, suppress that smell. Skip anything tooling already enforces (linters, formatters, type checks).

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

Brief: Report:
(a) requirements the spec asked for that are missing or partial in the diff;
(b) behaviour in the diff that the spec did not ask for (scope creep);
(c) requirements that look implemented but where the implementation appears incorrect.

Quote the spec line for each finding. Budget: under 400 words.
```

If the spec is unavailable (step 2 terminal state), do not spawn the Spec sub-agent.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings. Do **not** merge or rerank findings because the two axes are deliberately separate (see _Why two axes_ below).

Allowed edits to sub-agent output: remove duplicate blank lines, prepend a finding count (`N findings`). Do not reword, reorder, or merge findings across axes.

End with a one-line summary that gives the total findings and worst finding, if any, within each axis. Do not pick a winner across axes because that would rerank them.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
