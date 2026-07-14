---
name: knowledge-graph
description: Create, update, audit, and parse Obsidian-compatible local knowledge bases from user-provided technical documents, non-technical documents, code collections, meeting summaries, and task-analysis outputs. Also captures new and changing project-specific facts as timestamped, append-only project-fact notes that record confirmed ground truth, not speculation. Analyzes coverage gaps to identify areas with thin or missing source grounding and recommends additional resources to strengthen the vault as an agent grounding source. Covers Obsidian Flavored Markdown syntax (wikilinks, embeds, callouts, block references, properties, tags), Bases (.base) index views, JSON Canvas (.canvas), and the Obsidian CLI.
argument-hint: "What documents, code, or vault should be converted or maintained?"
---

The user has asked you to work with an Obsidian-compatible local knowledge base. Optimize only for Obsidian vaults: local folders of Markdown files, Obsidian WikiLinks, YAML frontmatter, attachments, and Obsidian indexing behavior. Do not generalize the workflow for other note platforms, static-site generators, or publishing systems unless the user explicitly asks in a separate task.

Use the workflow in [WORKFLOW.md](./WORKFLOW.md). It defines vault scoping, source inventory, extraction, note construction, subagent topology, model and thinking tiers, validation gates, and maintenance/audit procedures.

Syntax and artifact references, loaded on demand:

- [VAULT-ABSTRACT-FORMAT.md](./VAULT-ABSTRACT-FORMAT.md): LLM-optimized vault abstract — concise scope, taxonomy, source profile, coverage strengths, known gaps, and semantic descriptors for retrieval routing. Use after coverage analysis to generate `00_Meta/VAULT-ABSTRACT.md`.
- [references/OBSIDIAN-SYNTAX.md](./references/OBSIDIAN-SYNTAX.md): Obsidian Flavored Markdown — wikilinks, heading/block references, embeds, callouts, tags, highlights, comments, footnotes, math, Mermaid. Consult when composing or repairing note bodies.
- [references/BASES.md](./references/BASES.md): Obsidian Bases (`.base`) live index views. Use to replace hand-maintained MOC/index notes and static source tables with auto-updating queries over note frontmatter.
- [references/CANVAS.md](./references/CANVAS.md): JSON Canvas (`.canvas`) visual artifacts — mind maps, architecture and concept diagrams that can embed vault notes.
- [references/OBSIDIAN-CLI.md](./references/OBSIDIAN-CLI.md): the `obsidian` CLI as an optional, more reliable backend for live-vault interaction and validation when Obsidian is running.

## Obsidian workspace

Treat the user-named directory as the workspace and write all generated or updated notes inside it. Do not leave note artifacts in the current working directory, a temporary folder, or chat output when the user has provided a target knowledge base.

If the user has not named a directory and the current directory looks like an Obsidian knowledge base, use it. A directory looks like a knowledge base when it contains `.obsidian/`, a meaningful set of `.md` files, or an obvious structure such as `00_Meta/`, `10_Fleeting/`, `20_Permanent/`, or `30_Projects/`.

When creating a new knowledge base, name the top-level directory `{{topic}}-kb` (e.g., `metabolomics-kb`, `platform-architecture-kb`, `drug-discovery-kb`) so the purpose is immediately clear from the directory name alone. Use a short, lowercase, hyphenated slug derived from the domain or project the knowledge base covers. Do not use generic names like `vault/`, `notes/`, `kb/`, or `knowledge-base/` without a qualifying topic prefix. If the user provides an explicit directory name, use that instead.

Use this default internal structure unless the user provides an existing convention:

- `00_Meta/Templates/`: reusable note templates.
- `00_Meta/Attachments/`: images, PDFs, diagrams, and other binary files.
- `00_Meta/Sources/`: source registers, ingestion notes, and provenance ledgers.
- `10_Fleeting/`: temporary triage notes, rough imports, and scratch work.
- `20_Permanent/`: evergreen concept notes intended for long-term retrieval.
- `30_Projects/`: project-specific or time-bound notes.
- `40_Project/`: timestamped, append-only notes logging new and changing project-specific facts — confirmed ground truth, not speculation.

