# Learning Record Format

Learning records live in `./learning-records/` and use sequential names such as `0001-slug.md` and `0002-slug.md`. Create the directory only when writing the first record.

Learning records are the teaching equivalent of ADRs. They capture non-obvious lessons, key insights, and stated prior knowledge that guide future sessions and determine the zone of proximal development.

## Template

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned (or what prior knowledge was established), and why it matters for future sessions.}
```

A learning record may be a single paragraph. Record what is now known and why it changes what to teach next; do not add sections for their own sake.

## Optional sections

Only include these when they add genuine value. Most records won't need them.

- **Status** frontmatter (`active | superseded by LR-NNNN`): use when a later record replaces an earlier understanding.
- **Evidence**: record how the user demonstrated understanding when the claim may need to be revisited.
- **Implications**: record what the learning unlocks or rules out when that effect is not obvious.

## Numbering

Scan `./learning-records/` for the highest existing number and increment by one.

## When to write a learning record

Write one when any of these is true:

1. **The user demonstrated genuine understanding of something non-trivial.** Require evidence that they can use the concept, not merely that they encountered it. This establishes a new floor for future teaching.
2. **The user disclosed prior knowledge.** Record what they already know and the depth they claim so future sessions do not reteach it.
3. **A misconception was corrected.** Record what changed and why; the misconception may predict related stumbling blocks.
4. **The mission shifted in response to learning.** Cross-link to [[MISSION.md]] and update it.

### What does _not_ qualify

- Material that was merely covered. Coverage is not learning. Wait for evidence.
- Anything already captured tersely in [[GLOSSARY.md]] as a term definition. Don't duplicate.
- Session-by-session activity logs. Learning records are decision-grade insights, not a journal.

## Supersession

When a later record contradicts an earlier one because the user's understanding deepened or was corrected, mark the old record `Status: superseded by LR-NNNN` rather than deleting it. The history of that change provides useful context.
