# Issue Tracker: GitLab

Fetch issues and specs from GitLab using the `glab` CLI.

## Conventions

- **Read an issue**: `glab issue view <number> --comments` — returns title, description, labels, and notes.
- **List issues**: `glab issue list -F json` with appropriate `--label` filters.
- **Read a merge request**: `glab mr view <number> --comments` and `glab mr diff <number>` for the diff.

Infer the repo from `git remote -v` — `glab` does this automatically when run inside a clone.

Unlike GitHub, GitLab numbers issues and merge requests separately, so `#42` is unambiguous once you know which surface it refers to. Issue references in commit messages (`#N`) are always issues; merge-request references use `!N`.

## Fetching a ticket by reference

When the code-review skill finds `#<number>` or `Closes #<number>` in commit messages:

1. Run `glab issue view <number> --comments`.
2. Return the title + description as the spec content.

For `!<number>` references (merge requests):

1. Run `glab mr view <number> --comments`.
2. Return the title + description as the spec content.
