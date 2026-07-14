# Coverage Analysis Format

Template for `COVERAGE-ANALYSIS.md`, written as a sibling to the vault root directory (not inside the vault). Use this format when analyzing an existing knowledge base to identify areas with poor reference coverage, shallow understanding, or missing context that would benefit from additional source material. The goal is to ensure the vault can serve as a comprehensive grounding resource for domain-specific agent responses.

---

## Template

```markdown
---
id: coverage-analysis-{{YYYYMMDD}}
type: coverage-analysis
vault: "{{vault root}}"
scope: "{{domain or topic boundary}}"
analyzed: {{YYYY-MM-DD}}
notes_assessed: {{count}}
sources_assessed: {{count}}
status: current
---

# Coverage Analysis

> [!info] Scope
> {{One-line description of what domain/topics this analysis covers}}

## Summary

| metric | count |
| --- | --- |
| Total permanent notes | {{n}} |
| Notes with ≥2 independent sources | {{n}} |
| Notes with single-source grounding | {{n}} |
| Notes with no source grounding | {{n}} |
| Concept clusters identified | {{n}} |
| Clusters with adequate coverage | {{n}} |
| Clusters with thin coverage | {{n}} |
| Clusters with critical gaps | {{n}} |

## Coverage rating

| rating | meaning |
| --- | --- |
| ◆ Strong | Multiple independent sources, cross-referenced, supports confident grounding |
| ◇ Adequate | At least one quality source, grounded claims, minor gaps acceptable |
| △ Thin | Single source or shallow extraction; agent may hallucinate beyond what is grounded |
| ▽ Critical gap | No source material or only tangential references; high risk of ungrounded responses |

## Concept cluster analysis

For each identified cluster of related notes:

### {{Cluster name}}

- **Notes**: {{WikiLinks to constituent notes}}
- **Coverage rating**: {{◆/◇/△/▽}}
- **Source diversity**: {{count}} independent sources
- **Grounding depth**: {{brief assessment — e.g., "definitions grounded, mechanisms speculative"}}
- **What the vault currently supports**: {{what an agent CAN confidently answer from this cluster}}
- **What is missing or undergrounded**:
  - {{specific concept, relationship, or detail that lacks source backing}}
  - {{...}}
- **Recommended additional resources**:
  - {{type of resource}} — {{why it would fill the gap}}
  - {{...}}
- **Risk if not addressed**: {{what goes wrong if an agent uses this cluster as-is for grounding}}

## Cross-cutting gaps

Areas that span multiple clusters or represent structural weaknesses:

### {{Gap title}}

- **Affected notes**: {{WikiLinks}}
- **Nature of gap**: {{missing relationships, contradictions, temporal staleness, domain boundary unclear}}
- **Impact on agent grounding**: {{how this gap manifests in agent responses}}
- **Recommended action**: {{resource type, integration approach, or vault restructuring}}

## Source quality assessment

| source ID | type | coverage | staleness risk | notes grounded |
| --- | --- | --- | --- | --- |
| {{src-id}} | {{type}} | {{broad/narrow/tangential}} | {{low/medium/high}} | {{count}} |

### Sources with disproportionate influence

Sources that ground a large fraction of the vault, creating single-point-of-failure risk:

- **{{source ID}}**: grounds {{n}} notes ({{%}} of vault). If this source is wrong or outdated, {{impact}}.

### Source type gaps

- {{Missing source types that would strengthen the vault — e.g., "no primary experimental data", "no authoritative specification", "only secondary review articles"}}

## Recommendations prioritized

Ordered by impact on agent grounding quality:

| priority | cluster/gap | action | expected improvement |
| --- | --- | --- | --- |
| 1 | {{cluster or gap name}} | {{specific resource or action}} | {{what becomes groundable}} |
| 2 | ... | ... | ... |

## Agent grounding readiness

Assessment of whether this vault, as-is, can reliably ground agent responses in its domain:

- **Ready for confident grounding**: {{topics/questions where the vault is sufficient}}
- **Ready with caveats**: {{topics where the agent should hedge or cite uncertainty}}
- **Not ready — high hallucination risk**: {{topics where the vault lacks sufficient grounding}}

## Open questions

- {{Ambiguities about scope, priorities, or resource availability that affect recommendations}}
```

---

## Construction rules

1. Run this analysis after initial vault creation or after significant source ingestion, not during incremental single-note updates.
2. Identify concept clusters by analyzing WikiLink connectivity, shared tags, and frontmatter relationships — not by folder structure alone.
3. Assess coverage by examining the `Source grounding` section of each permanent note and cross-referencing against `SOURCE-REGISTER.md`.
4. A note has "strong" coverage only when its core claims are supported by ≥2 independent sources or one authoritative primary source with verifiable claims.
5. "Thin" coverage means the note's substance derives from a single source with no independent corroboration, or from extraction that captured surface information without mechanisms, constraints, or edge cases.
6. "Critical gap" means the vault implies coverage of a topic (via links, aliases, or cluster membership) but has no substantive source-backed content — an agent following these links would find nothing to ground on and would likely hallucinate.
7. Evaluate source diversity: a vault built entirely from one textbook or one API doc has correlated blind spots. Identify where independent sources (papers, implementations, specifications, user reports) would provide triangulation.
8. Assess staleness risk: sources with publication dates, version numbers, or API versions that may have changed since ingestion. Flag notes grounded on potentially outdated material.
9. Consider the agent use case: what questions will an agent need to answer using this vault? Gaps matter more in areas where agents will face queries.
10. Prioritize recommendations by:
    - Critical gaps in high-query areas first;
    - Thin coverage on core domain concepts second;
    - Source diversity improvements third;
    - Staleness remediation fourth.
11. Be specific in resource recommendations: name the *type* of resource (textbook chapter, API specification, primary research paper, implementation source code, domain expert review, experimental dataset documentation) and *why* it fills the identified gap — not just "more sources needed."
12. Do not recommend resources for topics outside the vault's declared scope unless the analysis reveals the scope should expand.
13. Update this file in place when a new analysis supersedes the prior one. Keep only the most recent analysis as `current`; archive prior versions by renaming to `COVERAGE-ANALYSIS-{{date}}.md` if the user wants history.
