# Issue Tracker: GitHub

Fetch issues and specs from GitHub using the `gh` CLI.

## Conventions

- **Read an issue**: `gh issue view <number> --comments` — returns title, body, labels, and full comment thread.
- **List issues**: `gh issue list --state open --json number,title,body,labels --jq '[.[] | {number, title, body, labels: [.labels[].name]}]'` with appropriate `--label` and `--state` filters.
- **Read a PR**: `gh pr view <number> --comments` and `gh pr diff <number>` for the diff.

Infer the repo from `git remote -v` — `gh` does this automatically when run inside a clone.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either — resolve with `gh issue view 42` first; if it 404s, try `gh pr view 42`.

## Fetching a ticket by reference

When the code-review skill finds `#<number>` in commit messages:

1. Run `gh issue view <number> --comments`.
2. If the issue body is empty or very short (< 50 chars), check whether it's a PR instead: `gh pr view <number> --comments`.
3. Return the title + body as the spec content.
