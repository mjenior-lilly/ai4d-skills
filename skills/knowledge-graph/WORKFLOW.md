# Obsidian Knowledge Base Workflow

Use this workflow to create, update, parse, or audit an Obsidian-compatible local knowledge base from user-provided technical/scientific documents, non-technical documents, code collections, meeting summaries, and task-analysis outputs. The coordinator owns all phase gates. Subagents are bounded workers; their outputs are advisory until the coordinator verifies them against source material, vault conventions, and Obsidian compatibility rules.

## Objectives

- Convert varied source material into a coherent Obsidian vault with shallow folders, unique filenames, stable WikiLinks, strict YAML frontmatter, and centralized attachments.
- When the user provides a target vault or knowledge base, create or update the output notes inside that vault and connect them to the existing graph rather than returning detached markdown artifacts.
- Preserve provenance from source documents, code paths, pages, sections, line ranges, commits, task-note dates, analysis periods, or other locators.
- Split long or complex sources into durable evergreen notes rather than source-shaped summaries.
- Maintain a graph that is readable for humans and predictable for LLMs: clear note titles, explicit aliases, consistent tags, backlinks, and short concept notes.
- Audit and repair Obsidian-specific risks: duplicate filenames, invalid YAML, broken WikiLinks, orphaned attachments, inconsistent tags, deep nesting, and indexer-heavy folders.
- Capture new and changing project-specific facts on in-scope topics as provenance-anchored, timestamped, append-only project-fact notes that record confirmed ground truth, not speculation.

## Obsidian compatibility rules

1. Keep the vault as standard local Markdown files and attachments.
2. Prefer WikiLinks for internal links: `[[Note Title]]` or `[[Note Title|display text]]`.
3. Use unique note filenames across the entire vault. Avoid duplicate names such as `Index.md` in multiple folders.
4. Use cross-platform-safe filenames: letters, numbers, spaces, hyphens, and underscores. Avoid `/`, `:`, `\\`, control characters, and other OS-hostile punctuation.
5. Keep folder depth shallow. Default to top-level domain folders under `20_Permanent/` only when they improve human navigation.
6. Put attachments in `00_Meta/Attachments/` unless an existing vault convention says otherwise.
7. Put frontmatter first, bounded by `---` lines.
8. In frontmatter, use arrays for `aliases`, `tags`, `sources`, and `related`. Do not prefix frontmatter tags with `#`.
9. Quote YAML strings that contain colons, brackets, braces, hashes, dates that should remain strings, or other special characters.
10. Do not store large generated folders, dependency directories, datasets, or code repositories as indexed knowledge notes. If they must remain in the vault, mark them as Obsidian indexer exclusions in the manifest or audit.
11. Use the full Obsidian Flavored Markdown syntax in [references/OBSIDIAN-SYNTAX.md](./references/OBSIDIAN-SYNTAX.md) — heading and block references, embeds, and callouts — so notes are navigable, not flat. Use typed frontmatter properties so notes are queryable.
12. Prefer a generated `.base` view ([references/BASES.md](./references/BASES.md)) for note listings that should stay current, and reserve `.canvas` ([references/CANVAS.md](./references/CANVAS.md)) for visual artifacts. Both are standard local files and keep the vault portable.

## Model and thinking tiers

Use the smallest tier that can satisfy the phase gate.

| tier | use when | model | thinking | max task size |
| --- | --- | --- | --- | --- |
| quick | Mechanical vault checks, filename normalization proposals, duplicate detection, link checks, attachment inventory, simple non-technical extraction. | GPT-5.5 or Claude Haiku-4.5 | low | 10-40 files or less than 20 minutes |
| standard | Mixed document ingestion, ordinary technical notes, source registers, note merging, metadata normalization, moderate code walkthroughs. | GPT-5.5 or Claude Sonnet-4.6 | medium | One source cluster, 5-15 documents, or 3-8 related code files |
| complex | Dense scientific papers, specifications, mathematical material, large architecture documents, ambiguous terminology, cross-document synthesis, or codebases with many entry points. | GPT-5.5 or Claude Opus-4.8 | high | One complex source, one subsystem, or any high-risk synthesis task |
| verifier | Independent audit of note quality, link integrity, frontmatter validity, source-grounding, merge decisions, and Obsidian compatibility. | GPT-5.5 or Claude Sonnet-4.6; use Claude Opus-4.8 for complex source-grounding review | medium by default, high for complex tier changes | Bounded to changed notes, source cluster, or vault audit |

