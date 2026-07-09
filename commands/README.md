# commands/

Plain Markdown prompts intended for explicit slash command-style invocation. These are the source prompts for task-specific workflows: each file tells one agent how to perform a bounded action against real repository context — code, tests, diffs, plans, or logs.

## analysis, audit, and debugging

- `/abstract` - targeted structural and maintainability review for a file or module
- `/agentify` - multi-agent repository analysis for LLM navigability, static traceability, context locality, and autonomous change safety
- `/audit` - change-set audit against callers, contracts, and regressions
- `/cleanup` - read-only audit for behavioral defects and unreachable code
- `/investigate` - root-cause investigation from workflow errors and intermediate output
- `/prompts` - audit of prompts, agent instructions, and model-facing text against actual behavior
- `/test-audit` - test-suite audit for behavior coverage, reachability, isolation, and maintainability

## planning and implementation workflow

These commands form a plan lifecycle: build a plan (`/plan`), check it against the codebase (`/fit`), pressure-test it (`/grill`), resolve its open risks (`/risks`), fold findings back in (`/apply`), then execute it (`/implement`).

- `/apply` - update an implementation plan using findings and critique
- `/fit` - check whether a plan fits the current codebase and existing abstractions
- `/grill` - interactive pressure-test of a plan through focused questioning
- `/implement` - execute a provided plan in order with ongoing verification
- `/plan` - build an implementation plan from findings, diffs, diagnostics, or requests
- `/risks` - resolve plan risks, assumptions, and open questions back into the plan

## documentation and communication

- `/annotate` - synchronize README files, docstrings, and code comments with implementation
- `/specs` - write a redacted temporary specsheet document for a fresh agent, with artifact references and suggested skills
- `/humanize` - rewrite target text into natural, concise, human-sounding prose while preserving meaning
- `/write-mr` - write a merge request title and description from actual branch history and diff

## repository execution workflow

- `/yeet` - end-to-end repository workflow for preflight, triage, commit, push, and merge request creation. The largest command in the directory, and deliberately kept as an explicit command rather than a skill: it drives high-risk, stateful git operations that should only run on exact user invocation.

## How to use

Use these files when your harness supports explicit user-invoked slash commands or named prompt templates.

1. choose a command file that matches the task,
2. register it in your harness as a slash command or reusable prompt,
3. invoke it with the relevant repo context, plan file, diff, or logs.

Examples:

- use `/investigate` for CI failures or broken workflow output
- use `/audit` to review a branch or diff for contract drift and regressions
- use `/agentify` to score a repository's agent readiness and identify structural friction for LLM coding agents
- use `/annotate` to update docs and comments without changing executable code
- use `/specs` to save a redacted session summary outside the workspace for a fresh agent or team of agents
- use `/humanize` to rewrite text so it sounds natural, concise, and less generated
- use `/yeet` only when you want the agent to drive the full commit and MR flow explicitly

Several commands have skill counterparts in `skills/` (`annotate`, `audit`, `fit`, `humanize`, `investigate`) for harnesses that route by natural-language intent instead of explicit invocation. See the main README for guidance on choosing between the two forms.
