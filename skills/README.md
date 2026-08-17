# skills/

Reusable procedures for harnesses that select capabilities from natural-language intent. Routable skills carry YAML front matter with a name, description, and optional tool or argument metadata. Keep that front matter intact when installing them.

The directory contains three forms:

- **Single-file skills** contain a complete, bounded procedure in one Markdown file.
- **Multi-file skills** use a directory-level `SKILL.md` entry point and load workflow, format, or reference files on demand.
- **Standalone workflow definitions** contain a complete multi-phase orchestration procedure in one file and may require explicit selection rather than front-matter routing.

## Single-file skills

- `repo-explorer.md` - clone and inspect external repositories in the reusable `~/.explore/repos` cache without cluttering the active workspace.
- `sub-agents.md` - select a model and thinking level and construct prompts for delegation through the Agent tool, Workflow tool, or Codex CLI.

## Standalone workflow definition

- `simplification-audit-to-pr.md` - evidence-gated workflow for auditing a repository, planning and reviewing accepted simplifications, implementing and verifying them, and optionally committing and opening a PR or MR when explicitly authorized.

## Multi-file skills

### `code-review/`

Review a diff from a user-supplied fixed point along two independent axes: repository standards and originating specification. Parallel reviewers report their results side by side without merging or reranking findings across axes.

- `SKILL.md` - fixed-point resolution, standards and specification discovery, parallel review prompts, and aggregation rules.
- `SMELL-BASELINE.md` - fallback code-smell checklist used as judgment guidance when repository standards do not address a concern.
- `ISSUE-TRACKER-GITHUB.md`, `ISSUE-TRACKER-GITLAB.md`, `ISSUE-TRACKER-LOCAL.md` - specification lookup for GitHub, GitLab, or local `.scratch/` sources.

### `knowledge-graph/`

Create, update, parse, audit, and analyze coverage of Obsidian-compatible knowledge bases. The skill also records confirmed project facts as timestamped append-only notes, migrates processed source files into an approval-gated `50_Reference/` archive outside the indexed note space, and can produce retrieval-oriented vault abstracts.

- `SKILL.md` - entry point, workspace conventions, default posture, project-fact capture, reference migration, coverage analysis, and safety rules.
- `WORKFLOW.md` - scoping, source inventory, extraction, note construction, subagent topology, validation, coverage analysis, maintenance, and audits.
- `NOTE-FORMAT.md`, `PROJECT-FACT-FORMAT.md`, `SOURCE-REGISTER-FORMAT.md` - note and provenance templates.
- `VAULT-MANIFEST-FORMAT.md`, `VAULT-AUDIT-FORMAT.md`, `COVERAGE-ANALYSIS-FORMAT.md`, `VAULT-ABSTRACT-FORMAT.md` - vault convention, validation, coverage, and retrieval-summary templates.
- `references/OBSIDIAN-SYNTAX.md`, `references/BASES.md`, `references/CANVAS.md`, `references/OBSIDIAN-CLI.md` - Obsidian Markdown, Bases, JSON Canvas, and optional CLI guidance.

### `research/`

Build an evidence-backed research brief through goal setting, parallel source discovery, source verification, claim extraction, skeptic review, and synthesis. Material claims must trace to verified sources.

- `SKILL.md` - entry point, durable workspace files, default posture, and clarification rules.
- `WORKFLOW.md` - phase gates, subagent topology, parallelization limits, evidence checks, skeptic review, and synthesis.
- `GOAL-FORMAT.md`, `SOURCE-REGISTER-FORMAT.md`, `CLAIMS-MATRIX-FORMAT.md`, `SYNTHESIS-FORMAT.md` - templates for scope, source status, claim evidence, and the final brief.

### `teach/`

Maintain a stateful teaching workspace grounded in the learner's mission and learning history. It separates knowledge acquisition from skill practice and produces self-contained HTML lessons plus reusable reference assets. Its front matter sets `disable-model-invocation: true`, so it must be invoked explicitly rather than selected automatically.

- `SKILL.md` - workspace state, teaching philosophy, lesson design, assets, mission handling, learning progression, reference documents, and notes.
- `MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md` - templates for goals, sources, learning records, and glossaries.

### `tldr/`

Summarize technical material with a fixed template selected by document type. Optional stages synthesize multiple summaries, research knowledge gaps, polish structure and style, and evaluate summary quality.

- `SKILL.md` - ingest, classify, summarize, title, and save workflow plus shared guardrails.
- `references/summary-publication.md`, `references/summary-document.md`, `references/summary-readme.md`, `references/summary-other.md` - per-type summary templates.
- `references/executive-summary.md`, `references/gap-research.md`, `references/polishing.md`, `references/evaluation.md` - optional synthesis, research, editing, and scoring stages.

## How to use

1. Install a single skill file or an entire multi-file skill directory where the target harness discovers reusable skills.
2. Keep relative support files beside their entry point.
3. Preserve YAML front matter on routable skills so the harness can match user intent and enforce declared tool constraints.
4. Invoke `simplification-audit-to-pr.md` explicitly if the harness does not route files without front matter.
