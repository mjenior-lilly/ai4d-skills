# AI4D - Skills

My personal prompt library to use across LLM harness platforms for work within the AI4Discovery group.

The content is oriented toward code review, debugging, planning, documentation sync, response style control, prompt auditing, agent-readiness analysis, deep research, benchmark generation, teaching workspaces, knowledge-base construction, task triage, document summarization, repository workflow execution, lightweight classification for routing, and copy-paste prompts for web tools. Most files are written as operational instructions for an agent working in a real repository with access to code, tests, diffs, and shell tools.

## repository layout

Each subdirectory has its own README covering its contents, file structure, and usage patterns in detail.

### [`commands/`](commands/README.md)

Plain Markdown prompts intended for explicit slash command-style invocation. Grouped into analysis/audit/debugging (`/abstract`, `/agentify`, `/audit`, `/cleanup`, `/investigate`, `/prompts`, `/test-audit`), a plan lifecycle (`/plan`, `/fit`, `/grill`, `/risks`, `/apply`, `/implement`), documentation and communication (`/annotate`, `/specs`, `/humanize`, `/write-mr`), and full repository execution (`/yeet`).

### [`skills/`](skills/README.md)

Reusable skills for harnesses that route from natural-language intent rather than explicit slash commands. Single-file skills cover bounded tasks (`annotate`, `audit`, `fit`, `humanize`, `investigate`, `notes`, `repo-explorer`, `resolve`, `sub-agents`); multi-file skill directories encode larger workflows through a `SKILL.md` entry point plus on-demand workflow, format, reference, and script files:

- `code-review/` - two-axis diff review (standards compliance + spec compliance) using parallel sub-agents, with issue-tracker integration and a smell baseline
- `knowledge-graph/` - Obsidian-compatible knowledge-base construction, update, audit, coverage gap analysis, and append-only project-fact capture
- `research/` - deep research with parallel source discovery, source verification, claim extraction, skeptic review, and synthesis
- `teach/` - stateful teaching workspace with mission-grounded lessons, learning records, references, and reusable assets
- `tldr/` - structured document summarization with per-type templates and optional synthesis, gap research, polishing, and scoring

### [`agents/`](agents/README.md)

System prompt text and layered policy files that define baseline agent behavior: a CLI-focused coding-agent system prompt (`SYSTEM.md`), a `CLAUDE.md` entry point with on-demand companion policies for coding practices (`CODE.md`), subjective preferences (`OPINIONS.md`), and prose voice (`VOICE.md`), plus a benchmark response judge (`judge.md`), a constrained routing classifier example (`classifier.md`), and a prompt-design reference (`prompt_skeleton.md`).

### [`workflows/`](workflows/README.md)

End-to-end operating procedures for multi-phase, coordinator-plus-subagent tasks that need more than a single command invocation: corpus-grounded benchmark dataset generation (`create-test-dataset`) and simplification-audit-to-PR conversion (`unvibe-code-repo`). A workflow defines the objective, phase gates, subagent topology, model and thinking tiers, verification requirements, and stopping conditions.

### [`notebooklm/`](notebooklm/README.md)

Copy-paste prompts for NotebookLM rather than slash-command or skill invocation: a neutral, technically precise Audio Overview prompt (`podcast.md`) and a dense, diagram-first infographic prompt (`infographic.md`), both for machine learning and computational research papers.

## what kind of content lives here

This is not a general prompt dump. The repository content is opinionated and procedural.

Common characteristics across the files:

- evidence-first reasoning over speculation
- preference for repository inspection before proposing abstractions
- explicit scope control
- strong verification requirements
- direct output formats designed for practical engineering work
- separation between read-only review workflows and mutating implementation workflows

A large portion of the library is aimed at software delivery tasks such as investigating failures, auditing changes and tests, refining or applying plans, aligning docs with code, generating reviewer-facing summaries, and completing branch-to-MR workflows. The rest supports personal knowledge and productivity systems: research briefs, knowledge bases, task analysis, meeting synthesis, document summarization, and teaching workspaces. Each subdirectory README describes its content in full.

## choosing commands vs skills

Several prompts exist in both forms (`annotate`, `audit`, `fit`, `humanize`, `investigate`).

Use a command when:

- the workflow is explicit and user-driven,
- the action is high-risk or highly stateful,
- you want exact invocation semantics.

Use a skill when:

- the task recurs across many conversations,
- the workflow benefits from automatic intent matching,
- the instructions are stable and reusable.

In this repo, `yeet.md` is a good example of something better kept as an explicit command, while `investigate.md`, `audit.md`, and `repo-explorer.md` translate well into skills.
