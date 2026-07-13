# skills/

Reusable skills for harnesses that select capabilities from natural-language intent rather than explicit slash commands. Each skill carries YAML front matter (name, description, and optionally allowed tools or an argument hint) that the harness uses to route relevant requests; keep the front matter intact when installing.

Skills come in two shapes:

- **Single-file skills** - one `.md` file containing the entire procedure. Best for bounded, stateless tasks.
- **Multi-file skills** - a directory with a `SKILL.md` entry point that loads supporting files on demand: a `WORKFLOW.md` with phase gates and subagent topology, `*-FORMAT.md` templates for generated artifacts, a `references/` directory of per-stage or per-syntax guides, and occasionally a `scripts/` directory of deterministic helpers. This structure keeps the always-loaded instruction surface small while encoding much larger workflows; the agent reads only the file for the stage it is executing.

## Single-file skills

- `annotate.md` - synchronize documentation, docstrings, and comments with the current implementation without changing executable behavior
- `audit.md` - audit a defined change set against its plan, callers, and boundary contracts
- `fit.md` - review an implementation plan for fit with the existing codebase, simplicity, and traceability
- `humanize.md` - write natural, concise, human-sounding user-facing prose for non-trivial responses
- `investigate.md` - diagnose workflow failures from actual logs, error messages, and intermediate output, without guessing
- `notes.md` - enrich handwritten Supernote meeting notes (per-page `.png` images synced via notesync) into a polished markdown artifact by mining the meeting audio recording for decisions, action items, owners, dates, risks, and follow-ups the notes missed; daily checklist pages are identified and excluded
- `repo-explorer.md` - clone and inspect external repositories in a reusable local cache (`~/.explore/repos`) without cluttering the active workspace
- `resolve.md` - resolve an in-progress git merge or rebase conflict by tracing each conflicting change back to its original intent, preserving both intents where possible, and finishing with the project's automated checks
- `sub-agents.md` - select the right model, thinking level, and prompt structure when delegating work to sub-agents via the Agent tool, Workflow tool, or Codex CLI

## Multi-file skills

### `knowledge-graph/`

Create, update, audit, and parse Obsidian-compatible local knowledge bases from technical documents, non-technical documents, code collections, meeting summaries, and task-analysis outputs. Also captures new and changing project-specific facts as timestamped, append-only notes recording confirmed ground truth (never speculation) under a vault's `40_Project/` folder. Defines a default vault structure (`00_Meta/`, `10_Fleeting/`, `20_Permanent/`, `30_Projects/`, `40_Project/`), safety rules for editing existing vaults, and a preference for generated `.base` index views over hand-maintained MOC notes.

- `SKILL.md` - entry point: workspace conventions, default posture, project-fact capture rules, safety rules
- `WORKFLOW.md` - vault scoping, source inventory, extraction, note construction, subagent topology, model and thinking tiers, validation gates, maintenance and audit procedures
- `NOTE-FORMAT.md`, `PROJECT-FACT-FORMAT.md`, `SOURCE-REGISTER-FORMAT.md`, `VAULT-MANIFEST-FORMAT.md`, `VAULT-AUDIT-FORMAT.md` - templates for permanent notes, project-fact log entries, source provenance registers, vault convention manifests, and validation reports
- `references/OBSIDIAN-SYNTAX.md` - Obsidian Flavored Markdown: wikilinks, heading/block references, embeds, callouts, tags, footnotes, math, Mermaid
- `references/BASES.md` - Obsidian Bases (`.base`) live index views over note frontmatter
- `references/CANVAS.md` - JSON Canvas (`.canvas`) visual artifacts: mind maps and architecture diagrams that embed vault notes
- `references/OBSIDIAN-CLI.md` - the `obsidian` CLI as an optional backend for live-vault interaction and validation

### `research/`

