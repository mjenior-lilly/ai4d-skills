# commands/

Plain Markdown prompts intended for explicit slash command-style invocation. Each file instructs an agent to perform a named task against repository context, source material, or the current git state.

## Investigation and audits

- `/investigate-issue` (`investigate-issue.md`) - diagnose workflow failures from supplied errors, logs, intermediate output, and relevant repository evidence.
- `/test-suite-audit` (`test-suite-audit.md`) - review a test suite for behavioral coverage, production-path reachability, isolation, duplication, and maintainability; it returns findings without editing tests unless edits are explicitly requested.
- `/slop-search` (`slop-search.md`) - run a repository-wide, read-only construction-quality audit and write one ranked report with explicit coverage and evidence. The command does not plan, implement, commit, or open a PR.

## Planning and implementation

- `/create-plan` (`create-plan.md`) - turn requests, findings, diffs, and diagnostics into a sequenced implementation plan saved as Markdown.
- `/cross-examine` (`cross-examine.md`) - pressure-test a plan through focused interview rounds using the installed `ask-user` skill and `ask_user` tool, then record decisions needed for implementation readiness.
- `/implement-plan` (`implement-plan.md`) - use read-only reconnaissance subagents to gather context, resequence and implement a supplied plan, isolate parallel writes in worktrees, verify changes, and run a fresh-context audit.
- `/audit-plan-implementation` (`audit-implementation.md`) - compare a workspace with a supplied plan, checking definitions, direct callers, boundary contracts, regressions, and omitted work.

## Repository and benchmark artifacts

- `/generate-test-dataset` (`generate-test-dataset.md`) - orchestrate corpus analysis and parallel item generation to produce a corpus-grounded adversarial benchmark dataset for use with `agents/judge.md`.
- `/map-repository` (`map-repository.md`) - orchestrate evidence gathering, synthesis, and validation to create or update an agent-focused `AGENTS.md` repository map.

## Documentation and communication

- `/annotate-code` (`annotate-code.md`) - synchronize README files, docstrings, and comments with implementation without changing executable behavior.
- `/engineer-context` (`engineer-context`) - rewrite supplied text as natural, concise prose while preserving its meaning and facts.
- `/write-branch-mr` (`write-branch-mr.md`) - inspect branch history and diff, then return a merge request title and description without changing the repository or creating an MR.
- `/agent-handoff` (`agent-handoff.md`) - write a redacted handoff document to the operating system's temporary directory for a fresh agent or agent team.

## Repository execution

- `/yeet` (`yeet.md`) - from the repository root, run the stateful branch-to-pull-request flow: preflight, triage, branch creation when needed, selective staging, commit, version handling, push, and pull request creation through an authenticated `gh` session. It requires `task` and `uv`, plus network access for preflight and remote operations, and is intentionally explicit because it mutates git and remote state.
