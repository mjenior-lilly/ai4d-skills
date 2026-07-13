# Issue Tracker: Local Markdown

Fetch issues and specs from local markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`

## Fetching a ticket by reference

When the code-review skill finds a reference like `#<number>` or a path in commit messages:

1. Search `.scratch/*/issues/` for a file whose number prefix matches (e.g., `01-*`, `02-*`).
2. If found, read and return its content as the spec.
3. If the branch name matches a feature slug, read `.scratch/<feature-slug>/spec.md` as the spec.