## Subagent roles

- **Coordinator**: Owns vault scoping, conventions, phase gates, note taxonomy, source register, integration, and final validation. Use GPT-5.5 or Claude Opus-4.8 with high thinking for large or highly technical vault builds; use GPT-5.5 or Claude Sonnet-4.6 with medium thinking otherwise.
- **Vault cartographer**: Inspects existing folder structure, `.obsidian/` settings when present, filename conventions, templates, frontmatter patterns, tags, attachments, and link style. Use GPT-5.5 or Claude Sonnet-4.6 with medium thinking; use GPT-5.5 or Claude Haiku-4.5 with low thinking for small vault inventories.
- **Source inventory scouts**: Catalog user-provided documents and code by type, size, complexity, provenance, and processing priority. Use GPT-5.5 or Claude Haiku-4.5 with low thinking for simple inventories; use GPT-5.5 or Claude Sonnet-4.6 with medium thinking for mixed or messy collections.
- **Document extractors**: Extract concepts, claims, definitions, procedures, entities, limitations, and relationships from documents. Use GPT-5.5 or Claude Sonnet-4.6 with medium thinking; use GPT-5.5 or Claude Opus-4.8 with high thinking for scientific, mathematical, legal, medical, or high-density technical material.
- **Code extractors**: Trace entry points, architecture, APIs, data models, configuration, tests, and operational workflows from code. Use GPT-5.5 or Claude Sonnet-4.6 with medium thinking; use GPT-5.5 or Claude Opus-4.8 with high thinking for large subsystems, dynamic dispatch, generated code, or cross-language projects.
- **Note composers**: Convert verified extractions into Obsidian notes following [NOTE-FORMAT.md](./NOTE-FORMAT.md). Use GPT-5.5 or Claude Sonnet-4.6 with medium thinking; use GPT-5.5 or Claude Haiku-4.5 with low thinking only for mechanical formatting from already verified extracts.
- **Vault verifier**: Checks final notes for broken links, duplicate filenames, malformed YAML, inconsistent tags, missing provenance, attachment issues, and excessive note length. Use GPT-5.5 or Claude Sonnet-4.6 with medium thinking; escalate to GPT-5.5 or Claude Opus-4.8 with high thinking when verifying dense source-grounding.

## Parallelization defaults

- Do not use subagents for fewer than 10 short files or a small single-topic update where coordination costs exceed direct work.
- Use 2-4 source inventory scouts for 25-100 mixed files. Use up to 6 only when files split cleanly by document type, domain, project, or source folder.
- For one very large file, split by sections, chapters, headings, page ranges, or code regions. Use 2-4 extractors for complex documents; use 1 extractor when the document is short or highly sequential.
- For many smaller files, batch by source type and domain: scientific papers, manuals, meeting notes, task analyses, policy documents, README/docs, source code, tests, configuration, and data schemas.
- Assign code extractors by subsystem or entry-point boundary, not by arbitrary file count.
- Keep note taxonomy, filename selection, merge decisions, and final link integration coordinator-owned to prevent duplicate concepts and inconsistent aliases.
- Run verifier subagents after composition, not in parallel with note writers that are still changing the same files.
- Never let parallel subagents write to the same note or source register section. They return bounded extraction output; the coordinator integrates.

## Phase gates

