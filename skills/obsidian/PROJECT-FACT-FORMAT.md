# Obsidian Project Fact Note Format

Use this format to log a **project-specific fact that is new or has changed** — a decision that was made, a state that changed, or a concrete detail about the project the vault covers that has been confirmed. Project facts record **ground truth**: only information that is known to be true, not speculation, predictions, proposals, or hypothetical discussion. If something is proposed, uncertain, or still under debate, it is **not** a project fact — do not log it here until it is confirmed. See [NOTE-FORMAT.md](./NOTE-FORMAT.md) for stable, source-grounded topic notes.

Store project facts as append-only, individually timestamped notes under `40_Project/`. One note per fact. When a previously recorded fact changes or is corrected, write a **new** note that supersedes the old one; do not overwrite or delete the prior entry, so the temporal record of how the project's ground truth evolved stays intact.

```md
---
id: YYYYMMDDHHMMSS-slug
title: "Fact: {short paraphrase of the fact}"
type: project-fact
subject: "[[Topic Note]]"
topics: [topic-a, topic-b]
statement: "{one-line factual statement}"
change: new | updated | corrected
source: "{how the fact was established — a decision, document, observed state, or the user's confirmation}"
confirmed: YYYY-MM-DDTHH:mm:ss
status: current | superseded | corrected
supersedes: "[[Fact: earlier statement]]"
tags: [project-fact]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Fact: {short paraphrase of the fact}

> [!note] Confirmed {YYYY-MM-DD}
> {The project fact, stated plainly. Record what is true, not what might be true.}

## Statement

{One or two sentences stating the fact precisely. Keep it concrete and verifiable. Do not hedge, speculate, or extrapolate beyond what is known.}

## Provenance

- Source: {how the fact was established — a decision the user reported, a document, an observed state of the project, or the user's direct confirmation}
- Confirmed: {YYYY-MM-DDTHH:mm:ss — when the fact became true or was confirmed}
- Relates to: `[[Topic Note]]` — {how this fact bears on the topic}
- Change: {new fact | updates a prior fact | corrects a prior fact}

## Details

- {Any concrete specifics that make the fact actionable: values, names, versions, dates. Omit this section rather than padding it with speculation.}

## Related

- `[[Topic Note]]`: {the in-scope topic this fact concerns}
- `[[Fact: earlier statement]]`: {only when this note supersedes or corrects a prior fact}
```

## Construction rules

- **Ground truth only.** Record what is confirmed to be true. Do not log speculation, predictions, proposals, open questions, or hypothetical discussion points. If a statement cannot be confirmed, hold it in `10_Fleeting/` until it is, or omit it — never present an unconfirmed hypothesis as a project fact.
- **Provenance is mandatory.** Every fact note must carry `source` (how the fact was established), `confirmed` (a full `date-time`, the timestamp for temporal reference), and a resolved `subject` link. The `confirmed` value is when the fact became true or was confirmed, not when a later edit occurred.
- **Append-only supersession.** A changed or corrected fact is a new note with `status: current` and a `supersedes` link to the prior note; set the prior note's `status: superseded` (or `corrected` when the earlier note stated something now known to be wrong). Never edit the substance of a past fact in place, so the record of how the project changed over time is preserved.
- **One current fact per claim.** At most one note per distinct fact about a `subject` should be `status: current`. Earlier entries remain in the vault as `superseded`/`corrected` history.
- **Subject resolution.** `subject` must point to an existing topic note whenever one exists (resolve via titles, aliases, and tags). If the fact clearly concerns an implied-but-absent topic, create a minimal stub note or hold the fact in `10_Fleeting/` until a topic note exists — do not force an unrelated link.
- **Typed frontmatter.** Keep `confirmed` a `date-time`, `subject`/`supersedes` links (quoted), and `topics`/`tags` arrays, so facts are queryable by Bases — see [references/BASES.md](./references/BASES.md) for a project-fact timeline view.
- **Scope.** Log facts that concern the project and the topics the vault covers. Do not log passing remarks, task instructions, or details unrelated to the knowledge base. A stable, well-established fact can graduate into a permanent note's `Source grounding` ([NOTE-FORMAT.md](./NOTE-FORMAT.md)); the project-fact log captures new and changing information as dated entries.
