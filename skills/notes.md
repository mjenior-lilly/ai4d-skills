---
name: notes
description: Enrich a set of handwritten Supernote meeting notes into a polished markdown artifact by using the meeting audio recording to recover critical information that the notes missed or under-captured — decisions, action items, owners, dates, risks, open questions, and follow-up requirements. The notes arrive as per-page .png images produced by notesync (which syncs .note files from the cloud and renders each page); run notesync first, then read the page images. The archive also contains daily checklist pages (checkbox-prefixed entries) that must be identified and excluded — only meeting notes (labeled at the top with the topic or person, e.g., "____ meeting") are enriched. Use this skill when the user provides Supernote meeting notes plus an audio recording or transcript and asks to enrich, complete, or fill gaps in their notes, or for meeting content analysis, minutes, action extraction, or a summary document.
---

Use this skill to enrich a set of personal meeting notes by mining the meeting audio recording for critical information that the notes captured poorly or missed entirely.

The personal notes are the backbone of the deliverable: preserve their structure, priorities, and the note-taker's intent. The audio's primary job is to close gaps — recover decisions, owners, dates, technical details, and follow-ups that the notes left thin, ambiguous, or absent.

The synced note archive contains two kinds of handwritten pages: **meeting notes** (the target of this skill) and **daily checklists** (not meeting content — never enrich these or mix them into the deliverable). Identify each page's type before synthesis; see "Distinguishing meeting notes from daily checklists" below.

The notes are handwritten pages captured on a Supernote device. `notesync` syncs the `.note` files from the cloud and renders **one `.png` image per page**; you read those images directly (the Read tool renders images visually). There is no extracted text layer — treat legibility as a first-class concern and mark any handwriting you cannot read with confidence.

The final deliverable is a markdown file artifact, not a chat-only response, unless the user asks otherwise.

## Prerequisite: sync and convert with notesync

Before any synthesis, make sure the page images exist and are current. The notes originate as `.note` files in the cloud, so run notesync first:

1. Run `notesync run` to sync the latest `.note` files from the remote and render each page to `.png`. This is incremental — already-converted, up-to-date notes are skipped, so it is cheap to run every time.
   - If the remote is unreachable or the user is offline, fall back to `notesync convert`, which re-renders from `.note` files already present locally.
   - Add `--force` only when the user reports that an existing image looks stale or wrong.
2. Confirm the command reported at least one converted or up-to-date note. If it reports `failed`, surface which notes failed and continue with whatever converted successfully.
3. Only after conversion succeeds, proceed to file identification below.

Do not attempt synthesis against `.note` files directly or assume a `.txt` text layer exists — neither is readable here. Always go through the rendered `.png` pages.

## File identification

Audio recordings and rendered note pages follow timestamp-based naming conventions and live in designated directories:

- **Audio files**: `YYYYMMDDHHMMSS.WAV` format (e.g., `20260624140145.WAV` = 2026-06-24 at 14:01:45)
  - Default location: `/media/matt-jenior/USB-DISK/RECORD`
- **Note pages**: `YYYYMMDD_HHMMSS-NN.png`, where `YYYYMMDD_HHMMSS` is the source `.note` timestamp and `NN` is the zero-padded 1-based page number (e.g., `20260624_140001-01.png`, `20260624_140001-02.png` = pages 1 and 2 of the note started 2026-06-24 at 14:00:01)
  - Default location: `/home/matt-jenior/Desktop/notes` (the `notesync` local directory; images are written alongside each `.note`)

The timestamps encode the collection time in military time. Corresponding audio and note files will have timestamps that are close but not necessarily identical. Use the date and approximate time to verify that files belong to the same meeting. If timestamps differ by more than a few minutes, confirm with the user that the files correspond to the same event.

A single meeting's notes span **all pages sharing one `YYYYMMDD_HHMMSS` stem**. Gather every `-NN.png` for that stem and read them in ascending page order so the note-taker's flow is preserved. A gap in the page numbers (e.g., `-01` then `-03`) means a page failed to render — note it and, if it matters, re-run `notesync convert --force`.