| phase | gate |
| --- | --- |
| vault scope | Knowledge base root (named `{{topic}}-kb` for new builds), creation/update mode, source locations, and modification permissions are known or explicitly assumed. |
| vault conventions | `00_Meta/VAULT-MANIFEST.md` exists or current conventions are recorded before new notes are written. |
| source inventory | `00_Meta/Sources/SOURCE-REGISTER.md` lists source IDs, types, locations, sizes, complexity, and processing status. |
| extraction | Extracted claims, concepts, code facts, and relationships cite source IDs and precise locators where available. |
| note planning | Proposed notes have unique filenames, target folders inside the vault, aliases, tags, source IDs, graph entry points, and merge/update decisions. |
| composition | Notes follow [NOTE-FORMAT.md](./NOTE-FORMAT.md), use Obsidian WikiLinks, include provenance, and are written to vault-relative paths. |
| integration | New and updated notes are referenced from relevant index, project, source, or related concept notes, and `SOURCE-REGISTER.md` lists the produced notes. |
| reference migration | Processed source files with `status: processed` are migrated to the `50_Reference/` archive with `source-id` prefix filenames, the source register's `Archived location` field is updated, and `50_Reference/` is listed in the vault manifest's indexer exclusions. |
| project-fact capture | Any new or changed project-specific fact on an in-scope topic is logged under `40_Project/` with a resolved `subject` link, a `confirmed` timestamp, a `source` provenance anchor, and `status`, append-only; only confirmed ground truth, never speculation. |
| vault validation | Links, filenames, frontmatter, tags, attachments, nesting depth, and indexer risks have been checked and recorded in `00_Meta/VAULT-AUDIT.md` when useful. |
| coverage analysis | Concept clusters are mapped, source grounding is rated per cluster, cross-cutting gaps and source concentration risks are identified, prioritized recommendations specify resource types, and agent grounding readiness is classified. Results recorded in `00_Meta/COVERAGE-ANALYSIS.md`. |
| vault abstract | `00_Meta/VAULT-ABSTRACT.md` synthesizes domain scope, concept taxonomy, source profile, coverage strengths, known gaps, explicit scope boundaries, and semantic descriptors from the manifest, source register, and coverage analysis into a concise LLM-optimized summary for retrieval routing. |

## Workflow loop

### 0. Scope the knowledge base and source collection

1. Identify whether the user wants to create a new knowledge base, update an existing one, parse an existing one, or audit/repair Obsidian compatibility.
2. Identify the knowledge base root and source locations. Sources may be PDFs, Markdown, text files, office documents converted to text, code repositories, API docs, notebooks, diagrams, meeting notes, task-analysis outputs from the `tasks` skill, or mixed folders.
3. When creating a new knowledge base, name the top-level directory `{{topic}}-kb` (e.g., `metabolomics-kb`, `platform-architecture-kb`) so the purpose is immediately clear from the directory name. Use the user's explicit name if they provide one.
4. If the user provides a target knowledge base, use that directory as the write target for every output note. Do not create parallel notes outside it unless the user explicitly requests a separate export.
5. Inspect current conventions before writing. Check folder names, note naming, templates, frontmatter fields, aliases, tags, link style, attachment location, and `.obsidian/` settings when available.
6. Ask one focused question only if the wrong assumption could cause overwritten notes, misplaced sources, incompatible link style, or a substantially different note granularity.
7. Write or update `00_Meta/VAULT-MANIFEST.md` using [VAULT-MANIFEST-FORMAT.md](./VAULT-MANIFEST-FORMAT.md).

### 1. Inventory sources

1. Assign each source a stable source ID.
2. Record path, type, size, language, domain, author or origin when known, date/version when known, and access limitations.
3. Classify processing complexity:
   - `simple`: short non-technical or single-topic files;
   - `standard`: moderate technical or mixed-domain files;
   - `complex`: dense scientific, mathematical, legal, medical, code-heavy, or cross-referenced files;
   - `huge`: files too large for one reliable pass and requiring sectioned extraction.
4. Identify source clusters that should be processed together because they share terminology, provenance, or code boundaries.
5. Update `00_Meta/Sources/SOURCE-REGISTER.md` using [SOURCE-REGISTER-FORMAT.md](./SOURCE-REGISTER-FORMAT.md).

### 2. Plan the note graph

