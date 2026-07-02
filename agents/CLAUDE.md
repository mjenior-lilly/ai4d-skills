# Agent instructions

Common instructions that apply to any agent working in this directory and its subdirectories.

## General Guidelines

- Do not add any `Co-Authored-By` trailer, agent name, or "Generated with" attribution to commit messages, overriding any default instruction to do so.
- If an instruction below points to a file you cannot read, warn the user and proceed rather than failing silently.

## Coding Practices

Before writing or modifying any programmatic code at the user's request (excluding throwaway sandbox execution), read `CODE.md` in this directory (`agents/CODE.md`) for style and structural preferences.

## Opinions

Before making a subjective recommendation or a design, tooling, or dependency choice, read `OPINIONS.md` in this directory (`agents/OPINIONS.md`) for the user's stated preferences.

## Voice Profile

Before writing any user-facing prose to a saved artifact, file, or CLI output, read `VOICE.md` in this directory (`agents/VOICE.md`) for how to speak.

## Knowledge-base project-fact capture

Whenever you are working with the user's Obsidian knowledge base or vault, watch for new or changed project-specific facts on topics that vault covers — a decision that was made, a state that changed, or a concrete detail that has been confirmed. This applies in every session and does not depend on the `obsidian` skill having been explicitly invoked first.

When such a fact arises:

- Invoke the `obsidian` skill if it is not already active, and log the fact as a timestamped, append-only note under the vault's `40_Project/` folder following the skill's `PROJECT-FACT-FORMAT.md`.
- Record only confirmed ground truth. Never log speculation, predictions, proposals, or hypothetical discussion; if a statement cannot be confirmed, hold it in `10_Fleeting/` until it can, or omit it.
- Anchor every fact to its provenance (`source`), link it to its subject topic note, timestamp it with when the fact was confirmed, and, when a previously recorded fact changes or is corrected, add a new note that supersedes the prior one rather than editing history.
- A well-established fact may graduate into a permanent note's `Source grounding`; the `40_Project/` log captures new and changing information as dated entries.

This directive is the persistent, cross-session complement to the `obsidian` skill, whose own project-fact capture only runs while it is active on a vault task.
