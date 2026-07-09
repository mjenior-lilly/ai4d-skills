# Obsidian CLI Reference (optional validation backend)

When Obsidian is running, the `obsidian` CLI is a more reliable backend than blind filesystem reads for interacting with and validating a live vault: it resolves WikiLinks, queries backlinks and tags, sets typed properties, and can confirm a note actually renders. Use it as an **optional** path during the validation phase; fall back to direct filesystem checks when Obsidian is not running or the CLI is unavailable.

Adapted from the Obsidian CLI documentation (https://help.obsidian.md/cli). Run `obsidian help` for the authoritative, up-to-date command list.

## Syntax

- **Parameters** take a value with `=`; quote values with spaces: `obsidian create name="My Note" content="Hello"`.
- **Flags** are bare switches: `obsidian create name="My Note" silent overwrite`.
- Multiline content uses `\n` and `\t`.
- `--copy` copies output to clipboard; `silent` prevents files from opening; `total` returns a count on list commands.

## File and vault targeting

- `file=<name>` resolves like a WikiLink (no path or extension needed).
- `path=<vault-relative path>` targets an exact file, e.g. `path="20_Permanent/Note.md"`.
- Without either, the active file is used.
- `vault=<name>` (as the first parameter) targets a specific vault; otherwise the most recently focused vault is used.

## Useful commands for this workflow

```bash
obsidian read file="Note Title"                         # read a note
obsidian create name="Note Title" content="# ..." silent  # create without opening
obsidian append file="Note Title" content="..."         # append
obsidian search query="term" limit=10                   # full-text search
obsidian backlinks file="Note Title"                    # who links here (orphan check)
obsidian tags sort=count counts                          # tag inventory / drift check
obsidian property:set name="status" value="evergreen" file="Note Title"
```

## Mapping to the validation phase

Use these to perform the checks in WORKFLOW.md "Validate the vault" against the live vault:

| Validation check | CLI approach |
|------------------|--------------|
| Broken / ambiguous WikiLinks | `obsidian backlinks` and `obsidian search` to confirm targets resolve |
| Orphan notes | `obsidian backlinks file=...` returns empty |
| Tag drift | `obsidian tags counts` to spot near-duplicate tags |
| Frontmatter values | `obsidian property:set` / read to confirm typed properties applied |
| Note renders correctly | `obsidian read` (and `dev:screenshot` for plugin/theme work) |

If the CLI is not available, perform the same checks via direct filesystem reads as described in WORKFLOW.md; do not block the workflow on the CLI.