1. Choose note granularity by concept, not by source file. A single source can yield many notes; several sources can update one concept note.
2. Prefer permanent notes for durable concepts, workflows, APIs, entities, algorithms, experimental findings, architecture decisions, and recurring terminology.
3. Keep project-specific execution notes in `30_Projects/` and temporary import notes in `10_Fleeting/`.
4. Define canonical note titles and vault-relative output paths before writing. Titles should be unique, descriptive, and stable.
5. For task-analysis outputs, preserve the period in the filename and place files under the existing vault convention for daily notes, reviews, or productivity logs. If no convention exists, use `30_Projects/Task Reviews/daily/`, `30_Projects/Task Reviews/weekly/`, `30_Projects/Task Reviews/monthly/`, or `30_Projects/Task Reviews/annual/`.
6. Define graph entry points for each note: related concept links, source links, project links, index/MOC links, task review indexes, or backlinks from existing notes. When a domain or source cluster needs a note listing, plan a generated `.base` index ([references/BASES.md](./references/BASES.md)) driven by frontmatter rather than a hand-maintained static index, so it stays current; embed it in a human-facing MOC with `![[Index.base]]`.
7. Define aliases for acronyms, synonyms, old names, paper-specific terms, and code symbols that users or agents may search for later.
8. Define tags sparingly. Use tags for broad retrieval facets, not as a replacement for links.
9. Decide merge vs create:
   - merge when an existing note covers the same concept and the new source adds evidence, nuance, or updated behavior;
   - create when the concept is distinct, the existing title would become overloaded, or source terminology needs a separate bridge note.

### 3. Extract source facts

1. Read source material directly. Do not infer technical claims from filenames, abstracts, tables of contents, or code names alone.
2. For scientific and technical documents, extract:
   - problem statement and motivation;
   - definitions and notation;
   - method, architecture, algorithm, or protocol;
   - assumptions and constraints;
   - empirical setup, datasets, metrics, and results;
   - limitations, failure modes, and open questions;
   - relationships to existing notes.
3. For non-technical documents, extract:
   - people, organizations, goals, decisions, timelines, obligations, definitions, and action-relevant context;
   - claims that affect interpretation of technical sources;
   - contradictions or unresolved ambiguity.
4. For task-analysis outputs, preserve the generated analysis as a period-specific artifact and extract only:
   - recurring execution patterns;
   - durable planning rules or constraints;
   - project-relevant commitments, blockers, and follow-up themes;
   - links to related project notes, daily notes, or review indexes.
   Do not promote every daily task into a permanent note.
5. For code, extract:
   - entry points and exported surfaces;
   - module responsibilities;
   - data models, schemas, configuration, environment variables, and persisted formats;
   - runtime flows, state transitions, and integration boundaries;
   - tests and examples that reveal intended behavior;
   - stable symbols worth adding as aliases or backlinks.
6. Record precise locators: section, heading, page, paragraph, line range, file path, function/class, commit, test name, task-note date, or analysis period.
7. Mark uncertain or conflicting facts explicitly. Do not smooth contradictions into a false synthesis.

### 4. Compose and integrate Obsidian notes

1. Use [NOTE-FORMAT.md](./NOTE-FORMAT.md) for permanent notes and [references/OBSIDIAN-SYNTAX.md](./references/OBSIDIAN-SYNTAX.md) for Obsidian Flavored Markdown syntax (embeds, callouts, heading/block references, math, Mermaid).
2. Write notes to their planned vault-relative paths. If a target vault was provided, all output notes must be created or updated inside it.
3. Put frontmatter first and keep it valid YAML.
4. Use a concise opening definition or claim so the note is useful in preview and graph contexts.
5. Link related concepts with WikiLinks on first meaningful mention.
6. Add aliases for acronyms, alternate names, code symbols, and source-specific terminology.
7. Keep notes focused. If a note grows beyond one concept or becomes difficult to scan, split it and link the parts.
8. Prefer prose and compact tables over long pasted excerpts.
9. Include short code snippets only when they explain an API, schema, invariant, or non-obvious mechanism. Cite the source path and line range.
10. Add a `Source grounding` section for claims that may need verification later.
11. Add `Open questions` only for material ambiguity that affects retrieval, interpretation, or future updates.
12. For task-analysis outputs, add frontmatter fields that support retrieval, such as `analysis_type`, `period_start`, `period_end`, `source_task_notes`, `projects`, `tags`, and `sources`, while preserving the analysis headings produced by the `tasks` skill.
13. Integrate each note into the vault graph by adding or updating relevant links in existing index, project, source, task review, or related concept notes when such notes exist. If no natural entry point exists, create the smallest useful index or source note rather than leaving the note orphaned.
14. Update `00_Meta/Sources/SOURCE-REGISTER.md` so each processed source lists the notes it produced or updated.

