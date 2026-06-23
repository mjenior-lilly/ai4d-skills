# SOURCE-REGISTER.md Format

`SOURCE-REGISTER.md` is the canonical list of sources considered by the research workflow. It prevents duplicate search, separates candidates from verified sources, and records why sources were rejected.

## Template

```md
# Source Register: {Topic}

## Summary
- Candidate sources found: {n}
- Verified sources: {n}
- Partially verified sources: {n}
- Rejected sources: {n}
- Used in synthesis: {n}

## Verified sources

### SRC-0001: {Title or name}
- Status: verified
- Type: {primary source | paper | docs | dataset | book | article | expert commentary | community | other}
- Stable locator: {URL, DOI, ISBN, archive URL, catalog record, repository path}
- Metadata: {author/org, publisher, publication date, version, access date}
- Verification method: {fetched page, opened PDF, confirmed DOI, checked official docs, catalog lookup, etc.}
- Expected contribution: {which research facet this source supports}
- Quality signals: {authority, method, primary status, citations, reputation, recency}
- Limitations: {bias, age, access limits, narrow sample, unknown method, etc.}
- Used in synthesis: {yes | no}

## Partially verified sources

### SRC-0002: {Title or name}
- Status: partially verified
- Stable locator: {locator}
- What was verified: {metadata or existence}
- What was not inspected: {full text, appendix, data, etc.}
- Use restrictions: {what claims this source can and cannot support}

## Rejected sources

### REJ-0001: {Title or name}
- Candidate locator: {URL or description}
- Rejection reason: {duplicate | inaccessible | low quality | off-goal | unverifiable | superseded | other}
- Notes: {anything useful to prevent repeating the search}
```

## Rules

- Assign stable IDs before extraction. Claims cite `SRC-0001`, not loose URLs.
- Verification is not endorsement. A verified source exists; it may still be biased, weak, outdated, or unused.
- Record rejected sources when the rejection saves future work.
- Mark access limits explicitly. Do not cite details from a source whose content was not inspected.
- Prefer source IDs that remain stable even if ordering changes. If a source is removed, do not reuse its ID in the same workspace.
