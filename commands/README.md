# commands/

Plain Markdown prompts intended for explicit slash command-style invocation. These are the source prompts for task-specific workflows: each file tells one agent how to perform a bounded action against real repository context — code, tests, diffs, plans, or logs.

## analysis, audit, and debugging

- `/abstract-codebase` - targeted structural and maintainability review for a file or module
- `/cleanup-repo` - read-only audit for behavioral defects and unreachable code
- `/investigate-issue` - root-cause investigation from workflow errors and intermediate output
- `/inspect-prompts` - audit of prompts, agent instructions, and model-facing text against actual behavior
- `/test-audit` - test-suite audit for behavior coverage, reachability, isolation, and maintainability

## planning and implementation workflow

These commands form a plan lifecycle: build a plan (`/create-plan`), check it against the codebase (`/fit-plan-to-codebase`), pressure-test it (`/cross-examine`), fold findings back in (`/apply-plan-updates`), execute it (`/implement-plan`), then audit the resulting change set against the plan (`/audit-plan-implementation`).

- `/create-plan` - build an implementation plan from findings, diffs, diagnostics, or requests
- `/fit-plan-to-codebase` - check whether a plan fits the current codebase and existing abstractions
- `/cross-examine` - interactive pressure-test of a plan through focused questioning
- `/apply-plan-updates` - update a plan using findings from investigation, fit review, risk review, or user feedback
- `/implement-plan` - execute a provided plan in order with ongoing verification
- `/audit-plan-implementation` - audit a plan's resulting code changes against callers, contracts, and regressions

## documentation and communication

- `/annotate-code` - synchronize README files, docstrings, and code comments with implementation
- `/humanize-text` - rewrite target text into natural, concise, human-sounding prose while preserving meaning
- `/write-mr` - write a merge request title and description from actual branch history and diff
- `/agent-handoff` - write a redacted handoff document, outside the workspace, so a fresh agent or agent team can resume the work

## repository execution workflow

- `/yeet` - end-to-end repository workflow for preflight, triage, commit, push, and merge request creation. The largest command in the directory, and deliberately kept as an explicit command rather than a skill: it drives high-risk, stateful git operations that should only run on exact user invocation.

## How to use

Use these files when your harness supports explicit user-invoked slash commands or named prompt templates.

1. choose a command file that matches the task,
2. register it in your harness as a slash command or reusable prompt,
3. invoke it with the relevant repo context, plan file, diff, or logs.

Examples:

- use `/investigate-issue` for CI failures or broken workflow output
- use `/audit-plan-implementation` to review a plan's resulting change set for contract drift and regressions
- use `/annotate-code` to update docs and comments without changing executable code
- use `/agent-handoff` to save a redacted session summary outside the workspace for a fresh agent or team of agents
- use `/humanize-text` to rewrite text so it sounds natural, concise, and less generated
- use `/yeet` only when you want the agent to drive the full commit and MR flow explicitly

Several commands have skill counterparts in `skills/` (`annotate`, `audit`, `fit`, `humanize`, `investigate`) for harnesses that route by natural-language intent instead of explicit invocation. See the main README for guidance on choosing between the two forms.