### 5. Migrate reference files

After integration is complete and source records show `status: processed`, migrate original source files into the structured `50_Reference/` archive so they remain accessible for provenance verification without cluttering the active workspace or degrading Obsidian indexing.

1. Identify sources eligible for migration: `status: processed` (or `status: partial` with all intended extraction explicitly complete), not actively edited by the user, and not living in a version-controlled repository the user works in.
2. Create the appropriate type subfolder under `50_Reference/` if it does not exist: `papers/`, `specs/`, `docs/`, `code/`, `meetings/`, `data/`, `media/`, or `other/`. Add a domain subfolder only when the type folder already exceeds ~15 files.
3. Copy or move the file into its target folder using the naming convention `{source-id}_{descriptive-slug}.{ext}` (e.g., `SRC-0003_smith-2024-enzyme-kinetics.pdf`).
4. Confirm the action with the user before deleting the original location. Default to copying; move only with explicit approval.
5. Update the source register entry:
   - Set `Archived location` to the vault-relative path (e.g., `50_Reference/papers/SRC-0003_smith-2024-enzyme-kinetics.pdf`).
   - Set or append `Obsidian handling` to `archived to 50_Reference`.
6. Ensure `50_Reference/` appears in `00_Meta/VAULT-MANIFEST.md` under indexer exclusions if not already listed.
7. For sources that cannot be migrated (external URLs, active repositories, user-managed files), record a stable reference (path, URL, commit, DOI) in the source register's `Location` field and set `Archived location` to `N/A — external reference`.

Use the **quick** model/thinking tier. Migration is mechanical file handling, not analysis.

### 6. Update and maintain existing notes

1. Before creating a note, search for existing titles, aliases, and backlinks that cover the concept.
2. Preserve existing user-written content unless it is clearly obsolete, contradicted by newer source evidence, or duplicated by a cleaner integrated note.
3. When updating, add source-backed changes in place rather than appending disconnected summaries.
4. Update aliases, tags, backlinks, source lists, task review indexes, and index/project references with the same change.
5. If two notes overlap, recommend a merge only when both note purposes are redundant. Otherwise add bridge links explaining the distinction.
6. Record major convention changes in `00_Meta/VAULT-MANIFEST.md`.

### 7. Validate the vault

Run the narrowest available checks for the touched scope. When Obsidian is running, the `obsidian` CLI ([references/OBSIDIAN-CLI.md](./references/OBSIDIAN-CLI.md)) is an optional, more reliable backend for link, backlink, tag, and render checks; otherwise perform the same checks via direct filesystem reads. Do not block the workflow on the CLI.

1. Duplicate filenames across the vault.
2. Invalid or missing frontmatter in permanent notes.
3. Frontmatter tags containing `#`.
4. Broken WikiLinks or links that resolve ambiguously.
5. Missing aliases for common acronyms and source names.
6. Orphan notes created by the workflow that should link into the graph.
7. Processed sources missing produced-note entries in `SOURCE-REGISTER.md`.
8. Task-analysis outputs missing expected period frontmatter, task-review index links, or source task-note provenance.
9. Generated notes written outside the target vault when a vault was provided.
10. Attachments outside the configured attachments folder.
11. Deeply nested folders beyond the vault convention.
12. Large non-Markdown folders inside the vault that may slow the Obsidian indexer.
13. Notes without source grounding when they contain technical, scientific, code, medical, legal, productivity-pattern, or factual claims.
14. `.base` files: valid YAML, every referenced property/formula defined, Duration math accessing a numeric field before rounding, and null-guarded formulas (see [references/BASES.md](./references/BASES.md)).
15. `.canvas` files: valid JSON, unique node and edge IDs, and every edge `fromNode`/`toNode` resolving to an existing node (see [references/CANVAS.md](./references/CANVAS.md)).
16. Project-fact notes under `40_Project/`: each has `source`, a `confirmed` `date-time`, and a resolved `subject` link; at most one `current` note per distinct fact about a `subject`; any superseded/corrected note retains a valid `supersedes` chain.
17. No speculation or hypothetical discussion recorded as a project fact or presented as source-grounded fact.
18. Migrated reference files in `50_Reference/` have matching `Archived location` entries in the source register; no processed source with a missing or broken archive path.

