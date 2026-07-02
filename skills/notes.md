---
name: notes
description: Enrich a set of personal .txt meeting notes into a polished markdown artifact by using the meeting audio recording to recover critical information that the notes missed or under-captured — decisions, action items, owners, dates, risks, open questions, and follow-up requirements. Use this skill when the user provides meeting notes plus an audio recording or transcript and asks to enrich, complete, or fill gaps in their notes, or for meeting content analysis, minutes, action extraction, or a summary document.
---

Use this skill to enrich a set of personal meeting notes by mining the meeting audio recording for critical information that the notes captured poorly or missed entirely.

The personal notes are the backbone of the deliverable: preserve their structure, priorities, and the note-taker's intent. The audio's primary job is to close gaps — recover decisions, owners, dates, technical details, and follow-ups that the notes left thin, ambiguous, or absent.

The final deliverable is a markdown file artifact, not a chat-only response, unless the user asks otherwise.

## File identification

Audio recordings and text notes follow specific timestamp-based naming conventions and are stored in designated directories:

- **Audio files**: `YYYYMMDDHHMMSS.WAV` format (e.g., `20260624140145.WAV` = 2026-06-24 at 14:01:45)
  - Default location: `/media/matt-jenior/USB-DISK/RECORD`
- **Text notes**: `YYYYMMDD_HHMMSS.txt` format (e.g., `20260624_140001.txt` = 2026-06-24 at 14:00:01)
  - Default location: `/home/matt-jenior/Desktop/notes`

The timestamps encode the collection time in military time. Corresponding audio and text files will have timestamps that are close but not necessarily identical. Use the date and approximate time to verify that files belong to the same meeting. If timestamps differ by more than a few minutes, confirm with the user that the files correspond to the same event.

Unless the user specifies different paths, look for files in these default directories.

## Source policy

1. Treat the personal notes as the anchor for structure, emphasis, terminology, acronyms, names, topic priorities, and the note-taker's intent. Carry their substance forward into the deliverable.
2. Treat the meeting recording or transcript as the authoritative evidence source and the primary enrichment tool. Mine it specifically for critical information the notes captured poorly or omitted: unrecorded decisions, missing or wrong owners and dates, technical details, action items, risks, dependencies, and open questions.
3. When the recording contradicts the notes on a factual point (a name, number, date, owner, or decision), prefer the recording and flag the correction so the note-taker can see what changed.
4. Do not discard content just because the notes are its only source. Preserve note-only points that carry the note-taker's priorities, but label them as note-derived and lower confidence when the recording does not support them.
5. Prioritize enrichment by criticality: decisions, commitments, owners, and deadlines first; then risks and open questions; then supporting context. Do not pad the notes with low-value recording detail.
6. Never invent participants, deadlines, decisions, owners, technical details, deliverables, or project names. If the recording is ambiguous, mark the item for clarification rather than guessing.

## Method

1. Read the notes first to establish the note-taker's structure, priorities, terminology, and topic anchors. Treat these as the scaffold you will enrich.
2. Review the full recording or transcript before writing. For long meetings, segment the content and keep a running evidence map so early topics are not lost.
3. Perform a gap analysis by comparing the recording against the notes. For each topic the notes raise, ask what the recording adds, corrects, or resolves. Then scan for critical topics the recording covers that the notes omit entirely. Track:
   - decisions and commitments the notes missed or recorded ambiguously;
   - owners, deadlines, and deliverables the notes left blank, vague, or wrong;
   - technical details, numbers, and names the notes garbled or abbreviated;
   - risks, blockers, dependencies, and open questions the notes did not capture.
4. Build a concise meeting model from both sources combined:
   - purpose or objective;
   - participants and roles, when known;
   - major discussion threads;
   - decisions and non-decisions;
   - action items and owners;
   - risks, blockers, dependencies, and open questions.
5. Group related discussion by topic, even if it occurred in multiple parts of the meeting.
6. Separate facts from interpretation. Mark missing owners, dates, or status as `Not specified` rather than guessing.
7. Attribute points to speakers when speaker identity is clear. Use `Unidentified speaker` when identity is uncertain.
8. Before finalizing, verify that every listed decision and action item is supported by the recording or clearly labeled as note-derived, and that each gap the recording filled is reflected in the deliverable.

## Output structure

Create a markdown file with this structure, adapting section depth to the meeting's complexity. Omit sections that have no substantive content, except for action items and open questions.

```markdown
# Meeting summary

## Meeting overview

| Field | Details |
| --- | --- |
| Purpose | ... |
| Participants | ... |
| Duration | ... |
| Overall outcome | ... |

## Executive summary

...

## Major discussion topics

### <topic title>

**Summary:** ...

**Key points**

- ...

**Decisions**

- ...

**Risks or concerns**

- ...

**Open questions**

- ...

**Related action items**

- ...

## Decisions register

| Decision | Context | Decision maker(s) | Evidence source |
| --- | --- | --- | --- |
| ... | ... | ... | Recording |

## Action items

| Owner | Action item | Deliverable | Due date | Dependencies | Status |
| --- | --- | --- | --- | --- | --- |
| ... | ... | ... | Not specified | ... | ... |

## Risks and blockers

| Risk or blocker | Impact | Owner | Mitigation or next step |
| --- | --- | --- | --- |
| ... | ... | Not specified | ... |

## Open questions

- ...

## Follow-up requirements

- ...

## Important context and insights

- ...

## Information requiring clarification

- ...

## Enrichment from recording

### Critical items the notes missed

- ...

### Items the recording corrected or clarified

- ...

### Note-only items (unconfirmed by recording)

- ...
```

## Quality bar

- Make the artifact complete enough to support follow-up work without re-listening to the meeting.
- The enriched notes should be visibly more complete than the original text: every critical decision, owner, date, and follow-up the recording reveals should be present, not just what the note-taker happened to write down.
- Keep prose concise and professional. Prefer dense, specific bullets over generic summaries.
- Do not produce a transcript unless requested.
- Keep the enrichment section focused on what the recording genuinely added or corrected; omit it if the notes already captured everything and there is nothing to surface.
- If the recording is unavailable or unusable, state that the output is based only on notes, that no enrichment was possible, and lower the confidence accordingly.