Unless the user specifies different paths, look for files in these default directories. If the user has set `NOTESYNC_OUTPUT_DIR`, the `.png` pages are written there instead of alongside the `.note` files.

## Distinguishing meeting notes from daily checklists

The rendered pages include both meeting notes and daily checklists, and filenames alone do not tell them apart — you must look at the page content. Classify every candidate page before including it in synthesis:

- **Daily checklists** always have a checkbox drawn to the left of each entry (an empty, checked, or crossed-out box at the start of each line). A page whose entries are checkbox-prefixed line items is a checklist, regardless of its date or proximity to an audio recording.
- **Meeting notes** generally carry a label at the top of the first page identifying the meeting — either the topic or the specific person being met with, typically in the form "____ meeting" (e.g., "Roadmap meeting", "Sarah meeting"). Body content is freeform prose, bullets, diagrams, and marginalia rather than uniform checkbox rows.

Apply the classification like this:

1. Checkboxes are the decisive signal: left-aligned checkboxes on the entries means checklist — exclude the page from meeting synthesis even if a top label is present or an audio file has a nearby timestamp.
2. No checkboxes plus a meeting-style header means meeting notes — include the page.
3. If a page has neither signal (no checkboxes, no header — e.g., a continuation page), use its `YYYYMMDD_HHMMSS` stem: all pages of one `.note` share a stem and a type, so classify the continuation page the same as page `-01` of that stem.
4. If a page is genuinely ambiguous (mixed content, or an unlabeled single-page note without checkboxes), ask the user whether it belongs to the meeting rather than silently including or dropping it.

When a checklist page's timestamp pairs closely with the requested meeting's audio, mention that you excluded it and why, so the user can override if the classification is wrong. Checklist content never feeds the meeting deliverable — do not fold checklist tasks into the action items table.

## Source policy

1. Treat the handwritten note pages as the anchor for structure, emphasis, terminology, acronyms, names, topic priorities, and the note-taker's intent. Carry their substance forward into the deliverable, including diagrams, arrows, boxes, and marginalia — describe visual structure the note-taker used to organize ideas.
2. Treat the meeting recording or transcript as the authoritative evidence source and the primary enrichment tool. Mine it specifically for critical information the notes captured poorly or omitted: unrecorded decisions, missing or wrong owners and dates, technical details, action items, risks, dependencies, and open questions.
3. When the recording contradicts the notes on a factual point (a name, number, date, owner, or decision), prefer the recording and flag the correction so the note-taker can see what changed. The recording is also the tiebreaker for illegible or ambiguous handwriting: use it to resolve a word you cannot read cleanly rather than guessing.
4. Do not discard content just because the notes are its only source. Preserve note-only points that carry the note-taker's priorities, but label them as note-derived and lower confidence when the recording does not support them.
5. Prioritize enrichment by criticality: decisions, commitments, owners, and deadlines first; then risks and open questions; then supporting context. Do not pad the notes with low-value recording detail.
6. Never invent participants, deadlines, decisions, owners, technical details, deliverables, or project names. If the recording is ambiguous, or the handwriting is illegible and the recording does not clarify it, mark the item for clarification rather than guessing.

## Method

1. Classify the candidate pages first (see "Distinguishing meeting notes from daily checklists") and set aside any checklist pages. Then read the meeting-note pages in ascending page order to establish the note-taker's structure, priorities, terminology, and topic anchors. Treat these as the scaffold you will enrich. As you read, transcribe the handwriting into a working outline and flag any word or number you are not confident you read correctly.
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
- Collect every handwriting reading you were unsure of under "Information requiring clarification" so the note-taker can confirm or correct it, unless the recording already resolved it.
- If the recording is unavailable or unusable, state that the output is based only on the note pages, that no enrichment was possible, and lower the confidence accordingly.
- If `notesync` produced no page images for the requested meeting (nothing synced or every note failed to render), stop and report that to the user rather than fabricating notes content; suggest re-running `notesync run` or checking the remote configuration.