Record results in `00_Meta/VAULT-AUDIT.md` using [VAULT-AUDIT-FORMAT.md](./VAULT-AUDIT-FORMAT.md) when the task is more than a trivial edit.

### Ongoing: capture project facts

This step is reactive rather than sequential: it runs whenever, during any phase, a new or changed project-specific fact on a topic the vault covers is confirmed — a decision made, a state changed, or a concrete detail established.

1. Detect the fact. A confirmed decision, state change, or concrete project detail on an in-scope topic. Ignore passing remarks, task instructions, and details unrelated to the knowledge base. Do not treat speculation, proposals, predictions, or open questions as facts.
2. Confirm it is ground truth. Log only what is known to be true and can be anchored to a `source` — a reported decision, a document, an observed state, or the user's direct confirmation. If it cannot be confirmed, hold it in `10_Fleeting/` until it can, or omit it.
3. Resolve the `subject`. Match the fact to an existing topic note via titles, aliases, and tags. If the topic is clearly implied but has no note, create a minimal stub under `20_Permanent/` or hold the fact in `10_Fleeting/` until a topic note exists. Do not attach the fact to an unrelated note.
4. Compose a project-fact note under `40_Project/` using [PROJECT-FACT-FORMAT.md](./PROJECT-FACT-FORMAT.md): precise statement, `subject` link, `source` provenance anchor, a `confirmed` `date-time`, `change`, and `status: current`. Timestamp with when the fact became true or was confirmed.
5. Handle change over time append-only. If a fact about a subject already has a `current` note and it changes or is corrected, write a new note with a `supersedes` link and set the prior note's `status` to `superseded` (or `corrected` if the earlier note stated something now known to be wrong). Never edit the substance of a past fact in place.
6. Keep the record accurate. Never record speculation as fact. If a new fact contradicts a source-grounded note, log the confirmed fact and flag the tension for the coordinator to reconcile against source material; do not silently overwrite grounded content.

### 8. Analyze coverage and identify gaps

Run this phase after initial vault creation from a collection of resources, after a major source-ingestion batch, or when the user explicitly asks for a coverage assessment. The goal is to evaluate whether the knowledge base provides sufficient grounding for agent responses across its domain, and to surface specific areas that need additional resources.

1. **Map concept clusters**. Analyze WikiLink connectivity, shared tags, co-occurring frontmatter properties, and folder proximity to identify natural groupings of related notes. A cluster is a set of notes that together should enable an agent to answer questions about one sub-domain.

2. **Assess source grounding per cluster**. For each cluster:
   - Count independent sources referenced across its notes (via `sources` frontmatter and `Source grounding` sections).
   - Evaluate whether core claims have verifiable backing or rely on single-source extraction without corroboration.
   - Check whether the grounding covers definitions, mechanisms, constraints, edge cases, and relationships — or only surface-level facts.

3. **Rate coverage**. Apply the rating scale from [COVERAGE-ANALYSIS-FORMAT.md](./COVERAGE-ANALYSIS-FORMAT.md):
   - ◆ Strong: multiple independent sources, cross-referenced, suitable for confident grounding.
   - ◇ Adequate: at least one quality source with grounded claims.
   - △ Thin: single source, shallow extraction, or missing mechanisms/constraints.
   - ▽ Critical gap: implied coverage with no substantive source-backed content.

4. **Identify cross-cutting gaps**. Look for:
   - Missing relationships between clusters that should connect (e.g., a "methods" cluster that never links to a "data models" cluster in the same system).
   - Contradictions between notes sourced from different materials.
   - Temporal staleness: sources with version numbers, publication dates, or API versions that may have changed.
   - Scope boundaries that are unclear — where the vault implies coverage but silently stops.

