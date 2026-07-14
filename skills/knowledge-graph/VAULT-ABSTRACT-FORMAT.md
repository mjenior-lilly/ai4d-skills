# Vault Abstract Format

Template for `00_Meta/VAULT-ABSTRACT.md`. This file provides a concise, LLM-optimized summary of the vault's content, scope, and coverage to enable fast relevance determination by retrieval systems and grounding agents. An LLM reading this file should be able to decide in one pass whether the vault is the correct resource to search for a given query — or whether to look elsewhere.

---

## Template

```markdown
---
id: vault-abstract-{{YYYYMMDD}}
type: vault-abstract
vault: "{{vault root directory name}}"
domain: "{{primary domain phrase — e.g., 'metabolomics data analysis', 'platform microservice architecture'}}"
scope_keywords:
  - {{keyword1}}
  - {{keyword2}}
  - {{keyword3}}
  - {{...up to 20 dense retrieval keywords/phrases covering the vault's topics}}
temporal_start: {{YYYY-MM-DD or YYYY — earliest source material date}}
temporal_end: {{YYYY-MM-DD or YYYY — latest source material date}}
note_count: {{total permanent notes}}
source_count: {{total sources in SOURCE-REGISTER}}
cluster_count: {{concept clusters identified in COVERAGE-ANALYSIS.md (sibling to vault root)}}
generated: {{YYYY-MM-DD — first creation date}}
updated: {{YYYY-MM-DD — last full regeneration date}}
vault_modified: {{YYYY-MM-DD — last known vault content change at generation time}}
stale_since: {{YYYY-MM-DD or null — set when vault is updated without regenerating this abstract}}
status: current
---

# Vault Abstract

## Domain and scope

{{2–3 sentences describing: (1) what knowledge domain this vault covers, (2) what purpose it serves (grounding agent responses, project documentation, research synthesis, etc.), and (3) any notable scope boundaries (what it explicitly does NOT cover).}}

## Concept taxonomy

| cluster | notes | coverage |
| --- | --- | --- |
| {{Cluster name}} | {{n}} | {{◆/◇/△/▽}} |
| {{...}} | {{...}} | {{...}} |

Coverage key: ◆ Strong · ◇ Adequate · △ Thin · ▽ Critical gap

## Source profile

- **Source types**: {{comma-separated list — e.g., peer-reviewed papers, API documentation, source code, meeting notes}}
- **Key authorities**: {{primary sources or authors that ground the majority of content}}
- **Temporal range**: {{temporal_start}} to {{temporal_end}}
- **Source count**: {{n}} sources across {{n}} types

## Coverage strengths

Topics where the vault provides confident, well-grounded answers:

- {{topic or question type with strong grounding}}
- {{...}}

## Known gaps and limitations

Topics where the vault has thin or no coverage — queries on these topics should be routed elsewhere:

- {{topic with ▽ Critical gap or △ Thin coverage, and brief reason}}
- {{...}}

### Explicit scope boundaries

This vault does NOT cover:

- {{domain or topic explicitly outside scope}}
- {{...}}

## Semantic descriptors

{{Dense comma-separated list of 30–60 keywords, phrases, entity names, acronyms, and technical terms that an embedding model or keyword matcher would associate with this vault's content. Include both canonical terms and common synonyms/abbreviations.}}
```

---

## Construction rules

1. Generate this file after `COVERAGE-ANALYSIS.md` exists (or is being generated in the same run), since the abstract synthesizes from three inputs:
   - `00_Meta/VAULT-MANIFEST.md` → domain description, scope, folder conventions
   - `00_Meta/Sources/SOURCE-REGISTER.md` → source count, types, temporal range, key authorities
   - `COVERAGE-ANALYSIS.md` (sibling to vault root) → cluster map, coverage ratings, readiness assessment, gaps
2. The abstract is a **synthesis**, not a copy. Do not reproduce full sections from its input artifacts. Distill each into the minimal information an LLM needs for relevance routing.
3. Target length: **≤120 lines** including frontmatter. If the vault is large, summarize clusters by top-level grouping rather than listing every sub-cluster.
4. The `scope_keywords` array in frontmatter should contain 10–20 terms optimized for retrieval matching — include domain nouns, key method names, organisms, technologies, frameworks, or other distinguishing vocabulary.
5. The `Semantic descriptors` section in the body is longer (30–60 terms) and includes synonyms, abbreviations, and alternate phrasings that a keyword or embedding search might use.
6. The `Known gaps and limitations` section is as important as `Coverage strengths`. An LLM that correctly rejects a vault saves more time than one that correctly selects it. Be specific about what is missing.
7. The `Explicit scope boundaries` subsection names topics that are adjacent to the vault's domain but intentionally excluded. This prevents false-positive matching on semantically similar but out-of-scope queries.
8. **Staleness handling**:
   - On full vault creation or major update: generate fresh, set `stale_since: null`.
   - On incremental update that does not materially change vault scope: set `stale_since` to the update date in the existing abstract's frontmatter without regenerating.
   - On parse or audit: generate if missing; regenerate if `stale_since` is set.
   - An LLM reading a stale abstract should still trust the content that IS present but should not assume completeness.
9. Update this file in place when regenerating. Do not archive prior versions unless the user explicitly requests history.
10. If `COVERAGE-ANALYSIS.md` does not yet exist as a sibling to the vault root (e.g., during a parse of a vault that was not built by this skill), derive what you can from direct vault inspection: count notes, identify clusters from tags and link connectivity, infer scope from note titles and frontmatter. Mark the abstract `status: provisional` and note in the Domain section that a full coverage analysis has not been performed.