Deep research workflow treating every question as an evidence-building exercise, not a memory recall: goal-setting, parallel source discovery, source existence verification (a search snippet is not a source), claim extraction, skeptic review, and synthesis. Every material claim in the final brief must trace to a verified source.

- `SKILL.md` - entry point: workspace files, default posture, when to ask before proceeding
- `WORKFLOW.md` - goal decision phase, subagent topology, model and thinking tiers, parallelization limits, verification gates, skeptic review points, synthesis requirements
- `GOAL-FORMAT.md`, `SOURCE-REGISTER-FORMAT.md`, `CLAIMS-MATRIX-FORMAT.md`, `SYNTHESIS-FORMAT.md` - templates for the research goal, the canonical source register, the claim-to-source evidence ledger, and the final research brief

### `teach/`

Stateful teaching workspace for learning a topic over multiple sessions. Grounds every lesson in a mission (why the user wants to learn), tracks progress via numbered learning records used to calculate the zone of proximal development, and separates knowledge acquisition (difficulty is the enemy) from skill practice (difficulty is the tool: retrieval practice, spacing, interleaving). Lessons are self-contained HTML files built from reusable components in `./assets/`, alongside printable reference documents and a resource register of high-trust sources.

- `SKILL.md` - entry point: workspace files, teaching philosophy, lesson design, assets, mission handling, knowledge/skills/wisdom split
- `MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md` - templates for the mission document, resource register, learning records, and topic glossaries

### `code-review/`

Two-axis review of a diff between `HEAD` and a user-supplied fixed point (commit, branch, tag, or merge-base). Runs a **Standards** axis (does the code follow this repo's documented coding standards and a smell baseline?) and a **Spec** axis (does the code match what the originating issue/PRD asked for?) as parallel sub-agents, then aggregates their findings side by side without merging or reranking across axes.

- `SKILL.md` - entry point: fixed-point resolution, spec source detection, standards discovery, sub-agent prompts, aggregation rules, rationale for two-axis separation
- `SMELL-BASELINE.md` - default code-smell checklist applied as judgement calls (never hard violations) when no repo standard addresses a concern
- `ISSUE-TRACKER-GITHUB.md` - workflow for fetching issue/PR spec content from GitHub remotes
- `ISSUE-TRACKER-GITLAB.md` - workflow for fetching issue/MR spec content from GitLab remotes
- `ISSUE-TRACKER-LOCAL.md` - workflow for locating spec content in local `.scratch/` files when no remote tracker is detected

### `tldr/`

Structured technical document summarization: classify each source as `publication`, `document`, `readme`, or `other`, then summarize with that type's fixed template — reading only the reference file for the stage being executed. Shared guardrails enforce completeness over brevity, all template sections present, objectivity, and a tone suited to cross-functional technical readers. Optional downstream stages: multi-document executive synthesis, gap analysis with web research, reorganization/stylistic polishing, and rubric-based summary quality scoring.

- `SKILL.md` - entry point: ingest → classify → summarize → title/save workflow, shared guardrails
- `references/summary-publication.md`, `summary-document.md`, `summary-readme.md`, `summary-other.md` - per-type summary templates
- `references/executive-summary.md` - synthesis of 2+ summaries on a common topic
- `references/gap-research.md` - identifying under-explained concepts and answering them via web search
- `references/polishing.md` - reorganizing poorly structured technical text, with optional stylistic rewrite
- `references/evaluation.md` - weighted-rubric scoring of a summary against its source, with multi-report consolidation

## How to use

1. place the skill file (or the whole skill directory, for multi-file skills) where your harness expects reusable skills,
2. keep the front matter intact so the harness can read the skill name, description, and allowed tools,
3. rely on the description text to route relevant natural-language requests to the right skill.

Skills in this repo are best suited to recurring, high-signal workflows such as investigation, audits, planning, documentation sync, response style control, repository exploration, deep research, knowledge-base maintenance, sub-agent orchestration, task triage, document summarization, and stateful teaching.