5. **Assess source quality and concentration**. Check for:
   - Single-point-of-failure sources that ground a disproportionate fraction of notes.
   - Missing source types (e.g., all review articles but no primary research; all documentation but no implementation source).
   - Sources with narrow coverage applied broadly across many notes.

6. **Generate prioritized recommendations**. For each gap, recommend:
   - The specific *type* of resource that would fill it (textbook chapter, API spec, primary paper, source code, expert review, dataset documentation, etc.).
   - *Why* that resource type addresses the specific gap (not generic "more sources").
   - The expected improvement in agent grounding quality.
   - Priority based on: critical gaps in likely query areas > thin core concepts > source diversity > staleness.

7. **Assess agent grounding readiness**. Classify the vault's topics into:
   - Ready for confident grounding (agent can answer reliably).
   - Ready with caveats (agent should hedge or cite uncertainty).
   - Not ready (high hallucination risk if agent treats vault as authoritative).

8. **Write results** to `00_Meta/COVERAGE-ANALYSIS.md` using [COVERAGE-ANALYSIS-FORMAT.md](./COVERAGE-ANALYSIS-FORMAT.md).

Use the **standard** model/thinking tier for small-to-medium vaults (under 50 notes). Use the **complex** tier for large vaults, highly technical domains, or when source-grounding verification requires deep reading. Use **quick** tier only for re-running the analysis on a vault that has changed minimally since the last assessment.

### 9. Generate vault abstract

Generate or update `00_Meta/VAULT-ABSTRACT.md` using [VAULT-ABSTRACT-FORMAT.md](./VAULT-ABSTRACT-FORMAT.md). This file is a concise, LLM-optimized summary that enables retrieval systems and grounding agents to determine in one pass whether this vault is the correct resource for a given query.

1. **Read inputs**. Synthesize from:
   - `00_Meta/VAULT-MANIFEST.md` → domain description, scope, intended purpose.
   - `00_Meta/Sources/SOURCE-REGISTER.md` → source count, types, authorities, temporal range.
   - `00_Meta/COVERAGE-ANALYSIS.md` → concept clusters, coverage ratings, readiness assessment, known gaps.
   If `COVERAGE-ANALYSIS.md` does not exist (e.g., parsing a vault not built by this skill), derive what you can from direct vault inspection: note count, tags, link connectivity, and note titles. Mark the abstract `status: provisional`.

2. **Compose the abstract**. Follow the template in [VAULT-ABSTRACT-FORMAT.md](./VAULT-ABSTRACT-FORMAT.md). Target ≤120 lines. Prioritize:
   - Clear domain and scope statement with explicit boundaries.
   - Concept taxonomy distilled to cluster names and coverage ratings.
   - Source profile summarized to types and temporal range.
   - Coverage strengths as confident-grounding topics.
   - Known gaps and explicit scope boundaries (what the vault does NOT cover) — these are as important as strengths for retrieval routing.
   - Dense semantic descriptors for keyword and embedding matching.

3. **Set staleness fields**. On full generation: `stale_since: null`, `updated: {{today}}`, `vault_modified: {{today}}`. On incremental updates that do not materially change vault scope: set `stale_since: {{update date}}` in the existing abstract without regenerating.

4. **When to regenerate vs. mark stale**:
   - **Regenerate**: on vault creation, after major source ingestion batches, when new sources expand into previously uncovered domains, or when the user requests it.
   - **Mark stale**: on incremental single-note updates, minor source additions within existing scope, or routine maintenance edits.
   - **On parse/audit**: generate if missing; regenerate if `stale_since` is set.

Use the **quick** model/thinking tier. The abstract is a synthesis of already-validated artifacts, not a primary analysis.

## Output to the user

Return a concise summary with:

- vault path;
- source count processed;
- notes created, updated, and skipped;
- project facts logged, with subject and supersession changes, when any were captured;
- validation performed and results;
- coverage analysis performed and key findings: cluster count, gaps identified, agent grounding readiness;
- unresolved source gaps, broken links, merge candidates, or indexer risks;
- prioritized recommendations for additional resources to strengthen grounding;
- paths to the manifest, source register, audit, coverage analysis, vault abstract, and notable notes.