Create files lazily as they become useful, always under the knowledge base root:

- `00_Meta/VAULT-MANIFEST.md`: vault conventions, folder roles, filename rules, link style, required frontmatter fields, and known exclusions. Use [VAULT-MANIFEST-FORMAT.md](./VAULT-MANIFEST-FORMAT.md).
- `00_Meta/Sources/SOURCE-REGISTER.md`: source inventory, provenance, processing status, and extraction coverage. Use [SOURCE-REGISTER-FORMAT.md](./SOURCE-REGISTER-FORMAT.md).
- `00_Meta/VAULT-AUDIT.md`: validation findings for filenames, links, frontmatter, tags, attachments, duplicates, and indexer risks. Use [VAULT-AUDIT-FORMAT.md](./VAULT-AUDIT-FORMAT.md).
- `00_Meta/COVERAGE-ANALYSIS.md`: coverage gap analysis identifying concept clusters with thin or missing source grounding, source concentration risks, and prioritized recommendations for additional resources to strengthen agent grounding. Use [COVERAGE-ANALYSIS-FORMAT.md](./COVERAGE-ANALYSIS-FORMAT.md).
- `00_Meta/VAULT-ABSTRACT.md`: LLM-optimized vault content summary for relevance determination and grounding search routing. Synthesizes scope, taxonomy, source profile, coverage strengths, known gaps, and semantic descriptors so a retrieval system or grounding agent can decide in one pass whether this vault is the correct resource for a given query. Use [VAULT-ABSTRACT-FORMAT.md](./VAULT-ABSTRACT-FORMAT.md).
- Permanent notes under `20_Permanent/`: evergreen, source-grounded Markdown notes. Use [NOTE-FORMAT.md](./NOTE-FORMAT.md).
- Project-fact notes under `40_Project/`: timestamped, append-only records of new and changed project-specific facts on in-scope topics. Use [PROJECT-FACT-FORMAT.md](./PROJECT-FACT-FORMAT.md).
- Project notes, meeting notes, task analyses, or generated summary artifacts under the appropriate existing vault folder, or under `30_Projects/` when they are time-bound rather than evergreen.
- Task-analysis outputs from the `tasks` skill under `30_Projects/Task Reviews/` by default when no existing daily-note, review, or productivity folder convention exists.

## Default posture

- Preserve Obsidian compatibility over general Markdown portability.
- When the user provides a target knowledge base, integrate generated notes into that vault's graph: choose vault-relative paths, add frontmatter, use vault link conventions, update source provenance, and add backlinks or index links so the notes are discoverable.
- Prefer WikiLinks in body text unless the existing vault manifest requires another Obsidian-supported convention. Use the full WikiLink, embed, callout, and block-reference syntax in [references/OBSIDIAN-SYNTAX.md](./references/OBSIDIAN-SYNTAX.md) to make notes navigable rather than flat.
- Prefer a generated `.base` index ([references/BASES.md](./references/BASES.md)) over a hand-maintained static index/MOC when a domain or source cluster needs a note listing, so the index stays current automatically.
- Use typed frontmatter properties (text, number, checkbox, date, date-time, list, link) so notes are queryable by Bases and Dataview, not just human-readable.
- Keep filenames unique across the vault so `[[Note Title]]` links do not require brittle folder paths.
- Keep folder nesting shallow, ideally no more than 2-3 levels below the vault root.
- Put YAML frontmatter as the first content in each permanent note.
- Use strict YAML: quote strings containing colons or special characters, omit `#` from frontmatter tags, and use arrays for multi-value fields.
- Centralize attachments under `00_Meta/Attachments/` unless the vault already has a configured attachment folder.
- Do not dump entire long documents or source files into permanent notes. Extract stable concepts, claims, APIs, workflows, definitions, and decision-relevant relationships.
- Keep source provenance explicit. Every important note should identify the source document, code path, section, page, line range, commit, or other locator that supports it.
- Record only confirmed ground truth; never present speculation, predictions, or hypothetical discussion as vault fact. Log new and changing project-specific facts as timestamped, provenance-anchored project-fact notes ([PROJECT-FACT-FORMAT.md](./PROJECT-FACT-FORMAT.md)); a stable fact can graduate into a permanent note's `Source grounding` once well-established.
- For code collections, create human-readable concept, architecture, API, and workflow notes. Avoid copying large code blocks; use short snippets only when they clarify a stable interface or non-obvious mechanism.
- For task-analysis outputs, preserve the generated daily, weekly, monthly, or annual analysis as a time-bound artifact; extract only durable planning principles, recurring patterns, or project-relevant commitments into permanent notes when they are useful beyond the reviewed period.

## Project-fact capture

While working with the user's vault, watch for new or changed project-specific facts on topics the knowledge base covers — a decision that was made, a state that changed, or a concrete detail that has been confirmed. When one arises, log it as a timestamped project-fact note under `40_Project/` using [PROJECT-FACT-FORMAT.md](./PROJECT-FACT-FORMAT.md), link it to the subject topic note, and record it append-only so the temporal record of how the project's ground truth evolved is preserved.

- Record only confirmed ground truth. Do not log speculation, predictions, proposals, or hypothetical discussion. If a statement cannot be confirmed, hold it in `10_Fleeting/` until it is, or omit it.
- Anchor every fact to its provenance (`source`): how it was established — a reported decision, a document, an observed state, or the user's direct confirmation.
- Resolve the fact's `subject` to an existing topic note via titles, aliases, and tags. If the topic is clearly implied but has no note, create a minimal stub or hold the fact in `10_Fleeting/`; do not force an unrelated link.
- When a previously recorded fact changes or is corrected, write a new note that supersedes the prior one rather than editing history.
- Log only facts that bear on in-scope topics. Skip passing remarks, task instructions, and details unrelated to the knowledge base.

Activation limit: this behavior applies while this skill is active on a vault task. It does not make project-fact capture ambient across every conversation or session. For always-on capture regardless of whether the skill is invoked, the user must also add a directive to their `CLAUDE.md` or persistent memory (a shell hook cannot detect facts semantically). Recommend this when the user wants capture to persist beyond skill-scoped work.

## Coverage gap analysis

After initial vault creation from a collection of resources, or when the user asks for an assessment, analyze the knowledge base to identify areas where source grounding is thin, missing, or concentrated in a single source. The purpose is to ensure the vault can reliably serve as a grounding source for agent responses across its domain.

Run this analysis by:
1. Mapping concept clusters via WikiLink connectivity, tags, and frontmatter relationships.
2. Rating each cluster's source grounding (strong / adequate / thin / critical gap).
3. Identifying cross-cutting gaps: missing inter-cluster relationships, contradictions, staleness, and unclear scope boundaries.
4. Assessing source quality and concentration risk (single-point-of-failure sources, missing source types).
5. Generating prioritized recommendations for specific resource types that would fill identified gaps.
6. Classifying the vault's agent grounding readiness per topic area.

Write results to `00_Meta/COVERAGE-ANALYSIS.md` using [COVERAGE-ANALYSIS-FORMAT.md](./COVERAGE-ANALYSIS-FORMAT.md). The output tells the user exactly where the vault is strong enough for confident agent grounding, where it should hedge, and where additional resources are needed to prevent hallucination.

## When to ask before proceeding

Ask one focused question when the vault location, desired note granularity, treatment of source files, or permission to modify an existing vault would materially change the result. Otherwise state the assumption in `00_Meta/VAULT-MANIFEST.md` or `00_Meta/Sources/SOURCE-REGISTER.md` and proceed.

## Safety rules

- Before editing an existing vault, inspect its current folder conventions, frontmatter fields, link style, templates, and attachment settings.
- Do not overwrite existing notes. If a generated note would collide with an existing filename, merge only when the note covers the same concept and provenance supports the update; otherwise choose a unique, descriptive filename inside the target vault.
- Do not reorganize large parts of an existing vault unless the user explicitly asks for restructuring.
- Do not move or delete source documents, attachments, code repositories, or existing notes without explicit user approval.
- If large code repositories, generated output, datasets, dependency folders, or binary collections are inside the vault, record an Obsidian indexer risk and recommend exclusion rather than ingesting them directly into permanent notes.
